import os
import sys
import types
from unittest.mock import Mock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Provide a minimal requests stub so the module can be imported without the
# real dependency installed.
requests_stub = types.ModuleType("requests")
requests_stub.post = lambda *args, **kwargs: None
sys.modules.setdefault("requests", requests_stub)

from flow.steps.AskOllama import AskOllama  # noqa: E402


def test_ask_ollama():
    step = AskOllama()
    mock_resp = Mock()
    mock_resp.json.return_value = {"response": "hi"}
    mock_resp.raise_for_status = Mock()
    with patch("requests.post", return_value=mock_resp) as post:
        result = step.execute("Hello")
        assert result == "hi"
        post.assert_called_once()
