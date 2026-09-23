"""Unit tests for Chapter 14."""
from __future__ import annotations
from dsa_labs.chapter_14.external_sort import SortStats, external_sort
from dsa_labs.chapter_14.leetcode_solutions import merge_sorted_array, sort_colors, maximum_gap

def test_merge_sorted_array():
    nums1 = [1, 2, 3, 0, 0, 0]
    merge_sorted_array(nums1, 3, [2, 5, 6], 3)
    assert nums1 == [1, 2, 2, 3, 5, 6]

def test_sort_colors():
    colors = [2, 0, 2, 1, 1, 0]
    sort_colors(colors)
    assert colors == [0, 0, 1, 1, 2, 2]

def test_maximum_gap():
    assert maximum_gap([3, 6, 9, 1]) == 3
    assert maximum_gap([10]) == 0
