"""Selbsttest: beweist die Harness-Pipeline ohne echte Aufnahme und ohne torch.

ABWEICHUNG vom Konzept (DECISIONS.md): Phase 0 verlangt 5–10 echte Vorlese-Clips
des Kindes. Die kann diese Umgebung nicht erzeugen. Der Selbsttest erstellt
stattdessen **gelabelte synthetische WAVs** und schickt sie über den
deterministischen :class:`ScriptedAligner` durch *exakt dieselbe* Pipeline wie
echte Daten. Damit ist nachgewiesen, dass

  Manifest → Scoring → Gating → Kalibrierung → GO/NO-GO

end-to-end korrekt arbeitet und ein erwartbares Verdikt liefert.

WAS DER SELBSTTEST **NICHT** LEISTET: Er validiert nicht die akustische Modellgüte
an echter Kinderstimme – das bleibt dem Lauf mit echten Aufnahmen (bzw. dem
torch-Smoke-Test) vorbehalten. Die synthetischen Töne sind keine Sprache; ihr
Zweck ist, das Energie-Gate und die Datei-/Manifest-Pfade real zu durchlaufen.
"""

from __future__ import annotations

from pathlib import Path

from .aligner import ScriptedAligner
from .audio import silence, tone, write_wav
from .manifest import ClipEntry, write_manifest
from .pipeline import run_pipeline
from .report import Phase0Report

# Synthetischer Datensatz: (id, kind, text, shown, label, ton-freq, laut?)
# Frequenz/Lautstärke nur zur Belegung des Gates – die Scores kommen aus dem
# ScriptedAligner anhand des Labels.
_SPEC = [
    ("flu-01", "vorlesen", "im regal stehen viele buecher", "", "fluent", 220, True),
    ("flu-02", "vorlesen", "die alte bibliothek war still", "", "fluent", 247, True),
    ("flu-03", "vorlesen", "mia oeffnete das blaue buch", "", "fluent", 262, True),
    ("sto-01", "vorlesen", "im regal stehen viele buecher", "", "stocked", 294, True),
    ("sto-02", "vorlesen", "die alte bibliothek war still", "", "stocked", 330, True),
    ("sto-03", "vorlesen", "mia oeffnete das blaue buch", "", "stocked", 349, True),
    ("lit-01", "fehlerjagd", "tisch", "tihsc", "literal", 392, True),
    ("lit-02", "fehlerjagd", "buch", "buhc", "literal", 440, True),
    ("auto-01", "fehlerjagd", "tisch", "tihsc", "autocorrected", 494, True),
    ("auto-02", "fehlerjagd", "buch", "buhc", "autocorrected", 523, True),
]


def generate_dataset(out_dir: str | Path) -> Path:
    """Schreibt synthetische WAVs + ein CSV-Manifest; gibt den Manifest-Pfad zurück.

    Zusätzlich wird ein **stiller** fehlerjagd-Clip erzeugt, der vom Energie-Gate
    verworfen werden muss (Negativ-Probe gegen "Stille = literal gelesen").
    """
    out_dir = Path(out_dir)
    audio_dir = out_dir / "audio"
    entries: list[ClipEntry] = []

    for cid, kind, text, shown, label, freq, _loud in _SPEC:
        wav = audio_dir / f"{cid}.wav"
        write_wav(wav, tone(freq, 0.6, amplitude=0.3, noise=0.01, seed=hash(cid) % 1000))
        entries.append(ClipEntry(str(wav), kind, text, shown, label))

    # Negativ-Probe fürs Gate: stiller Clip, als "literal" gelabelt – darf NICHT
    # in die Kalibrierung einfließen (Gate verwirft ihn).
    sil = audio_dir / "silent.wav"
    write_wav(sil, silence(0.6, noise=0.0005))
    entries.append(ClipEntry(str(sil), "fehlerjagd", "tisch", "tihsc", "literal",
                             note="negativprobe-gate-still"))

    manifest_path = out_dir / "manifest.csv"
    write_manifest(manifest_path, entries)
    return manifest_path


def run_selftest(out_dir: str | Path) -> Phase0Report:
    """Erzeugt den Datensatz und fährt die volle Pipeline mit ScriptedAligner."""
    from .manifest import load_manifest

    manifest_path = generate_dataset(out_dir)
    entries = load_manifest(manifest_path)
    labels = {e.clip: e.label for e in entries}
    aligner = ScriptedAligner(labels)
    report, _ = run_pipeline(aligner, entries)
    return report
