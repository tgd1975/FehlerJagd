"""Domänen-Modell des Story-Graphen (Branch & Bottleneck).

Reine Dataclasses ohne I/O – der Loader (``loader.py``) baut sie aus den
``graph.yaml``-Dateien, die Navigation (``navigation.py``) wandert darin.

Modi (siehe Konzept Abschnitt 3 & 6e, plus Tutorial fall-00):
* ``vorlesen``     – korrekter Text, phonetische Flüssigkeits-Bewertung.
* ``fehlerjagd``   – Fälscher-Notiz mit eingebauten Fehlern (Markieren).
* ``kalibrierung`` – Stimm-Eichung im Tutorial (keine Wertung, nur Übung).
"""

from __future__ import annotations

from dataclasses import dataclass, field

MODE_VORLESEN = "vorlesen"
MODE_FEHLERJAGD = "fehlerjagd"
MODE_KALIBRIERUNG = "kalibrierung"
VALID_MODES = frozenset({MODE_VORLESEN, MODE_FEHLERJAGD, MODE_KALIBRIERUNG})

# Bonus-/Gating-Bedingung für freischaltbare Szenen.
REQUIRES_ALL_GREEN = "all_green"


@dataclass(frozen=True)
class Choice:
    """Eine Entscheidungsoption, die zu einer Folge-Szene führt."""

    label: str
    goto: str


@dataclass(frozen=True)
class ProofreadError:
    """Ein eingebauter Fehler einer Fälscher-Notiz (mode: fehlerjagd)."""

    shown: str              # gezeigte Falschschreibung, z. B. "Bücehr"
    correct: str            # richtige Schreibweise, z. B. "Bücher"
    klasse: str             # Fehlerklasse (grossschreibung, ie, hoerbar …)
    regel: int | str        # Merkregel 1–8 oder "–"
    tipp: str               # kindgerechte Begründung für die Auflösung
    method: str             # markieren | lesen_oder_markieren

    @property
    def error_id(self) -> str:
        """Stabile ID für Persistenz/Dashboard (proofread_history)."""
        return f"{self.shown}->{self.correct}"

    @property
    def is_gap(self) -> bool:
        """True für Beistrich-Fehler (an der Lücke markieren, nicht am Wort)."""
        return self.method == "markieren_luecke"


@dataclass(frozen=True)
class Scene:
    """Ein Knoten im Story-Graphen."""

    scene_id: str
    text_file: str                          # Markdown-Datei (relativ zum Fall)
    mode: str
    target_patterns: list[str] = field(default_factory=list)
    choices: list[Choice] = field(default_factory=list)
    goto: str | None = None                 # linearer Übergang (ohne Choices)
    proofread_errors: list[ProofreadError] = field(default_factory=list)
    requires: str | None = None             # z. B. "all_green" (Bonus-Gate)
    next_case: str | None = None            # Übergang in den nächsten Fall
    eich_saetze: list[str] = field(default_factory=list)  # nur kalibrierung
    hints: bool = False
    scoring: str | None = None              # z. B. "uebung" (nie gatekeepen)

    @property
    def is_terminal(self) -> bool:
        """Endknoten: keine Choices, kein goto, kein Folgefall."""
        return not self.choices and self.goto is None and self.next_case is None

    @property
    def is_bonus(self) -> bool:
        return self.requires is not None

    def next_ids(self) -> list[str]:
        """Alle Szenen-IDs, die von hier aus erreichbar sind (für Validierung)."""
        ids = [c.goto for c in self.choices]
        if self.goto:
            ids.append(self.goto)
        return ids


@dataclass(frozen=True)
class Case:
    """Ein vollständiger Fall."""

    case_id: str
    titel: str
    start: str
    nodes: dict[str, Scene]
    schauplatz: str = ""
    ziel_muster: list[str] = field(default_factory=list)
    hints: bool = False
    title_image: str | None = None
    path: str = ""                          # Verzeichnis des Falls

    def scene(self, scene_id: str) -> Scene:
        if scene_id not in self.nodes:
            raise KeyError(f"Szene '{scene_id}' nicht in Fall '{self.case_id}'.")
        return self.nodes[scene_id]
