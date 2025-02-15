from flow.FlowStep import FlowStep


class TextDump(FlowStep):
    expected_input_types = (str,)
    output_type = list  # list of bytes

    def execute(self, input_data):
        print(input_data)
        return input_data
