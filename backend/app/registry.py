"""Geladene Fälle + aktiver Scoring-Provider (einmalig, prozessweit).

Die Story-Inhalte sind statisch (versionierte Markdown/YAML) – sie werden einmal
geladen und validiert. Schlägt die Validierung fehl, soll der Start scheitern
(lieber laut als mit kaputten Inhalten online).
"""

from __future__ import annotations

from functools import lru_cache

from .config import get_settings
from .scoring import ScoringProvider, get_provider
from .story.graph import Case
from .story.loader import discover_cases


@lru_cache
def get_cases() -> dict[str, Case]:
    return discover_cases(get_settings().stories_dir)


@lru_cache
def get_scoring_provider() -> ScoringProvider:
    return get_provider(get_settings().scoring_provider)


def reset_caches() -> None:
    """Für Tests: Caches leeren (z. B. nach Env-Wechsel)."""
    get_cases.cache_clear()
    get_scoring_provider.cache_clear()
