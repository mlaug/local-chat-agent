import os
import sys
import types

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Stub mistralai so the module can be imported without the real dependency.
mistralai_stub = types.ModuleType("mistralai")

class _Mistral:
    def __init__(self, *args, **kwargs):
        pass

mistralai_stub.Mistral = _Mistral
sys.modules.setdefault("mistralai", mistralai_stub)

from flow.steps.AskLeChat import AskLeChat


def test_detect_language():
    step = AskLeChat()
    assert step._detect_language("Hello, how are you?") == "en"
    assert step._detect_language("Wie geht es dir?") == "de"
    assert step._detect_language("Hola, como estas?") == "es"
