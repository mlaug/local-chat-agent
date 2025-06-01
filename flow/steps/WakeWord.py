from flow.FlowStep import FlowStep, FlowStepWithRecording
import pvporcupine
import pyaudio
import struct
import os

class WakeWord(FlowStepWithRecording):
    # For our use case the wake word step is used with waitFor so it expects None.
    expected_input_types = (type(None),)
    output_type = str

    def __init__(self, audio_stream) -> None:
        self.porcupine = pvporcupine.create(access_key=os.getenv("PORCUPINE_API_KEY"), keywords=['computer'])
        print("Looking for wake word...")
        super().__init__(audio_stream)

    def _execute_with_recording(self, input_data):
        pcm = self.audio_stream.read(self.porcupine.frame_length)
        pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)

        # Process the audio data with Porcupine
        return self.porcupine.process(pcm) >= 0
