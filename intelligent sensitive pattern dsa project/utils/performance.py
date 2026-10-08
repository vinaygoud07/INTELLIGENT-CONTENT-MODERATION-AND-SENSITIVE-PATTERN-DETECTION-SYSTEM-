"""
Performance & Benchmark Reporting Helpers.
Formats algorithm execution metrics for Streamlit table and chart displays.
"""

import pandas as pd
from typing import Dict, Any


def format_metric_table(algorithm_metrics: Dict[str, Any]) -> pd.DataFrame:
    """
    Converts raw algorithm metrics dictionary into a clean pandas DataFrame.

    Args:
        algorithm_metrics: Dict containing metrics per algorithm.

    Returns:
        pd.DataFrame formatted for Streamlit UI displaying execution times,
        character comparisons, matches, and theoretical time complexities.
    """
    rows = []
    for alg_name, metrics in algorithm_metrics.items():
        rows.append({
            "Algorithm": alg_name,
            "Execution Time (ms)": metrics.get("time_ms", 0.0),
            "Comparisons / Steps": metrics.get("comparisons", 0),
            "Matches Found": metrics.get("matches_found", 0),
            "Time Complexity": metrics.get("complexity", "N/A")
        })

    df = pd.DataFrame(rows)
    return df
