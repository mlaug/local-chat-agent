# Local Chat Agent

This repository provides a simple flow-based prototype that listens for a wake word, records a short audio snippet, transcribes it, sends the text to Mistral's Le Chat API, converts the reply to speech and plays it back.

## Requirements

- Python 3.9+
- PortAudio installed (`brew install portaudio` on macOS)
- [Porcupine](https://github.com/Picovoice/porcupine) and [Orca](https://github.com/picovoice/orca) API keys
- `pyaudio` and other Python dependencies from `requirements.txt`

## Environment Variables

Create a `.env` file or export the following variables:

```
PORCUPINE_API_KEY=<your_porcupine_key>
LE_CHAT_API_KEY=<your_mistral_key>
ORCA_API_KEY=<your_orca_key>
DEVICE_ID=<mic_device_id>  # optional, defaults to 1
```

Use `python helper/channels.py` to list available microphone device IDs.

## Running

Install dependencies and run the application:

```bash
pip install -r requirements.txt
python app.py
```

The default flow waits for the wake word and performs the full voice interaction loop. Press `Ctrl+C` to stop the program gracefully.

The assistant is configured to respond in a very simple "explain like I'm five" manner. It also filters replies for potentially inappropriate language so that responses remain child friendly.
