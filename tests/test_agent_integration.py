import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from langchain_agent import agent as la


def test_ensure_question():
    assert la.ensure_question("What is up?") == "What is up?"
    assert (
        la.ensure_question("Tell me something")
        == "Can you tell me more about Tell me something?"
    )


def test_transcribe_audio_handles_missing_model(tmp_path):
    audio_file = tmp_path / "in.wav"
    audio_file.write_bytes(b"\x00" * 32000)
    assert la.transcribe_audio.invoke({"audio": audio_file.read_bytes()}) == ""


def test_ask_local_llm_handles_missing_model():
    out = la.ask_local_llm("What is AI?")
    assert isinstance(out, str)


def test_text_to_speech_handles_missing_tts():
    out = la.text_to_speech("hello")
    assert isinstance(out, (bytes, bytearray))


def test_play_audio_no_error():
    la.play_audio.invoke({"audio": b""})
