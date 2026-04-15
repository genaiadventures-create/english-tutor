import pytest

from tools.correct_english import correct_english


def test_correct_english_returns_structured_response():
    result = correct_english(
        user_text="i am learning english",
        corrected_sentence="I am learning English.",
        hindi_explanation="यह वाक्य सही grammar के साथ लिखा गया है।",
        fluency_score=82,
        suggestions=[
            "Say this sentence aloud two times.",
            "Replace one word with a synonym.",
            "Use the same sentence in past tense.",
        ],
        encouragement_message="बहुत अच्छा! इसी तरह practice जारी रखो।",
        user_level="beginner",
    )
    assert result.corrected_sentence == "I am learning English."
    assert result.fluency_score >= 0 and result.fluency_score <= 100
    assert len(result.suggestions) == 3


def test_correct_english_rejects_empty_text():
    with pytest.raises(ValueError, match="non-empty"):
        correct_english(
            user_text="   ",
            corrected_sentence="I am fine.",
            hindi_explanation="यह सही है।",
            fluency_score=80,
            suggestions=["a", "b", "c"],
            encouragement_message="good",
        )


def test_correct_english_rejects_invalid_level():
    with pytest.raises(ValueError, match="user_level"):
        correct_english(
            user_text="I am okay",
            corrected_sentence="I am okay.",
            hindi_explanation="यह ठीक है।",
            fluency_score=88,
            suggestions=["a", "b", "c"],
            encouragement_message="great",
            user_level="expert",
        )


def test_correct_english_rejects_too_few_suggestions():
    with pytest.raises(ValueError, match="at least 3"):
        correct_english(
            user_text="I like tea",
            corrected_sentence="I like tea.",
            hindi_explanation="यह अच्छा है।",
            fluency_score=90,
            suggestions=["Only one"],
            encouragement_message="great",
            user_level="intermediate",
        )
