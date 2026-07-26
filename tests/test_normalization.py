import pytest

from croatian_locator.normalization import normalize_text


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("Čakovec", "cakovec"),
        ("Cakovec", "cakovec"),
        ("čakovec", "cakovec"),
        ("ČAKOVEC", "cakovec"),
        ("Šibenik", "sibenik"),
        ("Sibenik", "sibenik"),
        ("Đakovo", "dakovo"),
        ("Dakovo", "dakovo"),
        ("Županja", "zupanja"),
        ("Zupanja", "zupanja"),
        ("Pula", "pula"),
        ("PULA", "pula"),
        ("pula", "pula"),
        ("  ČAKOVEC  ", "cakovec"),
    ],
)
def test_normalize_text(value: str, expected: str):
    assert normalize_text(value) == expected