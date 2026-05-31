"""End-to-End: synthetischer Datensatz → Pipeline → GO/NO-GO."""

from fjp0.manifest import load_manifest
from fjp0.report import GO, GO_LIMITED
from fjp0.selftest import generate_dataset, run_selftest


def test_generate_dataset_creates_wavs_and_manifest(tmp_path):
    manifest = generate_dataset(tmp_path)
    assert manifest.exists()
    entries = load_manifest(manifest)
    # 10 echte Clips + 1 stille Negativprobe.
    assert len(entries) == 11
    for e in entries:
        assert e.clip.endswith(".wav")
        from pathlib import Path
        assert Path(e.clip).exists()


def test_selftest_reaches_go(tmp_path):
    report = run_selftest(tmp_path)
    # Synthetische Verteilungen sind klar trennbar → Vollerfolg erwartet.
    assert report.verdict in (GO, GO_LIMITED)
    assert report.fluency_pass is True


def test_silent_clip_is_gated_out_of_calibration(tmp_path):
    """Die stille Negativprobe darf die Fehlerprüfung nicht verfälschen."""
    from fjp0.aligner import ScriptedAligner
    from fjp0.pipeline import run_pipeline

    manifest = generate_dataset(tmp_path)
    entries = load_manifest(manifest)
    aligner = ScriptedAligner({e.clip: e.label for e in entries})
    _, scored = run_pipeline(aligner, entries)

    silent = [s for s in scored if s.entry.note == "negativprobe-gate-still"]
    assert len(silent) == 1
    assert silent[0].voiced is False
