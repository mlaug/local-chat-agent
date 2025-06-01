import audioop
import time

from flow.FlowStep import FlowStepWithRecording

CHUNK = 1024
RATE = 16000


class Record(FlowStepWithRecording):
    # Record expects the wake word and returns raw audio bytes.
    expected_input_types = ()
    output_type = bytes  # AudioData object

    def _execute_with_recording(self, input_data):
        print("Recording audio...")
        frames = []
        silence_chunks = 0
        start_time = time.time()

        while True:
            data = self.audio_stream.read(CHUNK)
            frames.append(data)

            rms = audioop.rms(data, 2)
            if rms > 800:
                silence_chunks = 0
            else:
                silence_chunks += 1

            if (
                silence_chunks > int(RATE / CHUNK * 0.8)
                and len(frames) > silence_chunks
            ):
                break

            if (time.time() - start_time) > 10:
                break

        raw_audio_data = b"".join(frames)

        return raw_audio_data
