"""Unit tests for Chapter 06."""
from __future__ import annotations
from dsa_labs.chapter_06.rolling_window import Decision, ExactRollingWindow
from dsa_labs.chapter_06.leetcode_solutions import is_palindrome, length_of_longest_substring, min_window

def test_rolling_window():
    rw = ExactRollingWindow(limit_tokens=100, horizon_s=10.0)
    assert rw.try_consume(now_s=0.0, tokens=50).allowed is True
    assert rw.try_consume(now_s=5.0, tokens=40).allowed is True
    assert rw.try_consume(now_s=6.0, tokens=30).allowed is False

def test_is_palindrome():
    assert is_palindrome("A man, a plan, a canal: Panama") is True
    assert is_palindrome("race a car") is False

def test_length_of_longest_substring():
    assert length_of_longest_substring("abcabcbb") == 3
    assert length_of_longest_substring("bbbbb") == 1
    assert length_of_longest_substring("pwwkew") == 3

def test_min_window():
    assert min_window("ADOBECODEBANC", "ABC") == "BANC"
    assert min_window("a", "a") == "a"
    assert min_window("a", "aa") == ""
