"""Kommandozeile für das Phase-0-Harness.

Unterbefehle
------------
``selftest``  Synthetischen Datensatz erzeugen und die volle Pipeline mit dem
              deterministischen Aligner fahren (ohne torch, ohne echte Stimme).
              Beweist die Harness-Logik. Exit 0 bei GO/GO-MIT-EINSCHRÄNKUNG.
``run``       Echte Auswertung über ein CSV-Manifest mit Aufnahmen.
              ``--backend torch`` (default) nutzt torchaudio; ``scripted`` testet
              die Pipeline trocken.
``score``     Schnellcheck eines einzelnen Clips (wie das alte Skript):
              Wort-für-Wort-Flüssigkeit + optionale lautgetreue Prüfung.
``smoke``     Mechanischer Smoke-Test des echten torchaudio-Alignments.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _print_report(report) -> None:
    from .report import to_markdown
    print(to_markdown(report))


def _exit_code(verdict: str) -> int:
    from .report import NO_GO
    return 1 if verdict == NO_GO else 0


# --------------------------------------------------------------------------- #
# selftest
# --------------------------------------------------------------------------- #
def cmd_selftest(args: argparse.Namespace) -> int:
    from .report import write_reports
    from .selftest import run_selftest

    out_dir = Path(args.out)
    report = run_selftest(out_dir)
    _print_report(report)
    json_p, md_p = write_reports(report, out_dir)
    print(f"\nReports: {json_p}  |  {md_p}")
    return _exit_code(report.verdict)


# --------------------------------------------------------------------------- #
# run (echtes Manifest)
# --------------------------------------------------------------------------- #
def _build_aligner(backend: str, entries):
    if backend == "scripted":
        from .aligner import ScriptedAligner
        return ScriptedAligner({e.clip: e.label for e in entries})
    if backend == "torch":
        from .aligner import TorchAudioAligner
        return TorchAudioAligner()
    raise ValueError(f"unbekanntes backend '{backend}'")


def cmd_run(args: argparse.Namespace) -> int:
    from .manifest import load_manifest
    from .pipeline import run_pipeline
    from .report import write_reports

    entries = load_manifest(args.manifest)
    if not entries:
        print("Manifest enthält keine Clips.", file=sys.stderr)
        return 2
    aligner = _build_aligner(args.backend, entries)
    report, scored = run_pipeline(aligner, entries)

    # Vom Gate verworfene Fehlerjagd-Clips sichtbar machen.
    gated = [s for s in scored if s.entry.is_literal and not s.voiced]
    if gated:
        print("Vom Energie-Gate verworfen (nicht gewertet):")
        for s in gated:
            print(f"  - {s.entry.clip}: {s.gate_reason}")
        print()

    _print_report(report)
    out_dir = Path(args.out)
    json_p, md_p = write_reports(report, out_dir)
    print(f"\nReports: {json_p}  |  {md_p}")
    return _exit_code(report.verdict)


# --------------------------------------------------------------------------- #
# score (Einzelclip, echtes torchaudio)
# --------------------------------------------------------------------------- #
def cmd_score(args: argparse.Namespace) -> int:
    from .aligner import TorchAudioAligner
    from .audio import read_wav
    from .gating import gate
    from .literal import classify, AUDIBLE
    from .normalize import normalize, word
    from .scoring import Thresholds, color

    aligner = TorchAudioAligner()
    t = Thresholds()

    print(f"\n=== Flüssigkeit: '{args.text}' ===")
    ws = aligner.word_scores(args.audio, normalize(args.text))
    for w in ws:
        print(f"  {color(w.score, t):4}  {w.score:5.2f}  {w.word}")

    if args.shown and args.correct:
        g = gate(read_wav(args.audio))
        ws2 = aligner.word_scores(args.audio, [word(args.correct)])
        res = classify(args.shown, args.correct, ws2[0].score, voiced=g.voiced)
        print(f"\n=== Fehlerprüfung (Klasse '{AUDIBLE}'): "
              f"gezeigt '{args.shown}' / richtig '{args.correct}' ===")
        print(f"  Score gegen '{args.correct}': {res.score:.2f}  →  {res.verdict}")
        if res.gated_out:
            print(f"  (Gate: {g.reason})")
    return 0


# --------------------------------------------------------------------------- #
# smoke (mechanischer torch-Test)
# --------------------------------------------------------------------------- #
def cmd_smoke(args: argparse.Namespace) -> int:
    import tempfile
    from .aligner import TorchAudioAligner
    from .audio import tone, write_wav

    aligner = TorchAudioAligner()
    with tempfile.TemporaryDirectory() as td:
        wav = Path(td) / "smoke.wav"
        # Kein echtes Sprachsignal – wir prüfen nur, dass die Forced-Alignment-
        # API mechanisch durchläuft und die richtige Anzahl Scores liefert.
        write_wav(wav, tone(220, 1.0, amplitude=0.3, sample_rate=aligner.sample_rate))
        words = ["tisch", "buch"]
        ws = aligner.word_scores(str(wav), words)
    ok = len(ws) == len(words) and all(0.0 <= w.score <= 1.0 for w in ws)
    print("torchaudio MMS_FA Smoke-Test:")
    for w in ws:
        print(f"  {w.word}: {w.score:.3f}")
    print("OK" if ok else "FEHLGESCHLAGEN")
    return 0 if ok else 1


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="fjp0",
        description="FehlerJagd – Phase-0-Validierung (Flüssigkeit + lautgetreue Prüfung).",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("selftest", help="synthetischer End-to-End-Beweis (ohne torch)")
    s.add_argument("--out", default="phase0/data/selftest", help="Ausgabeverzeichnis")
    s.set_defaults(func=cmd_selftest)

    r = sub.add_parser("run", help="echtes Manifest auswerten")
    r.add_argument("--manifest", required=True, help="CSV-Manifest")
    r.add_argument("--out", default="phase0/data/report", help="Ausgabeverzeichnis")
    r.add_argument("--backend", default="torch", choices=["torch", "scripted"])
    r.set_defaults(func=cmd_run)

    c = sub.add_parser("score", help="Einzelclip schnell prüfen (torchaudio)")
    c.add_argument("--audio", required=True, help="WAV-Datei")
    c.add_argument("--text", required=True, help="erwarteter Vorlese-Text")
    c.add_argument("--shown", help="gezeigte Falschschreibung (hörbarer Fehler)")
    c.add_argument("--correct", help="richtiges Wort")
    c.set_defaults(func=cmd_score)

    k = sub.add_parser("smoke", help="mechanischer torchaudio-Smoke-Test")
    k.set_defaults(func=cmd_smoke)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
