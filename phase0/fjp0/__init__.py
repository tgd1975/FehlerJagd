"""FehlerJagd – Phase 0 Validierungs-Harness.

Dieses Paket beantwortet die GO/NO-GO-Frage von Phase 0 (siehe
``docs/Konzept.md`` Abschnitt 7 und ``phase0/README.md``):

  (A) Flüssigkeit:  Trennt die phonetische Wort-für-Wort-Bewertung
      "flüssig gelesen" zuverlässig von "gestockt"?
  (B) Lautgetreue Fehlerprüfung: Erkennt die *akustische Distanz zum
      richtigen Wort* (NICHT ASR-Transkription!), ob ein hörbarer
      Fehler literal gelesen oder still auto-korrigiert wurde?

Architektur-Leitlinie: Die gesamte Entscheidungs-, Kalibrierungs- und
Report-Logik ist **dependency-frei** (nur Python-Stdlib) und damit ohne
torch testbar. Das schwergewichtige akustische Modell steckt hinter dem
austauschbaren :class:`fjp0.aligner.Aligner`-Interface – die echte
torchaudio-Implementierung wird nur geladen, wenn sie gebraucht wird.

Siehe ``phase0/DECISIONS.md`` für die wichtigen Umsetzungsentscheidungen
und die dokumentierten Abweichungen vom ursprünglichen Konzept.
"""

from __future__ import annotations

__all__ = [
    "normalize",
    "scoring",
    "literal",
    "gating",
    "aligner",
    "audio",
    "manifest",
    "calibrate",
    "report",
]

__version__ = "0.1.0"
