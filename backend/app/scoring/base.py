"""Austauschbares Scoring-Interface (Konzept 6c/6h: provider = local|azure|speechace).

Mechanik A (Flüssigkeit) und die optionale lautgetreue Prüfung (Mechanik B)
laufen über dieses Protokoll. So bleibt die App **GO/NO-GO-unabhängig**: bis zur
Phase-0-Freigabe steckt der :class:`~app.scoring.stub.StubScoringProvider`
dahinter; danach wird ohne Änderung an der App auf den echten Provider
(torchaudio, Azure …) umgestellt.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

# Farb-Schwellen identisch zur Phase-0-Logik (mild für Kinder, kalibrierbar).
GREEN = "grün"
YELLOW = "gelb"
RED = "rot"
UNRATED = "ungeprüft"   # vom Stub-Provider, solange Phase 0 nicht freigegeben ist


def color_for(score: float | None, green: float = 0.80, yellow: float = 0.55) -> str:
    if score is None:
        return UNRATED
    if score >= green:
        return GREEN
    if score >= yellow:
        return YELLOW
    return RED


@dataclass(frozen=True)
class WordFluency:
    word: str
    score: float | None     # None ⇒ nicht bewertet (Stub)
    color: str


@dataclass(frozen=True)
class FluencyResult:
    words: list[WordFluency]
    provider: str
    calibrated: bool        # False ⇒ Schwellen noch nicht via Phase 0 bestätigt

    @property
    def clip_score(self) -> float | None:
        scored = [w.score for w in self.words if w.score is not None]
        return sum(scored) / len(scored) if scored else None

    @property
    def all_green(self) -> bool:
        return bool(self.words) and all(w.color == GREEN for w in self.words)


@dataclass(frozen=True)
class LiteralResult:
    shown: str
    correct: str
    score: float | None     # akustische Nähe zum richtigen Wort
    verdict: str            # literal | autocorrected | invalid | ungeprüft
    provider: str
    calibrated: bool


@runtime_checkable
class ScoringProvider(Protocol):
    name: str

    def score_fluency(self, audio_path: str, expected_text: str) -> FluencyResult:
        ...

    def score_literal(self, audio_path: str, shown: str, correct: str) -> LiteralResult:
        ...
