"""TTS fürs Wort-Vorsprechen (Mikro-Lernschleife, Konzept §3).

Pluggable (Konzept 6d): Default ``browser`` weist den Client an, das Wort selbst
über die Web Speech API zu sprechen – keine Serverkosten, offline, kindersicher
(nur ein Einzelwort). Später kann ein Server-Provider Audio zurückliefern.
"""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from ..config import get_settings

router = APIRouter(prefix="/tts", tags=["tts"])


class TtsRequest(BaseModel):
    word: str
    lang: str = "de-AT"


class TtsResponse(BaseModel):
    mode: str           # 'browser' ⇒ Client spricht selbst; sonst 'audio'
    text: str
    lang: str
    audio_url: str | None = None


@router.post("/word", response_model=TtsResponse)
def tts_word(req: TtsRequest) -> TtsResponse:
    provider = get_settings().tts_provider
    if provider == "browser":
        return TtsResponse(mode="browser", text=req.word, lang=req.lang)
    # Platzhalter für künftige Server-Provider (local/azure/prerender).
    return TtsResponse(mode="browser", text=req.word, lang=req.lang)
