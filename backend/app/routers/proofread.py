"""Deterministische Fehlerjagd-Prüfung (/proofread/check)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from ..db import get_session
from ..models import ProofreadHistory
from ..proofread.check import check_markings, tokenize_note
from ..registry import get_cases
from ..schemas import (
    ErrorOutcomeOut,
    ProofreadCheckRequest,
    ProofreadCheckResponse,
    TokenOut,
)
from ..story.graph import MODE_FEHLERJAGD
from ..story.loader import read_scene_text

router = APIRouter(tags=["proofread"])


@router.post("/proofread/check", response_model=ProofreadCheckResponse)
def proofread_check(
    req: ProofreadCheckRequest,
    session: Session = Depends(get_session),
) -> ProofreadCheckResponse:
    cases = get_cases()
    if req.case_id not in cases:
        raise HTTPException(404, f"Fall '{req.case_id}' nicht gefunden.")
    case = cases[req.case_id]
    if req.scene_id not in case.nodes:
        raise HTTPException(404, f"Szene '{req.scene_id}' nicht in '{req.case_id}'.")
    scene = case.scene(req.scene_id)
    if scene.mode != MODE_FEHLERJAGD:
        raise HTTPException(400, f"Szene '{req.scene_id}' ist keine Fehlerjagd.")

    note_text = read_scene_text(case, scene)
    result = check_markings(
        note_text, scene.proofread_errors,
        req.marked_indices, req.marked_gap_indices,
    )

    # Fehlerjagd-Verlauf fürs Eltern-Dashboard (welche Regeln werden übersehen?).
    if req.profile_id is not None:
        for o in result.outcomes:
            session.add(ProofreadHistory(
                profile_id=req.profile_id, case_id=req.case_id,
                scene_id=req.scene_id, error_id=o.error_id,
                klasse=o.klasse, regel=str(o.regel), gefunden=o.found,
            ))
        session.commit()

    return ProofreadCheckResponse(
        total=result.total,
        found_count=result.found_count,
        false_positives=result.false_positives,
        all_found=result.all_found,
        score=result.score,
        outcomes=[
            ErrorOutcomeOut(
                shown=o.shown, correct=o.correct, klasse=o.klasse,
                regel=str(o.regel), tipp=o.tipp, method=o.method,
                token_index=o.token_index, is_gap=o.is_gap, found=o.found,
            )
            for o in result.outcomes
        ],
        false_positive_indices=result.false_positive_indices,
        false_positive_gap_indices=result.false_positive_gap_indices,
        tokens=[
            TokenOut(index=t.index, text=t.text, start=t.start, end=t.end)
            for t in tokenize_note(note_text)
        ],
    )
