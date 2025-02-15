from flow.FlowStep import FlowStep
from mistralai import Mistral
import os

class AskLeChat(FlowStep):
    # Expects a transcription (string) and returns a chat response (string).
    expected_input_types = (str,)
    output_type = str

    def __init__(self) -> None:
        self.client = Mistral(api_key=os.getenv("LE_CHAT_API_KEY"))

    def execute(self, input_data):
        print("Chatting with Le Chat...")

        try:
            chat_response = self.client.chat.complete(
                model="mistral-large-latest", messages=[{"role": "user", "content": f"Don't use any specical characters in your reply to this message: {input_data}"}]
            )
            if chat_response.choices and chat_response.choices[0].message:
                return chat_response.choices[0].message.content
            else:
                return "No valid response from Le Chat."
        except Exception as e:
            return "Error talking to Le Chat."
