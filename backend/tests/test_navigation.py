import pytest

from app.config import REPO_ROOT
from app.story.loader import discover_cases
from app.story.navigation import next_scene

CASES = discover_cases(REPO_ROOT / "stories")
FALL01 = CASES["fall-01"]


def test_choice_navigation():
    res = next_scene(FALL01, "szene-01", choice_index=0)
    assert res.next_scene_id == "szene-02a"
    assert not res.ended
    res = next_scene(FALL01, "szene-01", choice_index=1)
    assert res.next_scene_id == "szene-02b"


def test_linear_goto():
    res = next_scene(FALL01, "szene-02a")
    assert res.next_scene_id == "szene-03"


def test_choice_required():
    with pytest.raises(ValueError):
        next_scene(FALL01, "szene-01")  # hat choices, kein index


def test_choice_out_of_range():
    with pytest.raises(IndexError):
        next_scene(FALL01, "szene-01", choice_index=5)


def test_bonus_gated_when_not_all_green():
    # szene-07 -> bonus-01 (requires all_green)
    res = next_scene(FALL01, "szene-07", all_green=False)
    assert res.ended
    assert res.skipped_bonus
    assert res.next_scene_id is None


def test_bonus_open_when_all_green():
    res = next_scene(FALL01, "szene-07", all_green=True)
    assert res.next_scene_id == "bonus-01"
    assert not res.ended


def test_next_case_transition():
    tut = CASES["fall-00-tutorial"]
    res = next_scene(tut, "szene-06")
    assert res.next_case_id == "fall-01"
    assert res.ended
