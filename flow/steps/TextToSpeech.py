import os
import tempfile

import pvorca
import scipy
from scipy.io.wavfile import write as write_wav
from transformers import pipeline

from flow.FlowStep import FlowStep


class TextToSpeech(FlowStep):
    
    # Expects a string (chat response) and returns audio data as bytes.
    expected_input_types = (str,)
    output_type = bytes

    def __init__(self) -> None:
        USE_BARK = os.getenv("USE_BARK") == "1"
        self.bark = USE_BARK

        if USE_BARK:
            self.synthesiser = pipeline("text-to-speech", "suno/bark")
        else:
            access_key = os.getenv("ORCA_API_KEY") or ""
            self.orca = pvorca.create(access_key=access_key) if access_key else None

        super().__init__()

    def execute(self, input_data):
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav_file:
            temp_wav_path = temp_wav_file.name

        if self.bark:
            speech = self.synthesiser("Hello, my dog is cooler than you!", forward_params={"do_sample": True})
            scipy.io.wavfile.write(temp_wav_path, rate=speech["sampling_rate"], data=speech["audio"])
        elif self.orca is not None:
            # Synthesize speech via Orca
            self.orca.synthesize_to_file(text=input_data, output_path=temp_wav_path)
        else:
            raise RuntimeError("No TTS engine available")

        # Load the content of the temporary file into a bytes string
        with open(temp_wav_path, 'rb') as file:
            audio_data = file.read()

        return audio_data
