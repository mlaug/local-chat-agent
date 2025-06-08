import os

import requests

from flow.FlowStep import FlowStep


class AskOllama(FlowStep):
    """Send a prompt to a locally running Ollama model."""

    expected_input_types = (str,)
    output_type = str

    def __init__(self) -> None:
        self.endpoint = os.getenv(
            "OLLAMA_ENDPOINT", "http://localhost:11434/api/generate"
        )
        self.model = os.getenv("OLLAMA_MODEL", "llama3.2")
        super().__init__()

    def execute(self, input_data: str) -> str:
        payload = {"model": self.model, "prompt": input_data, "stream": False}
        resp = requests.post(self.endpoint, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get("response", "")
