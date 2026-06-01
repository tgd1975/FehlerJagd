"""Navigation zwischen Szenen (/scene/next)."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..registry import get_cases
from ..schemas import NextRequest, NextResponse
from ..serialize import scene_out
from ..story.navigation import next_scene

router = APIRouter(tags=["navigation"])


@router.post("/scene/next", response_model=NextResponse)
def scene_next(req: NextRequest) -> NextResponse:
    cases = get_cases()
    if req.case_id not in cases:
        raise HTTPException(404, f"Fall '{req.case_id}' nicht gefunden.")
    case = cases[req.case_id]
    if req.scene_id not in case.nodes:
        raise HTTPException(404, f"Szene '{req.scene_id}' nicht in '{req.case_id}'.")

    try:
        result = next_scene(
            case, req.scene_id,
            choice_index=req.choice_index, all_green=req.all_green,
        )
    except (ValueError, IndexError) as exc:
        raise HTTPException(400, str(exc)) from exc

    # Wechsel in den nächsten Fall: dessen Startszene mitliefern, falls vorhanden.
    if result.next_case_id and result.next_case_id in cases:
        nxt = cases[result.next_case_id]
        return NextResponse(
            ended=result.ended, skipped_bonus=result.skipped_bonus,
            next_case_id=result.next_case_id, next_scene_id=nxt.start,
            scene=scene_out(nxt, nxt.scene(nxt.start)),
        )

    scene = (
        scene_out(case, case.scene(result.next_scene_id))
        if result.next_scene_id else None
    )
    return NextResponse(
        ended=result.ended, skipped_bonus=result.skipped_bonus,
        next_scene_id=result.next_scene_id, next_case_id=result.next_case_id,
        scene=scene,
    )
