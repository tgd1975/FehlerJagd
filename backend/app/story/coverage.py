"""Abdeckung der acht Merkblatt-Punkte über alle Fälle (Konzept Abschnitt 2).

Wertet aus, welche der Regeln 1–8 in den Fälscher-Notizen wie oft vorkommen und
in welchen Fällen – die in ``docs/Faelle.md`` erwähnte „Abdeckungstabelle".
Phänomene außerhalb der acht Punkte (hoerbar, dehnungs-h, doppelvokal) werden
separat gezählt.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .graph import Case
from .regeln import KLASSE_ZU_REGEL, KLASSEN_OHNE_REGEL

# Regel-Nummer → kurzer Name (für die Tabelle).
REGEL_NAME = {
    1: "Groß/klein",
    2: "Beistrich",
    3: "Auslaut (Ende-Check)",
    4: "v/f",
    5: "i/ie",
    6: "das/dass",
    7: "ver-/vor-",
    8: "Vokallänge",
}


@dataclass
class Coverage:
    # Regel-Nummer → Liste der Fälle, die sie üben (mit Mehrfachzählung als len).
    by_regel: dict[int, list[str]] = field(default_factory=dict)
    # Klasse außerhalb der 8 → Liste der Fälle.
    outside: dict[str, list[str]] = field(default_factory=dict)

    def missing_regeln(self) -> list[int]:
        return [r for r in REGEL_NAME if not self.by_regel.get(r)]


def compute_coverage(cases: dict[str, Case]) -> Coverage:
    cov = Coverage(by_regel={r: [] for r in REGEL_NAME}, outside={})
    for case in cases.values():
        for scene in case.nodes.values():
            for err in scene.proofread_errors:
                regel = KLASSE_ZU_REGEL.get(err.klasse)
                if regel is not None:
                    cov.by_regel[regel].append(case.case_id)
                elif err.klasse in KLASSEN_OHNE_REGEL:
                    cov.outside.setdefault(err.klasse, []).append(case.case_id)
    return cov


def coverage_table(cov: Coverage) -> str:
    """Markdown-Tabelle der Abdeckung."""
    lines = [
        "| Regel | Punkt | Vorkommen | Fälle |",
        "|---|---|---|---|",
    ]
    for r, name in REGEL_NAME.items():
        cases = cov.by_regel.get(r, [])
        uniq = sorted(set(cases))
        lines.append(f"| {r} | {name} | {len(cases)} | {', '.join(uniq) or '—'} |")
    lines.append("")
    lines.append("**Außerhalb der 8 Punkte:**")
    lines.append("")
    lines.append("| Klasse | Vorkommen | Fälle |")
    lines.append("|---|---|---|")
    for klasse, cases in sorted(cov.outside.items()):
        uniq = sorted(set(cases))
        lines.append(f"| {klasse} | {len(cases)} | {', '.join(uniq)} |")
    return "\n".join(lines)
