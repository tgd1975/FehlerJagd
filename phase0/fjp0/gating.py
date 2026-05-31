"""Energie-Gate: hält Stille/Gemurmel aus der lautgetreuen Prüfung heraus.

Das ursprüngliche Skript notierte hier nur ein ``TODO``. Ohne dieses Gate hätte
die Distanzprüfung eine gefährliche Lücke: ein **stiller** Clip ist dem richtigen
Wort akustisch fern → niedriger Score → würde fälschlich als "literal gelesen"
gewertet. Das Kind bekäme einen Erfolg, ohne zu lesen.

Wir prüfen zwei einfache, robuste Bedingungen (Konzept-Risiko 2, Stolperfalle):

* **RMS-Energie** über einer Mindestschwelle (überhaupt Schall vorhanden?).
* **Stimmhafte Dauer** über einem Minimum (nicht nur ein Knacks/Atmer).

Bewusst kein ML-VAD – das genügt für Phase 0 und bleibt dependency-frei.
"""

from __future__ import annotations

from dataclasses import dataclass

from .audio import Clip

# Defaults – in Phase 0 an Headset/Umgebung anzupassen (siehe README).
DEFAULT_MIN_RMS = 0.01          # unter ~ -40 dBFS gilt als "still"
DEFAULT_MIN_VOICED_S = 0.15     # mind. 150 ms Schall oberhalb der Energie-Schwelle
_FRAME_MS = 20                  # Analysefenster für die stimmhafte Dauer


@dataclass(frozen=True)
class GateResult:
    voiced: bool        # True ⇒ verwertbares Sprachsignal vorhanden
    rms: float
    voiced_s: float     # geschätzte stimmhafte Dauer in Sekunden
    reason: str         # Klartext, warum (nicht) bestanden


def _voiced_seconds(clip: Clip, frame_rms_min: float) -> float:
    """Summiert die Dauer aller Frames mit RMS über der Schwelle."""
    if not clip.samples or clip.sample_rate == 0:
        return 0.0
    frame_len = max(1, int(clip.sample_rate * _FRAME_MS / 1000))
    voiced_frames = 0
    total_frames = 0
    for start in range(0, len(clip.samples), frame_len):
        frame = clip.samples[start : start + frame_len]
        total_frames += 1
        energy = (sum(s * s for s in frame) / len(frame)) ** 0.5
        if energy >= frame_rms_min:
            voiced_frames += 1
    return voiced_frames * frame_len / clip.sample_rate


def gate(
    clip: Clip,
    *,
    min_rms: float = DEFAULT_MIN_RMS,
    min_voiced_s: float = DEFAULT_MIN_VOICED_S,
) -> GateResult:
    """Entscheidet, ob ein Clip genug Sprachsignal für die Prüfung enthält."""
    rms = clip.rms()
    voiced_s = _voiced_seconds(clip, frame_rms_min=min_rms)

    if rms < min_rms:
        return GateResult(False, rms, voiced_s, f"zu leise (RMS {rms:.4f} < {min_rms})")
    if voiced_s < min_voiced_s:
        return GateResult(
            False, rms, voiced_s,
            f"zu kurz stimmhaft ({voiced_s:.2f}s < {min_voiced_s}s)",
        )
    return GateResult(True, rms, voiced_s, "ok")
