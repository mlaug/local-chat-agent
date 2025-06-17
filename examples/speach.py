from transformers import pipeline
import numpy as np
import soundfile as sf
from scipy.signal import butter, lfilter

# Load Bark text-to-speech model
tts = pipeline("text-to-speech", model="suno/bark")

# Generate speech
output = tts("Hallo, ich bin der Bernd!", forward_params={"do_sample": True})
audio = np.asarray(output["audio"], dtype=np.float32).squeeze()
rate = output["sampling_rate"]

# Bass boost filter
def bass_boost(audio, rate, gain_db=6.0, cutoff=150):
    nyq = 0.5 * rate
    normal_cutoff = cutoff / nyq
    b, a = butter(N=2, Wn=normal_cutoff, btype='low', analog=False)
    boosted = lfilter(b, a, audio)
    boosted = audio + (boosted * (10**(gain_db / 20.0)))
    return np.clip(boosted, -1.0, 1.0)

# Normalize loudness to target dBFS
def normalize(audio, target_dBFS=-14.0):
    rms = np.sqrt(np.mean(audio**2))
    current_dBFS = 20 * np.log10(rms + 1e-9)
    gain = 10 ** ((target_dBFS - current_dBFS) / 20)
    return np.clip(audio * gain, -1.0, 1.0)

# Soft harmonic saturation
def saturate(audio, amount=0.2):
    return np.tanh(audio * (1 + amount))

# Apply processing chain
audio = bass_boost(audio, rate, gain_db=6.0, cutoff=150)
audio = normalize(audio, target_dBFS=-14.0)
audio = saturate(audio, amount=0.15)
audio = np.clip(audio, -1.0, 1.0)

# Write as 24-bit WAV
sf.write("bark_out5.wav", audio, samplerate=rate, subtype='PCM_24')
