from app.story.regeln import (
    METHOD_MARK,
    METHOD_READ_OR_MARK,
    NO_REGEL,
    erwartete_regel,
    validate_error_regel,
)


def test_mapping():
    assert erwartete_regel("grossschreibung") == 1
    assert erwartete_regel("ie") == 5
    assert erwartete_regel("vokallaenge") == 8
    assert erwartete_regel("hoerbar") == NO_REGEL
    assert erwartete_regel("dehnungs-h") == NO_REGEL


def test_valid_combinations():
    assert validate_error_regel("ie", 5, METHOD_MARK) == []
    assert validate_error_regel("hoerbar", NO_REGEL, METHOD_READ_OR_MARK) == []
    assert validate_error_regel("vokallaenge", 8, METHOD_MARK) == []


def test_wrong_regel_number():
    errs = validate_error_regel("ie", 4, METHOD_MARK)
    assert errs and "verlangt regel 5" in errs[0]


def test_regel_must_be_dash_outside_eight():
    errs = validate_error_regel("hoerbar", 1, METHOD_READ_OR_MARK)
    assert errs and "außerhalb" in errs[0]


def test_only_hoerbar_may_be_read():
    # ie ist audio-blind → darf nicht 'lesen_oder_markieren' sein.
    errs = validate_error_regel("ie", 5, METHOD_READ_OR_MARK)
    assert any("hoerbar" in e for e in errs)


def test_unknown_class_and_method():
    assert validate_error_regel("quatsch", "–", METHOD_MARK)
    assert validate_error_regel("ie", 5, "raten")
