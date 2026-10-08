"""
Naive String Matching Algorithm Implementation.

DSA Concept:
The Naive algorithm slides the pattern window over the text one character at a time.
For each starting index i in text (0 to N - M), it compares characters of pattern with text.
If all M characters match, a match is recorded at index i.

Time Complexity:
- Worst Case: O((N - M + 1) * M) where N = len(text), M = len(pattern)
- Best Case: O(N) when first character mismatch occurs everywhere.

Space Complexity:
- O(1) auxiliary space.
"""

from typing import List, Dict, Any, Tuple


def naive_search(text: str, pattern: str) -> Tuple[List[int], int, List[Dict[str, Any]]]:
    """
    Performs Naive String Search to find all occurrences of pattern in text.

    Args:
        text: The target text to search in.
        pattern: The substring pattern to look for.

    Returns:
        Tuple containing:
        - matches (List[int]): Starting indices of matches in text.
        - comparisons (int): Total character comparisons made.
        - step_logs (List[Dict]): Log of matching steps for visualization.
    """
    matches: List[int] = []
    comparisons: int = 0
    step_logs: List[Dict[str, Any]] = []

    n = len(text)
    m = len(pattern)

    if m == 0 or n < m:
        return matches, comparisons, step_logs

    for i in range(n - m + 1):
        j = 0
        match_success = True
        
        while j < m:
            comparisons += 1
            if text[i + j] == pattern[j]:
                j += 1
            else:
                match_success = False
                break
        
        step_logs.append({
            'index': i,
            'matched_length': j,
            'is_match': match_success and (j == m),
            'window_text': text[i:i + m]
        })

        if j == m:
            matches.append(i)

    return matches, comparisons, step_logs
