"""Unit tests for Chapter 20."""
from __future__ import annotations
from dsa_labs.chapter_20.viterbi_tokenizer import Segmentation, UnigramTokenizer
from dsa_labs.chapter_20.leetcode_solutions import climb_stairs, coin_change, min_distance

def test_unigram_tokenizer():
    vocab = {"a": -0.5, "b": -0.8, "ab": -0.2}
    tok = UnigramTokenizer(vocab)
    seg = tok.segment("ab")
    assert seg.pieces in [("ab",), ("a", "b")]

def test_climb_stairs():
    assert climb_stairs(2) == 2
    assert climb_stairs(3) == 3

def test_coin_change():
    assert coin_change([1, 2, 5], 11) == 3
    assert coin_change([2], 3) == -1
    assert coin_change([1], 0) == 0

def test_min_distance():
    assert min_distance("horse", "ros") == 3
    assert min_distance("intention", "execution") == 5
