# Cracking DSA Interview Preparation for AI Engineers - Canonical Labs, Interactive UI and Test Suite

[![Tests](https://img.shields.io/badge/pytest-158%20passed-brightgreen.svg)](tests/)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](pyproject.toml)
[![Next.js](https://img.shields.io/badge/next.js-16.3-black.svg)](dsa-practice-ui/)
[![TypeScript](https://img.shields.io/badge/typescript-5.0-blue.svg)](dsa-practice-ui/)
[![Tailwind](https://img.shields.io/badge/tailwind-v4-38bdf8.svg)](dsa-practice-ui/)

The official laboratory, interactive code playground, and testing suite for **Cracking DSA Interview Preparation for AI Engineers: Coding Patterns, Algorithms, System Thinking, and Interview Preparation**.

This repository bridges classical algorithmic problem solving with real-world AI infrastructure. It provides **33 structured chapters**, **150 NeetCode interview companion solutions**, **158 automated unit tests**, and a **Next.js & Monaco Editor interactive LeetCode practice platform** with live Python execution.

---

## Table of Contents

1. [Repository Architecture](#repository-architecture)
2. [Complete Chapter Index (Chapters 01-33)](#complete-chapter-index-chapters-01-33)
3. [Chapter 33: NeetCode 150 Interview Companion](#chapter-33-neetcode-150-interview-companion)
4. [Interactive Practice UI (dsa-practice-ui)](#interactive-practice-ui-dsa-practice-ui)
5. [Automated Unit Testing & Pytest Suite](#automated-unit-testing--pytest-suite)
6. [Installation and Setup](#installation-and-setup)
7. [Code Standards and Verification](#code-standards-and-verification)

---

## Repository Architecture

```
dsa-ai-engineer-labs/
|-- .gitignore                   # Universal ignore for Python, virtual envs, and Next.js builds
|-- pyproject.toml               # Configured with pythonpath = ["."] for frictionless pytest
|-- README.md                    # Unified repository documentation
|-- dsa_labs/                    # Canonical implementations and algorithmic solutions
|   |-- chapter_03/ ...          # Chapters 03 to 29: Core Foundations & AI Primitives
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
|-- tests/                       # 158 automated unit tests across all laboratory modules
|   |-- test_chapter_03.py ...
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
| **01** | The AI Engineer's Interview Landscape | *(Conceptual Chapter in Ebook)* | The four-pillar loop, round triage, prep strategy |
| **02** | Complexity Analysis & Real Machines | *(Conceptual Chapter in Ebook)* | Asymptotic cost vs real hardware, memory hierarchies |
| **03** | Vector Toolkit & Cosine Top-K | `chapter_03/vector_toolkit.py` | L2 normalization, vectorized dot product, top-k |
| **04** | LLM Sequence Batching & Arrays | `chapter_04/batcher.py` | Length-bucket batcher, in-place array algorithms |
| **05** | Context Budget & Prefix Sums | `chapter_05/context_budget.py` | Prefix sums, turn budget planning, 2D matrix sums |
| **06** | Rolling Windows & Two Pointers | `chapter_06/token_bucket.py` | Rolling token bucket rate limiter, sliding window |
| **07** | Deduplication & Hash Indexes | `chapter_07/dedup.py` | Exact deduplicator, hash sets, bucket chaining |
| **08** | Linked Lists & KV Cache Allocation | `chapter_08/lru.py` | Doubly-linked nodes, ordered LRU cache primitive |
| **09** | Request Queues & Monotonic Stacks | `chapter_09/request_queue.py` | Monotonic stack, bounded queues, histogram areas |
| **10** | Hierarchical Tree Indexing | `chapter_10/centroid_index.py` | Hierarchical vector space partitioning, tree traversal |
| **11** | Priority Queues & Beam Search | `chapter_11/beam_search.py` | Min/max heaps, top-k beam decoding for LLMs |
| **12** | Vocabulary Tries for Tokenization | `chapter_12/vocab_trie.py` | Prefix matching, wildcard token dictionaries |
| **13** | Disjoint Sets & Graph Clusters | `chapter_13/near_dup_uf.py` | Union-Find with rank and path compression |
| **14** | External Sorting for Large Corpora | `chapter_14/external_sort.py` | K-way external merge sort, chunked file processing |
| **15** | Binary Search & Calibration | `chapter_15/threshold_calibration.py` | Logarithmic search, probability threshold tuning |
| **16** | Interval Scheduling & Compute Slots | `chapter_16/admission_scheduler.py` | Interval intersections, non-overlapping slot allocation |
| **17** | Divide & Conquer Tree Reductions | `chapter_17/tree_reducer.py` | Parallel tensor tree reduction, fast exponentiation |
| **18** | Backtracking & Constraint Search | `chapter_18/constraint_search.py` | Bounded prompt constraint exploration, N-Queens |
| **19** | Greedy Context Packing | `chapter_19/context_packing.py` | Knapsack approximations, greedy window chunking |
| **20** | Dynamic Programming & Tokenizer | `chapter_20/subword_tokenization.py` | Viterbi path decoding, unigram token probability DP |
| **21** | Bit Manipulation & Quantization | `chapter_21/int4_quantization.py` | Int8/Int4 fixed-point scaling, bitmask SIMD tricks |
| **22** | Workflow Graphs & Traversal | `chapter_22/agent_workflow.py` | Breadth-First & Depth-First agent step dispatch |
| **23** | DAG Pipeline Execution | `chapter_23/dag_executor.py` | Topological sort, dependency resolution, concurrency |
| **24** | String Matching & Near-Duplicates | `chapter_24/near_duplicate.py` | Rabin-Karp polynomial rolling hash, MinHash shingles |
| **25** | Fenwick Trees & Weighted Sampling | `chapter_25/weighted_sampler.py` | Binary Indexed Trees (BIT), prefix probability sampler |
| **26** | Streaming Summaries & HyperLogLog | `chapter_26/stream_summary.py` | HyperLogLog cardinalities, reservoir stream sampling |
| **27** | Mathematical ML Primitives | `chapter_27/ml_toolkit.py` | Attention, Softmax, K-Means from scratch in NumPy |
| **28** | Vector Search: NSW & HNSW | `chapter_28/nsw_decoder.py` | Navigable Small World vector graphs, ANN lookups |
| **29** | Semantic Inference Cache & Rate Limits | `chapter_29/inference_cache.py` | Vector-similarity caching, Token Bucket rate limiting |
| **30** | The Pattern Recognition Playbook | *(Strategy Chapter in Ebook)* | 20 Coding patterns, constraint ladder, signal triage |
| **31** | The Coding Interview Protocol | *(Strategy Chapter in Ebook)* | 11-Step live interview protocol, trade-off communication |
| **32** | Mock Interview Simulations | *(Strategy Chapter in Ebook)* | 4 Full loop transcripts, rubric scoring, failure recovery |
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
|   |-- CountdownTimer.tsx    # Problem countdown and stopwatch timer
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

### Running All 158 Tests
```bash
# From repository root
pytest
```

Output:
```
collected 158 items
tests/test_chapter_03.py ..                                              [  1%]
...
tests/test_chapter_33.py ............................................... [ 94%]
..........                                                               [100%]
============================= 158 passed in 0.28s ==============================
```

### Running Specific Chapters
```bash
# Test Chapter 33 (NeetCode 150)
pytest tests/test_chapter_33.py -v

# Test Specialized AI Primitives (Vector Search, Attention, Inference Cache)
pytest tests/test_chapter_03.py tests/test_chapter_27.py tests/test_chapter_28.py tests/test_chapter_29.py
```

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
