"""WAV-I/O, Energie-Messung und synthetische Testtöne – nur Python-Stdlib.

Bewusst **ohne numpy/soundfile**, damit das Energie-Gate und die
Selbsttest-Audioerzeugung überall (auch ohne torch-Stack) laufen. Für die
*echte* akustische Bewertung lädt der torchaudio-Aligner die WAV selbst; diese
Helfer dienen dem Gating und dem reproduzierbaren Selbsttest.
"""

from __future__ import annotations

import math
import struct
import wave
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Clip:
    """Dekodierte 16-bit-PCM-Mono-Audiodaten."""

    samples: list[float]   # normalisiert auf [-1, 1]
    sample_rate: int

    @property
    def duration_s(self) -> float:
        if self.sample_rate == 0:
            return 0.0
        return len(self.samples) / self.sample_rate

    def rms(self) -> float:
        """Root-Mean-Square-Energie in [0, 1]."""
        if not self.samples:
            return 0.0
        return math.sqrt(sum(s * s for s in self.samples) / len(self.samples))


_INT16_MAX = 32767


def read_wav(path: str | Path) -> Clip:
    """Liest eine WAV-Datei (beliebige Kanäle/Breite) als Mono-Float-Clip."""
    with wave.open(str(path), "rb") as w:
        n_channels = w.getnchannels()
        sampwidth = w.getsampwidth()
        sample_rate = w.getframerate()
        n_frames = w.getnframes()
        raw = w.readframes(n_frames)

    if sampwidth != 2:
        raise ValueError(
            f"{path}: nur 16-bit-PCM unterstützt (sampwidth={sampwidth}). "
            f"Bitte als 16-bit-WAV exportieren."
        )

    count = len(raw) // 2
    ints = struct.unpack("<" + "h" * count, raw)

    if n_channels > 1:
        # Kanäle interleaved → auf Mono mitteln.
        frames = [
            ints[i : i + n_channels] for i in range(0, len(ints), n_channels)
        ]
        mono = [sum(fr) / len(fr) for fr in frames]
    else:
        mono = list(ints)

    samples = [s / _INT16_MAX for s in mono]
    return Clip(samples=samples, sample_rate=sample_rate)


def write_wav(path: str | Path, clip: Clip) -> None:
    """Schreibt einen Float-Clip als 16-bit-PCM-Mono-WAV."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    ints = [
        max(-_INT16_MAX, min(_INT16_MAX, int(round(s * _INT16_MAX))))
        for s in clip.samples
    ]
    raw = struct.pack("<" + "h" * len(ints), *ints)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(clip.sample_rate)
        w.writeframes(raw)


def tone(
    freq_hz: float,
    duration_s: float,
    *,
    sample_rate: int = 16000,
    amplitude: float = 0.3,
    noise: float = 0.0,
    seed: int = 0,
) -> Clip:
    """Erzeugt einen Sinuston (+ optionales weißes Rauschen) als Testclip.

    Nur für den Selbsttest des Harness (Gating + Pipeline). Das ist KEINE
    Sprache – die akustische Modellgüte wird über echte Aufnahmen bzw. den
    torch-Smoke-Test validiert (siehe DECISIONS.md).
    """
    import random

    rng = random.Random(seed)
    n = int(duration_s * sample_rate)
    two_pi_f = 2 * math.pi * freq_hz
    samples = []
    for i in range(n):
        s = amplitude * math.sin(two_pi_f * i / sample_rate)
        if noise:
            s += rng.uniform(-noise, noise)
        samples.append(max(-1.0, min(1.0, s)))
    return Clip(samples=samples, sample_rate=sample_rate)


def silence(duration_s: float, *, sample_rate: int = 16000, noise: float = 0.0,
            seed: int = 0) -> Clip:
    """Stiller (optional leise verrauschter) Clip – für den Gating-Test."""
    return tone(0.0, duration_s, sample_rate=sample_rate, amplitude=0.0,
                noise=noise, seed=seed)
