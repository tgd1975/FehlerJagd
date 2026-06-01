"""FastAPI-App – FehlerJagd-Backend.

Verdrahtet Story-Engine, deterministische Fehlerjagd und das austauschbare
Scoring zu einer lokalen Web-API (PC-first; PWA-Frontend spricht dagegen).
Beim Start werden die Fälle geladen/validiert und die DB-Tabellen angelegt.
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .db import init_db
from .registry import get_cases, get_scoring_provider
from .routers import cases, navigation, progress, proofread, scoring


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    get_cases()              # früh laden & validieren (Start scheitert bei kaputten Inhalten)
    get_scoring_provider()
    yield


app = FastAPI(title="FehlerJagd API", version="0.1.0", lifespan=lifespan)

_settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(_settings.cors_origins),
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cases.router)
app.include_router(navigation.router)
app.include_router(proofread.router)
app.include_router(scoring.router)
app.include_router(progress.router)


@app.get("/health", tags=["meta"])
def health() -> dict:
    return {
        "status": "ok",
        "scoring_provider": _settings.scoring_provider,
        "scoring_calibrated": _settings.scoring_provider != "stub",
        "cases": list(get_cases().keys()),
    }
