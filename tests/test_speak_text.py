import os

import pytest

from tools import speak_text as speak_module


def test_speak_text_creates_audio_file(monkeypatch):
    class FakeTTS:
        def __init__(self, text, lang, tld, slow):
            assert text == "Hello from tutor"
            assert lang == "en"
            assert tld == "co.in"
            assert slow is False

        def save(self, path):
            with open(path, "wb") as file_obj:
                file_obj.write(b"mp3-content")

    monkeypatch.setattr(speak_module, "gTTS", FakeTTS)
    expected_output_dir = os.path.join(os.getcwd(), ".english_tutor_audio")

    output_path = speak_module.speak_text("Hello from tutor", "indian")
    assert os.path.exists(output_path)
    assert os.path.getsize(output_path) > 0
    assert output_path.startswith(expected_output_dir + os.sep)

    os.unlink(output_path)


def test_speak_text_invalid_accent_raises():
    with pytest.raises(ValueError, match="accent must be one of"):
        speak_module.speak_text("Hello", "martian")


def test_speak_text_empty_text_raises():
    with pytest.raises(ValueError, match="non-empty"):
        speak_module.speak_text("   ")


def test_speak_text_runtime_error_cleans_file(monkeypatch):
    class FakeTTS:
        def __init__(self, text, lang, tld, slow):
            del text, lang, tld, slow

        def save(self, path):
            raise RuntimeError(f"cannot save to {path}")

    monkeypatch.setattr(speak_module, "gTTS", FakeTTS)

    with pytest.raises(RuntimeError, match="Failed to synthesize speech"):
        speak_module.speak_text("Hello", "us")
