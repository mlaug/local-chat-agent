import signal
import sys

import pyaudio
from flow.Flow import Flow
from flow.steps.ConvertToMp3 import ConvertToMp3
from flow.steps.WakeWord import WakeWord
from flow.steps.Record import Record
from flow.steps.Transcribe import Transcribe
from flow.steps.AskLeChat import AskLeChat
from flow.steps.TextToSpeech import TextToSpeech
from flow.steps.PlayAudio import PlayAudio
from flow.steps.PlayAudioOnSonos import PlayAudioOnSonos
import os
from dotenv import load_dotenv
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
        # to not overflow, we stop and expect the steps to do the work before
        # this happens automatically if a step is implementing the StepWithRecording abstract class
        self._stream.stop_stream()

    def setup(self):
        # Create instances of our flow steps.
        wake_word = WakeWord(self._stream)
        record = Record(self._stream)
        transcribe = Transcribe()
        askLeChat = AskLeChat()
        textToSpeech = TextToSpeech()
        playAudio = PlayAudio()
        playAudioOnSonos = PlayAudioOnSonos()
        convertToMp3 = ConvertToMp3()

        # Chain the steps:
        # local setup
        #self.flow.waitFor(wake_word).then(record).then(transcribe).then(askLeChat).then(textToSpeech).then(playAudio).loop().start()

        # rasperry pi setup with sonos integration
        #self.flow.waitFor(wake_word).then(record).then(transcribe).then(askLeChat).then(textToSpeech).then(convertToMp3).then(playAudioOnSonos).loop().start()

        self.flow.then(record).then(convertToMp3).then(playAudioOnSonos).start()

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