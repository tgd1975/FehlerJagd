"""Deterministische Fehlerjagd-Prüfung (Markieren) – **kein ML**.

Der zuverlässige Rückhalt des ganzen Systems (Konzept Abschnitt 3 & Risiko 3):
Die markierten Wörter werden mit den eingebauten ``proofread_errors`` abgeglichen.
Funktioniert für **alle** Fehlerklassen, unabhängig vom Audio-Ergebnis.

Identifikation über die **Token-Position** in der Notiz (nicht nur den String),
damit doppelte Wörter eindeutig bleiben. ``tokenize_note`` ist die gemeinsame
Wahrheit für Backend und Frontend: gleiche Indizes ⇒ gleiches Wort.

Nach dem Abschicken liefert das Ergebnis die **Auflösung mit Regel-Bezug**:
richtige Schreibweise + Merkregel + kindgerechter Tipp pro Fehler.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from ..story.graph import ProofreadError

# Ein „Wort"-Token: Buchstaben (inkl. Umlaute/ß), Ziffern und Wort-Bindestriche.
_TOKEN_RE = re.compile(r"[0-9A-Za-zÄÖÜäöüß]+(?:-[0-9A-Za-zÄÖÜäöüß]+)*")


@dataclass(frozen=True)
class Token:
    index: int
    text: str
    start: int      # Zeichen-Offset im Originaltext (fürs Frontend-Highlighting)
    end: int


def tokenize_note(text: str) -> list[Token]:
    """Zerlegt den Notiz-Text in Wort-Token mit stabilen Indizes und Offsets."""
    return [
        Token(i, m.group(0), m.start(), m.end())
        for i, m in enumerate(_TOKEN_RE.finditer(text))
    ]


def locate_errors(tokens: list[Token], errors: list[ProofreadError]) -> dict[str, int]:
    """Ordnet jedem Fehler einen Token-Index zu.

    * Wort-Fehler: Index des Falschschreibungs-Tokens.
    * Beistrich-Fehler (``is_gap``): ``shown`` ist eine Wort-**Lücke** wie
      „Kuchen kein"; zurückgegeben wird der Index des **ersten** Worts – die
      Lücke (das fehlende Komma) liegt direkt danach.

    Mehrfachvorkommen werden der Reihe nach belegt. Nicht auffindbare Fehler
    fehlen im Ergebnis (vom Loader i. d. R. ausgeschlossen).
    """
    used: set[int] = set()
    located: dict[str, int] = {}
    by_index = {t.index: t for t in tokens}
    for err in errors:
        if err.is_gap:
            words = err.shown.split()
            for tok in tokens:
                if tok.index in used:
                    continue
                # Aufeinanderfolgende Tokens passend zur Lücken-Phrase?
                if all(
                    by_index.get(tok.index + offset) is not None
                    and by_index[tok.index + offset].text == w
                    for offset, w in enumerate(words)
                ):
                    located[err.error_id] = tok.index  # Lücke NACH diesem Token
                    used.update(tok.index + o for o in range(len(words)))
                    break
        else:
            for tok in tokens:
                if tok.index in used:
                    continue
                if tok.text == err.shown:
                    located[err.error_id] = tok.index
                    used.add(tok.index)
                    break
    return located


@dataclass(frozen=True)
class ErrorOutcome:
    error_id: str
    shown: str
    correct: str
    klasse: str
    regel: int | str
    tipp: str
    method: str
    token_index: int | None     # bei Lücken-Fehlern: Index des Worts VOR der Lücke
    is_gap: bool
    found: bool


@dataclass(frozen=True)
class ProofreadResult:
    outcomes: list[ErrorOutcome]            # je eingebautem Fehler ein Ergebnis
    false_positive_indices: list[int]       # Wort markiert, aber kein Fehler
    false_positive_gap_indices: list[int]   # Lücke markiert, aber kein Fehler
    total: int
    found_count: int
    false_positives: int

    @property
    def all_found(self) -> bool:
        return self.found_count == self.total and self.false_positives == 0

    @property
    def score(self) -> float:
        """Anteil korrekt gefundener Fehler in [0, 1] (ohne Falsch-Treffer-Abzug)."""
        return self.found_count / self.total if self.total else 0.0


def check_markings(
    note_text: str,
    errors: list[ProofreadError],
    marked_indices: list[int],
    marked_gap_indices: list[int] | None = None,
) -> ProofreadResult:
    """Gleicht markierte Wörter UND Lücken deterministisch gegen die Fehler ab.

    ``marked_indices``      = angetippte Wort-Token (für Wort-Fehler).
    ``marked_gap_indices``  = angetippte Lücken, je als Index des Worts davor
                              (für Beistrich-Fehler, ``method markieren_luecke``).
    """
    tokens = tokenize_note(note_text)
    located = locate_errors(tokens, errors)
    marked = set(marked_indices)
    marked_gaps = set(marked_gap_indices or [])

    word_error_indices: set[int] = set()
    gap_error_indices: set[int] = set()

    outcomes = []
    for err in errors:
        idx = located.get(err.error_id)
        if err.is_gap:
            if idx is not None:
                gap_error_indices.add(idx)
            found = idx is not None and idx in marked_gaps
        else:
            if idx is not None:
                word_error_indices.add(idx)
            found = idx is not None and idx in marked
        outcomes.append(
            ErrorOutcome(
                error_id=err.error_id, shown=err.shown, correct=err.correct,
                klasse=err.klasse, regel=err.regel, tipp=err.tipp,
                method=err.method, token_index=idx, is_gap=err.is_gap, found=found,
            )
        )

    fp_words = sorted(marked - word_error_indices)
    fp_gaps = sorted(marked_gaps - gap_error_indices)
    found_count = sum(1 for o in outcomes if o.found)
    return ProofreadResult(
        outcomes=outcomes,
        false_positive_indices=fp_words,
        false_positive_gap_indices=fp_gaps,
        total=len(errors),
        found_count=found_count,
        false_positives=len(fp_words) + len(fp_gaps),
    )
