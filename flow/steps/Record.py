from flow.FlowStep import FlowStepWithRecording
import time
import speech_recognition as sr

CHUNK = 1024

class Record(FlowStepWithRecording):
    # Record expects the wake word (a string) as input and returns recorded audio as AudioData.
    expected_input_types = ()
    output_type = bytes  # AudioData object

    def _execute_with_recording(self, input_data):
        print("Recording audio...")
        # Open stream
        frames = []
        start_time = time.time()

        while (time.time() - start_time) < 3:
            data = self.audio_stream.read(CHUNK)
            frames.append(data)

        # Concatenate frames into a single byte string
        raw_audio_data = b''.join(frames)

        return raw_audio_data
