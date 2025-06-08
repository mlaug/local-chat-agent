import os
import signal
import sys

import pyaudio
from dotenv import load_dotenv

from flow.Flow import Flow
from flow.steps.AskLeChat import AskLeChat
from flow.steps.AskOllama import AskOllama
from flow.steps.ConvertToMp3 import ConvertToMp3
from flow.steps.PlayAudio import PlayAudio
from flow.steps.PlayAudioOnSonos import PlayAudioOnSonos
from flow.steps.Record import Record
from flow.steps.TextToSpeech import TextToSpeech
from flow.steps.Transcribe import Transcribe
from flow.steps.WakeWord import WakeWord

load_dotenv()

# Audio parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
DEVICE_ID = int(os.getenv("DEVICE_ID") or "1")  # Use the MacBook Pro Microphone


class FlowManager:
    def __init__(self):
        self.flow = Flow()

        self._audio = pyaudio.PyAudio()
        # open the audio stream
        self._stream = self._audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
            input_device_index=DEVICE_ID,
        )
        # To avoid buffer overflows we keep the stream stopped by default. Steps
        # inheriting from ``FlowStepWithRecording`` manage the stream state.
        self._stream.stop_stream()

    def setup(self):
        # Create instances of our flow steps.
        wake_word = WakeWord(self._stream)
        record = Record(self._stream)
        transcribe = Transcribe()
        if os.getenv("USE_OLLAMA") == "1":
            askModel = AskOllama()
        else:
            askModel = AskLeChat()
        textToSpeech = TextToSpeech()
        playAudio = PlayAudio()

        # Chain the steps.
        # By default we run the local setup which performs the full
        # wake word -> record -> transcribe -> chat -> TTS -> playback flow.
        # To use the Sonos integration on a Raspberry Pi, comment the line
        # below and uncomment the alternative chain.

        (
            self.flow.waitFor(wake_word)
            .then(record)
            .then(transcribe)
            .then(askModel)
            .then(textToSpeech)
            .then(playAudio)
            .loop()
            .start()
        )

        # Raspberry Pi setup with Sonos integration
        # (
        #     self.flow.waitFor(wake_word)
        #     .then(record)
        #     .then(transcribe)
        #     .then(askLeChat)
        #     .then(textToSpeech)
        #     .then(convertToMp3)
        #     .then(playAudioOnSonos)
        #     .loop()
        #     .start()
        # )

    def cleanup(self):
        self.flow.cleanup()
        self._stream.close()
        self._audio.terminate()


def signal_handler(sig, frame):
    print("Ctrl+C detected. Cleaning up...")
    flow_manager.cleanup()
    sys.exit(0)


if __name__ == "__main__":
    flow_manager = FlowManager()
    # Register the signal handler
    signal.signal(signal.SIGINT, signal_handler)
    flow_manager.setup()
