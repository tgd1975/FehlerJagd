from app.config import REPO_ROOT
from app.proofread.check import check_markings, locate_errors, tokenize_note
from app.story.loader import discover_cases, read_scene_text

CASES = discover_cases(REPO_ROOT / "stories")
FALL01 = CASES["fall-01"]
S05 = FALL01.scene("szene-05")
NOTE = read_scene_text(FALL01, S05)


def _index_of(shown: str) -> int:
    located = locate_errors(tokenize_note(NOTE), S05.proofread_errors)
    err = next(e for e in S05.proofread_errors if e.shown == shown)
    return located[err.error_id]


def test_front_matter_stripped():
    assert not NOTE.lstrip().startswith("---")
    assert "Bücehr" in NOTE


def test_all_errors_locatable():
    located = locate_errors(tokenize_note(NOTE), S05.proofread_errors)
    assert len(located) == len(S05.proofread_errors)


def test_perfect_marking():
    marks = [_index_of(e.shown) for e in S05.proofread_errors]
    res = check_markings(NOTE, S05.proofread_errors, marks)
    assert res.all_found
    assert res.found_count == 4
    assert res.false_positives == 0
    assert res.score == 1.0


def test_partial_with_false_positive():
    marks = [_index_of("Bücehr"), 0]   # ein Treffer + Front-Wort als Falsch-Treffer
    res = check_markings(NOTE, S05.proofread_errors, marks)
    assert res.found_count == 1
    assert res.false_positives == 1
    assert not res.all_found


def test_resolution_carries_regel_and_tipp():
    res = check_markings(NOTE, S05.proofread_errors, [])
    by_shown = {o.shown: o for o in res.outcomes}
    assert by_shown["ales"].regel == 8
    assert "Doppel-Bremse" in by_shown["ales"].tipp
    assert by_shown["regal"].correct == "Regal"
    assert all(not o.found for o in res.outcomes)  # nichts markiert


def test_tokenizer_offsets_match_text():
    """Token-Offsets müssen exakt den Originaltext indexieren (fürs Highlighting)."""
    for tok in tokenize_note(NOTE):
        assert NOTE[tok.start:tok.end] == tok.text


# --- Beistrich-Lückenmodus (Fall 05) ---------------------------------------
FALL05 = CASES["fall-05"]
S05_5 = FALL05.scene("szene-05")
NOTE5 = read_scene_text(FALL05, S05_5)


def test_gap_error_located_before_gap():
    located = locate_errors(tokenize_note(NOTE5), S05_5.proofread_errors)
    gap_err = next(e for e in S05_5.proofread_errors if e.is_gap)
    toks = tokenize_note(NOTE5)
    gap_idx = located[gap_err.error_id]
    # Index zeigt auf 'Kuchen'; direkt danach folgt 'kein' (die Lücke dazwischen).
    assert toks[gap_idx].text == "Kuchen"
    assert toks[gap_idx + 1].text == "kein"


def test_gap_found_only_via_gap_channel():
    located = locate_errors(tokenize_note(NOTE5), S05_5.proofread_errors)
    gap_err = next(e for e in S05_5.proofread_errors if e.is_gap)
    gap_idx = located[gap_err.error_id]

    # Über den Wort-Kanal markiert → NICHT gefunden (Komma ist an der Lücke).
    res_word = check_markings(NOTE5, S05_5.proofread_errors, [gap_idx], [])
    komma = next(o for o in res_word.outcomes if o.is_gap)
    assert komma.found is False
    assert gap_idx in res_word.false_positive_indices

    # Über den Lücken-Kanal markiert → gefunden.
    res_gap = check_markings(NOTE5, S05_5.proofread_errors, [], [gap_idx])
    komma = next(o for o in res_gap.outcomes if o.is_gap)
    assert komma.found is True
    assert komma.regel == 2


def test_full_marking_mixed_channels():
    located = locate_errors(tokenize_note(NOTE5), S05_5.proofread_errors)
    word_marks = [located[e.error_id] for e in S05_5.proofread_errors if not e.is_gap]
    gap_marks = [located[e.error_id] for e in S05_5.proofread_errors if e.is_gap]
    res = check_markings(NOTE5, S05_5.proofread_errors, word_marks, gap_marks)
    assert res.all_found
    assert res.false_positives == 0
