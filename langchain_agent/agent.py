import os
import struct
import time
from typing import Optional

try:
    import pyaudio
except Exception:  # pragma: no cover - optional
    pyaudio = None

from langchain import LLMChain, PromptTemplate
from langchain.llms import HuggingFacePipeline
from langchain.tools import tool
from langgraph.graph import StateGraph

try:
    import whisper
except Exception:  # pragma: no cover - whisper may not be installed
    whisper = None

try:
    from TTS.api import TTS
except Exception:  # pragma: no cover - TTS may not be installed
    TTS = None

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
DEVICE_ID = int(os.getenv("DEVICE_ID") or "1")
STOP_WORD = os.getenv("STOP_WORD", "stop").lower()


class Microphone:
    """Simple microphone reader that falls back when no device is present."""

    def __init__(self) -> None:
        if not pyaudio:
            self.audio = None
            self.stream = None
            return
        try:
            self.audio = pyaudio.PyAudio()
            self.stream = self.audio.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=DEVICE_ID,
            )
            self.stream.stop_stream()
        except Exception:
            self.audio = None
            self.stream = None

    def start(self) -> None:
        if self.stream and not self.stream.is_active():
            self.stream.start_stream()

    def stop(self) -> None:
        if self.stream and self.stream.is_active():
            self.stream.stop_stream()

    def read(self, num_frames: int) -> bytes:
        if not self.stream:
            return b""
        return self.stream.read(num_frames)

    def close(self) -> None:
        if self.stream:
            self.stream.close()
        if self.audio:
            self.audio.terminate()


@tool
def wait_for_stop_word() -> bool:
    """Block until the stop word is detected in the microphone input."""

    recognizer = whisper.load_model("tiny") if whisper else None
    mic = Microphone()
    buffer = []
    print("Listening for stop word...")
    mic.start()
    try:
        while True:
            data = mic.read(CHUNK)
            buffer.append(data)
            if len(buffer) * CHUNK >= RATE:
                audio = b"".join(buffer)
                buffer = []
                if recognizer:
                    import numpy as np

                    audio_np = (
                        np.frombuffer(audio, dtype=np.int16).astype("float32") / 32768.0
                    )
                    result = recognizer.transcribe(audio_np, language="en", fp16=False)
                    text = result.get("text", "").lower()
                    if STOP_WORD in text:
                        print("Stop word detected")
                        return True
    finally:
        mic.stop()


@tool
def record_until_silence(_: Optional[bool] = None) -> bytes:
    """Record audio until silence is detected."""

    frames = []
    silence_chunks = 0
    start = time.time()
    mic = Microphone()
    mic.start()
    try:
        while True:
            data = mic.read(CHUNK)
            frames.append(data)
            rms = struct.unpack_from("%dh" % CHUNK, data)
            rms_val = max(rms)
            if rms_val > 500:
                silence_chunks = 0
            else:
                silence_chunks += 1
            if (
                silence_chunks > int(RATE / CHUNK * 0.8)
                and len(frames) > silence_chunks
            ):
                break
            if time.time() - start > 10:
                break
    finally:
        mic.stop()
    return b"".join(frames)


class WhisperTranscriber:
    def __init__(self) -> None:
        self.model = None

    def load(self) -> None:
        if self.model is None and whisper is not None:
            try:
                self.model = whisper.load_model("base")
            except Exception:
                self.model = None

    def __call__(self, audio_bytes: bytes) -> str:
        self.load()
        if not self.model:
            return ""
        import numpy as np

        audio_np = (
            np.frombuffer(audio_bytes, dtype=np.int16).astype("float32") / 32768.0
        )
        result = self.model.transcribe(audio_np, fp16=False)
        return result.get("text", "")


transcriber = WhisperTranscriber()


@tool
def transcribe_audio(audio: bytes) -> str:
    """Transcribe audio to text with language autodetection."""

    return transcriber(audio)


@tool
def ensure_question(text: str) -> str:
    """Return a question from the text or suggest one."""

    text = text.strip()
    if "?" in text or text.lower().startswith(
        ("who", "what", "when", "where", "why", "how")
    ):
        return text
    return f"Can you tell me more about {text}?"


class LocalModel:
    def __init__(self) -> None:
        self.chain = None

    def load(self) -> None:
        if self.chain is None:
            try:
                from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

                model_name = os.getenv("LLM_MODEL", "distilbert-base-uncased")
                tok = AutoTokenizer.from_pretrained(model_name)
                model = AutoModelForCausalLM.from_pretrained(model_name)
                pipe = pipeline("text-generation", model=model, tokenizer=tok)
                llm = HuggingFacePipeline(pipeline=pipe)
                template = (
                    "Answer the following question so that a 5 year old can understand:"
                    "\n{question}"
                )
                prompt = PromptTemplate.from_template(template)
                self.chain = LLMChain(llm=llm, prompt=prompt)
            except Exception:
                self.chain = None

    def __call__(self, question: str) -> str:
        self.load()
        if not self.chain:
            return ""
        return self.chain.run(question=question)


llm = LocalModel()


@tool
def ask_local_llm(question: str) -> str:
    """Get a simple answer from the local LLM."""

    return llm(question)


class LocalTTS:
    def __init__(self) -> None:
        self.tts = None

    def load(self) -> None:
        if self.tts is None and TTS is not None:
            try:
                self.tts = TTS("tts_models/en/vctk/vits")
            except Exception:
                self.tts = None

    def __call__(self, text: str) -> bytes:
        self.load()
        if not self.tts:
            return b""
        tmp = "/tmp/out.wav"
        self.tts.tts_to_file(text, tmp)
        with open(tmp, "rb") as fh:
            return fh.read()


tts = LocalTTS()


@tool
def text_to_speech(text: str) -> bytes:
    """Convert text to speech and return WAV bytes."""

    return tts(text)


@tool
def play_audio(audio: bytes) -> None:
    """Play audio data using PyAudio."""
    if not pyaudio:
        return
    p = pyaudio.PyAudio()
    try:
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True)
    except Exception:
        p.terminate()
        return
    stream.start_stream()
    stream.write(audio)
    stream.stop_stream()
    stream.close()
    p.terminate()


state = StateGraph(dict)
state.add_node("wait", wait_for_stop_word)
state.add_node("record", record_until_silence)
state.add_node("transcribe", transcribe_audio)
state.add_node("ensure_question", ensure_question)
state.add_node("ask", ask_local_llm)
state.add_node("speak", text_to_speech)
state.add_node("play", play_audio)
state.set_entry_point("wait")
state.add_edge("wait", "record")
state.add_edge("record", "transcribe")
state.add_edge("transcribe", "ensure_question")
state.add_edge("ensure_question", "ask")
state.add_edge("ask", "speak")
state.add_edge("speak", "play")
state.set_finish_point("play")
agent = state.compile()
