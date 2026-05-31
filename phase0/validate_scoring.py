#!/usr/bin/env python3
"""Kompatibilitäts-Shim für den im Konzept benannten Einstiegspunkt.

Die Phase-0-Logik wurde in das getestete Paket :mod:`fjp0` refaktoriert
(siehe ``phase0/DECISIONS.md``). Dieses Skript bleibt erhalten, damit der in
``docs/Konzept.md`` / ``CLAUDE.md`` referenzierte Aufruf weiter funktioniert –
es delegiert an die neue CLI.

Beispiele:
    # Einzelclip wie früher:
    python validate_scoring.py score --audio aufnahme.wav --text "der erwartete satz"
    # Voller GO/NO-GO-Lauf über ein Manifest:
    python validate_scoring.py run --manifest data/manifest.csv
    # Selbsttest (ohne torch, ohne echte Aufnahme):
    python validate_scoring.py selftest
"""

from __future__ import annotations

import sys
from pathlib import Path

# Paket aus dem eigenen Verzeichnis importierbar machen, egal von wo gestartet.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fjp0.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
