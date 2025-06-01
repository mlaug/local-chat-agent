import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flow.steps.stubs.TextDump import TextDump
from flow.steps.stubs.PlayAudioStub import PlayAudioStub
from flow.steps.stubs.RecordStub import RecordStub
from flow.steps.stubs.AskTheVoid import AskLeChat as AskTheVoid


def test_text_dump():
    step = TextDump()
    assert step.execute("hello") == "hello"


def test_play_audio_stub():
    step = PlayAudioStub()
    assert step.execute([b"test"]) == "Audio played"


def test_record_stub():
    step = RecordStub()
    assert step.execute("wake") == [b"audio data"]


def test_ask_the_void():
    step = AskTheVoid()
    assert step.execute("How are you?") == "I am fine, thank you."
