"""
Text Preprocessing & Word Boundary Validation Module.

Prepares raw user input for pattern matching by:
1. Lowercasing text.
2. Normalizing whitespace (converting multiple spaces, tabs, newlines to a single space).
3. Preserving essential character positions while validating word boundaries to avoid false positives.
"""

import re
from typing import List, Tuple


def normalize_text(text: str) -> str:
    """
    Normalizes input text for case-insensitive and whitespace-invariant pattern searching.

    Args:
        text: Raw user input text.

    Returns:
        Normalized string (lowercased, trimmed, whitespace collapsed).
    """
    if not text:
        return ""

    # Convert to lowercase
    normalized = text.lower()

    # Collapse multiple whitespaces into a single space
    normalized = re.sub(r'\s+', ' ', normalized).strip()

    return normalized


def is_valid_word_boundary(text: str, start_idx: int, pattern_len: int) -> bool:
    """
    Verifies if a matched pattern in text occurs at valid word boundaries.
    Prevents false positives (e.g. matching 'die' inside 'diet' or 'soldier').

    Args:
        text: Target text string.
        start_idx: Starting index of match.
        pattern_len: Length of matched pattern.

    Returns:
        True if match is a full word / bounded by punctuation/spaces/boundaries, False otherwise.
    """
    end_idx = start_idx + pattern_len
    n = len(text)

    # Check left boundary
    if start_idx > 0:
        left_char = text[start_idx - 1]
        if left_char.isalnum():
            return False

    # Check right boundary
    if end_idx < n:
        right_char = text[end_idx]
        if right_char.isalnum():
            return False

    return True


def get_tokenized_words(text: str) -> List[str]:
    """Splits text into alphanumeric word tokens."""
    return re.findall(r'\b\w+\b', text.lower())
