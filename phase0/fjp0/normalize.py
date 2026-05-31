"""Textnormalisierung für den Forced-Aligner.

Der mehrsprachige Aligner ``torchaudio.pipelines.MMS_FA`` arbeitet mit einem
kleinen, romanisierten Kleinbuchstaben-Alphabet. Deutsche Umlaute und ß sind
darin nicht enthalten, deshalb romanisieren wir sie hier pragmatisch
(ä→ae, ö→oe, ü→ue, ß→ss).

WICHTIGE ENTSCHEIDUNG (siehe DECISIONS.md): Diese Romanisierung ist bewusst
einfach gehalten. Sie ist eine *Phase-0-Annahme*, die in der Kalibrierung zu
überprüfen ist – falls ein dediziertes deutsches wav2vec2-Modell verwendet
wird, kann sie entfallen. Die Funktion ist absichtlich rein (kein torch), damit
die Wort-Segmentierung unabhängig vom Modell getestet werden kann.
"""

from __future__ import annotations

import re

# Romanisierung deutscher Sonderzeichen auf das MMS_FA-Alphabet.
_UMLAUT_MAP = {
    "ä": "ae",
    "ö": "oe",
    "ü": "ue",
    "ß": "ss",
}

# Erlaubt nach der Romanisierung nur noch a–z und Leerraum als Trenner.
_NON_WORD = re.compile(r"[^a-z\s]+")
_WHITESPACE = re.compile(r"\s+")


def romanize(text: str) -> str:
    """Kleinschreibung + Umlaut/ß-Romanisierung, ohne Wort-Trennung.

    >>> romanize("Süße Grüße, Tisch!")
    'suesse gruesse tisch'
    """
    text = text.lower()
    for src, dst in _UMLAUT_MAP.items():
        text = text.replace(src, dst)
    text = _NON_WORD.sub(" ", text)
    return _WHITESPACE.sub(" ", text).strip()


def normalize(text: str) -> list[str]:
    """Zerlegt einen Vorlese-Text in romanisierte Aligner-Token (Wörter).

    Leere Token werden verworfen. Das Ergebnis ist die Wortliste, die exakt so
    an den Tokenizer des Aligners übergeben wird.

    >>> normalize("Im Regal stehen viele Bücher.")
    ['im', 'regal', 'stehen', 'viele', 'buecher']
    """
    roman = romanize(text)
    return [w for w in roman.split(" ") if w]


def word(text: str) -> str:
    """Romanisiert ein einzelnes Wort (für die lautgetreue Fehlerprüfung).

    Wirft :class:`ValueError`, wenn nach der Normalisierung kein bzw. mehr als
    ein Token übrig bleibt – die Distanzprüfung ist pro *Einzelwort* definiert.

    >>> word("Tisch")
    'tisch'
    """
    tokens = normalize(text)
    if len(tokens) != 1:
        raise ValueError(
            f"erwarte genau ein Wort, bekam {len(tokens)} aus {text!r}: {tokens}"
        )
    return tokens[0]
