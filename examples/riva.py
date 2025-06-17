import riva.client
import soundfile as sf

auth = riva.client.Auth(uri="localhost:50051")
tts = riva.client.SpeechSynthesisService(auth)

response = tts.synthesize("System initialized and operational.")
sf.write("riva_output.wav", response.audio, response.sample_rate)
