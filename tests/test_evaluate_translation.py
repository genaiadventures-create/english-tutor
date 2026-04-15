import pytest

from tools.evaluate_translation import evaluate_translation


def test_evaluate_translation_returns_structured_response():
    result = evaluate_translation(
        hindi_sentence="मुझे चाय पसंद है।",
        user_english_attempt="I like tea.",
        is_correct=True,
        explanation_in_hindi="अनुवाद सही है।",
        correct_english="I like tea.",
        encouragement="बहुत बढ़िया!",
        error_tags=[],
        confidence=92,
    )

    assert result.is_correct is True
    assert result.correct_english == "I like tea."
    assert result.explanation_in_hindi == "अनुवाद सही है।"
    assert result.error_tags == []
    assert result.confidence == 92


def test_evaluate_translation_normalizes_error_tags():
    result = evaluate_translation(
        hindi_sentence="वह स्कूल जाता है।",
        user_english_attempt="He go to school",
        is_correct=False,
        explanation_in_hindi="Verb agreement गलत है।",
        correct_english="He goes to school.",
        encouragement="अच्छा प्रयास।",
        error_tags=[" Grammar ", "word-order", "GRAMMAR"],
        confidence=74,
    )

    assert result.error_tags == ["grammar", "word-order", "grammar"]


def test_evaluate_translation_rejects_empty_hindi_sentence():
    with pytest.raises(ValueError, match="hindi_sentence must be a non-empty string"):
        evaluate_translation(
            hindi_sentence=" ",
            user_english_attempt="I am going home.",
            is_correct=True,
            explanation_in_hindi="सही है।",
            correct_english="I am going home.",
            encouragement="good",
            confidence=80,
        )


def test_evaluate_translation_rejects_empty_attempt():
    with pytest.raises(ValueError, match="user_english_attempt must be a non-empty string"):
        evaluate_translation(
            hindi_sentence="मैं घर जा रहा हूँ।",
            user_english_attempt=" ",
            is_correct=False,
            explanation_in_hindi="अनुवाद खाली है।",
            correct_english="I am going home.",
            encouragement="try again",
            confidence=40,
        )


def test_evaluate_translation_rejects_non_list_error_tags():
    with pytest.raises(ValueError, match="error_tags must be a list"):
        evaluate_translation(
            hindi_sentence="मैं खाना खाता हूँ।",
            user_english_attempt="I eat food.",
            is_correct=True,
            explanation_in_hindi="सही है।",
            correct_english="I eat food.",
            encouragement="nice",
            error_tags="grammar",
            confidence=88,
        )


def test_evaluate_translation_confidence_range_enforced():
    with pytest.raises(ValueError):
        evaluate_translation(
            hindi_sentence="मैं पढ़ाई करता हूँ।",
            user_english_attempt="I study.",
            is_correct=True,
            explanation_in_hindi="सही है।",
            correct_english="I study.",
            encouragement="great",
            confidence=120,
        )
