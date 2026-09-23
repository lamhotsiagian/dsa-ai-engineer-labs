"""Unit tests for Chapter 05."""
from __future__ import annotations
from dsa_labs.chapter_05.context_budget import Turn, BudgetPlan, ContextBudget
from dsa_labs.chapter_05.leetcode_solutions import NumArray, subarray_sum, num_submatrix_sum_target

def test_context_budget():
    turns = [Turn("system", 50), Turn("user", 100), Turn("assistant", 150)]
    cb = ContextBudget(turns)
    assert cb.cost_of_last(2) == 250
    plan = cb.plan(context_limit=400, system_tokens=50, retrieved_tokens=50, generation_reserve=50)
    assert plan.fits is True
    assert plan.kept_turns > 0

def test_num_array():
    na = NumArray([-2, 0, 3, -5, 2, -1])
    assert na.sumRange(0, 2) == 1
    assert na.sumRange(2, 5) == -1
    assert na.sumRange(0, 5) == -3

def test_subarray_sum():
    assert subarray_sum([1, 1, 1], 2) == 2
    assert subarray_sum([1, 2, 3], 3) == 2

def test_num_submatrix_sum_target():
    mat = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
    assert num_submatrix_sum_target(mat, 0) == 4
