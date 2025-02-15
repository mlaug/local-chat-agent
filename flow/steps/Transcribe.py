from flow.FlowStep import FlowStep
import speech_recognition as sr
import io
import wave

class Transcribe(FlowStep):
    # Transcribe expects audio (bytes) and returns a transcription (a string).
    expected_input_types = (bytes,)
    output_type = str
    recognizer: sr.Recognizer

    def __init__(self) -> None:
        # Initialize the recognizer
        self.recognizer = sr.Recognizer()
        super().__init__()

    def execute(self, input_data):
        try:
            # Convert raw audio data to WAV format
            audio_bytes_io = io.BytesIO()
            with wave.open(audio_bytes_io, 'wb') as wf:
                wf.setnchannels(1)  # Mono
                wf.setsampwidth(2)  # 16-bit
                wf.setframerate(16000)  # 16kHz
                wf.writeframes(input_data)

            audio_bytes_io.seek(0)

            # Create an AudioFile object from the BytesIO object
            with sr.AudioFile(audio_bytes_io) as source:
                # Read the audio data into an AudioData instance
                audio_data = self.recognizer.record(source)

                # Transcribe the audio data
                print("Transcribing audio...")
                text = self.recognizer.recognize_google(audio_data)
                print(f"Transcribed: {text}")
                return text
        except sr.UnknownValueError:
            print("Speech Recognition could not understand the audio")
            return "Transcription failed: Unable to understand the audio"
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return f"Transcription failed: {e}"
