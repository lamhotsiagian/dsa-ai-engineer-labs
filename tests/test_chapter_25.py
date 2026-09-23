"""Unit tests for Chapter 25."""
from __future__ import annotations
from dsa_labs.chapter_25.weighted_sampler import WeightedSampler
from dsa_labs.chapter_25.leetcode_solutions import NumArrayFenwick, NumArray, count_smaller

def test_num_array_fenwick():
    na = NumArrayFenwick([-2, 0, 3, -5, 2, -1])
    assert na.sumRange(0, 2) == 1
    assert na.sumRange(2, 5) == -1

def test_num_array_mutable():
    na = NumArray([1, 3, 5])
    assert na.sumRange(0, 2) == 9
    na.update(1, 2)
    assert na.sumRange(0, 2) == 8

def test_count_smaller():
    assert count_smaller([5, 2, 6, 1]) == [2, 1, 1, 0]
    assert count_smaller([-1]) == [0]
