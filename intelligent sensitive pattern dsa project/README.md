# 🛡️ Intelligent Content Moderation and Sensitive Pattern Detection System

A complete Data Structures and Algorithms (DSA) project built with **Python** and **Streamlit**.

This application analyzes user-submitted text (comments, reviews, messages) for offensive language, harmful/abusive content, prohibited threats, and spam-like repetitions using a **Hybrid Detection Engine** powered by 5 manually implemented algorithms.

---

## 📌 Project Overview & Problem Statement

With the rapid growth of user-generated content on internet platforms, real-time automated content moderation is critical. While modern Deep Learning / LLM black-box models exist, they are computationally heavy, non-deterministic, and lack transparent mechanical explanations.

This project demonstrates how classical **Data Structures & Algorithms (DSA)** can be combined into a high-performance, deterministic, zero-black-box **Hybrid Detection Pipeline** capable of sub-millisecond pattern search and detailed risk assessment.

---

## 🎯 Key Objectives

1. **Manual Algorithm Implementation**: Implement core pattern matching algorithms from scratch without relying on external string-search library functions (`flashtext`, `re.finditer` for core search).
2. **Multi-Algorithm Hybrid Pipeline**: Chain Aho-Corasick, KMP, Rabin-Karp, Naive Search, and Randomized Sampling into a unified detection engine.
3. **Transparent Risk Scoring**: Compute a clear 0–100 risk score and categorize severity (`Safe`, `Low`, `Medium`, `High`, `Critical`).
4. **Educational Visualization**: Expose step-by-step internal states (KMP LPS array, Rabin-Karp rolling hashes, Aho-Corasick Trie structure, Monte Carlo sampling).
5. **College Viva Readiness**: Serve as a demonstration-ready DSA project with real-time benchmarks and theoretical matrix tables.

---

## 🚀 Key Features

* **Instant Text Analysis**: Paste or type text and click 🔍 **Analyze Content**.
* **Presets Buttons**: Quick test buttons for Safe Reviews, Offensive Text, Prohibited Threats, and Spam.
* **Moderation Status Card**: Clean status indicators (✅ SAFE, ⚠️ POTENTIALLY HARMFUL, 🚫 PROHIBITED).
* **Detailed Flagging Rationale**: Explains *why* content received its risk score and matched categories.
* **False-Positive Prevention**: Intelligent word-boundary verification (e.g. matching "die" while clearing "diet").
* **Interactive Algorithm Analysis Tab**: Real-time charts comparing execution times and character comparisons.
* **Step-by-Step DSA Visualizers**:
  * **KMP LPS Array Table** & transition step log.
  * **Rabin-Karp Rolling Hash Viewer** (pattern hash vs text window hashes & collision counter).
  * **Aho-Corasick Automaton Inspector** (nodes, failure links, output states).
  * **Randomized Sub-Window Inspector** (random prime modulo hash sampling).

---

## 🧠 DSA Algorithms Implemented

### 1. Naive String Matching Algorithm
* **Concept**: Slides the pattern window over the text one character at a time, comparing characters until a match or mismatch occurs.
* **Time Complexity**:
  * Worst Case: $O((N - M + 1) \cdot M)$
  * Best Case: $O(N)$
* **Space Complexity**: $O(1)$ auxiliary space.

### 2. Knuth-Morris-Pratt (KMP) Algorithm
* **Concept**: Precomputes a Longest Prefix Suffix (LPS / $\pi$) array. When a mismatch occurs, it skips redundant character comparisons without rewinding the text pointer $i$.
* **Time Complexity**:
  * Preprocessing: $O(M)$
  * Matching Phase: $O(N)$
  * Total: $O(N + M)$
* **Space Complexity**: $O(M)$ auxiliary space for LPS array.

### 3. Rabin-Karp Rolling Hash Algorithm
* **Concept**: Converts pattern matching into numeric hash comparison using polynomial rolling hashing ($Hash_{new} = (Base \cdot (Hash_{old} - char_{out} \cdot h) + char_{in}) \pmod{Prime}$).
* **Time Complexity**:
  * Average / Best Case: $O(N + M)$
  * Worst Case: $O(N \cdot M)$ (under heavy hash collisions)
* **Space Complexity**: $O(1)$ auxiliary space.

### 4. Aho-Corasick Multi-Pattern Search Algorithm
* **Concept**: Constructs a Finite State Automaton combining a Trie with BFS-constructed Failure Links. Enables searching for thousands of sensitive patterns simultaneously in a single pass over the text.
* **Time Complexity**:
  * Construction: $O(\sum M_i)$
  * Searching: $O(N + Z)$ where $Z$ is total pattern occurrences.
* **Space Complexity**: $O(\sum M_i \cdot \Sigma)$ where $\Sigma$ is alphabet size.

### 5. Randomized Algorithm (Monte Carlo Sampling & Universal Hashing)
* **Concept**: Applies non-deterministic random sampling to check long text for repetitive spam patterns ($O(k \cdot W)$ instead of $O(N)$), and uses universal hashing with random prime seeds to prevent adversarial collision attacks.
* **Time Complexity**: $O(k \cdot W)$ where $k$ is sample count, $W$ is window size.
* **Space Complexity**: $O(k)$ auxiliary space.

---

## 📊 Algorithm Complexity Summary Table

| Algorithm | Preprocessing Time | Search Time (Best) | Search Time (Worst) | Auxiliary Space | Use Case |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Naive Search** | $O(1)$ | $O(N)$ | $O(N \cdot M)$ | $O(1)$ | Simple baseline check |
| **KMP** | $O(M)$ | $O(N + M)$ | $O(N + M)$ | $O(M)$ | Single pattern search |
| **Rabin-Karp** | $O(M)$ | $O(N + M)$ | $O(N \cdot M)$ | $O(1)$ | Substring search & plagiarism detection |
| **Aho-Corasick** | $O(\sum M)$ | $O(N)$ | $O(N + Z)$ | $O(\sum M)$ | Multi-pattern dictionary search |
| **Randomized** | $O(1)$ | $O(k \cdot W)$ | $O(k \cdot W)$ | $O(k)$ | High-speed spam detection on large texts |

---

## 🏗️ System Architecture & Hybrid Pipeline

```
              ┌───────────────────────────┐
              │      Raw User Input       │
              └─────────────┬─────────────┘
                            │
                            ▼
              ┌───────────────────────────┐
              │    Text Preprocessing     │
              │  (Lowercase, Normalize)   │
              └─────────────┬─────────────┘
                            │
                            ▼
              ┌───────────────────────────┐
              │  Aho-Corasick Multi-Search│
              │   (Fast Candidate Scan)   │
              └─────────────┬─────────────┘
                            │
                            ▼
              ┌───────────────────────────┐
              │ KMP Non-Backtrack Verify  │
              │    (LPS Array Analysis)   │
              └─────────────┬─────────────┘
                            │
                            ▼
              ┌───────────────────────────┐
              │ Rabin-Karp Hash Verify    │
              │  (Rolling Hash & Collision│
              │        Verification)      │
              └─────────────┬─────────────┘
                            │
                            ▼
              ┌───────────────────────────┐
              │  Randomized Spam Check    │
              │ (Monte Carlo Sampling)    │
              └─────────────┬─────────────┘
                            │
                            ▼
              ┌───────────────────────────┐
              │   Risk Scoring Engine     │
              │   (Score 0-100 & Severity)│
              └─────────────┬─────────────┘
                            │
                            ▼
              ┌───────────────────────────┐
              │  Streamlit UI Output Card │
              │(✅ SAFE / ⚠️ HARMFUL / 🚫) │
              └───────────────────────────┘
```

---

## 📁 Project Directory Structure

```
intelligent_content_moderation/
│
├── app.py                      # Streamlit interactive web interface
├── requirements.txt            # Python dependencies
├── README.md                   # Comprehensive documentation & Viva guide
│
├── algorithms/                 # Core Manual DSA Implementations
│   ├── __init__.py
│   ├── naive_search.py          # Naive brute-force string search
│   ├── kmp.py                   # Knuth-Morris-Pratt algorithm & LPS table
│   ├── rabin_karp.py            # Rabin-Karp rolling hash pattern search
│   ├── aho_corasick.py          # Aho-Corasick Trie & failure links automaton
│   └── randomized_detection.py  # Monte Carlo sampling & universal prime hashing
│
├── moderation/                 # Moderation Pipeline & Scoring
│   ├── __init__.py
│   ├── patterns.py             # Categorized sensitive pattern dataset
│   ├── preprocessing.py        # Text cleaning & word boundary validation
│   ├── risk_scoring.py         # 0-100 risk score & severity rating
│   └── detector.py             # Hybrid Detection Engine orchestrator
│
├── utils/                      # Benchmarking Helpers
│   ├── __init__.py
│   └── performance.py          # DataFrame converter for Streamlit display
│
└── tests/                      # Automated Unit Test Suite
    ├── __init__.py
    └── test_algorithms.py      # Unit tests for all algorithms & modules
```

---

## 💻 Installation & Usage

### Prerequisites
* Python 3.8+ installed on your system.

### Step 1: Clone or Open Directory
Navigate to the project folder:
```bash
cd "c:/Users/dappu/OneDrive/Desktop/intelligent sensitive pattern dsa project"
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run Unit Tests
Validate that all DSA algorithms pass automated unit tests:
```bash
pytest tests/test_algorithms.py
```

### Step 4: Launch Web Application
```bash
streamlit run app.py
```
A browser tab will automatically open at `http://localhost:8501`.

---

## 🧪 Example Inputs & Expected Outputs

### Example 1: Safe Review
* **Input**: `"This is a normal product review. The product works very well."`
* **Status**: `✅ Safe Content`
* **Risk Score**: `0 / 100` | **Severity**: `Safe`
* **Matched Patterns**: `0`

### Example 2: Offensive Text
* **Input**: `"You are stupid and useless."`
* **Status**: `⚠️ Potentially Harmful`
* **Risk Score**: `42 / 100` | **Severity**: `Medium`
* **Matched Patterns**: `stupid`, `useless` (Offensive category)

### Example 3: Prohibited Threat
* **Input**: `"Will hack account and steal credit card with malware payload!"`
* **Status**: `🚫 Prohibited Content`
* **Risk Score**: `95 / 100` | **Severity**: `Critical`
* **Matched Patterns**: `hack account`, `steal credit card`, `malware payload`

### Example 4: Spam / Repetitive
* **Input**: `"Click here now! Free money guaranteed prize click here now buy followers free money!"`
* **Status**: `⚠️ Potentially Harmful`
* **Risk Score**: `54 / 100` | **Severity**: `Medium`
* **Matched Patterns**: `click here now`, `free money`, `guaranteed prize` + Spam Flag

---

## 🎓 Viva Questions & Answers

1. **Q: Why combine multiple algorithms into a Hybrid Engine instead of using just one?**  
   *A:* Each algorithm excels in different scenarios. Aho-Corasick quickly scans text for thousands of patterns in a single pass. KMP provides exact non-backtracking verification and LPS array analysis. Rabin-Karp validates rolling hashes and checks collisions. Randomized Monte Carlo sampling rapidly handles long repetitive text without scanning every byte.

2. **Q: What is a Spurious Hit in Rabin-Karp?**  
   *A:* A spurious hit occurs when two different strings produce the same hash value due to modulo arithmetic. When `pattern_hash == window_hash`, the algorithm must verify exact character equality to confirm if it is a real match or a spurious hit.

3. **Q: How does word boundary validation prevent false positives?**  
   *A:* Before confirming a pattern match (e.g. "die"), the system checks whether the character immediately to the left and right are alphanumeric. If surrounded by letters (e.g. "diet" or "soldier"), the match is rejected.

---

## 🔮 Future Improvements

1. **Graph-based Trie Visualizer**: Render dynamic D3.js or PyVis interactive network diagrams of the Aho-Corasick Trie in Streamlit.
2. **Elasticsearch / Indexing Integration**: Add persistent inverted index search for multi-gigabyte log moderation.
3. **Levensthein Distance / Fuzzy Matching**: Extend algorithms with Dynamic Programming to detect obfuscated words (e.g., "st*pid", "h@ck").
