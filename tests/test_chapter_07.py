"""Unit tests for Chapter 07."""
from __future__ import annotations
from dsa_labs.chapter_07.dedup import ExactDeduplicator
from dsa_labs.chapter_07.leetcode_solutions import is_anagram, group_anagrams, longest_consecutive

def test_exact_dedup():
    dedup = ExactDeduplicator(capacity=100)
    assert dedup.is_duplicate("hello") is False
    assert dedup.is_duplicate("hello") is True

def test_is_anagram():
    assert is_anagram("anagram", "nagaram") is True
    assert is_anagram("rat", "car") is False

def test_group_anagrams():
    res = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    sorted_res = sorted([sorted(g) for g in res])
    assert sorted_res == [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]

def test_longest_consecutive():
    assert longest_consecutive([100, 4, 200, 1, 3, 2]) == 4
    assert longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
