from fjp0.calibrate import Calibration, calibrate
from fjp0.report import (
    GO,
    GO_LIMITED,
    NO_GO,
    evaluate,
    to_markdown,
    write_reports,
)


def _good() -> Calibration:
    return calibrate(high=[0.85, 0.9, 0.88], low=[0.3, 0.35, 0.4])


def _bad() -> Calibration:
    # Stark überlappend → schlechte Trennung.
    return calibrate(high=[0.55, 0.5, 0.6], low=[0.52, 0.58, 0.5])


def test_both_good_is_go():
    rep = evaluate(_good(), _good())
    assert rep.verdict == GO
    assert rep.fluency_pass and rep.literal_pass


def test_literal_bad_is_go_limited():
    rep = evaluate(_good(), _bad())
    assert rep.verdict == GO_LIMITED
    assert rep.fluency_pass and not rep.literal_pass


def test_literal_missing_is_go_limited():
    rep = evaluate(_good(), None)
    assert rep.verdict == GO_LIMITED


def test_fluency_bad_is_no_go():
    rep = evaluate(_bad(), _good())
    assert rep.verdict == NO_GO
    assert not rep.fluency_pass


def test_fluency_missing_is_no_go():
    rep = evaluate(None, _good())
    assert rep.verdict == NO_GO


def test_markdown_and_files(tmp_path):
    rep = evaluate(_good(), _good())
    md = to_markdown(rep)
    assert "GO" in md and "Verdikt" in md
    json_p, md_p = write_reports(rep, tmp_path)
    assert json_p.exists() and md_p.exists()
    assert "verdict" in json_p.read_text(encoding="utf-8")
