from flow.FlowStep import FlowStep
import tempfile
import os
import pvorca

USE_BARK = os.getenv("USE_BARK") == "1"

try:
    import pyttsx3
except Exception:
    pyttsx3 = None

if USE_BARK:
    try:
        from bark import SAMPLE_RATE, generate_audio
        from scipy.io.wavfile import write as write_wav
    except Exception:
        generate_audio = None
        SAMPLE_RATE = None
        write_wav = None

class TextToSpeech(FlowStep):
    # Expects a string (chat response) and returns audio data as bytes.
    expected_input_types = (str,)
    output_type = bytes

    def __init__(self) -> None:
        self.use_bark = USE_BARK and generate_audio is not None

        if not self.use_bark:
            access_key = os.getenv("ORCA_API_KEY") or ""
            self.orca = pvorca.create(access_key=access_key) if access_key else None
            if not self.orca and pyttsx3:
                self.engine = pyttsx3.init()
            else:
                self.engine = None
        else:
            self.orca = None
            self.engine = None
        super().__init__()

    def execute(self, input_data):
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav_file:
            temp_wav_path = temp_wav_file.name

        if self.use_bark:
            if generate_audio is None:
                raise RuntimeError("USE_BARK is set but bark is not installed")
            audio_array = generate_audio(input_data)
            write_wav(temp_wav_path, SAMPLE_RATE, audio_array)
        elif self.orca is not None:
            # Synthesize speech via Orca
            self.orca.synthesize_to_file(text=input_data, output_path=temp_wav_path)
        elif self.engine is not None:
            # Fallback to local pyttsx3 if available
            self.engine.save_to_file(input_data, temp_wav_path)
            self.engine.runAndWait()
        else:
            raise RuntimeError("No TTS engine available")

        # Load the content of the temporary file into a bytes string
        with open(temp_wav_path, 'rb') as file:
            audio_data = file.read()

        return audio_data
