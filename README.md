# DSA for AI and ML Engineers - Canonical Labs, Interactive UI and Test Suite

[![Tests](https://img.shields.io/badge/pytest-167%20passed-brightgreen.svg)](tests/)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](pyproject.toml)
[![Next.js](https://img.shields.io/badge/next.js-16.3-black.svg)](dsa-practice-ui/)
[![TypeScript](https://img.shields.io/badge/typescript-5.0-blue.svg)](dsa-practice-ui/)
[![Tailwind](https://img.shields.io/badge/tailwind-v4-38bdf8.svg)](dsa-practice-ui/)

The official laboratory, interactive code playground, and testing suite for **DSA for AI & ML Engineers: From Data Structures to Scalable AI Systems**.

This repository bridges classical algorithmic problem solving with real-world AI infrastructure. It provides **33 structured chapters**, **150 NeetCode interview companion solutions**, **167 automated unit tests**, and a **Next.js & Monaco Editor interactive LeetCode practice platform** with live Python execution.

---

## Table of Contents

1. [Repository Architecture](#repository-architecture)
2. [Complete Chapter Index (Chapters 01-33)](#complete-chapter-index-chapters-01-33)
3. [Chapter 33: NeetCode 150 Interview Companion](#chapter-33-neetcode-150-interview-companion)
4. [Interactive Practice UI (dsa-practice-ui)](#interactive-practice-ui-dsa-practice-ui)
   - [UI Features & Layout](#ui-features--layout)
   - [Adaptive Challenge Countdown Timer](#adaptive-challenge-countdown-timer)
   - [Monaco Python Code Editor](#monaco-python-code-editor)
   - [Safe Subprocess Execution Engine](#safe-subprocess-execution-engine)
   - [Component Architecture](#component-architecture)
   - [Quickstart Guide](#quickstart-guide)
5. [Automated Unit Testing & Pytest Suite](#automated-unit-testing--pytest-suite)
6. [5-Step DSA Engineering Framework](#5-step-dsa-engineering-framework)
7. [Installation and Setup](#installation-and-setup)
8. [Code Standards and Verification](#code-standards-and-verification)

---

## Repository Architecture

```
dsa-ai-engineer-labs/
|-- .gitignore                   # Universal ignore for Python, virtual envs, and Next.js builds
|-- pyproject.toml               # Configured with pythonpath = ["."] for frictionless pytest
|-- README.md                    # Unified repository documentation
|-- dsa_labs/                    # Canonical implementations and algorithmic solutions
|   |-- chapter_01/ ...          # Chapters 01 to 32: Core Foundations & AI Primitives
|   `-- chapter_33/              # Chapter 33: NeetCode 150 Companion (18 algorithmic modules)
|       |-- arrays_and_hashing.py
|       |-- two_pointers.py
|       |-- sliding_window.py
|       |-- stack.py
|       |-- binary_search.py
|       |-- linked_list.py
|       |-- trees.py
|       |-- tries.py
|       |-- heap.py
|       |-- backtracking.py
|       |-- graphs.py
|       |-- advanced_graphs.py
|       |-- one_d_dp.py
|       |-- two_d_dp.py
|       |-- greedy.py
|       |-- intervals.py
|       |-- math_and_geometry.py
|       `-- bit_manipulation.py
|-- tests/                       # 167 automated unit tests across all 33 chapters
|   |-- test_chapter_01.py ...
|   `-- test_chapter_33.py       # Comprehensive 57-case test suite covering all 150 problems
`-- dsa-practice-ui/             # LeetCode-style interactive practice web platform
    |-- .gitignore               # UI build ignore (node_modules, .next, cache)
    |-- README.md                # UI subfolder reference pointing to main documentation
    |-- package.json             # Next.js 16 + React 19 + Tailwind v4 + Monaco Editor
    |-- app/
    |   |-- api/run/route.ts     # Python sandbox runner endpoint with safety timeouts
    |   |-- globals.css          # Tailwind CSS v4 & custom LeetCode scrollbars
    |   |-- layout.tsx           # Root layout with dark mode metadata
    |   `-- page.tsx             # Split-pane workspace with keyboard shortcuts
    |-- components/
    |   |-- CodeEditor.tsx       # Monaco Editor with Python 3 syntax highlighting
    |   |-- CountdownTimer.tsx   # Adaptive skill-based challenge timer (Beginner / Med / Adv)
    |   |-- ConsoleTabs.tsx      # Case 1..3 inputs and visual result status pills
    |   |-- ProblemDescription.tsx # Description, constraints, and 5-step editorial
    |   `-- ProblemModal.tsx     # 150-problem search & category filter drawer
    `-- lib/
        |-- runner.py            # Python evaluation engine with semantic Two Sum verification
        |-- problems.ts          # Problem lookup helpers and category metadata
        |-- problems.json        # Complete dataset with starter templates & editorials
        `-- types.ts             # TypeScript interfaces for problems, testcases, and results
```

---

## Complete Chapter Index (Chapters 01-33)

| Chapter | Topic & Focus | Core Module (`dsa_labs/`) | Key Algorithms & Structures |
| :---: | :--- | :--- | :--- |
| **01** | Prep Scheduler & Spaced Repetition | `chapter_01/prep_scheduler.py` | Leitner review intervals, priority scheduling |
| **02** | Asymptotic Complexity Prober | `chapter_02/complexity_probe.py` | Empirical scaling detection, slope classification |
| **03** | Vector Toolkit & Cosine Top-K | `chapter_03/vector_toolkit.py` | L2 normalization, vectorized dot product, top-k |
| **04** | LLM Sequence Batching & Arrays | `chapter_04/batching.py` | Length-bucket batcher, in-place array algorithms |
| **05** | Context Budget & Prefix Sums | `chapter_05/context_budget.py` | Prefix sums, turn budget planning, 2D matrix sums |
| **06** | Rolling Windows & Two Pointers | `chapter_06/rolling_window.py` | Streaming window decision engines, palindrome two-pointer |
| **07** | Deduplication & Hash Indexes | `chapter_07/dedup.py` | Exact deduplicator, hash sets, bucket chaining |
| **08** | Linked Lists & KV Cache Allocation | `chapter_08/linked.py` | Doubly-linked nodes, cycle detection, k-group reversal |
| **09** | Request Queues & Monotonic Stacks | `chapter_09/request_queue.py` | Monotonic stack, bounded queues, histogram areas |
| **10** | Hierarchical Tree Indexing | `chapter_10/hierarchical_index.py` | Hierarchical vector space partitioning, tree traversal |
| **11** | Priority Queues & Beam Search | `chapter_11/beam_search.py` | Min/max heaps, top-k beam decoding for LLMs |
| **12** | Vocabulary Tries for Tokenization | `chapter_12/vocab_trie.py` | Prefix matching, wildcard token dictionaries |
| **13** | Disjoint Sets & Graph Clusters | `chapter_13/dedup_clusters.py` | Union-Find with rank and path compression |
| **14** | External Sorting for Large Corpora | `chapter_14/external_sort.py` | K-way external merge sort, chunked file processing |
| **15** | Binary Search & Calibration | `chapter_15/threshold_search.py` | Logarithmic search, probability threshold tuning |
| **16** | Interval Scheduling & Compute Slots | `chapter_16/slot_scheduler.py` | Interval intersections, non-overlapping slot allocation |
| **17** | Divide & Conquer Tree Reductions | `chapter_17/tree_reduce.py` | Parallel tensor tree reduction, fast exponentiation |
| **18** | Backtracking & Constraint Search | `chapter_18/constraint_search.py` | Bounded prompt constraint exploration, N-Queens |
| **19** | Greedy Context Packing | `chapter_19/context_packing.py` | Knapsack approximations, greedy window chunking |
| **20** | Dynamic Programming & Tokenizer | `chapter_20/viterbi_tokenizer.py` | Viterbi path decoding, unigram token probability DP |
| **21** | Bit Manipulation & Quantization | `chapter_21/quantization.py` | Int8/Int4 fixed-point scaling, bitmask SIMD tricks |
| **22** | Workflow Graphs & Traversal | `chapter_22/workflow_graph.py` | Breadth-First & Depth-First agent step dispatch |
| **23** | DAG Pipeline Execution | `chapter_23/dag_executor.py` | Topological sort, dependency resolution, concurrency |
| **24** | String Matching & Near-Duplicates | `chapter_24/near_duplicates.py` | Rabin-Karp polynomial rolling hash, MinHash shingles |
| **25** | Fenwick Trees & Weighted Sampling | `chapter_25/weighted_sampler.py` | Binary Indexed Trees (BIT), prefix probability sampler |
| **26** | Streaming Summaries & HyperLogLog | `chapter_26/stream_summary.py` | HyperLogLog cardinalities, reservoir stream sampling |
| **27** | Mathematical ML Primitives | `chapter_27/ml_primitives.py` | Sigmoid, Logistic Regression, Scaled Dot-Product Attention |
| **28** | Vector Search: NSW & HNSW | `chapter_28/ann_index.py` | Navigable Small World vector graphs, ANN lookups |
| **29** | Semantic Inference Cache & Rate Limits | `chapter_29/inference_cache.py` | Vector-similarity caching, Token Bucket rate limiting |
| **30** | Pattern Triage & Signal Matcher | `chapter_30/triage.py` | Problem taxonomy mapping, algorithmic signal extractor |
| **31** | Interview Protocol & Telemetry | `chapter_31/protocol.py` | Live interview stage rubrics, time-boxed milestones |
| **32** | AI Engineering Rubric & Reporting | `chapter_32/rubric.py` | Multi-dimensional scoring (Correctness, Scale, ML) |
| **33** | **NeetCode 150 Companion** | `chapter_33/` (18 modules) | Complete 150 LeetCode solutions with 5-step framework |

---

## Chapter 33: NeetCode 150 Interview Companion

All 150 problems are implemented under `dsa_labs/chapter_33/` with clean typing, comprehensive docstrings, and in-depth inline explanations:

| Algorithmic Domain | Module | Problems Solved |
| :--- | :--- | :---: |
| **1. Arrays & Hashing** | `arrays_and_hashing.py` | 9 |
| **2. Two Pointers** | `two_pointers.py` | 5 |
| **3. Sliding Window** | `sliding_window.py` | 6 |
| **4. Stack** | `stack.py` | 7 |
| **5. Binary Search** | `binary_search.py` | 7 |
| **6. Linked List** | `linked_list.py` | 11 |
| **7. Trees** | `trees.py` | 15 |
| **8. Tries** | `tries.py` | 3 |
| **9. Heap / Priority Queue** | `heap.py` | 7 |
| **10. Backtracking** | `backtracking.py` | 9 |
| **11. Graphs** | `graphs.py` | 13 |
| **12. Advanced Graphs** | `advanced_graphs.py` | 6 |
| **13. 1-D Dynamic Programming** | `one_d_dp.py` | 12 |
| **14. 2-D Dynamic Programming** | `two_d_dp.py` | 11 |
| **15. Greedy** | `greedy.py` | 8 |
| **16. Intervals** | `intervals.py` | 6 |
| **17. Math & Geometry** | `math_and_geometry.py` | 8 |
| **18. Bit Manipulation** | `bit_manipulation.py` | 7 |
| **Total** | **18 Modules** | **150 Solutions** |

---

## Interactive Practice UI (dsa-practice-ui)

The repository includes a modern Next.js application that simulates the official LeetCode practice experience. It is located at `dsa-ai-engineer-labs/dsa-practice-ui`.

### UI Features & Layout

1. **Split-Pane LeetCode Dark Theme**:
   - **Left Column**: Problem description, constraints, input/output example cards, category badges, company tags, and direct LeetCode links.
   - **5-Step Editorial Tab**: Structured analysis breaking down the requirements, brute force baseline, optimal algorithm, Big-O complexity, and production Python reference solution with a 1-click copy button.
   - **Submissions Tab**: Tracks test pass history and runtime metrics for the active session.
   - **Top Navigation Bar**: Problem List drawer launcher, Prev/Next problem navigator, challenge countdown timer, and Run (`Cmd/Ctrl + Enter`) / Submit buttons.

2. **Problem Browser Drawer**:
   - Modal drawer to browse all 150 problems.
   - Real-time search by title, LeetCode number, algorithmic pattern, or category.
   - Filter dropdown across all 18 categories and 3 difficulty tiers (Easy / Medium / Hard).
   - Live counter tracking completed vs total problems.

### Adaptive Challenge Countdown Timer

The application includes an adaptive countdown timer tailored to user experience level and problem difficulty:

| Challenge Tier | Target Focus | Easy | Medium | Hard |
| :--- | :--- | :---: | :---: | :---: |
| **Beginner** | Just starting out | 30 min | 45 min | 60 min (1h) |
| **Intermediate** | Pattern mastery and optimal approaches | 20 min | 35 min | 50 min |
| **Advanced / Interview Ready** | Consistent practice and interview speed | 15 min | 25 min | 45 min |
| **Stopwatch Mode** | Free practice with no time limits | Count Up | Count Up | Count Up |

Timer features:
- **Automatic Adjustment**: Switching problems detects the difficulty tier and restarts the timer with the corresponding duration.
- **Urgency Alerts**: Font color transitions from neutral white to amber (< 3 min) and pulsing red (< 1 min).
- **Web Audio Chimes**: Generates built-in warning and expiration audio tones using browser-native Web Audio (zero external network assets required, fully offline compatible). Includes a 1-click mute toggle.
- **Controls**: Pause, resume, reset, and a quick `+5m` extension button.
- **Time's Up Banner**: When time expires, a banner prompts the user with a 1-click button to view the 5-step editorial solution.

### Monaco Python Code Editor

- **Engine**: `@monaco-editor/react` with VS-Dark theme.
- **Features**: Python 3 syntax highlighting, automatic indentation, bracket matching, line numbers, and smooth scrolling.
- **Persistence**: Code edits for each problem are saved to `localStorage` automatically, ensuring user code is never lost when navigating between problems or refreshing.
- **Shortcuts**: `Cmd + Enter` (macOS) or `Ctrl + Enter` (Windows/Linux) triggers instant evaluation.

### Safe Subprocess Execution Engine

Code is evaluated via a safe Node.js subprocess endpoint (`/api/run`) calling `lib/runner.py`:
- **Timeout Protection**: 4.0-second safety cutoff prevents infinite loops.
- **Multiple Calling Formats**: Automatically executes solutions written as LeetCode classes (`class Solution: def method(self, ...)`), standalone functions (`def method(...)`), or object-oriented design classes (`MinStack`, `LRUCache`, `Trie`, `MedianFinder`, etc.).
- **Smart Signature Adaptation**: Handles functions whether `self` was included or omitted.
- **Order-Insensitive Matching**: Handles problems where output ordering is arbitrary (e.g., Two Sum indices `[0, 1]` or `[1, 0]`, 3Sum triplets, Subsets, and Group Anagrams).
- **Semantic Two Sum Verification**: Validates Two Sum by checking array bounds and checking if `nums[i] + nums[j] == target` with `i != j`.
- **Feedback Metrics**: Status badges (**Accepted**, **Wrong Answer**, **Compile Error**, **Runtime Error**, **Time Limit Exceeded**), millisecond execution runtime, and full traceback reporting.
- **Console Stdout Capture**: Any `print(...)` statements executed inside user code are captured and displayed in the terminal output tab.

### Component Architecture

```
dsa-practice-ui/
|-- app/
|   |-- api/run/route.ts      # Python subprocess execution endpoint with timeout protection
|   |-- globals.css           # Tailwind CSS v4 & custom LeetCode scrollbars
|   |-- layout.tsx            # Root layout with dark mode metadata
|   `-- page.tsx              # Main split-pane workspace & keyboard shortcuts
|-- components/
|   |-- CodeEditor.tsx        # Monaco editor component with Python configuration
|   |-- ConsoleTabs.tsx       # Bottom-right testcase & result inspection console
|   |-- CountdownTimer.tsx    # Adaptive challenge countdown timer
|   |-- Navbar.tsx            # Top header with timer, problem switcher, and Run/Submit
|   |-- ProblemDescription.tsx# Problem description, constraints & 5-step editorial
|   `-- ProblemModal.tsx      # Searchable & filterable 150-problem drawer modal
`-- lib/
    |-- problems.json         # Complete 150-problem dataset with metadata and starter code
    |-- problems.ts           # Accessor functions and category mappings
    |-- runner.py             # Python sandbox evaluation runner with ListNode/TreeNode support
    `-- types.ts              # TypeScript interfaces for problems, testcases, and results
```

### Quickstart Guide

Ensure Node.js 18+ and Python 3.8+ are installed:

```bash
cd dsa-practice-ui
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

To create an optimized production build:
```bash
npm run build
npm run start
```

---

## Automated Unit Testing & Pytest Suite

Every lab implementation and algorithmic solution is validated with comprehensive unit tests.

### Running All 167 Tests
```bash
# From repository root
pytest
```

Output:
```
collected 167 items
tests/test_chapter_01.py ..                                              [  1%]
...
tests/test_chapter_33.py ............................................... [ 94%]
..........                                                               [100%]
============================= 167 passed in 0.25s ==============================
```

### Running Specific Chapters
```bash
# Test Chapter 33 (NeetCode 150)
pytest tests/test_chapter_33.py -v

# Test Specialized AI Primitives (Vector Search, Attention, Inference Cache)
pytest tests/test_chapter_03.py tests/test_chapter_27.py tests/test_chapter_28.py tests/test_chapter_29.py
```

---

## 5-Step DSA Engineering Framework

Every algorithmic solution in the book and editorial follows the **5-Step System**:

1. **Step 1: Clarify Requirements & Constraints**:
   - Identify input types, memory bounds, element value ranges, and edge cases (empty collections, singletons, negative values, duplicates).
2. **Step 2: Brute Force Baseline**:
   - Formulate the naive solution (e.g., exhaustive search or nested loops) to establish time and space baselines.
3. **Step 3: Optimal Strategy & Algorithm**:
   - Leverage data structure invariants (hash tables, monotonic stacks, binary search, two pointers, dynamic programming) to reduce complexity.
4. **Step 4: Complexity Analysis**:
   - State asymptotic Big-O Time and Space bounds with mathematical justification.
5. **Step 5: Production Python Implementation**:
   - Clean, typed, edge-case-hardened code adhering to PEP 8 standards.

---

## Installation and Setup

### Prerequisites
- **Python**: `>= 3.10`
- **Node.js**: `>= 18.0.0`
- **npm** or **pnpm**

### Clone and Run
```bash
git clone https://github.com/lamhotsiagian/dsa-ai-engineer-labs.git
cd dsa-ai-engineer-labs

# 1. Install Python testing dependencies
pip install -e .

# 2. Run Python tests
pytest

# 3. Launch the Interactive UI
cd dsa-practice-ui
npm install
npm run dev
```

---

## Code Standards and Verification

- **Zero Absolute Paths**: All imports, datasets, testcases, and child processes resolve using dynamic relative paths across all files.
- **Portability**: Verified across macOS, Linux, and Windows environments.
- **Full Test Coverage**: 167 unit tests covering 33 chapters pass cleanly in under 0.3 seconds.
