import pytest
from src.validation import validate_decision, validate_options

def test_validate_decision_rejects_blank():
    with pytest.raises(ValueError):
        validate_decision("   ")

def test_validate_options_rejects_blank():
    with pytest.raises(ValueError):
        validate_options(["A", " "])

def test_validate_options_rejects_duplicates_case_insensitively():
    with pytest.raises(ValueError):
        validate_options(["Study", "study"])

def test_validate_options_strips_values():
    assert validate_options([" A ", " B "]) == ["A", "B"]
