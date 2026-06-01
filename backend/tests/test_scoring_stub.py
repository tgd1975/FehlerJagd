from app.scoring import get_provider
from app.scoring.base import UNRATED


def test_stub_is_default():
    p = get_provider("stub")
    assert p.name == "stub"


def test_stub_fluency_unrated():
    p = get_provider("stub")
    res = p.score_fluency("", "Im Regal stehen viele Bücher")
    assert res.calibrated is False
    assert len(res.words) == 5
    assert all(w.color == UNRATED and w.score is None for w in res.words)
    assert res.clip_score is None
    assert res.all_green is False


def test_stub_literal_unrated():
    p = get_provider("stub")
    res = p.score_literal("", "Tihsc", "Tisch")
    assert res.verdict == UNRATED
    assert res.calibrated is False


def test_unknown_provider_raises():
    import pytest
    with pytest.raises(ValueError):
        get_provider("zauberei")
