import pytest

from fjp0.manifest import ClipEntry, load_manifest, write_manifest


def _write_csv(path, rows, header="clip,kind,text,shown,label,note"):
    lines = [header] + rows
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def test_load_valid_manifest(tmp_path):
    csv = _write_csv(tmp_path / "m.csv", [
        "a.wav,vorlesen,im regal,,fluent,",
        "b.wav,fehlerjagd,tisch,tihsc,literal,negativ",
    ])
    entries = load_manifest(csv)
    assert len(entries) == 2
    assert entries[0].is_fluency
    assert entries[1].is_literal
    assert entries[1].shown == "tihsc"
    # Pfade werden absolut gemacht.
    assert entries[0].clip.endswith("a.wav")
    assert entries[0].clip.startswith("/")


def test_missing_columns(tmp_path):
    csv = _write_csv(tmp_path / "m.csv", ["a.wav,vorlesen"], header="clip,kind")
    with pytest.raises(ValueError, match="fehlende Spalten"):
        load_manifest(csv)


def test_bad_label_for_fluency(tmp_path):
    csv = _write_csv(tmp_path / "m.csv", ["a.wav,vorlesen,text,,literal,"])
    with pytest.raises(ValueError, match="vorlesen"):
        load_manifest(csv)


def test_literal_requires_shown(tmp_path):
    csv = _write_csv(tmp_path / "m.csv", ["a.wav,fehlerjagd,tisch,,literal,"])
    with pytest.raises(ValueError, match="shown"):
        load_manifest(csv)


def test_unknown_kind(tmp_path):
    csv = _write_csv(tmp_path / "m.csv", ["a.wav,quatsch,text,,fluent,"])
    with pytest.raises(ValueError, match="kind"):
        load_manifest(csv)


def test_blank_rows_skipped(tmp_path):
    csv = _write_csv(tmp_path / "m.csv", [
        "a.wav,vorlesen,text,,fluent,",
        ",,,,,",
    ])
    assert len(load_manifest(csv)) == 1


def test_comment_rows_skipped(tmp_path):
    csv = _write_csv(tmp_path / "m.csv", [
        "# das ist ein Kommentar",
        "a.wav,vorlesen,text,,fluent,",
    ])
    entries = load_manifest(csv)
    assert len(entries) == 1
    assert entries[0].clip.endswith("a.wav")


def test_example_manifest_parses(tmp_path):
    """Die committete Beispiel-Datei muss gültig sein (Kommentare inklusive)."""
    from pathlib import Path
    example = Path(__file__).resolve().parents[1] / "manifest.example.csv"
    entries = load_manifest(example)
    assert len(entries) == 8
    assert {e.kind for e in entries} == {"vorlesen", "fehlerjagd"}


def test_roundtrip(tmp_path):
    entries = [
        ClipEntry("a.wav", "vorlesen", "im regal", "", "fluent"),
        ClipEntry("b.wav", "fehlerjagd", "tisch", "tihsc", "autocorrected", "n"),
    ]
    path = tmp_path / "out.csv"
    write_manifest(path, entries)
    back = load_manifest(path)
    assert len(back) == 2
    assert back[1].shown == "tihsc"
    assert back[1].label == "autocorrected"
