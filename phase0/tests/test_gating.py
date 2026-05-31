from fjp0.audio import silence, tone
from fjp0.gating import DEFAULT_MIN_VOICED_S, gate


def test_loud_clip_passes():
    res = gate(tone(220, 0.5, amplitude=0.3))
    assert res.voiced is True
    assert res.reason == "ok"
    assert res.voiced_s >= DEFAULT_MIN_VOICED_S


def test_silence_is_gated_out():
    res = gate(silence(0.5, noise=0.0005))
    assert res.voiced is False
    assert "leise" in res.reason


def test_too_short_voiced_is_gated_out():
    # Lauter, aber sehr kurzer Clip (< min_voiced_s).
    res = gate(tone(220, 0.05, amplitude=0.3))
    assert res.voiced is False


def test_thresholds_are_tunable():
    quiet = tone(220, 0.5, amplitude=0.02)
    assert gate(quiet, min_rms=0.05).voiced is False
    assert gate(quiet, min_rms=0.005).voiced is True
