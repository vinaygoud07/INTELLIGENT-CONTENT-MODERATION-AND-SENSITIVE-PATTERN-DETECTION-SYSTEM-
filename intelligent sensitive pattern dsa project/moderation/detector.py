"""
Hybrid Detection Engine.

Integrates 5 Core DSA Algorithms in a unified pipeline:
1. Text Preprocessing (normalization & boundary preservation)
2. Aho-Corasick Multi-Pattern Search (Primary fast candidate scanner)
3. KMP Search (Pattern index verification & LPS table analysis)
4. Rabin-Karp Rolling Hash Search (Hash verification & collision check)
5. Naive Search (Baseline comparison benchmark)
6. Randomized Detection (Monte Carlo sampling & spam repetition check)
7. Word Boundary Validation (False-positive elimination)
8. Transparent Risk Scoring (0-100 score & severity assignment)
"""

import time
from typing import List, Dict, Any

from algorithms import (
    naive_search,
    kmp_search,
    rabin_karp_search,
    AhoCorasick,
    randomized_spam_check,
    randomized_pattern_sample
)
from moderation.patterns import SENSITIVE_PATTERNS
from moderation.preprocessing import normalize_text, is_valid_word_boundary
from moderation.risk_scoring import calculate_risk_score


class HybridDetector:
    """Orchestrates multi-algorithm content moderation and analysis."""

    def __init__(self):
        # Pre-build Aho-Corasick Trie Automaton with sensitive patterns
        self.aho = AhoCorasick()
        self.pattern_map: Dict[str, Dict[str, Any]] = {}

        for item in SENSITIVE_PATTERNS:
            pat = item["pattern"].lower()
            cat = item["category"]
            self.aho.add_pattern(pat, cat)
            self.pattern_map[pat] = item

        self.aho.build_automaton()

    def analyze_text(self, raw_text: str) -> Dict[str, Any]:
        """
        Runs complete Hybrid Detection pipeline on raw input text.

        Returns comprehensive analysis payload containing moderation status,
        matched patterns, risk breakdown, and algorithm benchmark data.
        """
        start_total = time.perf_counter()

        # Step 1: Preprocessing
        normalized_text = normalize_text(raw_text)
        text_len = len(normalized_text)

        if text_len == 0:
            return {
                "raw_text": raw_text,
                "normalized_text": "",
                "status_card": "✅ Safe Content",
                "risk_score": 0,
                "severity": "Safe",
                "matched_patterns": [],
                "explanations": ["Input text is empty."],
                "algorithm_metrics": {},
                "visualizers": {},
                "total_execution_ms": 0.0
            }

        # Step 2: Aho-Corasick Multi-Pattern Search
        t0 = time.perf_counter()
        ac_matches_raw, ac_transitions = self.aho.search(normalized_text)
        t_ac = (time.perf_counter() - t0) * 1000.0

        # Filter candidates via word boundaries to avoid false positives
        verified_matches: List[Dict[str, Any]] = []
        unique_matched_patterns = set()

        for m in ac_matches_raw:
            pat = m['pattern']
            start_idx = m['start_index']
            if is_valid_word_boundary(normalized_text, start_idx, len(pat)):
                verified_matches.append({
                    'pattern': pat,
                    'category': m['category'],
                    'start_index': start_idx,
                    'end_index': m['end_index'],
                    'matched_text': m['matched_text'],
                    'severity': self.pattern_map.get(pat, {}).get('severity', 'Medium')
                })
                unique_matched_patterns.add(pat)

        # Candidate pattern list for secondary algorithm verifications
        candidate_patterns = list(unique_matched_patterns)
        if not candidate_patterns and len(SENSITIVE_PATTERNS) > 0:
            # If no matches, include a default pattern for algorithm comparison demo
            sample_demo_pattern = SENSITIVE_PATTERNS[0]["pattern"].lower()
        else:
            sample_demo_pattern = candidate_patterns[0] if candidate_patterns else "stupid"

        # Step 3: KMP Verification & LPS Array Computation
        t0 = time.perf_counter()
        kmp_total_matches = 0
        kmp_total_comparisons = 0
        kmp_sample_lps = []
        kmp_sample_steps = []

        for pat in (candidate_patterns if candidate_patterns else [sample_demo_pattern]):
            m_indices, k_comp, lps_arr, k_steps = kmp_search(normalized_text, pat)
            kmp_total_matches += len(m_indices)
            kmp_total_comparisons += k_comp
            if pat == sample_demo_pattern:
                kmp_sample_lps = lps_arr
                kmp_sample_steps = k_steps

        t_kmp = (time.perf_counter() - t0) * 1000.0

        # Step 4: Rabin-Karp Rolling Hash Verification
        t0 = time.perf_counter()
        rk_total_matches = 0
        rk_total_comparisons = 0
        rk_spurious_hits = 0
        rk_sample_logs = []

        for pat in (candidate_patterns if candidate_patterns else [sample_demo_pattern]):
            m_indices, rk_comp, spur_hits, rk_logs = rabin_karp_search(normalized_text, pat)
            rk_total_matches += len(m_indices)
            rk_total_comparisons += rk_comp
            rk_spurious_hits += spur_hits
            if pat == sample_demo_pattern:
                rk_sample_logs = rk_logs

        t_rk = (time.perf_counter() - t0) * 1000.0

        # Step 5: Naive Search Baseline Benchmark
        t0 = time.perf_counter()
        naive_total_matches = 0
        naive_total_comparisons = 0
        for pat in (candidate_patterns if candidate_patterns else [sample_demo_pattern]):
            m_indices, n_comp, _ = naive_search(normalized_text, pat)
            naive_total_matches += len(m_indices)
            naive_total_comparisons += n_comp
        t_naive = (time.perf_counter() - t0) * 1000.0

        # Step 6: Randomized Algorithm Spam Check & Monte Carlo Sampling
        t0 = time.perf_counter()
        is_spam, spam_score, spam_logs, spam_rationale = randomized_spam_check(normalized_text)
        sampled_windows, sample_explanation = randomized_pattern_sample(normalized_text)
        t_rand = (time.perf_counter() - t0) * 1000.0

        # Step 7: Risk Scoring & Moderation Status Calculation
        risk_score, severity, status_card, explanations = calculate_risk_score(
            verified_matches, spam_score, text_len
        )

        total_execution_ms = (time.perf_counter() - start_total) * 1000.0

        # Build comprehensive output payload
        return {
            "raw_text": raw_text,
            "normalized_text": normalized_text,
            "status_card": status_card,
            "risk_score": risk_score,
            "severity": severity,
            "matched_patterns": verified_matches,
            "unique_patterns_count": len(unique_matched_patterns),
            "explanations": explanations,
            "spam_info": {
                "is_spam": is_spam,
                "spam_score": spam_score,
                "rationale": spam_rationale,
                "sampled_windows": sampled_windows,
                "sample_explanation": sample_explanation
            },
            "algorithm_metrics": {
                "Naive Search": {
                    "time_ms": round(t_naive, 4),
                    "comparisons": naive_total_comparisons,
                    "matches_found": naive_total_matches,
                    "complexity": "O(N * M)"
                },
                "KMP": {
                    "time_ms": round(t_kmp, 4),
                    "comparisons": kmp_total_comparisons,
                    "matches_found": kmp_total_matches,
                    "complexity": "O(N + M)"
                },
                "Rabin-Karp": {
                    "time_ms": round(t_rk, 4),
                    "comparisons": rk_total_comparisons,
                    "spurious_hits": rk_spurious_hits,
                    "matches_found": rk_total_matches,
                    "complexity": "O(N + M) avg"
                },
                "Aho-Corasick": {
                    "time_ms": round(t_ac, 4),
                    "comparisons": ac_transitions,
                    "matches_found": len(ac_matches_raw),
                    "complexity": "O(N + sum(M))"
                },
                "Randomized Detection": {
                    "time_ms": round(t_rand, 4),
                    "comparisons": len(sampled_windows),
                    "matches_found": 1 if is_spam else 0,
                    "complexity": "O(k * W) Monte Carlo"
                }
            },
            "visualizers": {
                "demo_pattern": sample_demo_pattern,
                "kmp_lps": kmp_sample_lps,
                "kmp_steps": kmp_sample_steps[:15],  # Top 15 steps for clear UI display
                "rabin_karp_logs": rk_sample_logs[:15],
                "aho_corasick_trie": self.aho.get_trie_structure()
            },
            "total_execution_ms": round(total_execution_ms, 3)
        }
