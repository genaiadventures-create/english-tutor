import pytest

from tools.correct_english import correct_english


def test_correct_english_returns_structured_response():
    result = correct_english("i am learning english", "beginner")
    assert result.corrected_sentence == "I am learning english."
    assert result.fluency_score >= 0 and result.fluency_score <= 100
    assert len(result.suggestions) == 3
    assert "हिंदी" not in result.corrected_sentence


def test_correct_english_rejects_empty_text():
    with pytest.raises(ValueError, match="non-empty"):
        correct_english("   ", "beginner")


def test_correct_english_rejects_invalid_level():
    with pytest.raises(ValueError, match="user_level"):
        correct_english("I am okay", "expert")


def test_correct_english_normalizes_level_case():
    result = correct_english("i dont like tea", "InTerMediate")
    assert result.corrected_sentence.startswith("I don't")
    assert "because" in " ".join(result.suggestions).lower()
