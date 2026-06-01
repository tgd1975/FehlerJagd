"""Eltern-Dashboard-Endpunkt."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session, select

from ..dashboard import aggregate_fluency, aggregate_proofread
from ..db import get_session
from ..models import ProofreadHistory, ScoreHistory

router = APIRouter(tags=["dashboard"])


class KlasseStatOut(BaseModel):
    klasse: str
    regel: str
    total: int
    found: int
    missed: int
    found_ratio: float


class SceneFluencyOut(BaseModel):
    case_id: str
    scene_id: str
    words: int
    green: int
    yellow: int
    red: int
    avg_score: float | None


class DashboardOut(BaseModel):
    profile_id: int
    proofread_by_klasse: list[KlasseStatOut]
    fluency_by_scene: list[SceneFluencyOut]
    most_missed: list[str]          # Klassen mit der schlechtesten Trefferquote


@router.get("/dashboard/{profile_id}", response_model=DashboardOut)
def dashboard(profile_id: int, session: Session = Depends(get_session)) -> DashboardOut:
    pr_rows = session.exec(
        select(ProofreadHistory).where(ProofreadHistory.profile_id == profile_id)
    ).all()
    sc_rows = session.exec(
        select(ScoreHistory).where(ScoreHistory.profile_id == profile_id)
    ).all()

    pr_stats = aggregate_proofread(pr_rows)
    fl_stats = aggregate_fluency(sc_rows)
    most_missed = [s.klasse for s in pr_stats if s.found_ratio < 0.5 and s.missed > 0]

    return DashboardOut(
        profile_id=profile_id,
        proofread_by_klasse=[
            KlasseStatOut(klasse=s.klasse, regel=s.regel, total=s.total,
                          found=s.found, missed=s.missed, found_ratio=s.found_ratio)
            for s in pr_stats
        ],
        fluency_by_scene=[
            SceneFluencyOut(case_id=s.case_id, scene_id=s.scene_id, words=s.words,
                            green=s.green, yellow=s.yellow, red=s.red,
                            avg_score=s.avg_score)
            for s in fl_stats
        ],
        most_missed=most_missed,
    )
