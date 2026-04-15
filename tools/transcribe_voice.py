from openclaw.tools import tool
import requests
from faster_whisper import WhisperModel
import os

@tool
def transcribe_voice(voice_input: str) -> str:
    """
    Transcribe a Telegram voice note.
    Accepts either:
      - a direct URL, or
      - a local file path on the server (what Telegram usually provides)
    """
    # If it's already a local file path, use it directly
    if os.path.exists(voice_input):
        audio_path = voice_input
    else:
        # Assume it's a URL and download it
        audio_path = "/tmp/voice_note.ogg"
        response = requests.get(voice_input, timeout=30)
        with open(audio_path, "wb") as f:
            f.write(response.content)

    # Transcribe with faster-whisper
    model = WhisperModel("small", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(audio_path, beam_size=5, language=None)
    text = "".join(segment.text for segment in segments).strip()

    # Cleanup only if we downloaded it
    if audio_path.startswith("/tmp/"):
        os.unlink(audio_path)

    return text