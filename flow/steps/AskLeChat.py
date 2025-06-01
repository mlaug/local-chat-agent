from flow.FlowStep import FlowStep
from mistralai import Mistral
import os

BANNED_WORDS = {
    "sex",
    "porn",
    "violence",
    "drugs",
    "kill",
    "murder",
    "suicide",
}

class AskLeChat(FlowStep):
    # Expects a transcription (string) and returns a chat response (string).
    expected_input_types = (str,)
    output_type = str

    def __init__(self) -> None:
        self.client = Mistral(api_key=os.getenv("LE_CHAT_API_KEY"))

    def execute(self, input_data):
        print("Chatting with Le Chat...")
        try:
            system_prompt = (
                "You are a friendly assistant for children. "
                "Answer every question in a simple way a five-year-old could understand. "
                "Never include content that is inappropriate for kids." 
                "If the user requests something adult or unsafe, respond with 'I can't talk about that.'"
            )
            chat_response = self.client.chat.complete(
                model="mistral-large-latest",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": input_data},
                ],
            )
            if chat_response.choices and chat_response.choices[0].message:
                reply = chat_response.choices[0].message.content
                if self._is_safe(reply):
                    return reply
                else:
                    return "I can't talk about that."
            else:
                return "No valid response from Le Chat."
        except Exception:
            return "Error talking to Le Chat."

    def _is_safe(self, text: str) -> bool:
        lower = text.lower()
        for word in BANNED_WORDS:
            if word in lower:
                return False
        return True
