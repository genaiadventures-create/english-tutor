import os
import tempfile

import pytest

from tools.delete_file import delete_file


def test_delete_file_deletes_existing_temp_file():
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, "english_tutor_delete_test.tmp")
    with open(file_path, "wb") as file_obj:
        file_obj.write(b"temporary-data")

    assert os.path.exists(file_path)
    assert delete_file(file_path) is True
    assert not os.path.exists(file_path)


def test_delete_file_returns_false_when_missing():
    file_path = os.path.join(tempfile.gettempdir(), "missing_english_tutor_file.tmp")
    if os.path.exists(file_path):
        os.unlink(file_path)
    assert delete_file(file_path) is False


def test_delete_file_rejects_empty_path():
    with pytest.raises(ValueError, match="non-empty"):
        delete_file(" ")


def test_delete_file_rejects_non_absolute_path():
    with pytest.raises(ValueError, match="absolute"):
        delete_file("relative/path.mp3")


def test_delete_file_rejects_outside_temp_dir():
    outside_file = "/root/english-tutor/tests/outside.tmp"
    with open(outside_file, "wb") as file_obj:
        file_obj.write(b"x")
    try:
        with pytest.raises(ValueError, match="approved cleanup directory"):
            delete_file(str(outside_file))
    finally:
        if os.path.exists(outside_file):
            os.unlink(outside_file)


def test_delete_file_deletes_workspace_audio_file():
    audio_dir = os.path.join(os.getcwd(), ".english_tutor_audio")
    os.makedirs(audio_dir, exist_ok=True)
    file_path = os.path.join(audio_dir, "delete_me.mp3")
    with open(file_path, "wb") as file_obj:
        file_obj.write(b"audio")

    assert delete_file(file_path) is True
    assert not os.path.exists(file_path)
