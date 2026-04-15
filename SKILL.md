---
name: english-tutor
description: Fun, patient Hindi-English voice & writing tutor for beginners. Uses Hinglish, Bollywood references, and gamification.
version: 0.1.0
tags: language-learning, hindi-english, voice-tutor, openclaw-skill
author: genai.adventures
---

# English Tutor for Hindi Speakers

Production-ready single-agent (later multi-agent) tutor built on OpenClaw + LangGraph.
- Supports voice notes (STT + TTS)
- Structured English corrections with Hindi explanations
- Gamification and daily challenges
- Long-term memory of user mistakes and progress

# rsync -av --exclude='venv' --exclude='.git' --exclude='__pycache__'          --exclude='*.pyc' --exclude='temp_*'          . ~/.openclaw/workspace/skills/english-tutor/

# Instructions for OpenClaw Agent:
# Run the following command (or equivalent of this command) to install the skill dependencies:
docker compose exec -u root openclaw-gateway pip3 install --break-system-packages -r english-tutor/requirements.txt

## Tools
- `transcribe_voice` – Converts voice notes to text (Hindi + English)
- `speak_text` – Generates voice replies using gTTS
- `correct_english` – Structured grammar correction with Hindi explanation