"""
Risk Scoring & Moderation Status Generator.

Calculates a transparent, deterministic risk score from 0 to 100 based on:
1. Category Risk Weights (Offensive, Harmful, Prohibited, Spam)
2. Match Frequency & Density relative to total text length
3. Spam / Repetition score from Randomized Algorithm
4. Severity thresholds mapped to human-readable Moderation Status cards.
"""

from typing import List, Dict, Any, Tuple
from .patterns import CATEGORY_WEIGHTS


def calculate_risk_score(
    matches: List[Dict[str, Any]],
    spam_score: float,
    text_length: int
) -> Tuple[int, str, str, List[str]]:
    """
    Computes total risk score (0 - 100) and produces moderation status breakdown.

    Args:
        matches: Verified pattern matches found in text.
        spam_score: Spam/repetition score between 0.0 and 1.0 from randomized detector.
        text_length: Total character length of normalized input text.

    Returns:
        Tuple containing:
        - risk_score (int): 0 to 100
        - severity (str): Safe / Low / Medium / High / Critical
        - status_card (str): ✅ Safe Content / ⚠️ Potentially Harmful / 🚫 Prohibited Content
        - explanations (List[str]): List of reasons explaining the risk rating.
    """
    if text_length == 0:
        return 0, "Safe", "✅ Safe Content", ["No content provided."]

    accumulated_points = 0
    explanations: List[str] = []

    # Track matches per category
    category_counts: Dict[str, int] = {}
    matched_words: List[str] = []

    for match in matches:
        cat = match.get('category', 'Spam / Suspicious')
        pat = match.get('pattern', '')
        category_counts[cat] = category_counts.get(cat, 0) + 1
        if pat not in matched_words:
            matched_words.append(pat)

    # 1. Base Score from Category Weights
    for cat, count in category_counts.items():
        base_weight = CATEGORY_WEIGHTS.get(cat, 10)
        # Apply diminishing return for multiple occurrences of same category
        cat_points = base_weight + (count - 1) * (base_weight * 0.4)
        accumulated_points += cat_points
        explanations.append(
            f"Detected {count} instance(s) in category '{cat}' (+{int(cat_points)} pts)."
        )

    # 2. Add Spam / Repetition penalty
    if spam_score > 0.3:
        spam_points = spam_score * 30
        accumulated_points += spam_points
        explanations.append(
            f"Randomized spam check detected repetitive pattern (+{int(spam_points)} pts)."
        )

    # 3. Density Multiplier for short text with high concentration of sensitive words
    if len(matched_words) > 0 and text_length < 50:
        density_bonus = 15
        accumulated_points += density_bonus
        explanations.append(f"High density of sensitive patterns relative to short text length (+{density_bonus} pts).")

    # Clamp final risk score to 0 - 100
    risk_score = min(100, int(round(accumulated_points)))

    # Determine Severity Level & Status Card
    severity, status_card = get_severity_level(risk_score, category_counts)

    if risk_score == 0:
        explanations.append("No sensitive or prohibited patterns detected. Content is clean.")

    return risk_score, severity, status_card, explanations


def get_severity_level(risk_score: int, category_counts: Dict[str, int]) -> Tuple[str, str]:
    """
    Maps risk score and category flags to severity ratings and UI status cards.

    Returns:
        Tuple of (SeverityLevel, StatusCard)
    """
    # Direct escalation if critical prohibited patterns are present
    has_prohibited = category_counts.get("Prohibited / Illegal / Threat", 0) > 0

    if has_prohibited or risk_score >= 70:
        return "Critical" if risk_score >= 85 else "High", "🚫 Prohibited Content"
    elif risk_score >= 40:
        return "Medium", "⚠️ Potentially Harmful"
    elif risk_score >= 15:
        return "Low", "⚠️ Potentially Harmful"
    else:
        return "Safe", "✅ Safe Content"
