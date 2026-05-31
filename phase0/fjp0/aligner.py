"""Austauschbares Aligner-Backend.

Das akustische Modell ist hinter einem schmalen Protokoll gekapselt, damit die
gesamte Phase-0-Logik (Kalibrierung, Gating, Report) **ohne torch** getestet
werden kann:

* :class:`ScriptedAligner` – deterministisch, gespeist aus gelabelten Clips.
  Treibt Selbsttest und Unit-Tests; lädt kein Modell.
* :class:`TorchAudioAligner` – die *echte* Implementierung über
  ``torchaudio.pipelines.MMS_FA`` Forced-Alignment. torch/torchaudio werden
  **lazy** importiert, also nur wenn diese Klasse tatsächlich benutzt wird.

ENTSCHEIDUNG (DECISIONS.md): Die Trennung Interface ↔ Implementierung ist die
zentrale Architektur-Entscheidung von Phase 0. Sie erlaubt es, die Methodik
(trennt die Bewertung? erkennt sie literal vs. auto-korrigiert?) als Pipeline
end-to-end zu beweisen, ohne ein 200-MB-Modell und ohne echte Kinderstimme.
"""

from __future__ import annotations

import random
from typing import Protocol, runtime_checkable

from .scoring import WordScore


@runtime_checkable
class Aligner(Protocol):
    """Liefert pro Referenzwort einen Score in [0, 1] (akustische Nähe)."""

    sample_rate: int

    def word_scores(self, wav_path: str, words: list[str]) -> list[WordScore]:
        ...


# --------------------------------------------------------------------------- #
# Deterministischer Aligner für Selbsttest & Unit-Tests (kein torch, kein Modell)
# --------------------------------------------------------------------------- #

# Wie ein gelabelter Clip auf eine Score-Verteilung abgebildet wird.
# (Mittelwert, Streuung) – bewusst überlappend, damit Kalibrierung nicht-trivial,
# aber trennbar ist.
_LABEL_DISTRIBUTION = {
    "fluent": (0.88, 0.05),         # flüssig gelesen → hohe Nähe zum Sollwort
    "stocked": (0.45, 0.08),        # gestockt/falsch → niedrige Nähe
    "autocorrected": (0.85, 0.05),  # still korrigiert → klingt wie richtiges Wort
    "literal": (0.30, 0.08),        # Falschschreibung literal gelesen → fern
}


class ScriptedAligner:
    """Erzeugt reproduzierbare Scores aus pro-Clip hinterlegten Labels.

    Die Zuordnung ``{wav_path: label}`` bestimmt die Score-Verteilung. Damit
    lässt sich die volle Pipeline (inkl. Kalibrierung und GO/NO-GO) deterministisch
    durchspielen, ohne Audio zu analysieren.
    """

    def __init__(self, labels: dict[str, str], *, sample_rate: int = 16000,
                 seed: int = 1975) -> None:
        self.sample_rate = sample_rate
        self._labels = labels
        self._rng = random.Random(seed)

    def _score_for(self, wav_path: str) -> float:
        label = self._labels.get(wav_path)
        if label not in _LABEL_DISTRIBUTION:
            raise KeyError(
                f"kein Label für {wav_path!r} (bekannt: {list(self._labels)})"
            )
        mu, sigma = _LABEL_DISTRIBUTION[label]
        return min(1.0, max(0.0, self._rng.gauss(mu, sigma)))

    def word_scores(self, wav_path: str, words: list[str]) -> list[WordScore]:
        # Ein Clip-Grundscore, pro Wort leicht variiert – stabil über den Seed.
        base = self._score_for(wav_path)
        out = []
        for w in words:
            jitter = self._rng.uniform(-0.04, 0.04)
            out.append(WordScore(w, min(1.0, max(0.0, base + jitter))))
        return out


# --------------------------------------------------------------------------- #
# Echte Implementierung: torchaudio MMS_FA Forced Alignment (lazy import)
# --------------------------------------------------------------------------- #


class TorchAudioAligner:
    """Forced-Alignment-Aligner über ``torchaudio.pipelines.MMS_FA``.

    Lädt Modell/Tokenizer/Aligner einmalig (lazy). Für echte Aufnahmen gedacht;
    in CI/ohne torch wird er nicht instanziiert.
    """

    def __init__(self) -> None:
        # Lazy: torch nur importieren, wenn die echte Engine wirklich läuft.
        import torch  # noqa: F401
        import torchaudio
        from torchaudio.pipelines import MMS_FA as bundle

        self._torch = torch
        self._torchaudio = torchaudio
        self._bundle = bundle
        self.sample_rate = bundle.sample_rate
        self._model = bundle.get_model()
        self._tokenizer = bundle.get_tokenizer()
        self._aligner = bundle.get_aligner()

    def _load(self, wav_path: str):
        waveform, sr = self._torchaudio.load(wav_path)
        if waveform.size(0) > 1:                       # → Mono
            waveform = waveform.mean(dim=0, keepdim=True)
        if sr != self.sample_rate:
            waveform = self._torchaudio.functional.resample(
                waveform, sr, self.sample_rate
            )
        return waveform

    @staticmethod
    def _word_score(spans) -> float:
        """Längen-gewichteter Mittelwert der Token-Scores eines Wortes."""
        total = sum(len(s) for s in spans)
        if total == 0:
            return 0.0
        return sum(s.score * len(s) for s in spans) / total

    def word_scores(self, wav_path: str, words: list[str]) -> list[WordScore]:
        waveform = self._load(wav_path)
        with self._torch.inference_mode():
            emission, _ = self._model(waveform)
            token_spans = self._aligner(emission[0], self._tokenizer(words))
        return [
            WordScore(w, self._word_score(spans))
            for w, spans in zip(words, token_spans)
        ]
