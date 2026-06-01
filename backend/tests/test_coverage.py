from app.config import REPO_ROOT
from app.story.coverage import compute_coverage, coverage_table
from app.story.loader import discover_cases

CASES = discover_cases(REPO_ROOT / "stories")


def test_all_eight_regeln_covered():
    cov = compute_coverage(CASES)
    assert cov.missing_regeln() == []          # alle 8 Punkte kommen vor
    assert len(cov.by_regel[8]) >= 1           # Vokallänge (Phonetik-Fokus)


def test_outside_classes_tracked():
    cov = compute_coverage(CASES)
    assert "hoerbar" in cov.outside
    assert "dehnungs-h" in cov.outside


def test_table_renders():
    table = coverage_table(compute_coverage(CASES))
    assert "Beistrich" in table and "Vokallänge" in table


def test_lint_cli_exit_zero():
    import lint_stories
    assert lint_stories.main(["--stories", str(REPO_ROOT / "stories"), "--coverage"]) == 0
