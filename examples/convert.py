from pydub import AudioSegment

def convert_m4a_to_wav(input_file, output_file):
    # Load the M4A file
    audio = AudioSegment.from_file(input_file, format="m4a")

    # Export the audio as WAV
    audio.export(output_file, format="wav")
    print(f"Converted {input_file} to {output_file}")

# Example usage
input_m4a = "./joke.m4a"
output_wav = "./joke.wav"
convert_m4a_to_wav(input_m4a, output_wav)
