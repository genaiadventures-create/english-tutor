from typing import List

from pydantic import BaseModel, Field

try:
    from openclaw.tools import tool
except ImportError:
    # Local test fallback when OpenClaw runtime is unavailable.
    def tool(func):
        return func

class CorrectionResponse(BaseModel):
    corrected_sentence: str
    hindi_explanation: str
    fluency_score: int = Field(..., ge=0, le=100)
    suggestions: List[str]
    encouragement_message: str

@tool
def correct_english(
    user_text: str,
    corrected_sentence: str,
    hindi_explanation: str,
    fluency_score: int,
    suggestions: List[str],
    encouragement_message: str,
    user_level: str = "beginner",
) -> CorrectionResponse:
    """
    Validate and normalize an LLM-generated English correction payload.
    The analysis itself must come from the LLM (OpenClaw), not hardcoded rules.
    """
    cleaned_text = _normalize_text(user_text)
    if not cleaned_text:
        raise ValueError("user_text must be a non-empty string")

    _normalize_level(user_level)
    normalized_corrected = _normalize_text(corrected_sentence)
    if not normalized_corrected:
        raise ValueError("corrected_sentence must be a non-empty string")

    normalized_hindi_explanation = _normalize_text(hindi_explanation)
    if not normalized_hindi_explanation:
        raise ValueError("hindi_explanation must be a non-empty string")

    normalized_suggestions = _normalize_suggestions(suggestions)
    normalized_message = _normalize_text(encouragement_message)
    if not normalized_message:
        raise ValueError("encouragement_message must be a non-empty string")

    return CorrectionResponse(
        corrected_sentence=normalized_corrected,
        hindi_explanation=normalized_hindi_explanation,
        fluency_score=fluency_score,
        suggestions=normalized_suggestions,
        encouragement_message=normalized_message,
    )


def _normalize_text(value: str) -> str:
    if not isinstance(value, str):
        return ""
    return " ".join(value.strip().split())


def _normalize_level(level: str) -> str:
    valid_levels = {"beginner", "intermediate", "advanced"}
    normalized = (level or "beginner").strip().lower()
    if normalized not in valid_levels:
        raise ValueError(
            "user_level must be one of: beginner, intermediate, advanced"
        )
    return normalized


def _normalize_suggestions(suggestions: List[str]) -> List[str]:
    if not isinstance(suggestions, list):
        raise ValueError("suggestions must be a list of non-empty strings")

    normalized = []
    for item in suggestions:
        cleaned = _normalize_text(item)
        if cleaned:
            normalized.append(cleaned)

    if len(normalized) < 3:
        raise ValueError("suggestions must include at least 3 non-empty items")
    return normalized