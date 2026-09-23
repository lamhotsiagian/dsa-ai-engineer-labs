"""Chapter 33: NeetCode 150 - Backtracking"""
from __future__ import annotations
import math
import heapq
import bisect
from collections import defaultdict, deque, Counter, OrderedDict
from typing import Optional, List, Dict, Set, Tuple

# ----------------------------------------------------------------------------
# Problem: Subsets (LeetCode: subsets)
# ----------------------------------------------------------------------------
def subsets(nums: list[int]) -> list[list[int]]:
    res = []
    subset = []

    def dfs(i: int) -> None:
        # Base case: reached beyond array end, record subset copy
        if i >= len(nums):
            res.append(subset.copy())
            return
        # Decision 1: Include nums[i]
        subset.append(nums[i])
        dfs(i + 1)
        # Decision 2: Exclude nums[i] (backtrack)
        subset.pop()
        dfs(i + 1)

    dfs(0)
    return res

# ----------------------------------------------------------------------------
# Problem: Combination Sum (LeetCode: combination-sum)
# ----------------------------------------------------------------------------
def combinationSum(candidates: list[int], target: int) -> list[list[int]]:
    res = []

    def dfs(i: int, curr: list[int], total: int) -> None:
        if total == target:
            res.append(curr.copy())
            return
        if i >= len(candidates) or total > target:
            return
        # Branch 1: Pick candidate[i] (can be reused indefinitely)
        curr.append(candidates[i])
        dfs(i, curr, total + candidates[i])
        # Branch 2: Skip candidate[i] and move to next candidate
        curr.pop()
        dfs(i + 1, curr, total)

    dfs(0, [], 0)
    return res

# ----------------------------------------------------------------------------
# Problem: Permutations (LeetCode: permutations)
# ----------------------------------------------------------------------------
def permute(nums: list[int]) -> list[list[int]]:
    res = []
    
    def backtrack(curr: list[int], used: list[bool]) -> None:
        if len(curr) == len(nums):
            res.append(curr.copy())
            return
        for i in range(len(nums)):
            if not used[i]:
                used[i] = True
                curr.append(nums[i])
                backtrack(curr, used)
                curr.pop()       # Backtrack
                used[i] = False

    backtrack([], [False] * len(nums))
    return res

# ----------------------------------------------------------------------------
# Problem: Subsets II (LeetCode: subsets-ii)
# ----------------------------------------------------------------------------
def subsetsWithDup(nums: list[int]) -> list[list[int]]:
    nums.sort()  # Sort to bring duplicate elements adjacent
    res = []
    subset = []

    def dfs(i: int) -> None:
        if i >= len(nums):
            res.append(subset.copy())
            return
        # Decision 1: Include nums[i]
        subset.append(nums[i])
        dfs(i + 1)
        subset.pop()
        # Decision 2: Exclude nums[i] and skip all identical duplicates
        while i + 1 < len(nums) and nums[i] == nums[i + 1]:
            i += 1
        dfs(i + 1)

    dfs(0)
    return res

# ----------------------------------------------------------------------------
# Problem: Combination Sum II (LeetCode: combination-sum-ii)
# ----------------------------------------------------------------------------
def combinationSum2(candidates: list[int], target: int) -> list[list[int]]:
    candidates.sort()  # Sort for clean duplicate skipping
    res = []

    def dfs(pos: int, curr: list[int], total: int) -> None:
        if total == target:
            res.append(curr.copy())
            return
        if total > target:
            return
        for i in range(pos, len(candidates)):
            # Skip sibling duplicates at the same decision depth
            if i > pos and candidates[i] == candidates[i - 1]:
                continue
            curr.append(candidates[i])
            dfs(i + 1, curr, total + candidates[i])  # Each item used at most once
            curr.pop()

    dfs(0, [], 0)
    return res

# ----------------------------------------------------------------------------
# Problem: Word Search (LeetCode: word-search)
# ----------------------------------------------------------------------------
def exist(board: list[list[str]], word: str) -> bool:
    ROWS, COLS = len(board), len(board[0])

    def dfs(r: int, c: int, i: int) -> bool:
        if i == len(word):
            return True
        if not (0 <= r < ROWS and 0 <= c < COLS) or board[r][c] != word[i]:
            return False
        
        # Mark cell as visited
        tmp = board[r][c]
        board[r][c] = "#"
        # Explore cardinal directions: Down, Up, Right, Left
        found = (dfs(r + 1, c, i + 1) or
                 dfs(r - 1, c, i + 1) or
                 dfs(r, c + 1, i + 1) or
                 dfs(r, c - 1, i + 1))
        board[r][c] = tmp  # Restore cell state
        return found

    for r in range(ROWS):
        for c in range(COLS):
            if dfs(r, c, 0):
                return True
    return False

# ----------------------------------------------------------------------------
# Problem: Palindrome Partitioning (LeetCode: palindrome-partitioning)
# ----------------------------------------------------------------------------
def partition(s: str) -> list[list[str]]:
    res = []
    part = []

    def is_pali(sub: str) -> bool:
        return sub == sub[::-1]

    def dfs(i: int) -> None:
        if i >= len(s):
            res.append(part.copy())
            return
        for j in range(i, len(s)):
            prefix = s[i : j + 1]
            if is_pali(prefix):
                part.append(prefix)
                dfs(j + 1)
                part.pop()

    dfs(0)
    return res

# ----------------------------------------------------------------------------
# Problem: Letter Combinations of a Phone Number (LeetCode: letter-combinations-of-a-phone-number)
# ----------------------------------------------------------------------------
def letterCombinations(digits: str) -> list[str]:
    if not digits:
        return []
    phone = {
        "2": "abc", "3": "def", "4": "ghi", "5": "jkl",
        "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"
    }
    res = []

    def backtrack(i: int, curr: str) -> None:
        if len(curr) == len(digits):
            res.append(curr)
            return
        for char in phone[digits[i]]:
            backtrack(i + 1, curr + char)

    backtrack(0, "")
    return res

# ----------------------------------------------------------------------------
# Problem: N-Queens (LeetCode: n-queens)
# ----------------------------------------------------------------------------
def solveNQueens(n: int) -> list[list[str]]:
    col_set = set()
    pos_diag = set()  # (r + c)
    neg_diag = set()  # (r - c)
    res = []
    board = [["."] * n for _ in range(n)]

    def backtrack(r: int) -> None:
        if r == n:
            res.append(["".join(row) for row in board])
            return
        for c in range(n):
            if c in col_set or (r + c) in pos_diag or (r - c) in neg_diag:
                continue
            # Place Queen
            col_set.add(c)
            pos_diag.add(r + c)
            neg_diag.add(r - c)
            board[r][c] = "Q"

            backtrack(r + 1)

            # Remove Queen (backtrack)
            col_set.remove(c)
            pos_diag.remove(r + c)
            neg_diag.remove(r - c)
            board[r][c] = "."

    backtrack(0)
    return res

