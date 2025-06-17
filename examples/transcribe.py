import torch
import torchaudio
from transformers import WhisperProcessor, WhisperForConditionalGeneration

# Load model and processor
processor = WhisperProcessor.from_pretrained("openai/whisper-large")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large")

# Ensure correct device usage
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

# Load audio
def load_audio(file_path, sampling_rate=16000):
    waveform, sr = torchaudio.load(file_path)
    if sr != sampling_rate:
        resampler = torchaudio.transforms.Resample(orig_freq=sr, new_freq=sampling_rate)
        waveform = resampler(waveform)
    return waveform.squeeze(0)

# Transcribe function
def transcribe_audio(file_path, language="en"):
    audio = load_audio(file_path)
    inputs = processor(audio, sampling_rate=16000, return_tensors="pt")
    input_features = inputs.input_features.to(device)

    # Generate predicted ids
    predicted_ids = model.generate(input_features)

    # Decode
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
    return transcription[0]

# Example usage
if __name__ == "__main__":
    audio_path = "bark_out5.wav"
    result = transcribe_audio(audio_path)
    print("Transcription:", result)
