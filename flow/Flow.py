import threading
import time

from flow.ChainElement import ChainElement

class Flow:
    def __init__(self):
        self.chain = []
        self._stop_event = threading.Event()
        self._interrupt_flag = False
        self._is_loop = False
        self._interrupt_thread = None

    def waitFor(self, step, timeout=None):
        self.chain.append(ChainElement(step, kind="waitFor", timeout=timeout))
        return self

    def then(self, step):
        self.chain.append(ChainElement(step, kind="normal"))
        return self

    def interrupt(self, step):
        """
        Adds an interrupt step that runs in a separate thread.
        If the step returns True, the flow is stopped and reset.
        """
        def interrupt_wrapper():
            while not self._stop_event.is_set():
                if step.execute(None):
                    self._interrupt_flag = True
                    self._stop_event.set()
                time.sleep(0.5)

        # keep a reference so we can join the thread on cleanup
        self._interrupt_thread = threading.Thread(target=interrupt_wrapper)
        self._interrupt_thread.daemon = True
        self._interrupt_thread.start()
        return self

    def handle(self, exception_type, handler_function):
        if not self.chain:
            raise Exception("No step available to attach handler.")
        self.chain[-1].handler = (exception_type, handler_function)
        return self

    def start(self):
        # start the flow
        while True:
            self._stop_event.clear()
            self._interrupt_flag = False
            current_input = None
            for element in self.chain:
                step = element.step
                if not self._check_compatibility(step.expected_input_types, current_input):
                    raise TypeError(
                        f"Incompatible input for {step.__class__.__name__}. "
                        f"Expected one of {step.expected_input_types} but got {type(current_input)}."
                    )

                if self._interrupt_flag:
                    print("Flow interrupted and reset.")
                    break

                if element.kind == "waitFor":
                    current_input = self._execute_wait_for(
                        step, current_input, element.timeout, element.handler
                    )
                else:
                    current_input = self._execute_step(step, current_input, element.handler)
            else:
                print("Flow completed. Final output:", current_input)
                if not hasattr(self, '_is_loop') or not self._is_loop:
                    break

    def cleanup(self):
        """
        Stops any currently running loop and clears threads and other resources gracefully.
        """
        self._stop_event.set()
        if self._interrupt_thread and self._interrupt_thread.is_alive():
            self._interrupt_thread.join()
        
        print("Cleanup complete. All threads stopped and resources cleared.")

    def _execute_step(self, step, input_data, handler):
        try:
            result = step.execute(input_data)
        except Exception as e:
            if handler and isinstance(e, handler[0]):
                result = handler[1](e, input_data)
            else:
                raise
        return result

    def _execute_wait_for(self, step, input_data, timeout, handler):
        start_time = time.time()
        result = None
        while True:
            try:
                result = step.execute(input_data)
                if result:
                    break
            except Exception as e:
                if handler and isinstance(e, handler[0]):
                    result = handler[1](e, input_data)
                    break
                else:
                    raise
            if timeout is not None and (time.time() - start_time) > timeout:
                raise TimeoutError(
                    f"Timeout waiting for condition in step {step.__class__.__name__}."
                )
        return result

    def _check_compatibility(self, expected_types, input_value):
        for expected in expected_types:
            if expected is type(None):
                if input_value is None:
                    return True
            elif expected is str:
                if isinstance(input_value, str):
                    return True
            elif expected is list:
                if isinstance(input_value, list) and any(
                    isinstance(x, expected) for x in input_value
                ):
                    return True
            elif isinstance(input_value, expected):
                return True
        # an empty list is always true as it accepts any input
        return True

    def loop(self):
        """
        Enables looping of the flow.
        """
        self._is_loop = True
        return self
