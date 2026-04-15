from openclaw.tools import tool
from pydantic import BaseModel, Field
from typing import List

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
    # This will be filled by the LLM in the main agent prompt
    # For now we return a structured skeleton — the actual logic lives in the agent
    return CorrectionResponse(
        corrected_sentence=user_text,
        hindi_explanation="यह सही वाक्य है।",
        fluency_score=70,
        suggestions=["Better version 1", "Better version 2", "Better version 3"],
        encouragement_message="बहुत अच्छा प्रयास! Keep practicing 😊"
    )