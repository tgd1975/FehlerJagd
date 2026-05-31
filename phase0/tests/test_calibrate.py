import pytest

from fjp0.calibrate import calibrate


def test_perfect_separation():
    cal = calibrate(high=[0.85, 0.90, 0.95], low=[0.30, 0.35, 0.40])
    assert cal.balanced_accuracy == 1.0
    assert cal.overlap == 0
    assert cal.margin > 0
    assert 0.40 < cal.threshold < 0.85


def test_threshold_sits_between_classes():
    cal = calibrate(high=[0.8, 0.9], low=[0.2, 0.3])
    assert all(s >= cal.threshold for s in [0.8, 0.9])
    assert all(s < cal.threshold for s in [0.2, 0.3])


def test_overlapping_classes_reduce_accuracy():
    cal = calibrate(high=[0.55, 0.60, 0.45], low=[0.50, 0.40, 0.65])
    assert cal.balanced_accuracy < 1.0
    assert cal.overlap >= 1


def test_requires_both_classes():
    with pytest.raises(ValueError):
        calibrate(high=[0.8], low=[])
    with pytest.raises(ValueError):
        calibrate(high=[], low=[0.2])


def test_identical_values_handled():
    cal = calibrate(high=[0.5, 0.5], low=[0.5, 0.5])
    # Nicht trennbar → schlechte Genauigkeit, aber kein Absturz.
    assert 0.0 <= cal.balanced_accuracy <= 1.0
    assert cal.margin == 0.0
