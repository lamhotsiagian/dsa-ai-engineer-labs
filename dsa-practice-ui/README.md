# DSA for AI Engineers - Interactive Practice Platform (LeetCode Style)

A high-performance, dark-themed interactive coding and compilation platform built with Next.js, Monaco Editor, Tailwind CSS, and Python 3. It provides a full LeetCode-style environment for practicing all 150 NeetCode / DSA problems and labs.

For the comprehensive laboratory overview, complete chapter index (01-33), and automated test suite documentation, see the [Main Repository README](../README.md).

---

## Key Features

- **Full Problem Suite (150 Problems across 18 Categories):**
  - Arrays & Hashing, Two Pointers, Sliding Window, Stack, Binary Search, Linked List, Trees, Tries, Heap, Backtracking, Graphs, Advanced Graphs, 1-D DP, 2-D DP, Greedy, Intervals, Math & Geometry, and Bit Manipulation.
  - Official LeetCode numbers, difficulty badges (Easy / Medium / Hard), patterns, and company tags.
- **Interactive Evaluation:** Immediate testcase feedback, execution metrics, and console output.

---

## Getting Started

### 1. Requirements
- Node.js 18+ (tested on Node.js 20+)
- Python 3.8+ available in your PATH (`python3`)

### 2. Install Dependencies
```bash
cd dsa-practice-ui
npm install
```

### 3. Run Development Server
```bash
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

### 4. Build & Production Run
```bash
npm run build
npm run start
```

---

## Project Architecture

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
|   |-- ProblemDescription.tsx# Problem markdown description, examples, constraints & 5-step editorial
|   `-- ProblemModal.tsx      # Searchable & filterable 150-problem drawer modal
`-- lib/
    |-- problems.json         # Complete 150-problem dataset with metadata and starter code
    |-- problems.ts           # Accessor functions and category mappings
    |-- runner.py             # Python sandbox evaluation runner with ListNode/TreeNode support
    `-- types.ts              # TypeScript interfaces for problems, testcases, and results
```
