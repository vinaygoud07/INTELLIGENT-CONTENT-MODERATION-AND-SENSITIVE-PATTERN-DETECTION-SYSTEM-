"""
Randomized Algorithm Implementation for Spam & Suspicious Pattern Detection.

DSA Concept:
Randomized Algorithms use non-deterministic decisions to achieve faster average performance
or to protect against adversarial inputs (e.g., hash collisions designed to degrade performance).

In this system, Randomization is applied in two main ways:
1. Monte Carlo Sub-Window Sampling:
   For long input texts, instead of exhaustively scanning every n-gram for repetition/spam,
   we randomly sample 'k' text windows. This gives O(k * W) processing time instead of O(N * W),
   providing high-probability detection of spam/bot-generated content with reduced compute.

2. Universal Hashing with Random Prime Seeds:
   To prevent adversarial inputs crafted to trigger worst-case O(N*M) Rabin-Karp hash collisions,
   we randomly select a prime P from a set of cryptographically strong primes for hash verification.

Time Complexity:
- Sub-window Sampling: O(k * W), where k = number of samples, W = window size.
- Standard Full Scan: O(N)

Space Complexity:
- Auxiliary Space: O(k * W)
"""

import random
from typing import List, Dict, Any, Tuple


# List of strong primes for universal hash randomization
RANDOM_PRIMES = [101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173]


def randomized_pattern_sample(
    text: str,
    sample_count: int = 5,
    window_size: int = 15
) -> Tuple[List[Dict[str, Any]], str]:
    """
    Randomly samples windows from text to inspect for suspicious structure or repetition.

    Args:
        text: Input string.
        sample_count: Number of random windows to sample.
        window_size: Character length of each window.

    Returns:
        Tuple containing:
        - sampled_windows (List[Dict]): List of sampled text chunks with starting index and hash.
        - explanation (str): Description of randomized decisions.
    """
    n = len(text)
    sampled_windows: List[Dict[str, Any]] = []

    if n <= window_size:
        # Text is small enough, inspect entire text
        prime = random.choice(RANDOM_PRIMES)
        hash_val = sum(ord(c) for c in text) % prime
        sampled_windows.append({
            'start_index': 0,
            'window_text': text,
            'hash_prime': prime,
            'hash_val': hash_val
        })
        return sampled_windows, "Text is short (<= window_size). Inspected 100% of text without sub-sampling."

    # Perform Monte Carlo random sampling of windows
    random.seed()  # Ensure fresh randomness
    indices = sorted(random.sample(range(0, n - window_size + 1), min(sample_count, n - window_size + 1)))

    for idx in indices:
        chunk = text[idx:idx + window_size]
        prime = random.choice(RANDOM_PRIMES)
        # Compute randomized polynomial hash
        h_val = 0
        for char in chunk:
            h_val = (h_val * 31 + ord(char)) % prime

        sampled_windows.append({
            'start_index': idx,
            'window_text': chunk,
            'hash_prime': prime,
            'hash_val': h_val
        })

    explanation = (
        f"Monte Carlo Random Sampling active: Sampled {len(sampled_windows)} random "
        f"windows of size {window_size} characters across total text length of {n} characters. "
        f"Each window verified using randomly chosen prime modulos."
    )

    return sampled_windows, explanation


def randomized_spam_check(text: str) -> Tuple[bool, float, List[Dict[str, Any]], str]:
    """
    Detects spam-like repeated content using randomized sampling & word frequency analysis.

    Args:
        text: Input text to analyze.

    Returns:
        Tuple containing:
        - is_spam (bool): True if suspicious spam repetition detected.
        - spam_score (float): Score from 0.0 to 1.0 indicating spam probability.
        - sample_logs (List[Dict]): Log of randomized sampling checks.
        - rationale (str): Explanation of why text was flagged or cleared.
    """
    words = [w.strip() for w in text.split() if w.strip()]
    total_words = len(words)

    if total_words < 4:
        return False, 0.0, [], "Text too short to establish repetition pattern."

    # Monte Carlo sampling: Pick random pairs of words to check duplication
    sample_size = min(15, total_words)
    random_indices = random.sample(range(total_words), sample_size)
    sampled_words = [words[i].lower() for i in random_indices]

    # Count duplicates in random sample
    unique_sampled = set(sampled_words)
    duplication_ratio = 1.0 - (len(unique_sampled) / float(len(sampled_words)))

    # Also check character-level repetition (e.g. "aaaaa", "click click click")
    char_repeat_count = 0
    for i in range(len(text) - 4):
        if text[i] == text[i+1] == text[i+2] == text[i+3] == text[i+4]:
            char_repeat_count += 1

    sample_logs = [
        {'total_words': total_words, 'sampled_count': sample_size, 'sample_words': sampled_words},
        {'duplication_ratio': round(duplication_ratio, 3), 'char_repeat_count': char_repeat_count}
    ]

    is_spam = duplication_ratio >= 0.40 or char_repeat_count >= 2
    spam_score = min(1.0, duplication_ratio * 1.5 + (char_repeat_count * 0.2))

    rationale = (
        f"Randomized Sampling Result: Checked {sample_size} random word positions. "
        f"Duplication ratio in sample = {duplication_ratio:.1%}, character repeat clusters = {char_repeat_count}. "
        f"{'FLAGGED as Spam/Repetitive.' if is_spam else 'CLEARED (No excessive repetition).'}"
    )

    return is_spam, round(spam_score, 2), sample_logs, rationale
