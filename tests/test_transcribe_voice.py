from types import SimpleNamespace

import pytest

from tools import transcribe_voice as transcribe_module


class FakeResponse:
    def __init__(self, chunks, status_error=None):
        self._chunks = chunks
        self._status_error = status_error

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def raise_for_status(self):
        if self._status_error:
            raise self._status_error

    def iter_content(self, chunk_size=8192):
        del chunk_size
        for chunk in self._chunks:
            yield chunk


def test_transcribe_voice_with_local_file(monkeypatch, tmp_path):
    audio_file = tmp_path / "voice.ogg"
    audio_file.write_bytes(b"audio-data")

    def fake_get_model():
        class Model:
            def transcribe(self, path, beam_size=5, language=None):
                assert path == str(audio_file)
                assert beam_size == 5
                assert language is None
                return [SimpleNamespace(text="hello"), SimpleNamespace(text="world")], {}

        return Model()

    monkeypatch.setattr(transcribe_module, "_get_model", fake_get_model)
    result = transcribe_module.transcribe_voice(str(audio_file))
    assert result == "hello world"


def test_transcribe_voice_with_url_downloads_and_cleans_up(monkeypatch):
    saved_paths = []

    monkeypatch.setattr(
        transcribe_module.requests,
        "get",
        lambda *args, **kwargs: FakeResponse([b"chunk-1", b"chunk-2"]),
    )

    def fake_get_model():
        class Model:
            def transcribe(self, path, beam_size=5, language=None):
                assert path
                saved_paths.append(path)
                return [SimpleNamespace(text="downloaded text")], {}

        return Model()

    monkeypatch.setattr(transcribe_module, "_get_model", fake_get_model)
    result = transcribe_module.transcribe_voice("https://example.com/voice.ogg")
    assert result == "downloaded text"
    assert saved_paths
    assert not transcribe_module.os.path.exists(saved_paths[0])


def test_transcribe_voice_rejects_invalid_input():
    with pytest.raises(ValueError, match="non-empty"):
        transcribe_module.transcribe_voice("   ")


def test_transcribe_voice_rejects_non_url_missing_file():
    with pytest.raises(ValueError, match="existing local file path"):
        transcribe_module.transcribe_voice("/does/not/exist.ogg")
