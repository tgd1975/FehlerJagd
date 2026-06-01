from dataclasses import dataclass

from app.dashboard import aggregate_fluency, aggregate_proofread


@dataclass
class PR:
    klasse: str
    regel: str
    gefunden: bool


@dataclass
class SC:
    case_id: str
    scene_id: str
    color: str
    score: float | None


def test_proofread_aggregation_sorted_by_miss():
    rows = [
        PR("vokallaenge", "8", True),
        PR("vokallaenge", "8", False),
        PR("ie", "5", False),
        PR("ie", "5", False),
        PR("hoerbar", "–", True),
    ]
    stats = aggregate_proofread(rows)
    # 'ie' (0% gefunden) muss vor 'vokallaenge' (50%) und 'hoerbar' (100%) stehen.
    assert stats[0].klasse == "ie"
    assert stats[0].found_ratio == 0.0
    assert stats[0].missed == 2
    vl = next(s for s in stats if s.klasse == "vokallaenge")
    assert vl.found == 1 and vl.total == 2


def test_fluency_aggregation_counts_colors():
    rows = [
        SC("fall-01", "s1", "grün", 0.9),
        SC("fall-01", "s1", "rot", 0.3),
        SC("fall-01", "s1", "ungeprüft", None),
    ]
    stats = aggregate_fluency(rows)
    assert len(stats) == 1
    s = stats[0]
    assert s.words == 3 and s.green == 1 and s.red == 1
    assert s.avg_score == 0.6   # nur bewertete fließen in den Schnitt
