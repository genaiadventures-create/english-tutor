import os
import tempfile
from functools import lru_cache
from typing import Iterable
from urllib.parse import urlparse

import requests
try:
    from faster_whisper import WhisperModel
except ImportError:
    WhisperModel = None

try:
    from openclaw.tools import tool
except ImportError:
    # Local test fallback when OpenClaw runtime is unavailable.
    def tool(func):
        return func

@tool
def transcribe_voice(voice_input: str) -> str:
    """
    Transcribe a Telegram voice note.
    Accepts either:
      - a direct URL, or
      - a local file path on the server (what Telegram usually provides)
    """
    cleaned_input = (voice_input or "").strip()
    if not cleaned_input:
        raise ValueError("voice_input must be a non-empty file path or URL")

    audio_path = cleaned_input
    downloaded_temp_path = None

    if os.path.exists(cleaned_input):
        if not os.path.isfile(cleaned_input):
            raise ValueError(f"voice_input path is not a file: {cleaned_input}")
    elif _is_http_url(cleaned_input):
        downloaded_temp_path = _download_audio(cleaned_input)
        audio_path = downloaded_temp_path
    else:
        raise ValueError(
            "voice_input must be an existing local file path or a valid http(s) URL"
        )

    try:
        model = _get_model()
        segments, _ = model.transcribe(audio_path, beam_size=5, language=None)
        text = _combine_segments(segments)
        if not text:
            raise RuntimeError("Transcription produced no text output")
        return text
    except Exception as exc:
        raise RuntimeError(f"Failed to transcribe voice input: {exc}") from exc
    finally:
        if downloaded_temp_path and os.path.exists(downloaded_temp_path):
            os.unlink(downloaded_temp_path)


def _is_http_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _download_audio(url: str) -> str:
    max_bytes = 25 * 1024 * 1024  # 25 MB
    total = 0
    with requests.get(url, stream=True, timeout=(10, 60)) as response:
        response.raise_for_status()
        with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tmp_file:
            for chunk in response.iter_content(chunk_size=8192):
                if not chunk:
                    continue
                total += len(chunk)
                if total > max_bytes:
                    raise ValueError("Downloaded audio exceeds 25 MB limit")
                tmp_file.write(chunk)
            return tmp_file.name


@lru_cache(maxsize=1)
def _get_model():
    if WhisperModel is None:
        raise RuntimeError("faster-whisper is not installed")
    model_size = os.getenv("WHISPER_MODEL_SIZE", "small")
    return WhisperModel(model_size, device="cpu", compute_type="int8")


def _combine_segments(segments: Iterable) -> str:
    parts = []
    for segment in segments:
        value = getattr(segment, "text", "")
        value = value.strip()
        if value:
            parts.append(value)
    return " ".join(parts).strip()