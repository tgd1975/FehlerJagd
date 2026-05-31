"""Lautgetreue Fehlerprüfung (Mechanik B, nur *hörbare* Fehler).

Die Logik ist gegenüber der Flüssigkeit **umgekehrt** (Konzept Abschnitt 6c):
wir messen die akustische Nähe der Aufnahme zum *richtigen* Wort.

* Score **hoch** → klingt wie das richtige Wort → das Kind hat still
  **auto-korrigiert** (NICHT genau gelesen).
* Score **niedrig** → literaler Dekodier-Versuch der Falschschreibung →
  **erkannt** (gut).

Zwei harte Leitplanken aus dem Konzept (Risiken 2 & 3):

1. Diese Prüfung läuft über akustische Distanz / Forced-Alignment, **nie** über
   ASR-Transkription (die würde "Tihsc" still zu "Tisch" reparieren).
2. Sie gilt **ausschließlich** für die Fehlerklasse ``hoerbar``. Bei
   ``vokallaenge``/``homophon`` ist Audio blind → dort nur Markieren. Diese
   Modulfunktionen lehnen andere Klassen darum aktiv ab.

Ein **Energie-Gate** (siehe ``gating.py``) muss *vor* dieser Bewertung greifen,
sonst rutscht Stille/Gemurmel als "niedriger Score = literal gelesen" durch.
"""

from __future__ import annotations

from dataclasses import dataclass

# Nur für diese Klasse ist die akustische Distanzprüfung definiert.
AUDIBLE = "hoerbar"

# Default-Schwelle: Score gegen das RICHTIGE Wort UNTER diesem Wert ⇒ "literal".
DEFAULT_LITERAL_MAX = 0.55

LITERAL = "literal gelesen (erkannt)"
AUTOCORRECTED = "auto-korrigiert"
INVALID = "ungültig (zu leise / kein Sprachsignal)"


@dataclass(frozen=True)
class LiteralResult:
    shown: str          # gezeigte Falschschreibung, z. B. "Tihsc"
    correct: str        # richtiges Wort, z. B. "Tisch"
    score: float        # akustische Nähe zum richtigen Wort [0, 1]
    verdict: str        # LITERAL | AUTOCORRECTED | INVALID
    gated_out: bool     # True, wenn das Energie-Gate den Clip verworfen hat

    @property
    def detected_literal(self) -> bool:
        return self.verdict == LITERAL


def assert_audible(klasse: str) -> None:
    """Stellt sicher, dass die Distanzprüfung nur auf ``hoerbar`` läuft."""
    if klasse != AUDIBLE:
        raise ValueError(
            f"lautgetreue Prüfung ist nur für Klasse '{AUDIBLE}' definiert, "
            f"nicht für '{klasse}' – diese Fehler laufen ausschließlich über "
            f"Markieren (deterministisch)."
        )


def classify(
    shown: str,
    correct: str,
    score: float,
    *,
    voiced: bool,
    literal_max: float = DEFAULT_LITERAL_MAX,
) -> LiteralResult:
    """Wertet einen einzelnen hörbaren Fehler aus.

    ``voiced`` kommt aus dem Energie-Gate: ist es ``False`` (Stille/Gemurmel),
    wird das Ergebnis als ungültig markiert – ein niedriger Score darf dann
    NICHT als "literal gelesen" zählen.
    """
    if not voiced:
        return LiteralResult(shown, correct, score, INVALID, gated_out=True)
    verdict = LITERAL if score < literal_max else AUTOCORRECTED
    return LiteralResult(shown, correct, score, verdict, gated_out=False)
