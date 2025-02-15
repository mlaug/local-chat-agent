from flow.FlowStep import FlowStep


class RecordStub(FlowStep):
    # Record expects the wake word (a string) as input and returns recorded audio as list of bytes.
    expected_input_types = (str,)
    output_type = list  # list of bytes

    def execute(self, input_data):
        print("Recording audio...")
        # Simulate recording (in real life, capture audio data)
        return [b"audio data"]
