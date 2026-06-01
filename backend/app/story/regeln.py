"""Merkregel-Mapping (Antonias Merkblatt, Regeln 1–8).

Quelle: ``CLAUDE.md`` / ``docs/Konzept.md`` Abschnitt 2 & „Auflösung mit
Regel-Bezug". Jeder korrigierte Fehler verweist in der Auflösung auf die
passende Merkregel. Phänomene außerhalb der acht Punkte (dehnungs-h, doppelvokal,
reine hörbare Dreher) tragen ``regel: "–"`` und nur einen Klartext-Tipp.

Dieses Modul ist die *einzige* Quelle der Wahrheit für das Mapping und die
Konsistenz-Validierung – der Story-Loader prüft jeden ``proofread_error``
dagegen, damit Inhalte nicht versehentlich gegen das didaktische Konzept
verstoßen.
"""

from __future__ import annotations

# Fehlerklasse → Merkregel-Nummer (1–8). Schreibweise der Klassen wie in den
# graph.yaml-Dateien (grossschreibung, vokallaenge, v/f …).
KLASSE_ZU_REGEL: dict[str, int] = {
    "grossschreibung": 1,
    "komma": 2,
    "auslaut": 3,
    "v/f": 4,
    "ie": 5,
    "das/dass": 6,
    "ver/vor": 7,
    "vokallaenge": 8,
}

# Außerhalb der acht Punkte: kein Regel-Bezug, nur Klartext-Tipp ⇒ regel "–".
KLASSEN_OHNE_REGEL: frozenset[str] = frozenset(
    {"hoerbar", "dehnungs-h", "doppelvokal"}
)

# Drei-Klassen-Erkennungsmodell → erlaubte Prüf-Methode (Konzept-Risiko 3).
# Nur hörbare Fehler dürfen *vorlesend* gejagt werden; alles andere ist
# audio-blind und läuft ausschließlich über Markieren (deterministisch).
METHOD_MARK = "markieren"
METHOD_READ_OR_MARK = "lesen_oder_markieren"
# Beistrich-Lückenmodus: nicht am Wort, sondern an der Lücke markieren
# (Konzept Abschnitt 2, „Interaktions-Erweiterung für Beistriche").
METHOD_MARK_GAP = "markieren_luecke"
VALID_METHODS = frozenset({METHOD_MARK, METHOD_READ_OR_MARK, METHOD_MARK_GAP})

NO_REGEL = "–"


def erwartete_regel(klasse: str) -> int | str:
    """Liefert die laut Konzept erwartete Regel-Angabe für eine Fehlerklasse."""
    if klasse in KLASSE_ZU_REGEL:
        return KLASSE_ZU_REGEL[klasse]
    return NO_REGEL


def validate_error_regel(klasse: str, regel: int | str, method: str) -> list[str]:
    """Prüft einen ``proofread_error`` gegen das Konzept. Gibt Fehlertexte zurück.

    Leere Liste = alles korrekt. Geprüft wird:
    * Regel-Nummer passt zur Klasse (bzw. „–" außerhalb der acht Punkte).
    * ``method`` ist gültig und nur ``hoerbar`` darf vorlesend gejagt werden.
    """
    errors: list[str] = []
    expected = erwartete_regel(klasse)

    if klasse in KLASSE_ZU_REGEL:
        if regel != expected:
            errors.append(
                f"Klasse '{klasse}' verlangt regel {expected}, hat aber {regel!r}."
            )
    elif klasse in KLASSEN_OHNE_REGEL:
        if regel != NO_REGEL:
            errors.append(
                f"Klasse '{klasse}' liegt außerhalb der 8 Regeln und braucht "
                f"regel '–', hat aber {regel!r}."
            )
    else:
        errors.append(f"unbekannte Fehlerklasse '{klasse}'.")

    if method not in VALID_METHODS:
        errors.append(
            f"method '{method}' ungültig (erlaubt: {sorted(VALID_METHODS)})."
        )
    elif method == METHOD_READ_OR_MARK and klasse != "hoerbar":
        errors.append(
            f"nur Klasse 'hoerbar' darf method '{METHOD_READ_OR_MARK}' nutzen; "
            f"'{klasse}' ist audio-blind → nur '{METHOD_MARK}'."
        )
    elif method == METHOD_MARK_GAP and klasse != "komma":
        errors.append(
            f"method '{METHOD_MARK_GAP}' ist der Beistrich-Lückenmodus und nur "
            f"für Klasse 'komma' gedacht, nicht für '{klasse}'."
        )

    return errors
