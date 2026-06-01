"""Belohnungen: Punkte, Pinnwand-Panels, Avatar (Konzept §5)."""

from __future__ import annotations

import json

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from ..db import get_session
from ..models import Profile, UnlockedItem
from ..rewards import (
    AVATAR_CATALOG,
    affordable_items,
    proofread_points,
    scene_reward,
)

router = APIRouter(tags=["rewards"])


def _unlock(session: Session, profile_id: int, item_key: str) -> bool:
    """Schaltet ein Item frei (idempotent). True, wenn neu."""
    exists = session.exec(
        select(UnlockedItem).where(
            UnlockedItem.profile_id == profile_id,
            UnlockedItem.item_key == item_key,
        )
    ).first()
    if exists:
        return False
    session.add(UnlockedItem(profile_id=profile_id, item_key=item_key))
    return True


class SceneCompleteIn(BaseModel):
    profile_id: int
    case_id: str
    scene_id: str
    all_green: bool = False


class RewardOut(BaseModel):
    points: int
    awarded: int
    new_unlocks: list[str]


@router.post("/rewards/scene-complete", response_model=RewardOut)
def reward_scene(body: SceneCompleteIn, session: Session = Depends(get_session)) -> RewardOut:
    profile = session.get(Profile, body.profile_id)
    if not profile:
        raise HTTPException(404, "Profil nicht gefunden.")
    rw = scene_reward(body.case_id, body.scene_id, body.all_green)
    profile.points += rw.points
    new = _unlock(session, body.profile_id, rw.panel_key)
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return RewardOut(points=profile.points, awarded=rw.points,
                     new_unlocks=[rw.panel_key] if new else [])


class ProofreadRewardIn(BaseModel):
    profile_id: int
    found_count: int
    total: int


@router.post("/rewards/proofread", response_model=RewardOut)
def reward_proofread(body: ProofreadRewardIn, session: Session = Depends(get_session)) -> RewardOut:
    profile = session.get(Profile, body.profile_id)
    if not profile:
        raise HTTPException(404, "Profil nicht gefunden.")
    pts = proofread_points(body.found_count, body.total)
    profile.points += pts
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return RewardOut(points=profile.points, awarded=pts, new_unlocks=[])


class CatalogItem(BaseModel):
    item_key: str
    name: str
    cost: int
    affordable: bool
    equipped: bool


@router.get("/rewards/catalog/{profile_id}", response_model=list[CatalogItem])
def catalog(profile_id: int, session: Session = Depends(get_session)) -> list[CatalogItem]:
    profile = session.get(Profile, profile_id)
    if not profile:
        raise HTTPException(404, "Profil nicht gefunden.")
    equipped = set(json.loads(profile.avatar_state or "{}").get("equipped", []))
    affordable = set(affordable_items(profile.points))
    return [
        CatalogItem(item_key=k, name=name, cost=cost,
                    affordable=k in affordable, equipped=k in equipped)
        for k, (name, cost) in AVATAR_CATALOG.items()
    ]


class EquipIn(BaseModel):
    profile_id: int
    item_key: str


@router.post("/avatar/equip", response_model=Profile)
def equip(body: EquipIn, session: Session = Depends(get_session)) -> Profile:
    profile = session.get(Profile, body.profile_id)
    if not profile:
        raise HTTPException(404, "Profil nicht gefunden.")
    if body.item_key not in AVATAR_CATALOG:
        raise HTTPException(400, f"Unbekanntes Item '{body.item_key}'.")
    cost = AVATAR_CATALOG[body.item_key][1]
    if profile.points < cost:
        raise HTTPException(400, "Nicht genug Punkte für dieses Item.")
    state = json.loads(profile.avatar_state or "{}")
    equipped = set(state.get("equipped", []))
    equipped.symmetric_difference_update({body.item_key})  # toggle
    state["equipped"] = sorted(equipped)
    profile.avatar_state = json.dumps(state)
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile
