import abc


class FlowStep(abc.ABC):
    # Each step defines the allowed type(s) for its input and what it produces.
    # Allowed input types: either None (for the first step), a str, or a list of bytes.
    expected_input_types = ()  # e.g. (type(None),) or (str,) or (list,)
    output_type = None  # e.g. str or list

    @abc.abstractmethod
    def execute(self, input_data, audio_stream=None):
        """
        Executes the step.

        :param input_data: The output of the previous step.
        :return: A new output (either a string or a list of bytes).
        """
        pass

class FlowStepWithRecording(FlowStep):

    def __init__(self, audio_stream):
        self.audio_stream = audio_stream

    def execute(self, input_data):
        """
        Executes the step with recording logic.

        :param input_data: The output of the previous step.
        :return: A new output (either a string or a list of bytes).
        """
        self.audio_stream.start_stream()

        result = None
        try:
            result = self._execute_with_recording(input_data)
        finally:
            if isinstance(result, bool) and result:
                self.audio_stream.stop_stream()
            
            if not isinstance(result, bool):
                self.audio_stream.stop_stream()

        return result

    @abc.abstractmethod
    def _execute_with_recording(self, input_data):
        """
        The actual execution logic to be implemented by subclasses.

        :param input_data: The output of the previous step.
        :return: A new output (either a string or a list of bytes).
        """
        pass