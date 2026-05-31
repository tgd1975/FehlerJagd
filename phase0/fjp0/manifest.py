"""Datensatz-Manifest: beschreibt die Clips und ihre Wahrheits-Labels.

ENTSCHEIDUNG / ABWEICHUNG (DECISIONS.md): Die Story-Engine nutzt YAML
(``graph.yaml``). Für das Phase-0-Manifest verwenden wir bewusst **CSV**
(Stdlib ``csv``) statt YAML – so bleibt das gesamte Harness inklusive
Datensatz-Handling **dependency-frei** und ohne PyYAML testbar. CSV ist zudem
diff-freundlich und in jeder Tabellenkalkulation editierbar.

Spalten
-------
``clip``      Pfad zur WAV-Datei, relativ zum Manifest-Verzeichnis.
``kind``      ``vorlesen`` (Flüssigkeit) | ``fehlerjagd`` (lautgetreue Prüfung).
``text``      Bei ``vorlesen``: erwarteter Satz. Bei ``fehlerjagd``: das *richtige*
              Wort, gegen das die Distanz gemessen wird.
``shown``     Nur ``fehlerjagd``: die gezeigte Falschschreibung (z. B. ``Tihsc``).
``label``     Wahrheit für die Kalibrierung:
              ``vorlesen``  → ``fluent`` | ``stocked``
              ``fehlerjagd``→ ``literal`` | ``autocorrected``
``note``      Optional, frei.

Echte Aufnahmen + ihr Manifest liegen unter ``phase0/data/`` (per .gitignore
ausgeschlossen – Kinderstimmen werden nie committet).
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

KIND_FLUENCY = "vorlesen"
KIND_LITERAL = "fehlerjagd"

LABELS_FLUENCY = {"fluent", "stocked"}
LABELS_LITERAL = {"literal", "autocorrected"}

_REQUIRED_COLUMNS = {"clip", "kind", "text", "label"}


@dataclass(frozen=True)
class ClipEntry:
    clip: str           # absoluter Pfad zur WAV
    kind: str
    text: str           # Satz (vorlesen) bzw. richtiges Wort (fehlerjagd)
    shown: str          # Falschschreibung (nur fehlerjagd), sonst ""
    label: str
    note: str = ""

    @property
    def is_fluency(self) -> bool:
        return self.kind == KIND_FLUENCY

    @property
    def is_literal(self) -> bool:
        return self.kind == KIND_LITERAL


def _validate(entry: ClipEntry, row_no: int) -> None:
    if entry.kind == KIND_FLUENCY:
        if entry.label not in LABELS_FLUENCY:
            raise ValueError(
                f"Zeile {row_no}: label '{entry.label}' für kind=vorlesen muss "
                f"eines von {sorted(LABELS_FLUENCY)} sein."
            )
    elif entry.kind == KIND_LITERAL:
        if entry.label not in LABELS_LITERAL:
            raise ValueError(
                f"Zeile {row_no}: label '{entry.label}' für kind=fehlerjagd muss "
                f"eines von {sorted(LABELS_LITERAL)} sein."
            )
        if not entry.shown:
            raise ValueError(
                f"Zeile {row_no}: kind=fehlerjagd braucht eine 'shown'-Spalte "
                f"(die gezeigte Falschschreibung)."
            )
    else:
        raise ValueError(
            f"Zeile {row_no}: unbekanntes kind '{entry.kind}' "
            f"(erlaubt: {KIND_FLUENCY}, {KIND_LITERAL})."
        )


def load_manifest(path: str | Path) -> list[ClipEntry]:
    """Liest und validiert ein CSV-Manifest; Clip-Pfade werden absolut gemacht."""
    path = Path(path)
    base = path.parent
    entries: list[ClipEntry] = []
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        missing = _REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            raise ValueError(
                f"{path}: fehlende Spalten {sorted(missing)} "
                f"(gefunden: {reader.fieldnames})."
            )
        for i, row in enumerate(reader, start=2):  # Zeile 1 = Header
            clip_rel = (row.get("clip") or "").strip()
            if not clip_rel or clip_rel.startswith("#"):
                continue  # Leer- bzw. Kommentarzeile (#) überspringen
            entry = ClipEntry(
                clip=str((base / clip_rel).resolve()),
                kind=(row.get("kind") or "").strip(),
                text=(row.get("text") or "").strip(),
                shown=(row.get("shown") or "").strip(),
                label=(row.get("label") or "").strip(),
                note=(row.get("note") or "").strip(),
            )
            _validate(entry, i)
            entries.append(entry)
    return entries


def write_manifest(path: str | Path, entries: list[ClipEntry]) -> None:
    """Schreibt Einträge als CSV (Clip-Pfade so, wie übergeben)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["clip", "kind", "text", "shown", "label", "note"])
        for e in entries:
            writer.writerow([e.clip, e.kind, e.text, e.shown, e.label, e.note])
