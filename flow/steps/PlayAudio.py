from flow.FlowStep import FlowStep
from pydub import AudioSegment
from pydub.playback import play
import io

class PlayAudio(FlowStep):
    # Expects audio data (bytes) and returns a status message (string).
    expected_input_types = (bytes,)
    output_type = str

    def execute(self, input_data):
        try:
            # Convert bytes to a BytesIO object
            audio_bytes_io = io.BytesIO(input_data)

            # Load the audio data using pydub
            audio = AudioSegment.from_file(audio_bytes_io, format="raw", sample_width=2, frame_rate=16000, channels=1)

            # Play the audio
            play(audio)

            print("Playing audio")
            return "Audio played"
        except Exception as e:
            print(f"An error occurred: {e}")
            return "Failed to play audio"
