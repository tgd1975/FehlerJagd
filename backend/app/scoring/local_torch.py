"""Echtes lokales Scoring über die Phase-0-validierte torchaudio-Engine.

Delegiert bewusst an das Paket ``phase0/fjp0`` – das ist der in Phase 0
kalibrierte, getestete Kern (Forced-Alignment statt ASR, Energie-Gate). So gibt
es keine zweite, abweichende Scoring-Implementierung. torch wird **lazy**
geladen; dieser Provider wird erst nach dem GO als Default gesetzt
(``FJ_SCORING=local``).

Stimme bleibt am Gerät (DSGVO, Konzept-Risiko 6).
"""

from __future__ import annotations

import sys
from pathlib import Path

from .base import (
    FluencyResult,
    LiteralResult,
    ScoringProvider,
    WordFluency,
    color_for,
)

# phase0/ in den Importpfad heben (Repo-Layout: backend/ und phase0/ nebeneinander).
_PHASE0 = Path(__file__).resolve().parents[3] / "phase0"


def _import_fjp0():
    if str(_PHASE0) not in sys.path:
        sys.path.insert(0, str(_PHASE0))
    import fjp0.aligner as aligner
    import fjp0.audio as audio
    import fjp0.gating as gating
    import fjp0.literal as literal
    import fjp0.normalize as normalize
    return aligner, audio, gating, literal, normalize


class LocalTorchScoringProvider:
    """:class:`ScoringProvider` auf Basis von ``phase0.fjp0`` + torchaudio."""

    name = "local"

    def __init__(self, green: float = 0.80, yellow: float = 0.55,
                 literal_max: float = 0.55) -> None:
        self.green = green
        self.yellow = yellow
        self.literal_max = literal_max
        self._aligner = None  # lazy

    def _ensure_aligner(self):
        if self._aligner is None:
            aligner, *_ = _import_fjp0()
            self._aligner = aligner.TorchAudioAligner()
        return self._aligner

    def score_fluency(self, audio_path: str, expected_text: str) -> FluencyResult:
        _, _, _, _, normalize = _import_fjp0()
        aligner = self._ensure_aligner()
        words = normalize.normalize(expected_text)
        scored = aligner.word_scores(audio_path, words)
        out = [
            WordFluency(w.word, w.score, color_for(w.score, self.green, self.yellow))
            for w in scored
        ]
        return FluencyResult(words=out, provider=self.name, calibrated=True)

    def score_literal(self, audio_path: str, shown: str, correct: str) -> LiteralResult:
        _, audio, gating, literal, normalize = _import_fjp0()
        aligner = self._ensure_aligner()
        g = gating.gate(audio.read_wav(audio_path))
        scored = aligner.word_scores(audio_path, [normalize.word(correct)])
        score = scored[0].score if scored else 0.0
        res = literal.classify(shown, correct, score, voiced=g.voiced,
                               literal_max=self.literal_max)
        return LiteralResult(
            shown=shown, correct=correct, score=score, verdict=res.verdict,
            provider=self.name, calibrated=True,
        )


_provider: ScoringProvider = LocalTorchScoringProvider()
