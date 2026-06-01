"""Konfiguration über Umgebungsvariablen (mit sinnvollen Defaults).

Bewusst schlank (kein pydantic-settings nötig). Alle Provider-/Pfad-/Schwellen-
Entscheidungen hängen hier – die App liest nur ``settings``.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

# Repo-Wurzel: backend/app/config.py → parents[2].
REPO_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    # Scoring-Provider: 'stub' bis zur Phase-0-Freigabe, danach 'local'.
    scoring_provider: str = os.getenv("FJ_SCORING", "stub")
    # Story-Inhalte.
    stories_dir: str = os.getenv("FJ_STORIES_DIR", str(REPO_ROOT / "stories"))
    # SQLite-DB (per .gitignore ausgeschlossen). In-Memory für Tests via Env.
    database_url: str = os.getenv("FJ_DB_URL", f"sqlite:///{REPO_ROOT / 'backend' / 'fehlerjagd.db'}")
    # Flüssigkeits-Schwellen (Phase 0 kalibriert sie).
    green: float = float(os.getenv("FJ_GREEN", "0.80"))
    yellow: float = float(os.getenv("FJ_YELLOW", "0.55"))
    literal_max: float = float(os.getenv("FJ_LITERAL_MAX", "0.55"))
    # CORS für die lokale Frontend-Entwicklung (Vite-Default-Port).
    cors_origins: tuple[str, ...] = tuple(
        os.getenv("FJ_CORS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
