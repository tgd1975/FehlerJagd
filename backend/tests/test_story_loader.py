from pathlib import Path

import pytest

from app.config import REPO_ROOT
from app.story.graph import MODE_FEHLERJAGD, MODE_VORLESEN
from app.story.loader import StoryValidationError, discover_cases, load_case

STORIES = REPO_ROOT / "stories"


def test_real_cases_load_and_validate():
    """Alle echten Fälle im Repo müssen gültig sein."""
    cases = discover_cases(STORIES)
    assert "fall-01" in cases
    assert "fall-02" in cases
    fall01 = cases["fall-01"]
    assert fall01.titel.startswith("Das Geheimnis")
    assert fall01.start == "szene-01"
    # Fehlerjagd-Szene hat klassifizierte Fehler.
    s05 = fall01.scene("szene-05")
    assert s05.mode == MODE_FEHLERJAGD
    assert len(s05.proofread_errors) == 4
    assert any(e.klasse == "vokallaenge" for e in s05.proofread_errors)


def test_tutorial_case_id_from_dir():
    """fall-00 hat keine case_id im YAML → aus Verzeichnis abgeleitet."""
    case = load_case(STORIES / "fall-00-tutorial" / "graph.yaml")
    assert case.case_id == "fall-00-tutorial"
    assert any(s.mode == "kalibrierung" for s in case.nodes.values())


def test_proofread_only_on_fehlerjagd(tmp_path):
    case_dir = tmp_path / "fall-x"
    case_dir.mkdir()
    (case_dir / "s1.md").write_text("Text", encoding="utf-8")
    (case_dir / "graph.yaml").write_text(
        "case_id: fall-x\nstart: s1\nnodes:\n"
        "  s1:\n    text: s1.md\n    mode: vorlesen\n"
        "    proofread_errors:\n"
        "      - { shown: x, correct: X, klasse: grossschreibung, regel: 1, tipp: t, method: markieren }\n",
        encoding="utf-8",
    )
    with pytest.raises(StoryValidationError, match="proofread_errors nur auf"):
        load_case(case_dir / "graph.yaml")


def test_missing_goto_target(tmp_path):
    case_dir = tmp_path / "fall-y"
    case_dir.mkdir()
    (case_dir / "s1.md").write_text("Text", encoding="utf-8")
    (case_dir / "graph.yaml").write_text(
        "case_id: fall-y\nstart: s1\nnodes:\n"
        "  s1: { text: s1.md, mode: vorlesen, goto: nirgendwo }\n",
        encoding="utf-8",
    )
    with pytest.raises(StoryValidationError, match="existiert nicht"):
        load_case(case_dir / "graph.yaml")


def test_bad_regel_caught(tmp_path):
    case_dir = tmp_path / "fall-z"
    case_dir.mkdir()
    (case_dir / "s1.md").write_text("vile", encoding="utf-8")
    (case_dir / "graph.yaml").write_text(
        "case_id: fall-z\nstart: s1\nnodes:\n"
        "  s1:\n    text: s1.md\n    mode: fehlerjagd\n"
        "    proofread_errors:\n"
        "      - { shown: vile, correct: viele, klasse: ie, regel: 9, tipp: t, method: markieren }\n",
        encoding="utf-8",
    )
    with pytest.raises(StoryValidationError, match="verlangt regel 5"):
        load_case(case_dir / "graph.yaml")
