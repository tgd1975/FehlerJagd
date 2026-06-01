"""Navigation im Story-Graphen (Branch & Bottleneck + sanftes Gating).

Bestimmt aus aktueller Szene + Entscheidung die nächste Szene. Kapselt die
sanfte Gating-Regel: eine Bonus-Szene (``requires: all_green``) wird nur betreten,
wenn durchgehend grün gelesen wurde – sonst endet der Fall regulär (kein hartes
Blockieren, Konzept Abschnitt 3 / Risiko 4).
"""

from __future__ import annotations

from dataclasses import dataclass

from .graph import REQUIRES_ALL_GREEN, Case, Scene


@dataclass(frozen=True)
class NavResult:
    next_scene_id: str | None       # None ⇒ Fall zu Ende (an dieser Stelle)
    next_case_id: str | None        # gesetzt, wenn in den nächsten Fall gewechselt wird
    ended: bool                     # True ⇒ kein weiterer Knoten in diesem Fall
    skipped_bonus: bool = False     # True ⇒ Bonus war gesperrt (nicht all_green)


def _gate_ok(scene: Scene, all_green: bool) -> bool:
    if scene.requires == REQUIRES_ALL_GREEN:
        return all_green
    return True


def next_scene(
    case: Case,
    current_id: str,
    *,
    choice_index: int | None = None,
    all_green: bool = False,
) -> NavResult:
    """Ermittelt die Folge-Szene.

    ``choice_index`` ist nur bei Szenen mit ``choices`` nötig (und dann Pflicht).
    ``all_green`` steuert das Bonus-Gate.
    """
    scene = case.scene(current_id)

    if scene.choices:
        if choice_index is None:
            raise ValueError(
                f"Szene '{current_id}' hat Entscheidungen – choice_index nötig."
            )
        if not 0 <= choice_index < len(scene.choices):
            raise IndexError(
                f"choice_index {choice_index} außerhalb 0..{len(scene.choices) - 1}."
            )
        target = scene.choices[choice_index].goto
    elif scene.goto:
        target = scene.goto
    elif scene.next_case:
        return NavResult(None, scene.next_case, ended=True)
    else:
        return NavResult(None, None, ended=True)

    target_scene = case.scene(target)
    if not _gate_ok(target_scene, all_green):
        # Bonus gesperrt → Fall endet regulär, kein harter Stopp.
        return NavResult(None, None, ended=True, skipped_bonus=True)

    return NavResult(target, None, ended=False)
