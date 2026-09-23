"""Unit tests for Chapter 02."""
from __future__ import annotations
from dsa_labs.chapter_02.complexity_probe import measure_scaling, _classify

def test_classify():
    assert _classify(0.1) == "O(1) or O(log n)"
    assert _classify(1.0) == "O(n)"
    assert _classify(1.3) == "O(n log n)"
    assert _classify(2.0) == "O(n^2)"

def test_measure_scaling():
    def linear_fn(arr):
        return sum(arr)
    report = measure_scaling(linear_fn, lambda n: list(range(n)), sizes=(500, 1000, 2000), repeats=2)
    assert report.exponent >= 0.0
    assert str(report) != ""
