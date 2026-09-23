"""Unit tests for Chapter 15."""
from __future__ import annotations
import numpy as np
from dsa_labs.chapter_15.threshold_search import calibrate_threshold
from dsa_labs.chapter_15.leetcode_solutions import search, search_rotated, find_median_sorted_arrays

def test_threshold_search():
    scores = np.array([0.1, 0.4, 0.6, 0.8, 0.9])
    labels = np.array([0, 0, 1, 1, 1])
    op, ok = calibrate_threshold(scores, labels, target_precision=0.9)
    assert op.threshold >= 0.0

def test_search():
    assert search([-1, 0, 3, 5, 9, 12], 9) == 4
    assert search([-1, 0, 3, 5, 9, 12], 2) == -1

def test_search_rotated():
    assert search_rotated([4, 5, 6, 7, 0, 1, 2], 0) == 4
    assert search_rotated([4, 5, 6, 7, 0, 1, 2], 3) == -1

def test_find_median_sorted_arrays():
    assert find_median_sorted_arrays([1, 3], [2]) == 2.0
    assert find_median_sorted_arrays([1, 2], [3, 4]) == 2.5
