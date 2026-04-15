from typing import List

from pydantic import BaseModel, Field

try:
    from openclaw.tools import tool
except ImportError:
    # Local test fallback when OpenClaw runtime is unavailable.
    def tool(func):
        return func

class TranslationEvaluation(BaseModel):
    is_correct: bool
    explanation_in_hindi: str
    correct_english: str
    encouragement: str
    error_tags: List[str] = Field(default_factory=list)
    confidence: int = Field(..., ge=0, le=100)

@tool
def evaluate_translation(
    hindi_sentence: str,
    user_english_attempt: str,
    is_correct: bool,
    explanation_in_hindi: str,
    correct_english: str,
    encouragement: str,
    error_tags: List[str] | None = None,
    confidence: int = 75,
) -> TranslationEvaluation:
    """
    Validate and normalize an LLM-generated translation evaluation payload.
    Translation reasoning and grading must come from OpenClaw LLM logic.
    """
    cleaned_hindi_sentence = _normalize_text(hindi_sentence)
    if not cleaned_hindi_sentence:
        raise ValueError("hindi_sentence must be a non-empty string")

    cleaned_attempt = _normalize_text(user_english_attempt)
    if not cleaned_attempt:
        raise ValueError("user_english_attempt must be a non-empty string")

    cleaned_explanation = _normalize_text(explanation_in_hindi)
    if not cleaned_explanation:
        raise ValueError("explanation_in_hindi must be a non-empty string")

    cleaned_correct_english = _normalize_text(correct_english)
    if not cleaned_correct_english:
        raise ValueError("correct_english must be a non-empty string")

    cleaned_encouragement = _normalize_text(encouragement)
    if not cleaned_encouragement:
        raise ValueError("encouragement must be a non-empty string")

    normalized_tags = _normalize_error_tags(error_tags or [])

    return TranslationEvaluation(
        is_correct=is_correct,
        explanation_in_hindi=cleaned_explanation,
        correct_english=cleaned_correct_english,
        encouragement=cleaned_encouragement,
        error_tags=normalized_tags,
        confidence=confidence,
    )


def _normalize_text(value: str) -> str:
    if not isinstance(value, str):
        return ""
    return " ".join(value.strip().split())


def _normalize_error_tags(tags: List[str]) -> List[str]:
    if not isinstance(tags, list):
        raise ValueError("error_tags must be a list of strings")

    normalized = []
    for tag in tags:
        cleaned = _normalize_text(tag).lower()
        if cleaned:
            normalized.append(cleaned)
    return normalized