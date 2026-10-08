"""
Automated Unit Tests for DSA Algorithms & Hybrid Content Moderation Pipeline.
"""

import pytest
from algorithms import (
    naive_search,
    compute_lps_array,
    kmp_search,
    rabin_karp_search,
    AhoCorasick,
    randomized_spam_check,
    randomized_pattern_sample
)
from moderation.preprocessing import normalize_text, is_valid_word_boundary
from moderation.risk_scoring import calculate_risk_score, get_severity_level
from moderation.detector import HybridDetector


def test_naive_search():
    text = "the product works very well"
    pattern = "works"
    matches, comparisons, steps = naive_search(text, pattern)
    assert matches == [12]
    assert comparisons > 0
    assert len(steps) > 0


def test_kmp_lps_computation():
    pattern = "ababaca"
    lps, comparisons, steps = compute_lps_array(pattern)
    assert lps == [0, 0, 1, 2, 3, 0, 1]
    assert comparisons > 0


def test_kmp_search():
    text = "you are stupid and useless"
    pattern = "stupid"
    matches, comparisons, lps, steps = kmp_search(text, pattern)
    assert matches == [8]
    assert lps == [0, 0, 0, 0, 0, 0]


def test_rabin_karp_search():
    text = "hack account immediately and steal credit card"
    pattern = "hack account"
    matches, comparisons, spurious, logs = rabin_karp_search(text, pattern)
    assert matches == [0]
    assert len(logs) > 0


def test_aho_corasick():
    ac = AhoCorasick()
    ac.add_pattern("stupid", "Offensive")
    ac.add_pattern("kill yourself", "Harmful")
    ac.build_automaton()

    matches, transitions = ac.search("you are stupid and useless")
    patterns_found = [m['pattern'] for m in matches]
    assert "stupid" in patterns_found
    assert transitions > 0


def test_randomized_detection():
    # Test repetitive spam
    spam_text = "click click click click click click click click"
    is_spam, score, logs, rationale = randomized_spam_check(spam_text)
    assert is_spam is True
    assert score > 0.3

    # Test random window sampling
    long_text = "This is a long sample text to test Monte Carlo window sampling across the entire string."
    windows, explanation = randomized_pattern_sample(long_text, sample_count=3, window_size=10)
    assert len(windows) == 3
    assert "Monte Carlo" in explanation


def test_word_boundary_validation():
    text = "soldier diet soldier"
    # 'die' in 'diet' should NOT match as a standalone word
    assert is_valid_word_boundary(text, 9, 3) is False  # 'die' inside 'diet'
    # 'diet' as full word should match
    assert is_valid_word_boundary(text, 8, 4) is True


def test_hybrid_detector_safe_content():
    detector = HybridDetector()
    res = detector.analyze_text("This is a normal product review. The product works very well.")
    assert res["status_card"] == "✅ Safe Content"
    assert res["risk_score"] == 0
    assert res["severity"] == "Safe"


def test_hybrid_detector_potentially_harmful():
    detector = HybridDetector()
    res = detector.analyze_text("You are stupid and useless.")
    assert res["status_card"] in ["⚠️ Potentially Harmful", "🚫 Prohibited Content"]
    assert res["risk_score"] > 0
    assert len(res["matched_patterns"]) > 0


def test_hybrid_detector_prohibited():
    detector = HybridDetector()
    res = detector.analyze_text("Will hack account and steal credit card with malware payload!")
    assert res["status_card"] == "🚫 Prohibited Content"
    assert res["severity"] in ["High", "Critical"]
    assert res["risk_score"] >= 66
