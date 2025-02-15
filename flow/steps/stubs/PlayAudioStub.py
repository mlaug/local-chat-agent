from flow.FlowStep import FlowStep


class PlayAudioStub(FlowStep):
    # Expects audio data (list of bytes) and returns a status message (string).
    expected_input_types = (list,)
    output_type = str

    def execute(self, input_data):
        print("Playing audio on Sonos...")
        return "Audio played"
