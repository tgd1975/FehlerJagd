"""Mechanischer Smoke-Test der echten torchaudio-Engine.

Wird übersprungen, wenn torch/torchaudio nicht installiert ist oder das
MMS_FA-Modell nicht geladen werden kann (z. B. kein Netzwerk). Prüft NICHT die
akustische Güte – nur, dass die Forced-Alignment-API durchläuft und pro Wort
einen plausiblen Score liefert.
"""

import pytest

torch = pytest.importorskip("torch")
torchaudio = pytest.importorskip("torchaudio")


@pytest.fixture(scope="module")
def aligner():
    from fjp0.aligner import TorchAudioAligner
    try:
        return TorchAudioAligner()
    except Exception as exc:  # Modell-Download/Netzwerk kann fehlschlagen.
        pytest.skip(f"MMS_FA nicht ladbar: {exc}")


def test_smoke_alignment_runs(aligner, tmp_path):
    from fjp0.audio import tone, write_wav

    wav = tmp_path / "smoke.wav"
    write_wav(wav, tone(220, 1.0, amplitude=0.3, sample_rate=aligner.sample_rate))
    words = ["tisch", "buch"]
    scores = aligner.word_scores(str(wav), words)
    assert [s.word for s in scores] == words
    assert all(0.0 <= s.score <= 1.0 for s in scores)
