"""LeetCode Solutions for chapter_18."""
from __future__ import annotations

# ----------------------------------------------------------------------------
# Problem: Subsets (LeetCode 78) [\LTwo]
# ----------------------------------------------------------------------------
def subsets(nums: list[int]) -> list[list[int]]:
    result = []
    curr_subset = []

    def backtrack(start_idx: int) -> None:
        result.append(list(curr_subset))
        for i in range(start_idx, len(nums)):
            curr_subset.append(nums[i])
            backtrack(i + 1)
            curr_subset.pop()  # un-choose

    backtrack(0)
    return result

# ----------------------------------------------------------------------------
# Problem: Combination Sum (LeetCode 39) [\LThree]
# ----------------------------------------------------------------------------
def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    candidates.sort()
    result = []
    curr_combination = []

    def backtrack(remaining: int, start_idx: int) -> None:
        if remaining == 0:
            result.append(list(curr_combination))
            return

        for i in range(start_idx, len(candidates)):
            val = candidates[i]
            if val > remaining:
                break  # Prune search branch
            curr_combination.append(val)
            backtrack(remaining - val, i)  # i allows reuse
            curr_combination.pop()

    backtrack(target, 0)
    return result

# ----------------------------------------------------------------------------
# Problem: N-Queens (LeetCode 51) [\LFour]
# ----------------------------------------------------------------------------
def solve_n_queens(n: int) -> list[list[str]]:
    cols = set()
    pos_diag = set()  # r + c
    neg_diag = set()  # r - c

    board = [["."] * n for _ in range(n)]
    solutions = []

    def backtrack(r: int) -> None:
        if r == n:
            solutions.append(["".join(row) for row in board])
            return

        for c in range(n):
            if c in cols or (r + c) in pos_diag or (r - c) in neg_diag:
                continue

            cols.add(c)
            pos_diag.add(r + c)
            neg_diag.add(r - c)
            board[r][c] = "Q"

            backtrack(r + 1)

            cols.remove(c)
            pos_diag.remove(r + c)
            neg_diag.remove(r - c)
            board[r][c] = "."

    backtrack(0)
    return solutions

