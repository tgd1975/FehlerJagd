"""Profile, Fortschritt, Punkte/Belohnungen (SQLite)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from ..db import get_session
from ..models import Profile, Progress, UnlockedItem

router = APIRouter(tags=["progress"])


class ProfileIn(BaseModel):
    name: str


class ProgressIn(BaseModel):
    profile_id: int
    case_id: str
    current_scene: str
    completed: bool = False


@router.post("/profiles", response_model=Profile)
def create_profile(body: ProfileIn, session: Session = Depends(get_session)) -> Profile:
    profile = Profile(name=body.name)
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile


@router.get("/profiles", response_model=list[Profile])
def list_profiles(session: Session = Depends(get_session)) -> list[Profile]:
    return list(session.exec(select(Profile)).all())


@router.put("/progress", response_model=Progress)
def upsert_progress(body: ProgressIn, session: Session = Depends(get_session)) -> Progress:
    existing = session.exec(
        select(Progress).where(
            Progress.profile_id == body.profile_id,
            Progress.case_id == body.case_id,
        )
    ).first()
    if existing:
        existing.current_scene = body.current_scene
        existing.completed = body.completed
        session.add(existing)
        session.commit()
        session.refresh(existing)
        return existing
    progress = Progress(**body.model_dump())
    session.add(progress)
    session.commit()
    session.refresh(progress)
    return progress


@router.get("/progress/{profile_id}", response_model=list[Progress])
def get_progress(profile_id: int, session: Session = Depends(get_session)) -> list[Progress]:
    return list(session.exec(
        select(Progress).where(Progress.profile_id == profile_id)
    ).all())


class PointsIn(BaseModel):
    profile_id: int
    delta: int


@router.post("/points", response_model=Profile)
def add_points(body: PointsIn, session: Session = Depends(get_session)) -> Profile:
    profile = session.get(Profile, body.profile_id)
    if not profile:
        raise HTTPException(404, "Profil nicht gefunden.")
    profile.points = max(0, profile.points + body.delta)
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile


@router.get("/rewards/{profile_id}", response_model=list[UnlockedItem])
def get_rewards(profile_id: int, session: Session = Depends(get_session)) -> list[UnlockedItem]:
    return list(session.exec(
        select(UnlockedItem).where(UnlockedItem.profile_id == profile_id)
    ).all())
