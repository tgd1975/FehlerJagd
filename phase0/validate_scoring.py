"""
Phase-0-Starter: phonetische Vorlese-Bewertung mit torchaudio Forced Alignment.

ZWECK
  (1) Flüssigkeit: pro Wort einen Score (0..1) gegen den ERWARTETEN Text ->
      grün/gelb/rot. Hohe Übereinstimmung = gut.
  (2) Lautgetreue Fehlerprüfung (Skizze): Distanz zum RICHTIGEN Wort.
      Klingt die Aufnahme wie das richtige Wort -> sie hat auto-korrigiert.
      Klingt sie NICHT danach -> sie hat literal dekodiert (gut).

WICHTIG
  Diese Prüfung läuft über akustisches Forced-Alignment, NICHT über
  ASR-Transkription (die würde "Tihsc" automatisch zu "Tisch" reparieren).

STATUS
  Ausgangspunkt, bewusst noch nicht getestet. Modellwahl (deutsches bzw.
  mehrsprachiges Modell), Textnormalisierung (Umlaute/ß) und Schwellen sind
  zu kalibrieren. MMS_FA erwartet i. d. R. romanisierten/normalisierten Text.

SETUP
  pip install torch torchaudio soundfile numpy --index-url https://download.pytorch.org/whl/cpu
  python validate_scoring.py --audio aufnahme.wav --text "der erwartete satz"
"""

from __future__ import annotations
import argparse
import re

import torch
import torchaudio

# Mehrsprachiger Forced-Aligner (CPU-tauglich). Für Deutsch ggf. Text
# normalisieren/romanisieren; alternativ ein deutsches wav2vec2-Modell prüfen.
from torchaudio.pipelines import MMS_FA as BUNDLE

# Schwellen — in Phase 0 empirisch einstellen (für Kinder eher mild).
GREEN = 0.80
YELLOW = 0.55
# Negative-Check: liegt der Score gegen das RICHTIGE Wort UNTER diesem Wert,
# gilt das Wort als "literal gelesen" (nicht auto-korrigiert).
LITERAL_MAX = 0.55
# Mindest-Energie, damit reines Murmeln/Stille nicht als "nicht-Tisch" durchrutscht.
# (TODO: in Phase 0 über RMS/VAD ergänzen.)


def normalize(text: str) -> list[str]:
    """Sehr einfache Normalisierung in Wörter. TODO: Umlaute/ß behandeln."""
    text = text.lower()
    text = re.sub(r"[^a-zäöüß\s]", " ", text)
    return [w for w in text.split() if w]


def load_audio(path: str, target_sr: int) -> torch.Tensor:
    waveform, sr = torchaudio.load(path)
    if waveform.size(0) > 1:                      # auf Mono mischen
        waveform = waveform.mean(dim=0, keepdim=True)
    if sr != target_sr:
        waveform = torchaudio.functional.resample(waveform, sr, target_sr)
    return waveform


def _word_score(spans) -> float:
    """Längen-gewichteter Mittelwert der Token-Scores eines Wortes."""
    total = sum(len(s) for s in spans)
    if total == 0:
        return 0.0
    return sum(s.score * len(s) for s in spans) / total


def align_word_scores(waveform: torch.Tensor, words: list[str]):
    """Liefert (wort, score) gegen den gegebenen Referenztext."""
    model = BUNDLE.get_model()
    tokenizer = BUNDLE.get_tokenizer()
    aligner = BUNDLE.get_aligner()
    with torch.inference_mode():
        emission, _ = model(waveform)
        token_spans = aligner(emission[0], tokenizer(words))
    return [(w, _word_score(spans)) for w, spans in zip(words, token_spans)]


def color(score: float) -> str:
    if score >= GREEN:
        return "GRÜN "
    if score >= YELLOW:
        return "GELB "
    return "ROT  "


def fluency_report(audio_path: str, expected_text: str) -> None:
    """(1) Flüssigkeit: Wort-für-Wort-Bewertung gegen den erwarteten Text."""
    waveform = load_audio(audio_path, BUNDLE.sample_rate)
    print(f"\n=== Flüssigkeit: '{expected_text}' ===")
    for word, score in align_word_scores(waveform, normalize(expected_text)):
        print(f"  {color(score)} {score:5.2f}  {word}")


def literal_check(audio_path: str, shown: str, correct: str) -> None:
    """(2) Skizze: hat sie 'shown' literal gelesen oder zu 'correct' korrigiert?

    Wir messen, wie gut die Aufnahme zum RICHTIGEN Wort passt.
    Hoher Score -> klingt wie 'correct' -> AUTO-KORRIGIERT (nicht genau gelesen).
    Niedriger Score -> literaler Leseversuch -> ERKANNT.
    Funktioniert nur für HÖRBARE Fehler (Klasse 'hoerbar'); bei Vokallängen-/
    homophonen Fehlern ist Audio blind -> dort nur Markieren verwenden.
    """
    waveform = load_audio(audio_path, BUNDLE.sample_rate)
    (_, score), = align_word_scores(waveform, normalize(correct))
    verdict = "literal gelesen (ERKANNT)" if score < LITERAL_MAX else "auto-korrigiert"
    print(f"\n=== Fehlerprüfung: gezeigt '{shown}' / richtig '{correct}' ===")
    print(f"  Score gegen '{correct}': {score:.2f}  ->  {verdict}")


def main() -> None:
    p = argparse.ArgumentParser(description="Phase-0-Validierung der Vorlese-Bewertung")
    p.add_argument("--audio", required=True, help="WAV-Datei (Mono, 16 kHz ideal)")
    p.add_argument("--text", required=True, help="erwarteter Vorlese-Text")
    p.add_argument("--shown", help="gezeigte Falschschreibung (für Fehlerprüfung)")
    p.add_argument("--correct", help="richtiges Wort (für Fehlerprüfung)")
    args = p.parse_args()

    fluency_report(args.audio, args.text)
    if args.shown and args.correct:
        literal_check(args.audio, args.shown, args.correct)


if __name__ == "__main__":
    main()
