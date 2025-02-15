import pyaudio

audio = pyaudio.PyAudio()

# List available audio devices
for i in range(audio.get_device_count()):
    info = audio.get_device_info_by_index(i)
    print(f"Device ID {i}: {info['name']}, Input Channels: {info['maxInputChannels']}, Output Channels: {info['maxOutputChannels']}")

audio.terminate()
