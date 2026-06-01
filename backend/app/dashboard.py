"""Aggregation fürs Eltern-Dashboard (Konzept §3).

Reine Funktionen über einfache Zeilen-Objekte (entkoppelt von der DB, testbar).
Beantwortet vor allem: *Welche Regel-Kategorien werden noch oft übersehen?*
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass


@dataclass(frozen=True)
class KlasseStat:
    klasse: str
    regel: str
    total: int
    found: int

    @property
    def missed(self) -> int:
        return self.total - self.found

    @property
    def found_ratio(self) -> float:
        return self.found / self.total if self.total else 0.0


def aggregate_proofread(rows) -> list[KlasseStat]:
    """Gruppiert Fehlerjagd-Verlauf nach Fehlerklasse.

    ``rows`` müssen Felder ``klasse``, ``regel`` (str), ``gefunden`` (bool) haben.
    Nach Trefferquote aufsteigend sortiert (am häufigsten übersehen zuerst).
    """
    total: dict[str, int] = defaultdict(int)
    found: dict[str, int] = defaultdict(int)
    regel: dict[str, str] = {}
    for r in rows:
        total[r.klasse] += 1
        found[r.klasse] += 1 if r.gefunden else 0
        regel.setdefault(r.klasse, str(r.regel))
    stats = [
        KlasseStat(klasse=k, regel=regel.get(k, "–"), total=total[k], found=found[k])
        for k in total
    ]
    return sorted(stats, key=lambda s: (s.found_ratio, s.klasse))


@dataclass(frozen=True)
class SceneFluency:
    case_id: str
    scene_id: str
    words: int
    green: int
    yellow: int
    red: int
    avg_score: float | None


def aggregate_fluency(rows) -> list[SceneFluency]:
    """Gruppiert Flüssigkeits-Verlauf je (Fall, Szene).

    ``rows``: Felder ``case_id``, ``scene_id``, ``color``, ``score`` (float|None).
    """
    buckets: dict[tuple[str, str], list] = defaultdict(list)
    for r in rows:
        buckets[(r.case_id, r.scene_id)].append(r)
    out = []
    for (case_id, scene_id), items in buckets.items():
        scores = [i.score for i in items if i.score is not None]
        out.append(SceneFluency(
            case_id=case_id, scene_id=scene_id, words=len(items),
            green=sum(1 for i in items if i.color == "grün"),
            yellow=sum(1 for i in items if i.color == "gelb"),
            red=sum(1 for i in items if i.color == "rot"),
            avg_score=(sum(scores) / len(scores) if scores else None),
        ))
    return sorted(out, key=lambda s: (s.case_id, s.scene_id))
