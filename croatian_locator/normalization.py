import unicodedata


def normalize_text(value: str):
    """Normalize text for case-insensitive and diacritic-insensitive comparison."""
    stripped_value = value.strip()
    casefolded_value = stripped_value.casefold()
    replaced_value = casefolded_value.replace("đ", "d")
    decomposed_value = unicodedata.normalize("NFD", replaced_value)

    return "".join(
        character
        for character in decomposed_value
        if not unicodedata.combining(character)
    )