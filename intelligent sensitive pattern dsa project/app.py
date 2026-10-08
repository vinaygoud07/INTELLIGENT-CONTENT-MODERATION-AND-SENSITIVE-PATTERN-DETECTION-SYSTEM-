"""
Intelligent Content Moderation & Sensitive Pattern Detection System
Interactive Streamlit Web Application (DSA Project)
"""

import streamlit as st
import pandas as pd
import time
from moderation import HybridDetector
from utils import format_metric_table

# Page Configuration
st.set_page_config(
    page_title="Intelligent Content Moderation (DSA Project)",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.3rem;
        font-weight: 800;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.1rem;
        text-align: center;
        color: #555555;
        margin-bottom: 25px;
    }
    .status-card-safe {
        background-color: #E8F5E9;
        border-left: 6px solid #2E7D32;
        padding: 20px;
        border-radius: 10px;
        color: #1B5E20;
        text-align: center;
        font-size: 1.8rem;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .status-card-warning {
        background-color: #FFFDE7;
        border-left: 6px solid #FBC02D;
        padding: 20px;
        border-radius: 10px;
        color: #F57F17;
        text-align: center;
        font-size: 1.8rem;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .status-card-prohibited {
        background-color: #FFEBEE;
        border-left: 6px solid #C62828;
        padding: 20px;
        border-radius: 10px;
        color: #B71C1C;
        text-align: center;
        font-size: 1.8rem;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .alg-badge {
        background-color: #E3F2FD;
        color: #0D47A1;
        padding: 4px 10px;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 5px;
        display: inline-block;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_detector():
    """Instantiates and caches the Hybrid Detection Engine."""
    return HybridDetector()


detector = load_detector()

# Header
st.markdown("<h1 class='main-header'>🛡️ Intelligent Content Moderation & Sensitive Pattern Detection</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Powered by Data Structures & Algorithms: <b>Naive Search, KMP, Rabin-Karp, Aho-Corasick & Randomized Monte Carlo</b></p>", unsafe_allow_html=True)

# Sidebar - Project Metadata & DSA Viva Quick Sheet
with st.sidebar:
    st.header("📌 DSA Project Overview")
    st.markdown("""
    **Project Title:**  
    Intelligent Content Moderation System

    **Core Algorithms Implemented:**
    1. **Naive Search**: Brute force string matching (`O(N*M)`)
    2. **KMP Algorithm**: LPS array non-backtracking search (`O(N+M)`)
    3. **Rabin-Karp**: Rolling hash pattern matching (`O(N+M) avg`)
    4. **Aho-Corasick**: Trie + failure link automaton (`O(N + ΣM)`)
    5. **Randomized Algorithm**: Monte Carlo window sampling & universal hashing

    ---
    **System Features:**
    - Zero Black-Box ML Dependencies
    - Manual Python DSA Implementations
    - Real-Time Execution Benchmarks
    - Step-by-Step Algorithm Visualizer
    """)

# Main Interactive UI
st.subheader("📝 Input Text to Analyze")

# Preset Examples
col_ex1, col_ex2, col_ex3, col_ex4 = st.columns(4)

preset_text = ""
if col_ex1.button("Example 1: Safe Content"):
    preset_text = "This is a normal product review. The product works very well."
if col_ex2.button("Example 2: Offensive Text"):
    preset_text = "You are stupid and useless."
if col_ex3.button("Example 3: Prohibited Threat"):
    preset_text = "Will hack account and steal credit card with malware payload!"
if col_ex4.button("Example 4: Spam / Repetition"):
    preset_text = "Click here now! Free money guaranteed prize click here now buy followers free money click here now!"

user_input = st.text_area(
    "Enter text/comment/review to analyze:",
    value=preset_text if preset_text else "",
    height=120,
    placeholder="Type or paste any comment here..."
)

analyze_button = st.button("🔍 Analyze Content", type="primary", use_container_width=True)

if analyze_button or user_input:
    if not user_input.strip():
        st.warning("⚠️ Please enter some text to analyze.")
    else:
        results = detector.analyze_text(user_input)

        st.markdown("---")
        st.subheader("🎯 Moderation Result")

        card_class = "status-card-safe"
        if results["status_card"] == "⚠️ Potentially Harmful":
            card_class = "status-card-warning"
        elif results["status_card"] == "🚫 Prohibited Content":
            card_class = "status-card-prohibited"

        st.markdown(f"<div class='{card_class}'>{results['status_card']}</div>", unsafe_allow_html=True)

        # Metric Columns
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)

        with m_col1:
            st.metric(label="Risk Score", value=f"{results['risk_score']} / 100")
            st.progress(results['risk_score'] / 100.0)

        with m_col2:
            st.metric(label="Severity Level", value=results['severity'])

        with m_col3:
            st.metric(label="Matched Sensitive Patterns", value=results['unique_patterns_count'])

        with m_col4:
            st.metric(label="Total Execution Time", value=f"{results['total_execution_ms']} ms")

        # Flag Explanations & Matched Patterns
        exp_col, pat_col = st.columns([1, 1])

        with exp_col:
            st.markdown("### 🔍 Why Content Was Flagged")
            for exp in results["explanations"]:
                st.write(f"- {exp}")

            if results["spam_info"]["is_spam"]:
                st.warning(f"⚠️ **Spam Alert:** {results['spam_info']['rationale']}")

        with pat_col:
            st.markdown("### 🏷️ Matched Sensitive Patterns")
            matched_list = results["matched_patterns"]

            if not matched_list:
                st.success("No prohibited or sensitive words detected in text.")
            else:
                pat_data = []
                for m in matched_list:
                    pat_data.append({
                        "Pattern": m["pattern"],
                        "Category": m["category"],
                        "Severity": m["severity"],
                        "Index Range": f"{m['start_index']} - {m['end_index']}"
                    })
                df_pat = pd.DataFrame(pat_data)
                st.dataframe(df_pat, use_container_width=True)

        st.markdown("### ⚙️ Algorithms Used in Hybrid Detection")
        st.markdown("""
        <span class='alg-badge'>Aho-Corasick Multi-Pattern Search</span>
        <span class='alg-badge'>KMP Non-Backtracking Verification</span>
        <span class='alg-badge'>Rabin-Karp Rolling Hash Verification</span>
        <span class='alg-badge'>Randomized Sub-window Monte Carlo</span>
        <span class='alg-badge'>Naive Search Baseline</span>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Algorithm Analysis & DSA Visualizer Tabs
        st.header("📊 Algorithm Analysis & Interactive DSA Visualizer")

        tab_perf, tab_kmp, tab_rk, tab_ac, tab_rand = st.tabs([
            "⚡ Performance Benchmark",
            "🧩 KMP LPS Visualizer",
            "🔢 Rabin-Karp Hash Log",
            "🌲 Aho-Corasick Automaton",
            "🎲 Randomized Monte Carlo"
        ])

        # Tab 1: Performance Benchmark
        with tab_perf:
            st.markdown("#### Real-Time Execution Metrics & Comparisons")
            df_metrics = format_metric_table(results["algorithm_metrics"])
            st.dataframe(df_metrics, use_container_width=True)

            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Execution Time Comparison (ms)**")
                st.bar_chart(df_metrics.set_index("Algorithm")["Execution Time (ms)"])

            with c2:
                st.markdown("**Character Comparisons / Step Operations**")
                st.bar_chart(df_metrics.set_index("Algorithm")["Comparisons / Steps"])

        # Tab 2: KMP Visualizer
        with tab_kmp:
            st.markdown(f"#### KMP Longest Prefix Suffix (LPS) Array Analysis")
            demo_pat = results["visualizers"]["demo_pattern"]
            lps_arr = results["visualizers"]["kmp_lps"]
            st.write(f"**Inspected Pattern:** `{demo_pat}`")

            if lps_arr:
                # Format LPS table
                lps_data = {"Index": list(range(len(demo_pat))), "Character": list(demo_pat), "LPS Value": lps_arr}
                st.table(pd.DataFrame(lps_data).T)

            st.markdown("#### KMP Search Execution Steps")
            steps = results["visualizers"]["kmp_steps"]
            if steps:
                df_steps = pd.DataFrame(steps)
                st.dataframe(df_steps, use_container_width=True)

        # Tab 3: Rabin-Karp Visualizer
        with tab_rk:
            st.markdown("#### Rabin-Karp Rolling Hash Log")
            demo_pat = results["visualizers"]["demo_pattern"]
            st.write(f"**Inspected Pattern:** `{demo_pat}`")

            rk_logs = results["visualizers"]["rabin_karp_logs"]
            if rk_logs:
                df_rk = pd.DataFrame(rk_logs)
                st.dataframe(df_rk, use_container_width=True)
                st.info("💡 **Key Insight:** When `pattern_hash == text_hash`, exact character matching is performed to verify whether it is a true match or a hash collision (spurious hit).")

        # Tab 4: Aho-Corasick Automaton
        with tab_ac:
            st.markdown("#### Aho-Corasick Trie & Automaton Overview")
            ac_info = results["visualizers"]["aho_corasick_trie"]
            col_t1, col_t2 = st.columns(2)
            col_t1.metric("Total Automaton Nodes", ac_info["total_nodes"])
            col_t2.metric("Total Preloaded Patterns", ac_info["total_patterns"])

            st.markdown("#### Trie Node Inspector")
            df_nodes = pd.DataFrame(ac_info["nodes"])
            st.dataframe(df_nodes.head(20), use_container_width=True)

        # Tab 5: Randomized Monte Carlo
        with tab_rand:
            st.markdown("#### Randomized Sub-Window Sampling")
            spam_data = results["spam_info"]
            st.write(f"**Rationale:** {spam_data['sample_explanation']}")

            sampled_win = spam_data["sampled_windows"]
            if sampled_win:
                st.markdown("#### Sampled Windows & Universal Prime Hash Logs")
                st.dataframe(pd.DataFrame(sampled_win), use_container_width=True)

        # Viva Reference Section
        with st.expander("📚 College Viva & DSA Theoretical Reference"):
            st.markdown("""
            ### Algorithm Comparison Matrix

            | Algorithm | Time Complexity (Best) | Time Complexity (Worst) | Auxiliary Space | Key Advantage |
            | :--- | :--- | :--- | :--- | :--- |
            | **Naive Search** | $O(N)$ | $O((N-M+1) \cdot M)$ | $O(1)$ | Simple implementation, no preprocessing. |
            | **KMP Algorithm** | $O(N + M)$ | $O(N + M)$ | $O(M)$ | Zero backtracking in text pointer using LPS array. |
            | **Rabin-Karp** | $O(N + M)$ | $O(N \cdot M)$ | $O(1)$ | $O(1)$ sliding window hash comparison. |
            | **Aho-Corasick** | $O(N + \Sigma M)$ | $O(N + \Sigma M)$ | $O(\Sigma M)$ | Single-pass search for thousands of patterns simultaneously. |
            | **Randomized Detection** | $O(k \cdot W)$ | $O(k \cdot W)$ | $O(k)$ | Fast sub-linear checking for spam in large texts. |

            ---
            ### Common Viva Questions & Answers

            **Q1: Why build Aho-Corasick when KMP is already $O(N+M)$?**  
            *A:* KMP is designed for searching a single pattern of length $M$ in text $N$. If you have $K$ patterns, running KMP $K$ times takes $O(K \cdot (N+M))$. Aho-Corasick constructs a Trie with failure links, enabling searching for ALL $K$ patterns simultaneously in a single pass over the text in $O(N + \text{total pattern length})$.

            **Q2: What is the purpose of the LPS array in KMP?**  
            *A:* The Longest Prefix Suffix (LPS) array stores the length of the longest proper prefix of `pattern[0..i]` that is also a suffix of `pattern[0..i]`. On a character mismatch, it tells us how many characters can be safely skipped without re-evaluating text characters.

            **Q3: How does Rabin-Karp handle Hash Collisions (Spurious Hits)?**  
            *A:* Since different strings can hash to the same value (modulo arithmetic), when Rabin-Karp detects `pattern_hash == window_hash`, it performs an explicit character-by-character string comparison to confirm a true match.

            **Q4: Where and why is Randomization applied in this system?**  
            *A:* Randomization is used in (1) Monte Carlo sub-window sampling to inspect long texts for repetitive spam without scanning every single byte, and (2) Universal hashing with randomly selected prime modulos to prevent adversarial inputs from forcing worst-case hash collisions.
            """)
