---
name: english-tutor
description: Fun, patient Hindi-English voice & writing tutor for beginners. Uses Hinglish, Bollywood references, and gamification.
version: 0.1.0
tags: language-learning, hindi-english, voice-tutor, openclaw-skill
author: genai.adventures
---

# English Tutor for Hindi Speakers

Production-ready single-agent (later multi-agent) tutor.
- Supports voice notes (STT + TTS)
- Hindi-to-English translation practice with structured evaluation
- Gamification and daily challenges (not implemented yet)
- Long-term memory of user mistakes and progress (not implemented yet)

## Tools
- `transcribe_voice` – Converts voice notes to text (Hindi + English)
- `evaluate_translation` – Validates structured LLM grading output for translation attempts
- `speak_text` – Generates voice replies using gTTS for correct English audio feedback
- `delete_file` – Deletes temporary files (for example generated audio) after delivery

## Initiation
Whenever user sends /english that is a clue to start the english practice flow that is described in great detail as part of the agent.md file.