import pytest

from fjp0.scoring import (
    GREEN,
    RED,
    YELLOW,
    Thresholds,
    clip_fluency,
    color,
    green_fraction,
)


def test_color_default_thresholds():
    assert color(0.95) == GREEN
    assert color(0.80) == GREEN
    assert color(0.70) == YELLOW
    assert color(0.55) == YELLOW
    assert color(0.40) == RED


def test_thresholds_validation():
    with pytest.raises(ValueError):
        Thresholds(green=0.5, yellow=0.8)  # yellow > green
    with pytest.raises(ValueError):
        Thresholds(green=1.2, yellow=0.5)


def test_custom_thresholds():
    t = Thresholds(green=0.6, yellow=0.3)
    assert color(0.65, t) == GREEN
    assert color(0.45, t) == YELLOW
    assert color(0.20, t) == RED


def test_clip_fluency_mean():
    assert clip_fluency([0.8, 0.6, 1.0]) == pytest.approx(0.8)
    assert clip_fluency([]) == 0.0


def test_green_fraction():
    assert green_fraction([0.9, 0.9, 0.4, 0.5]) == pytest.approx(0.5)
    assert green_fraction([]) == 0.0
