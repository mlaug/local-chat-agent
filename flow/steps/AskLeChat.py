from flow.FlowStep import FlowStep
from mistralai import Mistral
import os

try:
    from langdetect import detect
except Exception:
    detect = None

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

    def _detect_language(self, text: str) -> str:
        """Return ISO code for detected language (en, de, es)."""
        if detect is not None:
            try:
                code = detect(text)
            except Exception:
                code = "en"
        else:
            words = set(text.lower().split())
            score = {"en": 0, "de": 0, "es": 0}
            for word in ("the", "and", "is"):
                if word in words:
                    score["en"] += 1
            for word in ("und", "ist", "nicht", "wie", "geht"):
                if word in words:
                    score["de"] += 1
            for word in ("y", "el", "la", "como", "estas"):
                if word in words:
                    score["es"] += 1
            code = max(score, key=score.get)
        if code not in ("en", "de", "es"):
            code = "en"
        return code

    def execute(self, input_data):
        print("Chatting with Le Chat...")
        try:
            lang_code = self._detect_language(input_data)
            lang_names = {"en": "English", "de": "German", "es": "Spanish"}
            system_prompt = (
                "You are a friendly assistant for children. "
                f"Answer every question in {lang_names[lang_code]} in a simple way a five-year-old could understand. "
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
