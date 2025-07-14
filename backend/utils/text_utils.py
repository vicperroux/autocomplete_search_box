"""
Text processing utilities for the autocomplete service
"""


def normalize_text(text):
    """Normalize text by standardizing apostrophes and other characters

    Args:
        text: The text to normalize

    Returns:
        str: Normalized text in lowercase with standardized characters
    """
    if not isinstance(text, str):
        return text

    # Replace various apostrophe types with a standard apostrophe (happens for McDonald's)
    apostrophe_variants = ["'", "`", "´", "′", "'"]
    normalized = text.lower()
    for variant in apostrophe_variants:
        normalized = normalized.replace(variant, "'")

    return normalized
