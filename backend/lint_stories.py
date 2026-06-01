#!/usr/bin/env python3
"""Story-Linter: validiert alle Fälle und zeigt die Merkblatt-Abdeckung.

Eigenständiges Werkzeug (für CI / pre-commit). Nutzt dieselbe strenge
Validierung wie der Backend-Loader, sodass Inhaltsfehler früh auffallen.

    python lint_stories.py [--stories ../stories] [--coverage]

Exit-Code 0 = alle Fälle gültig, 1 = mindestens ein Fall ungültig.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Paket importierbar machen, egal von wo gestartet.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.config import REPO_ROOT  # noqa: E402
from app.story.coverage import compute_coverage, coverage_table  # noqa: E402
from app.story.loader import StoryValidationError, load_case  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="FehlerJagd Story-Linter")
    p.add_argument("--stories", default=str(REPO_ROOT / "stories"),
                   help="Verzeichnis mit den Fällen")
    p.add_argument("--coverage", action="store_true",
                   help="Abdeckungstabelle der 8 Merkblatt-Punkte ausgeben")
    args = p.parse_args(argv)

    stories = Path(args.stories)
    graphs = sorted(stories.glob("*/graph.yaml"))
    if not graphs:
        print(f"Keine Fälle unter {stories} gefunden.", file=sys.stderr)
        return 1

    valid: dict = {}
    errors = 0
    for graph in graphs:
        try:
            case = load_case(graph)
            valid[case.case_id] = case
            n_scenes = len(case.nodes)
            n_errs = sum(len(s.proofread_errors) for s in case.nodes.values())
            print(f"✓ {case.case_id:20} {n_scenes:2} Szenen, {n_errs:2} Fehler  — {case.titel}")
        except StoryValidationError as exc:
            errors += 1
            print(f"✗ {graph.parent.name}", file=sys.stderr)
            for e in exc.errors:
                print(f"    - {e}", file=sys.stderr)

    print(f"\n{len(valid)} gültig, {errors} ungültig.")

    if args.coverage and valid:
        cov = compute_coverage(valid)
        print("\n" + coverage_table(cov))
        missing = cov.missing_regeln()
        if missing:
            print(f"\n⚠ Nicht abgedeckte Regeln: {missing}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
