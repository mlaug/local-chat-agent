from flow.FlowStep import FlowStep


class AskLeChat(FlowStep):
    # Expects a transcription (string) and returns a chat response (string).
    expected_input_types = (str,)
    output_type = str

    def execute(self, input_data):
        print("Chatting with Le Chat...")
        return "I am fine, thank you."
