"""Pydantic-Schemas für die API (Requests/Responses)."""

from __future__ import annotations

from pydantic import BaseModel


# --- Fälle / Szenen ---------------------------------------------------------
class CaseSummary(BaseModel):
    case_id: str
    titel: str
    schauplatz: str
    ziel_muster: list[str]
    start: str
    title_image: str | None = None


class ChoiceOut(BaseModel):
    index: int
    label: str
    goto: str


class ProofreadErrorPublic(BaseModel):
    """Öffentlich sichtbarer Teil eines Fehlers (OHNE Lösung!).

    correct/regel/tipp werden bewusst NICHT vor dem Abschicken ausgeliefert,
    damit die Auflösung nicht vorab sichtbar ist.
    """

    shown: str
    method: str


class TokenOut(BaseModel):
    index: int
    text: str
    start: int
    end: int


class SceneOut(BaseModel):
    case_id: str
    scene_id: str
    mode: str
    text: str
    target_patterns: list[str] = []
    choices: list[ChoiceOut] = []
    # Nur bei mode=fehlerjagd befüllt: Wort-Token (für die Markier-UI). Keine
    # Lösungen – nur die sichtbaren Wörter mit stabilen Indizes/Offsets.
    tokens: list[TokenOut] = []
    has_goto: bool = False
    is_terminal: bool = False
    is_bonus: bool = False
    hints: bool = False
    scoring: str | None = None
    eich_saetze: list[str] = []
    # Anzahl Fehler vorab (für die Fehlerjagd-UI), aber nicht die Lösungen.
    proofread_error_count: int = 0
    next_case: str | None = None


# --- Navigation -------------------------------------------------------------
class NextRequest(BaseModel):
    case_id: str
    scene_id: str
    choice_index: int | None = None
    all_green: bool = False


class NextResponse(BaseModel):
    ended: bool
    skipped_bonus: bool = False
    next_scene_id: str | None = None
    next_case_id: str | None = None
    scene: SceneOut | None = None


# --- Fehlerjagd -------------------------------------------------------------
class ProofreadCheckRequest(BaseModel):
    case_id: str
    scene_id: str
    marked_indices: list[int] = []          # angetippte Wörter
    marked_gap_indices: list[int] = []      # angetippte Lücken (Beistrich-Modus)
    profile_id: int | None = None           # optional: Verlauf speichern


class ErrorOutcomeOut(BaseModel):
    shown: str
    correct: str
    klasse: str
    regel: str
    tipp: str
    method: str
    token_index: int | None
    is_gap: bool
    found: bool


class ProofreadCheckResponse(BaseModel):
    total: int
    found_count: int
    false_positives: int
    all_found: bool
    score: float
    outcomes: list[ErrorOutcomeOut]
    false_positive_indices: list[int]
    false_positive_gap_indices: list[int]
    tokens: list[TokenOut]


# --- Scoring (Mechanik A/B) -------------------------------------------------
class WordFluencyOut(BaseModel):
    word: str
    score: float | None
    color: str


class FluencyResponse(BaseModel):
    provider: str
    calibrated: bool
    clip_score: float | None
    all_green: bool
    can_continue: bool
    earned_bonus: bool
    gate_message: str
    words: list[WordFluencyOut]


class LiteralResponse(BaseModel):
    shown: str
    correct: str
    score: float | None
    verdict: str
    provider: str
    calibrated: bool
