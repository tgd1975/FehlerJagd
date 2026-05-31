"""Schwellen-Kalibrierung und Trennschärfe-Metriken.

Beide Phase-0-Fragen sind im Kern dasselbe Zwei-Klassen-Problem: Trennen die
Scores die "gute" von der "schlechten" Klasse? Hier wird die optimale Schwelle
gesucht und gemessen, *wie gut* sie trennt.

* Flüssigkeit:  Clip-Score, ``fluent`` (hoch) vs. ``stocked`` (niedrig).
* Lautgetreu:   Distanz-Score, ``autocorrected`` (hoch) vs. ``literal`` (niedrig).

In beiden Fällen ist die positive ("gute") Klasse niedrig-scorend bei der
Fehlerprüfung bzw. hoch-scorend bei der Flüssigkeit – die Kalibrierung ist
richtungs-agnostisch und bekommt explizit gesagt, welche Klasse "high" ist.
"""

from __future__ import annotations

from dataclasses import dataclass
from statistics import median


@dataclass(frozen=True)
class Calibration:
    threshold: float            # optimale Trennschwelle
    balanced_accuracy: float    # (Sensitivität + Spezifität) / 2  in [0, 1]
    margin: float               # Median(high) − Median(low); >0 = sauber getrennt
    n_high: int
    n_low: int
    high_median: float
    low_median: float
    overlap: int                # # Clips auf der "falschen" Seite der Schwelle

    @property
    def usable(self) -> bool:
        return self.n_high > 0 and self.n_low > 0


def _candidate_thresholds(values: list[float]) -> list[float]:
    """Mittelpunkte zwischen benachbarten, sortierten, eindeutigen Werten."""
    uniq = sorted(set(values))
    if len(uniq) == 1:
        # Eine einzige Score-Lage: Schwellen knapp darunter/darüber probieren.
        v = uniq[0]
        return [v - 0.01, v + 0.01]
    mids = [(a + b) / 2 for a, b in zip(uniq, uniq[1:])]
    return [uniq[0] - 0.01] + mids + [uniq[-1] + 0.01]


def _balanced_accuracy(high: list[float], low: list[float], thr: float) -> float:
    """Anteil korrekt eingeordneter High- und Low-Clips, klassen-balanciert.

    "high" gilt als korrekt, wenn score >= thr; "low", wenn score < thr.
    """
    if not high or not low:
        return 0.0
    sens = sum(1 for s in high if s >= thr) / len(high)   # High richtig erkannt
    spec = sum(1 for s in low if s < thr) / len(low)      # Low richtig erkannt
    return (sens + spec) / 2


def calibrate(high: list[float], low: list[float]) -> Calibration:
    """Findet die Schwelle mit maximaler balancierter Genauigkeit.

    ``high`` = Scores der hoch-scorenden Klasse, ``low`` = der niedrig-scorenden.
    Bei Gleichstand gewinnt die Schwelle, die mittiger zwischen den Klassen liegt
    (größerer Abstand zu beiden Verteilungen → robuster).
    """
    if not high or not low:
        raise ValueError("Kalibrierung braucht je mindestens einen Clip pro Klasse.")

    candidates = _candidate_thresholds(high + low)
    hi_med = median(high)
    lo_med = median(low)
    mid = (hi_med + lo_med) / 2

    best: tuple[float, float] | None = None  # (balanced_accuracy, -|thr-mid|)
    best_thr = candidates[0]
    for thr in candidates:
        ba = _balanced_accuracy(high, low, thr)
        key = (ba, -abs(thr - mid))
        if best is None or key > best:
            best = key
            best_thr = thr

    overlap = sum(1 for s in high if s < best_thr) + sum(1 for s in low if s >= best_thr)
    return Calibration(
        threshold=round(best_thr, 4),
        balanced_accuracy=round(best[0], 4),
        margin=round(hi_med - lo_med, 4),
        n_high=len(high),
        n_low=len(low),
        high_median=round(hi_med, 4),
        low_median=round(lo_med, 4),
        overlap=overlap,
    )
