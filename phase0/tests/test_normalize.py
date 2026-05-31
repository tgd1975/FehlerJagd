import pytest

from fjp0.normalize import normalize, romanize, word


def test_romanize_umlauts_and_sharp_s():
    assert romanize("Süße Grüße, Tisch!") == "suesse gruesse tisch"


def test_romanize_lowercases_and_strips_punctuation():
    assert romanize("Im Regal: viele Bücher!!!") == "im regal viele buecher"


def test_normalize_splits_words():
    assert normalize("Im Regal stehen viele Bücher.") == [
        "im", "regal", "stehen", "viele", "buecher",
    ]


def test_normalize_drops_empty_tokens():
    assert normalize("   ,,,   ") == []


def test_word_single():
    assert word("Tisch") == "tisch"
    assert word("Zahl") == "zahl"


def test_word_rejects_multiple_tokens():
    with pytest.raises(ValueError):
        word("zwei woerter")


def test_word_rejects_empty():
    with pytest.raises(ValueError):
        word("...")
