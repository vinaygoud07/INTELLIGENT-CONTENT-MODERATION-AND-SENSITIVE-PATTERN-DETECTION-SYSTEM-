"""
Rabin-Karp Algorithm Implementation using Rolling Hash.

DSA Concept:
Rabin-Karp converts pattern matching into a numeric hash comparison.
Instead of comparing strings character-by-character at every window position, it compares:
1. Hash of Pattern vs Hash of Text Window (O(1) comparison).
2. If hashes match, it performs exact character-by-character verification to handle collisions.
3. It slides the window in O(1) time using a Rolling Hash:
   Hash_new = (Base * (Hash_old - text[i]*h) + text[i+m]) % Prime

Time Complexity:
- Average / Best Case: O(N + M)
- Worst Case: O(N * M) (if poor hash function causes collisions at every window)

Space Complexity:
- Auxiliary Space: O(1)
"""

from typing import List, Dict, Any, Tuple


def rabin_karp_search(
    text: str,
    pattern: str,
    base: int = 256,
    prime: int = 101
) -> Tuple[List[int], int, int, List[Dict[str, Any]]]:
    """
    Performs Rabin-Karp string search using rolling hash.

    Args:
        text: The source text to search in.
        pattern: The target pattern substring.
        base: Number of unique characters in alphabet (default 256 for ASCII).
        prime: A prime number used for modulo arithmetic to prevent integer overflow.

    Returns:
        Tuple containing:
        - matches (List[int]): Starting indices of all occurrences.
        - total_comparisons (int): Total character comparisons made during verification.
        - spurious_hits (int): Number of hash collisions where characters did not match.
        - step_logs (List[Dict]): Detailed rolling hash log for interactive visualization.
    """
    matches: List[int] = []
    step_logs: List[Dict[str, Any]] = []
    spurious_hits = 0
    total_comparisons = 0

    n = len(text)
    m = len(pattern)

    if m == 0 or n < m:
        return matches, total_comparisons, spurious_hits, step_logs

    # Compute h = base^(m-1) % prime
    h = 1
    for _ in range(m - 1):
        h = (h * base) % prime

    p_hash = 0  # Hash value for pattern
    t_hash = 0  # Hash value for current window in text

    # Compute initial hash for pattern and first window of text
    for i in range(m):
        p_hash = (base * p_hash + ord(pattern[i])) % prime
        t_hash = (base * t_hash + ord(text[i])) % prime

    step_logs.append({
        'window_idx': 0,
        'window_text': text[0:m],
        'pattern_hash': p_hash,
        'text_hash': t_hash,
        'hash_match': p_hash == t_hash,
        'status': 'INITIAL_WINDOW'
    })

    # Slide pattern over text window
    for i in range(n - m + 1):
        if p_hash == t_hash:
            # Hash match detected: verify character by character to handle collisions
            match_found = True
            for j in range(m):
                total_comparisons += 1
                if text[i + j] != pattern[j]:
                    match_found = False
                    spurious_hits += 1
                    break

            if match_found:
                matches.append(i)
                step_logs[-1]['status'] = f'MATCH_FOUND at index {i}'
            else:
                step_logs[-1]['status'] = f'COLLISION at index {i}'

        # Compute hash for next window
        if i < n - m:
            t_hash = (base * (t_hash - ord(text[i]) * h) + ord(text[i + m])) % prime
            # If t_hash becomes negative, convert to positive
            if t_hash < 0:
                t_hash = t_hash + prime

            step_logs.append({
                'window_idx': i + 1,
                'window_text': text[i + 1:i + 1 + m],
                'pattern_hash': p_hash,
                'text_hash': t_hash,
                'hash_match': p_hash == t_hash,
                'status': 'SLIDING_WINDOW'
            })

    return matches, total_comparisons, spurious_hits, step_logs
