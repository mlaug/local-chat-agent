from flow.FlowStep import FlowStep
import pvorca
import tempfile
import os

class TextToSpeech(FlowStep):
    # Expects a string (chat response) and returns audio data as bytes.
    expected_input_types = (str,)
    output_type = bytes

    def __init__(self) -> None:
        self.orca = pvorca.create(access_key=os.getenv("ORCA_API_KEY") or "")
        super().__init__()

    def execute(self, input_data):
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav_file:
            temp_wav_path = temp_wav_file.name

        # Synthesize speech to the temporary file
        self.orca.synthesize_to_file(text=input_data, output_path=temp_wav_path)

        # Load the content of the temporary file into a bytes string
        with open(temp_wav_path, 'rb') as file:
            audio_data = file.read()

        return audio_data
