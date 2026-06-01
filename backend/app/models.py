"""SQLite-Persistenz (SQLModel) – siehe Konzept Abschnitt 6f.

Bewusst nahe an der Konzept-Tabelle gehalten. Audio wird **nie** gespeichert
(nur Scores/Ergebnisse) – Stimme bleibt am Gerät (Risiko 6).
"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


def _now() -> datetime:
    return datetime.now(timezone.utc)


class Profile(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    avatar_state: str = "{}"        # JSON-String (ausgestattete Items)
    points: int = 0
    created_at: datetime = Field(default_factory=_now)


class Progress(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    profile_id: int = Field(foreign_key="profile.id", index=True)
    case_id: str = Field(index=True)
    current_scene: str
    completed: bool = False
    updated_at: datetime = Field(default_factory=_now)


class ScoreHistory(SQLModel, table=True):
    """Flüssigkeits-Verlauf (Mechanik A), pro Wort."""

    id: int | None = Field(default=None, primary_key=True)
    profile_id: int = Field(foreign_key="profile.id", index=True)
    case_id: str = Field(index=True)
    scene_id: str = Field(index=True)
    word: str
    score: float | None = None
    color: str = ""
    attempt: int = 1
    ts: datetime = Field(default_factory=_now)


class ProofreadHistory(SQLModel, table=True):
    """Fehlerjagd-Verlauf (Mechanik B) fürs Eltern-Dashboard.

    Erlaubt die Auswertung „welche Regel-Kategorien werden oft übersehen?".
    """

    id: int | None = Field(default=None, primary_key=True)
    profile_id: int = Field(foreign_key="profile.id", index=True)
    case_id: str = Field(index=True)
    scene_id: str = Field(index=True)
    error_id: str
    klasse: str = Field(index=True)
    regel: str = ""                 # als Text (1–8 oder „–")
    gefunden: bool = False
    ts: datetime = Field(default_factory=_now)


class UnlockedItem(SQLModel, table=True):
    """Freigeschaltete Belohnungen (Avatar-Teile, Pinnwand-Panels)."""

    id: int | None = Field(default=None, primary_key=True)
    profile_id: int = Field(foreign_key="profile.id", index=True)
    item_key: str
    ts: datetime = Field(default_factory=_now)
