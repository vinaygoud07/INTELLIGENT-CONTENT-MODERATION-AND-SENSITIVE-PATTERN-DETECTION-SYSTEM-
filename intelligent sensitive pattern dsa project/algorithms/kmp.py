"""
Knuth-Morris-Pratt (KMP) Algorithm Implementation.

DSA Concept:
KMP avoids re-comparing characters that have already been matched in previous steps.
It uses a precomputed Longest Prefix Suffix (LPS) array (also known as the Pi table or Failure function).
LPS[i] stores the length of the longest proper prefix of pattern[0..i] that is also a suffix of pattern[0..i].

When a mismatch occurs at text[i] and pattern[j]:
- Instead of resetting i to i - j + 1 and j to 0 (like Naive search), KMP keeps i fixed
  and shifts pattern by setting j = LPS[j - 1].

Time Complexity:
- Preprocessing (LPS construction): O(M)
- Search phase: O(N)
- Total Time Complexity: O(N + M)

Space Complexity:
- Auxiliary Space: O(M) to store the LPS array.
"""

from typing import List, Dict, Any, Tuple


def compute_lps_array(pattern: str) -> Tuple[List[int], int, List[Dict[str, Any]]]:
    """
    Computes the Longest Prefix Suffix (LPS) array for the given pattern.

    Args:
        pattern: The target pattern string.

    Returns:
        Tuple containing:
        - lps (List[int]): The LPS array of length M.
        - comparisons (int): Character comparisons during LPS construction.
        - lps_steps (List[Dict]): Detailed computation log for visualization.
    """
    m = len(pattern)
    lps = [0] * m
    comparisons = 0
    lps_steps: List[Dict[str, Any]] = []

    length = 0  # Length of the previous longest prefix suffix
    i = 1

    lps_steps.append({
        'index': 0,
        'char': pattern[0] if m > 0 else '',
        'lps_val': 0,
        'len_prev': 0,
        'explanation': 'LPS[0] is always 0 by definition.'
    })

    while i < m:
        comparisons += 1
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            lps_steps.append({
                'index': i,
                'char': pattern[i],
                'lps_val': length,
                'len_prev': length - 1,
                'explanation': f"Match: pattern[{i}] ('{pattern[i]}') == pattern[{length-1}] ('{pattern[length-1]}'). LPS[{i}] = {length}."
            })
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
                lps_steps.append({
                    'index': i,
                    'char': pattern[i],
                    'lps_val': lps[i],
                    'len_prev': length,
                    'explanation': f"Mismatch: fallback length to LPS[{length}] = {length}."
                })
            else:
                lps[i] = 0
                lps_steps.append({
                    'index': i,
                    'char': pattern[i],
                    'lps_val': 0,
                    'len_prev': 0,
                    'explanation': f"Mismatch & length=0: LPS[{i}] set to 0."
                })
                i += 1

    return lps, comparisons, lps_steps


def kmp_search(text: str, pattern: str) -> Tuple[List[int], int, List[int], List[Dict[str, Any]]]:
    """
    Performs Knuth-Morris-Pratt (KMP) string search.

    Args:
        text: The text to search inside.
        pattern: The pattern to find.

    Returns:
        Tuple containing:
        - matches (List[int]): Starting indices of all matches.
        - total_comparisons (int): Total character comparisons made.
        - lps (List[int]): Computed LPS array.
        - search_steps (List[Dict]): Execution steps for interactive visualization.
    """
    matches: List[int] = []
    n = len(text)
    m = len(pattern)

    if m == 0 or n < m:
        return matches, 0, [], []

    lps, lps_comparisons, _ = compute_lps_array(pattern)
    search_comparisons = 0
    search_steps: List[Dict[str, Any]] = []

    i = 0  # index for text
    j = 0  # index for pattern

    while i < n:
        search_comparisons += 1
        if pattern[j] == text[i]:
            search_steps.append({
                'text_idx': i,
                'pattern_idx': j,
                'char_text': text[i],
                'char_pattern': pattern[j],
                'action': 'MATCH_CHAR',
                'lps_used': None
            })
            i += 1
            j += 1

        if j == m:
            matches.append(i - j)
            search_steps.append({
                'text_idx': i - 1,
                'pattern_idx': j - 1,
                'char_text': text[i - 1],
                'char_pattern': pattern[j - 1],
                'action': f'PATTERN_FOUND at index {i - j}',
                'lps_used': lps[j - 1]
            })
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                old_j = j
                j = lps[j - 1]
                search_steps.append({
                    'text_idx': i,
                    'pattern_idx': old_j,
                    'char_text': text[i],
                    'char_pattern': pattern[old_j],
                    'action': f'MISMATCH -> Shift pattern index from {old_j} to LPS[{old_j-1}] = {j}',
                    'lps_used': j
                })
            else:
                search_steps.append({
                    'text_idx': i,
                    'pattern_idx': 0,
                    'char_text': text[i],
                    'char_pattern': pattern[0],
                    'action': 'MISMATCH at j=0 -> Increment text index i',
                    'lps_used': 0
                })
                i += 1

    total_comparisons = lps_comparisons + search_comparisons
    return matches, total_comparisons, lps, search_steps
