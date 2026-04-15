import os
import tempfile

from gtts import gTTS

try:
    from openclaw.tools import tool
except ImportError:
    # Local test fallback when OpenClaw runtime is unavailable.
    def tool(func):
        return func

@tool
def speak_text(corrected_sentence: str, accent: str = "indian") -> str:
    """
    If Openclaw is calling this tool after correct_english tool, then use the corrected_sentence as the text to speak.
    Convert text to speech and return a file path that OpenClaw can send as voice.
    Uses gTTS with Indian English accent.
    """
    cleaned_text = (corrected_sentence or "").strip()
    if not cleaned_text:
        raise ValueError("corrected_sentence must be a non-empty string")

    tld = _accent_to_tld(accent)
    tts = gTTS(text=cleaned_text, lang="en", tld=tld, slow=False)
    output_dir = _get_audio_output_dir()

    temp_path = ""
    try:
        with tempfile.NamedTemporaryFile(
            suffix=".mp3",
            prefix="english_tutor_",
            dir=output_dir,
            delete=False,
        ) as temp_file:
            temp_path = temp_file.name
        tts.save(temp_path)
    except Exception as exc:
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)
        raise RuntimeError(f"Failed to synthesize speech: {exc}") from exc

    if not os.path.exists(temp_path) or os.path.getsize(temp_path) == 0:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        raise RuntimeError("Speech synthesis failed to produce a valid audio file")

    return temp_path  # OpenClaw will handle uploading the voice note


def _get_audio_output_dir() -> str:
    configured = os.getenv("ENGLISH_TUTOR_AUDIO_DIR", "").strip()
    if configured:
        output_dir = os.path.abspath(configured)
    else:
        output_dir = os.path.join(os.getcwd(), ".english_tutor_audio")

    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def _accent_to_tld(accent: str) -> str:
    accent_key = (accent or "indian").strip().lower()
    accent_map = {
        "indian": "co.in",
        "us": "com",
        "uk": "co.uk",
        "australian": "com.au",
        "canadian": "ca",
    }
    if accent_key not in accent_map:
        supported = ", ".join(sorted(accent_map))
        raise ValueError(f"accent must be one of: {supported}")
    return accent_map[accent_key]