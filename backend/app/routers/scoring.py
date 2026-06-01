"""Phonetisches Scoring (Mechanik A & B) über den austauschbaren Provider.

Wichtig: Audio wird in eine **temporäre** Datei geschrieben, bewertet und
**sofort gelöscht** – die Stimme wird nie persistiert (Risiko 6). Solange der
Stub-Provider aktiv ist (vor Phase-0-GO), wird das Audio gar nicht analysiert.
"""

from __future__ import annotations

import os
import tempfile

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlmodel import Session

from ..db import get_session
from ..models import ScoreHistory
from ..registry import get_scoring_provider
from ..schemas import FluencyResponse, WordFluencyOut

router = APIRouter(prefix="/score", tags=["scoring"])


def _save_temp(audio: UploadFile | None) -> str | None:
    if audio is None:
        return None
    suffix = os.path.splitext(audio.filename or "")[1] or ".wav"
    fd, path = tempfile.mkstemp(suffix=suffix)
    with os.fdopen(fd, "wb") as fh:
        fh.write(audio.file.read())
    return path


@router.post("/fluency", response_model=FluencyResponse)
def score_fluency(
    expected_text: str = Form(...),
    case_id: str = Form(""),
    scene_id: str = Form(""),
    profile_id: int | None = Form(None),
    attempt: int = Form(1),
    audio: UploadFile | None = File(None),
    session: Session = Depends(get_session),
) -> FluencyResponse:
    provider = get_scoring_provider()
    path = _save_temp(audio)
    try:
        result = provider.score_fluency(path or "", expected_text)
    finally:
        if path and os.path.exists(path):
            os.remove(path)        # Stimme nie aufbewahren

    if profile_id is not None and case_id and scene_id:
        for w in result.words:
            session.add(ScoreHistory(
                profile_id=profile_id, case_id=case_id, scene_id=scene_id,
                word=w.word, score=w.score, color=w.color, attempt=attempt,
            ))
        session.commit()

    return FluencyResponse(
        provider=result.provider,
        calibrated=result.calibrated,
        clip_score=result.clip_score,
        all_green=result.all_green,
        words=[WordFluencyOut(word=w.word, score=w.score, color=w.color)
               for w in result.words],
    )
