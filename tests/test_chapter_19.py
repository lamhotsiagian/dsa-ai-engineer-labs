"""Unit tests for Chapter 19."""
from __future__ import annotations
from dsa_labs.chapter_19.context_packing import Chunk, pack_greedy
from dsa_labs.chapter_19.leetcode_solutions import max_profit, can_jump, candy

def test_pack_greedy():
    chunks = [Chunk("c1", 10, 1.0), Chunk("c2", 20, 2.0), Chunk("c3", 15, 1.5)]
    packing = pack_greedy(chunks, budget=30)
    assert packing.total_tokens <= 30

def test_max_profit():
    assert max_profit([7, 1, 5, 3, 6, 4]) == 5
    assert max_profit([7, 6, 4, 3, 1]) == 0

def test_can_jump():
    assert can_jump([2, 3, 1, 1, 4]) is True
    assert can_jump([3, 2, 1, 0, 4]) is False

def test_candy():
    assert candy([1, 0, 2]) == 5
    assert candy([1, 2, 2]) == 4
