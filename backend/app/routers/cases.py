"""Fälle & Szenen abrufen."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..registry import get_cases
from ..schemas import CaseSummary, SceneOut
from ..serialize import case_summary, scene_out

router = APIRouter(prefix="/cases", tags=["cases"])


@router.get("", response_model=list[CaseSummary])
def list_cases() -> list[CaseSummary]:
    return [case_summary(c) for c in get_cases().values()]


@router.get("/{case_id}", response_model=CaseSummary)
def get_case(case_id: str) -> CaseSummary:
    cases = get_cases()
    if case_id not in cases:
        raise HTTPException(404, f"Fall '{case_id}' nicht gefunden.")
    return case_summary(cases[case_id])


@router.get("/{case_id}/scene/{scene_id}", response_model=SceneOut)
def get_scene(case_id: str, scene_id: str) -> SceneOut:
    cases = get_cases()
    if case_id not in cases:
        raise HTTPException(404, f"Fall '{case_id}' nicht gefunden.")
    case = cases[case_id]
    if scene_id not in case.nodes:
        raise HTTPException(404, f"Szene '{scene_id}' nicht in '{case_id}'.")
    return scene_out(case, case.scene(scene_id))
