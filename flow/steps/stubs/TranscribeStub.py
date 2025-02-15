from flow.FlowStep import FlowStep

class RequestError(Exception):
    pass


class TranscribeStrub(FlowStep):
    # Transcribe expects audio (a list of bytes) and returns a transcription (a string).
    expected_input_types = (list,)
    output_type = str

    def execute(self, input_data):
        print("Transcribing audio...")
        # For demonstration, we simulate a transcription failure.
        # In a real scenario, you might only raise an error under certain conditions.
        raise RequestError("Transcription failed")
