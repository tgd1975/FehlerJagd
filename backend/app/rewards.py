"""Belohnungs- und Gating-Logik (Konzept §3/§5) – reine Funktionen.

* **Punkte:** fürs Abschließen von Szenen und gefundene Fehler, Bonus für
  durchgehend grünes Lesen bzw. eine fehlerfreie Fehlerjagd.
* **Pinnwand:** je abgeschlossener Szene ein Panel (doppelt als Fortschritt).
* **Avatar:** Items mit Punkte-Kosten; freischalten = genug Punkte.
* **Sanftes Gating:** Mindestschwelle zum Weiterkommen, aber nie hart
  blockieren (für Kinder mild). Solange unkalibriert (Stub, vor Phase-0-GO),
  ist Weiterkommen immer erlaubt.
"""

from __future__ import annotations

from dataclasses import dataclass

# Punkte-Regeln (bewusst einfach, kindgerecht großzügig).
POINTS_SCENE = 10
POINTS_ALL_GREEN_BONUS = 5
POINTS_PER_FOUND = 5
POINTS_PERFECT_HUNT_BONUS = 10

# Avatar-Katalog: item_key → (Anzeigename, Punkte-Kosten).
AVATAR_CATALOG: dict[str, tuple[str, int]] = {
    "hut": ("Detektivhut", 30),
    "lupe": ("Lupe", 20),
    "mantel": ("Trenchcoat", 50),
    "notizbuch": ("Spürnasen-Logbuch", 40),
    "frieda-button": ("Frieda-Anstecker", 25),
}


@dataclass(frozen=True)
class SceneReward:
    points: int
    panel_key: str          # freigeschaltetes Pinnwand-Panel


def scene_reward(case_id: str, scene_id: str, all_green: bool) -> SceneReward:
    points = POINTS_SCENE + (POINTS_ALL_GREEN_BONUS if all_green else 0)
    return SceneReward(points=points, panel_key=f"panel:{case_id}:{scene_id}")


def proofread_points(found_count: int, total: int) -> int:
    pts = found_count * POINTS_PER_FOUND
    if total > 0 and found_count == total:
        pts += POINTS_PERFECT_HUNT_BONUS
    return pts


def affordable_items(points: int) -> list[str]:
    """Item-Keys, die mit dem aktuellen Punktestand freischaltbar sind."""
    return [k for k, (_, cost) in AVATAR_CATALOG.items() if points >= cost]


@dataclass(frozen=True)
class GateDecision:
    can_continue: bool
    earned_bonus: bool
    message: str


def evaluate_gate(
    clip_score: float | None,
    *,
    calibrated: bool,
    min_advance: float,
    green: float,
    all_green: bool,
) -> GateDecision:
    """Sanftes Gating nach dem Vorlesen.

    Unkalibriert (Stub) → immer weiter, freundlich. Kalibriert → Mindestschwelle
    fürs Weiterkommen, Bonus für sehr gutes Lesen; „zu niedrig" wird nie als
    hartes „Falsch" gerahmt.
    """
    if not calibrated or clip_score is None:
        return GateDecision(True, False, "Weiter geht's!")
    if clip_score >= green or all_green:
        return GateDecision(True, True, "Super gelesen — Bonus freigeschaltet!")
    if clip_score >= min_advance:
        return GateDecision(True, False, "Gut gelesen — weiter.")
    return GateDecision(
        False, False,
        "Der Hinweis ist noch etwas verschwommen — lies die markierten Stellen "
        "noch einmal.",
    )
