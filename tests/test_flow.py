import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flow.Flow import Flow


def test_check_compatibility_with_str():
    flow = Flow()
    assert flow._check_compatibility((str,), "hello")
