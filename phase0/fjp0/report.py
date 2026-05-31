"""GO/NO-GO-Auswertung – das eigentliche Ergebnis von Phase 0.

Bindet die beiden Kalibrierungen zu einem Verdikt zusammen. Wichtig ist die
**asymmetrische** Logik, die direkt aus dem Konzept folgt:

* **Flüssigkeit (Mechanik A) ist die harte Bedingung.** Trennt sie nicht, fehlt
  das Kern-Signal der App → Gesamt-Verdikt **NO-GO**.
* **Lautgetreue Prüfung (Mechanik B) ist optional/degradierbar.** Das Markieren
  ist der deterministische Rückhalt für *alle* Fehlerklassen (Konzept, Risiko 3).
  Trennt die akustische Distanz nicht sauber, ist das kein Projekt-Stopp – dann
  laufen *hörbare* Fehler eben **nur über Markieren**. Verdikt: **GO mit
  Einschränkung**.

Schwellen für "trennt sauber" sind konservativ (für Kinder mild kalibriert,
aber die Trennschärfe selbst muss klar sein).
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .calibrate import Calibration

# Mindest-Trennschärfe, damit eine Mechanik als "validiert" gilt.
MIN_BALANCED_ACCURACY = 0.80
MIN_MARGIN = 0.10

GO = "GO"
GO_LIMITED = "GO-MIT-EINSCHRÄNKUNG"
NO_GO = "NO-GO"


def _passes(cal: Calibration) -> bool:
    return cal.balanced_accuracy >= MIN_BALANCED_ACCURACY and cal.margin >= MIN_MARGIN


@dataclass(frozen=True)
class Phase0Report:
    fluency: Calibration | None
    literal: Calibration | None
    fluency_pass: bool
    literal_pass: bool
    verdict: str
    rationale: list[str]

    def to_dict(self) -> dict:
        return {
            "verdict": self.verdict,
            "fluency_pass": self.fluency_pass,
            "literal_pass": self.literal_pass,
            "rationale": self.rationale,
            "fluency": asdict(self.fluency) if self.fluency else None,
            "literal": asdict(self.literal) if self.literal else None,
        }


def evaluate(
    fluency: Calibration | None,
    literal: Calibration | None,
) -> Phase0Report:
    """Leitet aus den Kalibrierungen das GO/NO-GO ab."""
    rationale: list[str] = []

    fluency_pass = bool(fluency and _passes(fluency))
    literal_pass = bool(literal and _passes(literal))

    if fluency is None:
        rationale.append(
            "Keine Flüssigkeits-Clips (kind=vorlesen) im Manifest – Mechanik A "
            "ungeprüft. Das ist die harte Bedingung."
        )
    elif fluency_pass:
        rationale.append(
            f"Flüssigkeit trennt sauber: balancierte Genauigkeit "
            f"{fluency.balanced_accuracy:.2f}, Margin {fluency.margin:+.2f} bei "
            f"Schwelle {fluency.threshold:.2f}."
        )
    else:
        rationale.append(
            f"Flüssigkeit trennt NICHT ausreichend: Genauigkeit "
            f"{fluency.balanced_accuracy:.2f} (Ziel ≥ {MIN_BALANCED_ACCURACY}), "
            f"Margin {fluency.margin:+.2f} (Ziel ≥ {MIN_MARGIN}). Modellwahl/"
            f"Schwellen/Headset überprüfen, mehr Clips aufnehmen."
        )

    if literal is None:
        rationale.append(
            "Keine Fehlerprüfungs-Clips (kind=fehlerjagd) – lautgetreue Prüfung "
            "ungeprüft. Hörbare Fehler laufen vorerst nur über Markieren."
        )
    elif literal_pass:
        rationale.append(
            f"Lautgetreue Prüfung trennt sauber: Genauigkeit "
            f"{literal.balanced_accuracy:.2f}, Margin {literal.margin:+.2f} bei "
            f"Schwelle {literal.threshold:.2f}. Hörbare Fehler dürfen *vorlesend* "
            f"gejagt werden."
        )
    else:
        rationale.append(
            f"Lautgetreue Prüfung trennt NICHT ausreichend: Genauigkeit "
            f"{literal.balanced_accuracy:.2f}, Margin {literal.margin:+.2f}. "
            f"Kein Stopp – hörbare Fehler laufen dann NUR über Markieren "
            f"(deterministischer Rückhalt)."
        )

    if not fluency_pass:
        verdict = NO_GO
        rationale.append(
            "→ NO-GO: Ohne tragfähige Flüssigkeits-Bewertung fehlt das Kern-Signal."
        )
    elif literal_pass:
        verdict = GO
        rationale.append("→ GO: Beide Mechaniken validiert.")
    else:
        verdict = GO_LIMITED
        rationale.append(
            "→ GO mit Einschränkung: App bauen, aber hörbare Fehler nur per "
            "Markieren prüfen, bis die akustische Distanz nachkalibriert ist."
        )

    return Phase0Report(
        fluency=fluency,
        literal=literal,
        fluency_pass=fluency_pass,
        literal_pass=literal_pass,
        verdict=verdict,
        rationale=rationale,
    )


def _fmt_cal(name: str, cal: Calibration | None) -> list[str]:
    if cal is None:
        return [f"### {name}", "_keine Clips_", ""]
    return [
        f"### {name}",
        "",
        f"| Kennzahl | Wert |",
        f"|---|---|",
        f"| Schwelle | {cal.threshold:.3f} |",
        f"| balancierte Genauigkeit | {cal.balanced_accuracy:.2f} |",
        f"| Margin (Median-Abstand) | {cal.margin:+.3f} |",
        f"| Median hoch / niedrig | {cal.high_median:.3f} / {cal.low_median:.3f} |",
        f"| Clips hoch / niedrig | {cal.n_high} / {cal.n_low} |",
        f"| Fehlklassifiziert (Overlap) | {cal.overlap} |",
        "",
    ]


def to_markdown(report: Phase0Report) -> str:
    """Erzeugt den menschenlesbaren GO/NO-GO-Report (Markdown)."""
    lines = [
        "# FehlerJagd – Phase 0 GO/NO-GO-Report",
        "",
        f"## Verdikt: **{report.verdict}**",
        "",
        "### Begründung",
        "",
    ]
    lines += [f"- {r}" for r in report.rationale]
    lines += ["", "## Kennzahlen", ""]
    lines += _fmt_cal("Flüssigkeit (Mechanik A)", report.fluency)
    lines += _fmt_cal("Lautgetreue Fehlerprüfung (Mechanik B)", report.literal)
    lines += [
        "## Lesehilfe",
        "",
        f"- **balancierte Genauigkeit** ≥ {MIN_BALANCED_ACCURACY:.2f} und "
        f"**Margin** ≥ {MIN_MARGIN:.2f} ⇒ Mechanik gilt als validiert.",
        "- **Margin** = Abstand der Klassen-Mediane; >0 heißt korrekt geordnet.",
        "- **Flüssigkeit** ist die harte Bedingung; **lautgetreue Prüfung** ist "
        "degradierbar (Fallback: Markieren).",
        "",
    ]
    return "\n".join(lines)


def write_reports(report: Phase0Report, out_dir: str | Path) -> tuple[Path, Path]:
    """Schreibt JSON + Markdown und gibt beide Pfade zurück."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "report.json"
    md_path = out_dir / "report.md"
    json_path.write_text(
        json.dumps(report.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    md_path.write_text(to_markdown(report), encoding="utf-8")
    return json_path, md_path
