"""Platzhalter-Scoring bis zur Phase-0-Freigabe.

Bewertet NICHT – er gibt jedes Wort als ``ungeprüft`` zurück und markiert die
Antwort als ``calibrated: false``. So kann die gesamte App (Navigation,
Fehlerjagd, Frontend) entwickelt und durchgespielt werden, **ohne** ein
phonetisches Ergebnis vorzutäuschen. Nach dem GO wird er gegen den echten
Provider getauscht.
"""

from __future__ import annotations

from .base import (
    UNRATED,
    FluencyResult,
    LiteralResult,
    ScoringProvider,
    WordFluency,
)
from ..story import regeln  # noqa: F401  (Konsistenz mit Paket-Layout)


def _words(text: str) -> list[str]:
    return [w for w in text.replace("\n", " ").split(" ") if w]


class StubScoringProvider:
    """Erfüllt :class:`ScoringProvider`, ohne zu bewerten."""

    name = "stub"

    def score_fluency(self, audio_path: str, expected_text: str) -> FluencyResult:
        words = [WordFluency(w, None, UNRATED) for w in _words(expected_text)]
        return FluencyResult(words=words, provider=self.name, calibrated=False)

    def score_literal(self, audio_path: str, shown: str, correct: str) -> LiteralResult:
        return LiteralResult(
            shown=shown,
            correct=correct,
            score=None,
            verdict=UNRATED,
            provider=self.name,
            calibrated=False,
        )


# Typ-Check zur Importzeit (billiger Schutz gegen Interface-Drift).
_provider: ScoringProvider = StubScoringProvider()
