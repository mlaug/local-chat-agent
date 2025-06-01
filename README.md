# Local Chat Agent

This repository provides a simple flow-based prototype that listens for a wake word, records a short audio snippet, transcribes it, sends the text to Mistral's Le Chat API, converts the reply to speech and plays it back.

## Requirements

- Python 3.9+
- PortAudio installed (`brew install portaudio` on macOS)
- [Porcupine](https://github.com/Picovoice/porcupine) and [Orca](https://github.com/picovoice/orca) API keys
- `pyaudio` and other Python dependencies from `requirements.txt`
- Optional: `pyttsx3` for offline text to speech

## Environment Variables

Create a `.env` file or export the following variables:

```
PORCUPINE_API_KEY=<your_porcupine_key>
LE_CHAT_API_KEY=<your_mistral_key>
ORCA_API_KEY=<your_orca_key>
DEVICE_ID=<mic_device_id>  # optional, defaults to 1
OLLAMA_ENDPOINT=http://localhost:11434/api/generate  # optional
OLLAMA_MODEL=llama3  # optional
```

Use `python helper/channels.py` to list available microphone device IDs.

## Running

Install dependencies and run the application:

```bash
pip install -r requirements.txt
python app.py
```

The default flow waits for the wake word and performs the full voice interaction loop. Press `Ctrl+C` to stop the program gracefully.

If you want to use a locally deployed Ollama model instead of Mistral's API,
set the environment variable `USE_OLLAMA=1`. The step will communicate with the
endpoint defined by `OLLAMA_ENDPOINT`.

The assistant is configured to respond in a very simple "explain like I'm five" manner. It also filters replies for potentially inappropriate language so that responses remain child friendly.

### Offline text to speech

If no `ORCA_API_KEY` is provided the application falls back to [`pyttsx3`](https://pyttsx3.readthedocs.io/) for speech synthesis. This runs entirely locally but you need a TTS engine available on your system.

### Multilingual input

Speech can be provided in German, English or Spanish. The detected language is used for the reply so the assistant answers in the same language.

## Development Container

The repository includes a VS Code devcontainer configuration for testing audio
input and output entirely inside Docker. On macOS you need a running PulseAudio
server on the host:

```bash
brew install pulseaudio
pulseaudio --load=module-native-protocol-tcp --exit-idle-time=-1
```

After starting the server, open the project in VS Code and choose **Reopen in
Container**. The devcontainer connects to the host's PulseAudio instance at
`host.docker.internal:4713`, allowing microphone and speaker access from inside
the container.
