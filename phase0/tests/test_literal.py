import pytest

from fjp0.literal import (
    AUDIBLE,
    AUTOCORRECTED,
    INVALID,
    LITERAL,
    assert_audible,
    classify,
)


def test_low_score_voiced_is_literal():
    res = classify("Tihsc", "Tisch", 0.30, voiced=True)
    assert res.verdict == LITERAL
    assert res.detected_literal is True
    assert res.gated_out is False


def test_high_score_voiced_is_autocorrected():
    res = classify("Tihsc", "Tisch", 0.85, voiced=True)
    assert res.verdict == AUTOCORRECTED
    assert res.detected_literal is False


def test_low_score_but_silence_is_invalid_not_literal():
    # Der entscheidende Gating-Schutz: leise → NICHT als literal werten.
    res = classify("Tihsc", "Tisch", 0.10, voiced=False)
    assert res.verdict == INVALID
    assert res.detected_literal is False
    assert res.gated_out is True


def test_custom_literal_max():
    assert classify("a", "b", 0.50, voiced=True, literal_max=0.40).verdict == AUTOCORRECTED
    assert classify("a", "b", 0.50, voiced=True, literal_max=0.60).verdict == LITERAL


def test_assert_audible_rejects_other_classes():
    assert_audible(AUDIBLE)  # ok
    for klasse in ("vokallaenge", "homophon", "dehnungs-h"):
        with pytest.raises(ValueError):
            assert_audible(klasse)
