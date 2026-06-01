"""Wandelt Domänen-Objekte in API-Schemas (versteckt u. a. die Lösungen)."""

from __future__ import annotations

from .proofread.check import tokenize_note
from .schemas import CaseSummary, ChoiceOut, SceneOut, TokenOut
from .story.graph import MODE_FEHLERJAGD, Case, Scene
from .story.loader import read_scene_text


def case_summary(case: Case) -> CaseSummary:
    return CaseSummary(
        case_id=case.case_id,
        titel=case.titel,
        schauplatz=case.schauplatz,
        ziel_muster=case.ziel_muster,
        start=case.start,
        title_image=case.title_image,
    )


def scene_out(case: Case, scene: Scene) -> SceneOut:
    text = read_scene_text(case, scene)
    tokens = (
        [TokenOut(index=t.index, text=t.text, start=t.start, end=t.end)
         for t in tokenize_note(text)]
        if scene.mode == MODE_FEHLERJAGD else []
    )
    return SceneOut(
        case_id=case.case_id,
        scene_id=scene.scene_id,
        mode=scene.mode,
        text=text,
        tokens=tokens,
        target_patterns=scene.target_patterns,
        choices=[
            ChoiceOut(index=i, label=c.label, goto=c.goto)
            for i, c in enumerate(scene.choices)
        ],
        has_goto=scene.goto is not None,
        is_terminal=scene.is_terminal,
        is_bonus=scene.is_bonus,
        hints=scene.hints or case.hints,
        scoring=scene.scoring,
        eich_saetze=scene.eich_saetze,
        proofread_error_count=len(scene.proofread_errors),
        next_case=scene.next_case,
    )
