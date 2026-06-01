"""Lädt und **validiert** Fälle aus ``stories/<fall>/graph.yaml``.

Die Validierung ist bewusst streng – sie macht das didaktische Konzept
maschinenprüfbar und fängt Autorenfehler früh ab. Geprüft wird u. a.:

* gültiger ``mode`` pro Knoten;
* ``proofread_errors`` **nur** auf ``mode: fehlerjagd`` (harte Konzept-Regel:
  Falschschreibungen niemals im Vorlese-Text → Interferenz-Schutz);
* Regel-/Methoden-Konsistenz jedes Fehlers (siehe ``regeln.py``);
* alle ``goto``/``choices``-Ziele existieren; Startknoten existiert;
* referenzierte Szenen-Markdown-Dateien sind vorhanden.

Fehler werden gesammelt und als eine :class:`StoryValidationError` geworfen,
damit Autor:innen alle Probleme auf einmal sehen.
"""

from __future__ import annotations

from pathlib import Path

import yaml

from .graph import (
    REQUIRES_ALL_GREEN,
    VALID_MODES,
    Case,
    Choice,
    MODE_FEHLERJAGD,
    MODE_KALIBRIERUNG,
    ProofreadError,
    Scene,
)
from .regeln import validate_error_regel


class StoryValidationError(ValueError):
    """Gebündelte Validierungsfehler eines Falls."""

    def __init__(self, case_id: str, errors: list[str]) -> None:
        self.case_id = case_id
        self.errors = errors
        joined = "\n  - ".join(errors)
        super().__init__(f"Fall '{case_id}' ungültig:\n  - {joined}")


def _parse_proofread_error(raw: dict, where: str, errors: list[str]) -> ProofreadError | None:
    required = ("shown", "correct", "klasse", "regel", "tipp", "method")
    missing = [k for k in required if k not in raw]
    if missing:
        errors.append(f"{where}: proofread_error fehlt Felder {missing}.")
        return None
    pe = ProofreadError(
        shown=str(raw["shown"]),
        correct=str(raw["correct"]),
        klasse=str(raw["klasse"]),
        regel=raw["regel"],
        tipp=str(raw["tipp"]),
        method=str(raw["method"]),
    )
    for msg in validate_error_regel(pe.klasse, pe.regel, pe.method):
        errors.append(f"{where} ({pe.shown!r}): {msg}")
    return pe


def _parse_scene(scene_id: str, raw: dict, errors: list[str]) -> Scene:
    mode = raw.get("mode", "")
    if mode not in VALID_MODES:
        errors.append(f"Szene '{scene_id}': ungültiger mode '{mode}'.")

    choices = [
        Choice(label=str(c["label"]), goto=str(c["goto"]))
        for c in raw.get("choices", [])
        if isinstance(c, dict) and "label" in c and "goto" in c
    ]

    proofread_errors: list[ProofreadError] = []
    raw_pe = raw.get("proofread_errors", [])
    if raw_pe and mode != MODE_FEHLERJAGD:
        errors.append(
            f"Szene '{scene_id}': proofread_errors nur auf mode '{MODE_FEHLERJAGD}' "
            f"erlaubt (Falschschreibungen nie im Vorlese-Text)."
        )
    for pe_raw in raw_pe:
        pe = _parse_proofread_error(pe_raw, f"Szene '{scene_id}'", errors)
        if pe:
            proofread_errors.append(pe)

    if mode == MODE_FEHLERJAGD and not proofread_errors:
        errors.append(f"Szene '{scene_id}': mode fehlerjagd ohne proofread_errors.")

    requires = raw.get("requires")
    if requires is not None and requires != REQUIRES_ALL_GREEN:
        errors.append(
            f"Szene '{scene_id}': unbekanntes requires '{requires}' "
            f"(erlaubt: '{REQUIRES_ALL_GREEN}')."
        )

    eich = raw.get("eich_saetze", []) or []
    if mode == MODE_KALIBRIERUNG and not eich:
        errors.append(f"Szene '{scene_id}': mode kalibrierung ohne eich_saetze.")

    return Scene(
        scene_id=scene_id,
        text_file=str(raw.get("text", "")),
        mode=mode,
        target_patterns=list(raw.get("target_patterns", []) or []),
        choices=choices,
        goto=(str(raw["goto"]) if raw.get("goto") else None),
        proofread_errors=proofread_errors,
        requires=requires,
        next_case=(str(raw["next_case"]) if raw.get("next_case") else None),
        eich_saetze=[str(s) for s in eich],
        hints=bool(raw.get("hints", False)),
        scoring=(str(raw["scoring"]) if raw.get("scoring") else None),
    )


def _validate_references(case_dir: Path, nodes: dict[str, Scene],
                         start: str, errors: list[str]) -> None:
    if start not in nodes:
        errors.append(f"Startknoten '{start}' existiert nicht.")
    for scene in nodes.values():
        for target in scene.next_ids():
            if target not in nodes:
                errors.append(
                    f"Szene '{scene.scene_id}': Ziel '{target}' existiert nicht."
                )
        if scene.text_file:
            if not (case_dir / scene.text_file).is_file():
                errors.append(
                    f"Szene '{scene.scene_id}': Textdatei '{scene.text_file}' fehlt."
                )


def load_case(graph_path: str | Path) -> Case:
    """Lädt einen Fall aus seiner ``graph.yaml`` und validiert ihn streng."""
    graph_path = Path(graph_path)
    case_dir = graph_path.parent
    data = yaml.safe_load(graph_path.read_text(encoding="utf-8")) or {}

    # case_id darf fehlen (z. B. Tutorial) → aus dem Verzeichnisnamen ableiten.
    case_id = str(data.get("case_id") or case_dir.name)
    errors: list[str] = []

    raw_nodes = data.get("nodes") or data.get("scenes") or {}
    if not raw_nodes:
        errors.append("keine 'nodes' definiert.")

    nodes: dict[str, Scene] = {}
    for sid, raw in raw_nodes.items():
        if not isinstance(raw, dict):
            errors.append(f"Szene '{sid}': ungültige Definition.")
            continue
        nodes[str(sid)] = _parse_scene(str(sid), raw, errors)

    start = str(data.get("start", ""))
    if not start:
        errors.append("kein 'start' definiert.")

    if nodes:
        _validate_references(case_dir, nodes, start, errors)

    if errors:
        raise StoryValidationError(case_id, errors)

    return Case(
        case_id=case_id,
        titel=str(data.get("titel") or data.get("title") or case_id),
        start=start,
        nodes=nodes,
        schauplatz=str(data.get("schauplatz", "")),
        ziel_muster=list(data.get("ziel_muster", []) or []),
        hints=bool(data.get("hints", False)),
        title_image=(str(data["title_image"]) if data.get("title_image") else None),
        path=str(case_dir),
    )


def discover_cases(stories_dir: str | Path) -> dict[str, Case]:
    """Lädt alle Fälle unter ``stories_dir`` (jede ``*/graph.yaml``).

    Sortiert nach Fall-Verzeichnis, damit fall-00, fall-01, … in Reihenfolge
    erscheinen. Wirft beim ersten ungültigen Fall – Inhalte müssen valide sein.
    """
    stories_dir = Path(stories_dir)
    cases: dict[str, Case] = {}
    for graph in sorted(stories_dir.glob("*/graph.yaml")):
        case = load_case(graph)
        cases[case.case_id] = case
    return cases


def read_scene_text(case: Case, scene: Scene) -> str:
    """Liest den Szenen-Text und entfernt optionales YAML-Front-Matter.

    Front-Matter (``---`` … ``---`` am Dateianfang) ist Autoren-Metadaten und
    darf weder angezeigt noch (in der Fehlerjagd) mit-tokenisiert werden – sonst
    verschöben sich die Token-Indizes gegenüber dem, was das Kind sieht.
    """
    if not scene.text_file:
        return ""
    raw = (Path(case.path) / scene.text_file).read_text(encoding="utf-8")
    return strip_front_matter(raw)


def strip_front_matter(text: str) -> str:
    """Entfernt einen führenden ``---`` … ``---``-Block."""
    if text.lstrip().startswith("---"):
        body = text.lstrip()
        end = body.find("\n---", 3)
        if end != -1:
            after = body[end + 4 :]
            return after.lstrip("\n")
    return text
