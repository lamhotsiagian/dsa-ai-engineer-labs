"""Unit tests for Chapter 24."""
from __future__ import annotations
from dsa_labs.chapter_24.near_duplicates import NearDuplicateIndex
from dsa_labs.chapter_24.leetcode_solutions import str_str, find_repeated_dna_sequences, shortest_palindrome

def test_near_duplicate_index():
    idx = NearDuplicateIndex(permutations=16, threshold=0.5, shingle_size=2)
    labels, rep = idx.build(["machine learning models", "machine learning models"])
    assert rep.documents == 2

def test_str_str():
    assert str_str("sadbutsad", "sad") == 0
    assert str_str("leetcode", "leeto") == -1

def test_find_repeated_dna_sequences():
    s = "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"
    res = find_repeated_dna_sequences(s)
    assert "AAAAACCCCC" in res
    assert "CCCCCAAAAA" in res

def test_shortest_palindrome():
    assert shortest_palindrome("aacecaaa") == "aaacecaaa"
    assert shortest_palindrome("abcd") == "dcbabcd"
