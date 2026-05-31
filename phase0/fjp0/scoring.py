"""Flüssigkeits-Bewertung: Wort-Scores → Farbe → Clip-Kennzahl.

Mechanik A aus dem Konzept (Abschnitt 3). Der Aligner liefert pro Wort einen
Score in ``[0, 1]`` (akustische Nähe zum *richtigen* angezeigten Wort). Hier
geht es nur um die reine, modell-unabhängige Auswertung:

* ``color()``      – Score → grün/gelb/rot anhand kalibrierbarer Schwellen.
* ``clip_fluency`` – aggregiert Wort-Scores zu *einer* Clip-Kennzahl, die in
  der Kalibrierung "flüssig" von "gestockt" trennt.

Die Default-Schwellen stammen aus dem ursprünglichen Skript (GREEN=0.80,
YELLOW=0.55) und sind in Phase 0 zu kalibrieren – siehe ``calibrate.py``.
"""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean

# Default-Schwellen (bewusst mild für Kinderstimmen, vgl. Konzept Abschnitt 3).
# In Phase 0 über calibrate.py empirisch nachzuziehen.
DEFAULT_GREEN = 0.80
DEFAULT_YELLOW = 0.55

GREEN = "grün"
YELLOW = "gelb"
RED = "rot"


@dataclass(frozen=True)
class Thresholds:
    """Farb-Schwellen für die Flüssigkeits-Bewertung."""

    green: float = DEFAULT_GREEN
    yellow: float = DEFAULT_YELLOW

    def __post_init__(self) -> None:
        if not 0.0 <= self.yellow <= self.green <= 1.0:
            raise ValueError(
                f"erwarte 0 <= yellow ({self.yellow}) <= green ({self.green}) <= 1"
            )


def color(score: float, thresholds: Thresholds | None = None) -> str:
    """Bildet einen Wort-Score auf grün/gelb/rot ab."""
    t = thresholds or Thresholds()
    if score >= t.green:
        return GREEN
    if score >= t.yellow:
        return YELLOW
    return RED


@dataclass(frozen=True)
class WordScore:
    """Ein bewertetes Wort."""

    word: str
    score: float

    def color(self, thresholds: Thresholds | None = None) -> str:
        return color(self.score, thresholds)


def clip_fluency(word_scores: list[float]) -> float:
    """Aggregiert Wort-Scores zu einer Clip-Flüssigkeits-Kennzahl in [0, 1].

    ENTSCHEIDUNG (DECISIONS.md): Wir nehmen den **Mittelwert** der Wort-Scores.
    Das ist robust, einfach zu interpretieren und die Größe, auf der die
    Kalibrierung die flüssig/gestockt-Grenze sucht. Ein einzelnes gestocktes
    Wort zieht den Schnitt – wie gewünscht – nach unten, ohne dass ein Ausreißer
    (min) den ganzen Clip kippt.

    Leere Eingabe → 0.0 (kein verwertbares Signal).
    """
    if not word_scores:
        return 0.0
    return mean(word_scores)


def green_fraction(word_scores: list[float], thresholds: Thresholds | None = None) -> float:
    """Anteil grüner Wörter – Nebenkennzahl fürs Eltern-Dashboard/Reporting."""
    if not word_scores:
        return 0.0
    greens = sum(1 for s in word_scores if color(s, thresholds) == GREEN)
    return greens / len(word_scores)
