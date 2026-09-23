# DSA for AI Engineers - Interactive Practice Platform (LeetCode Style)

A high-performance, dark-themed interactive coding and compilation platform built with Next.js, Monaco Editor, Tailwind CSS, and Python 3. It provides a full LeetCode-style environment for practicing all 150 NeetCode / DSA problems and labs.

For the comprehensive laboratory overview, complete chapter index (01-33), and automated test suite documentation, see the [Main Repository README](../README.md).

---

## Key Features

1. **LeetCode Dark Theme & UI Layout:**
   - Split-pane layout matching LeetCode's interface: Problem Description & 5-Step Editorial on the left, Monaco Code Editor & interactive Testcase/Result Console on the right.
   - Prev/Next problem navigator and searchable problem browser modal.

2. **Adaptive Challenge Countdown Timer (Skill-Based Time Limits):**
   - **Beginner (Just Starting Out):**
     - Easy: 30 minutes | Medium: 45 minutes | Hard: 1 hour (60m)
   - **Intermediate (Pattern Mastery):**
     - Easy: 20 minutes | Medium: 35 minutes | Hard: 50 minutes
   - **Advanced / Interview Ready (Revision & Simulation):**
     - Easy: 15 minutes | Medium: 25 minutes | Hard: 45 minutes
   - **Free Practice:** Stopwatch mode (count up with no pressure).
   - **Controls & Audio:** Pause/Resume, Reset, Quick +5m extension, and built-in Web Audio warning & expiration chimes (with mute/unmute toggle).
   - **Time's Up Alert Banner:** Automatic prompt guiding the user to study the 5-step systematic editorial when time expires.

3. **Full Problem Suite (150 Problems across 18 Categories):**
   - Arrays & Hashing, Two Pointers, Sliding Window, Stack, Binary Search, Linked List, Trees, Tries, Heap, Backtracking, Graphs, Advanced Graphs, 1-D DP, 2-D DP, Greedy, Intervals, Math & Geometry, and Bit Manipulation.
   - Official LeetCode numbers, difficulty badges (Easy / Medium / Hard), patterns, and company tags.

4. **5-Step DSA Editorial System:**
   - Every problem includes structured analysis:
     - **Step 1:** Requirements & Edge-case constraints
     - **Step 2:** Brute Force baseline
     - **Step 3:** Optimal strategy and algorithm
     - **Step 4:** Time & Space Complexity analysis
     - **Step 5:** Python Reference Implementation (with 1-click copy)

5. **Monaco Python Editor:**
   - Full Python 3 syntax highlighting, indentation, bracket matching, line numbers, and keyboard shortcuts.
   - Shortcut: `Cmd + Enter` (Mac) or `Ctrl + Enter` (Windows/Linux) to instantly run code.
   - LocalStorage persistence: Your code edits are preserved across problems and reloads.

6. **Safe Serverless Execution Engine (/api/run):**
   - Direct Python 3 subprocess execution with a 4.0-second safety timeout.
   - Supports:
     - Regular function submissions (`def twoSum(nums, target): ...`)
     - LeetCode class submissions (`class Solution: def twoSum(self, ...): ...`)
     - Custom design data structures (`MinStack`, `LRUCache`, `Trie`, `MedianFinder`, etc.)
     - Custom data structures: `ListNode`, `TreeNode`, `Node`
   - Detailed feedback:
     - **Accepted** (with exact execution runtime in ms)
     - **Wrong Answer** (diff comparison between input, expected output, and your actual output)
     - **Compile Error / Syntax Error** (with line number and traceback)
     - **Runtime Error** (with complete Python traceback)
     - **Time Limit Exceeded**
     - **Console Stdout** (captures any `print()` output inside your solution)

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
|   |-- CountdownTimer.tsx    # Adaptive challenge countdown timer
|   |-- Navbar.tsx            # Top header with timer, problem switcher, and Run/Submit
|   |-- ProblemDescription.tsx# Problem markdown description, examples, constraints & 5-step editorial
|   `-- ProblemModal.tsx      # Searchable & filterable 150-problem drawer modal
`-- lib/
    |-- problems.json         # Complete 150-problem dataset with metadata and starter code
    |-- problems.ts           # Accessor functions and category mappings
    |-- runner.py             # Python sandbox evaluation runner with ListNode/TreeNode support
    `-- types.ts              # TypeScript interfaces for problems, testcases, and results
```
