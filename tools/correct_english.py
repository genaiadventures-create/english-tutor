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
def correct_english(user_text: str, user_level: str = "beginner") -> CorrectionResponse:
    """
    Give structured English correction with Hindi explanation.
    Returns clean JSON for the agent to use.
    """
    cleaned_text = _normalize_text(user_text)
    if not cleaned_text:
        raise ValueError("user_text must be a non-empty string")

    normalized_level = _normalize_level(user_level)
    corrected_sentence = _simple_corrections(cleaned_text)
    fluency_score = _estimate_fluency_score(cleaned_text, corrected_sentence)

    return CorrectionResponse(
        corrected_sentence=corrected_sentence,
        hindi_explanation=_hindi_explanation(cleaned_text, corrected_sentence),
        fluency_score=fluency_score,
        suggestions=_build_suggestions(corrected_sentence, normalized_level),
        encouragement_message=_encouragement_message(fluency_score),
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


def _simple_corrections(text: str) -> str:
    normalized = text.strip()
    replacements = {
        " i ": " I ",
        " im ": " I'm ",
        " dont ": " don't ",
        " cant ": " can't ",
        " doesnt ": " doesn't ",
    }
    padded = f" {normalized.lower()} "
    for src, dst in replacements.items():
        padded = padded.replace(src, dst)

    corrected = padded.strip()
    if corrected:
        corrected = corrected[0].upper() + corrected[1:]
    if corrected and corrected[-1] not in ".!?":
        corrected += "."
    return corrected


def _estimate_fluency_score(original: str, corrected: str) -> int:
    score = 90
    if original == corrected:
        score = 95
    if original.lower() != corrected.lower():
        score -= 10
    if len(original.split()) <= 3:
        score -= 5
    return max(0, min(100, score))


def _hindi_explanation(original: str, corrected: str) -> str:
    if original == corrected:
        return "आपका वाक्य पहले से ही सही है। बहुत बढ़िया!"
    return "मैंने capitalization और grammar को बेहतर बनाया ताकि वाक्य natural English लगे।"


def _build_suggestions(corrected_sentence: str, level: str) -> List[str]:
    if level == "beginner":
        return [
            corrected_sentence,
            "Try speaking this sentence slowly and clearly.",
            "Use one new English word from this sentence in your next reply.",
        ]
    if level == "intermediate":
        return [
            corrected_sentence,
            "Now rewrite this in past tense.",
            "Add one reason using 'because' to make it more natural.",
        ]
    return [
        corrected_sentence,
        "Create a second, more formal version of this sentence.",
        "Use this idea in a 2-line response with richer vocabulary.",
    ]


def _encouragement_message(score: int) -> str:
    if score >= 90:
        return "बहुत शानदार! You are sounding very natural."
    if score >= 75:
        return "बहुत अच्छा प्रयास! Keep practicing, you are improving fast."
    return "अच्छा प्रयास! छोटी-छोटी practice से fluency जल्दी improve होगी."