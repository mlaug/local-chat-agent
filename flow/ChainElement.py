class ChainElement:
    def __init__(self, step, kind="normal", timeout=None):
        """
        :param step: A FlowStep instance.
        :param kind: Either 'normal' or 'waitFor' (for conditional steps).
        :param timeout: For waitFor steps, maximum time (in seconds) to wait.
        """
        self.step = step
        self.kind = kind
        self.timeout = timeout
        # Optional exception handler attached to this step.
        self.handler = None  # Tuple (ExceptionType, handler_function)
