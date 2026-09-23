"""Unit tests for Chapter 18."""
from __future__ import annotations
from dsa_labs.chapter_18.constraint_search import SearchBudget, bounded_search
from dsa_labs.chapter_18.leetcode_solutions import subsets, combination_sum, solve_n_queens

def test_bounded_search():
    def is_complete(state):
        return len(state) == 3
    def candidates(state):
        return [1, 2]
    def is_valid(state, c):
        return True
    def apply(state, c):
        state.append(c)
    def undo(state, c):
        state.pop()
    def snapshot(state):
        return list(state)
    sols, rep = bounded_search([], is_complete, candidates, is_valid, apply, undo, snapshot)
    assert len(sols) == 8

def test_subsets():
    res = subsets([1, 2, 3])
    assert len(res) == 8
    assert [] in res
    assert [1, 2, 3] in res

def test_combination_sum():
    res = combination_sum([2, 3, 6, 7], 7)
    assert [7] in res
    assert [2, 2, 3] in res

def test_solve_n_queens():
    assert len(solve_n_queens(4)) == 2
    assert len(solve_n_queens(1)) == 1
