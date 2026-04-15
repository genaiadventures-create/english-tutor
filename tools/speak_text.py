from openclaw.tools import tool
from gtts import gTTS
import tempfile
import os

@tool
def speak_text(text: str, accent: str = "indian") -> str:
    """
    Convert text to speech and return a file path that OpenClaw can send as voice.
    Uses gTTS with Indian English accent.
    """
    tts = gTTS(text=text, lang="en", tld="com", slow=False)
    
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        temp_path = f.name
        tts.save(temp_path)
    
    return temp_path  # OpenClaw will handle uploading the voice note