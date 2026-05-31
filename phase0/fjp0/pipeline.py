"""Verdrahtung: Manifest + Aligner → Scores → Kalibrierung → GO/NO-GO.

Das ist die eine Stelle, an der alle dependency-freien Bausteine
zusammenlaufen. Welcher Aligner verwendet wird (echt vs. scripted), ist ein
Parameter – damit läuft genau dieselbe Pipeline im Selbsttest wie auf echten
Aufnahmen.
"""

from __future__ import annotations

from dataclasses import dataclass

from .aligner import Aligner
from .audio import read_wav
from .calibrate import Calibration, calibrate
from .gating import gate
from .manifest import ClipEntry
from .normalize import normalize, word
from .report import Phase0Report, evaluate
from .scoring import clip_fluency


@dataclass(frozen=True)
class ScoredClip:
    entry: ClipEntry
    score: float            # Clip-Flüssigkeit bzw. Distanz-Score zum richtigen Wort
    voiced: bool            # Gate-Ergebnis (nur fehlerjagd relevant)
    gate_reason: str


def score_clip(aligner: Aligner, entry: ClipEntry) -> ScoredClip:
    """Bewertet einen einzelnen Clip gemäß seiner Art."""
    if entry.is_fluency:
        words = normalize(entry.text)
        ws = aligner.word_scores(entry.clip, words)
        return ScoredClip(entry, clip_fluency([w.score for w in ws]), True, "ok")

    # fehlerjagd: Distanz zum RICHTIGEN Wort + Energie-Gate.
    correct = word(entry.text)
    g = gate(read_wav(entry.clip))
    ws = aligner.word_scores(entry.clip, [correct])
    score = ws[0].score if ws else 0.0
    return ScoredClip(entry, score, g.voiced, g.reason)


def _calibrate_fluency(scored: list[ScoredClip]) -> Calibration | None:
    high = [s.score for s in scored if s.entry.is_fluency and s.entry.label == "fluent"]
    low = [s.score for s in scored if s.entry.is_fluency and s.entry.label == "stocked"]
    if not high or not low:
        return None
    return calibrate(high, low)


def _calibrate_literal(scored: list[ScoredClip]) -> Calibration | None:
    # "autocorrected" = hoher Score (klingt wie richtiges Wort) = high-Klasse.
    # "literal"       = niedriger Score = low-Klasse.
    # Vom Gate verworfene Clips fließen NICHT in die Kalibrierung ein.
    valid = [s for s in scored if s.entry.is_literal and s.voiced]
    high = [s.score for s in valid if s.entry.label == "autocorrected"]
    low = [s.score for s in valid if s.entry.label == "literal"]
    if not high or not low:
        return None
    return calibrate(high, low)


def run_pipeline(aligner: Aligner, entries: list[ClipEntry]) -> tuple[
    Phase0Report, list[ScoredClip]
]:
    """Komplette Phase-0-Auswertung über ein Manifest."""
    scored = [score_clip(aligner, e) for e in entries]
    fluency = _calibrate_fluency(scored)
    literal = _calibrate_literal(scored)
    report = evaluate(fluency, literal)
    return report, scored
