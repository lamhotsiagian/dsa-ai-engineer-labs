"""Unit tests for Chapter 30."""
from __future__ import annotations
from dsa_labs.chapter_30.triage import target_for, match_signals, triage
from dsa_labs.chapter_30.templates import Templates

def test_triage():
    target = target_for(50)
    assert "O(n^3)" in target.label
    tri = triage("find the contiguous subarray that maximizes profit", n=1000)
    assert "sliding window" in tri["candidates"]

def test_templates():
    assert Templates.binary_search([1, 3, 5, 7], 5) == 2
    assert Templates.binary_search([1, 3, 5, 7], 6) == -1
    assert Templates.sliding_window("abcde", 2) == 2
