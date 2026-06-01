"""Austauschbares Scoring (stub bis GO; danach local/azure/speechace)."""

from __future__ import annotations

from .base import ScoringProvider
from .stub import StubScoringProvider


def get_provider(name: str) -> ScoringProvider:
    """Fabrik laut Config. Unbekannt/local-ohne-torch → klare Fehlermeldung."""
    name = (name or "stub").lower()
    if name == "stub":
        return StubScoringProvider()
    if name == "local":
        from .local_torch import LocalTorchScoringProvider
        return LocalTorchScoringProvider()
    raise ValueError(
        f"Scoring-Provider '{name}' unbekannt/nicht implementiert "
        f"(verfügbar: stub, local). azure/speechace folgen."
    )
