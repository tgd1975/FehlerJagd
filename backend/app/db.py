"""Datenbank-Engine/Session (SQLModel)."""

from __future__ import annotations

from collections.abc import Iterator

from sqlmodel import Session, SQLModel, create_engine

from .config import get_settings

_settings = get_settings()
# check_same_thread=False: FastAPI nutzt mehrere Threads gegen dieselbe SQLite.
_connect_args = {"check_same_thread": False} if _settings.database_url.startswith("sqlite") else {}
engine = create_engine(_settings.database_url, echo=False, connect_args=_connect_args)


def init_db() -> None:
    """Legt die Tabellen an (idempotent). Beim App-Start aufrufen."""
    import app.models  # noqa: F401  (registriert die Tabellen)
    SQLModel.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
    """FastAPI-Dependency: eine Session pro Request."""
    with Session(engine) as session:
        yield session
