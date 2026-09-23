"""Unit tests for Chapter 11."""
from __future__ import annotations
import numpy as np
from dsa_labs.chapter_11.beam_search import beam_search
from dsa_labs.chapter_11.leetcode_solutions import KthLargest, find_kth_largest, MedianFinder

def test_beam_search():
    def step_fn(seq):
        # 4-token vocab: 0=pad, 1=start, 2=word, 3=eos
        logits = np.array([-10.0, -10.0, 0.0, -1.0])
        if len(seq) >= 3:
            logits[3] = 10.0 # force EOS
        return logits
    beams = beam_search(step_fn, start_token=1, eos_token=3, beam_width=2, max_length=5)
    assert len(beams) > 0
    assert beams[0].tokens[0] == 1

def test_kth_largest_stream():
    kl = KthLargest(3, [4, 5, 8, 2])
    assert kl.add(3) == 4
    assert kl.add(5) == 5
    assert kl.add(10) == 5

def test_find_kth_largest():
    assert find_kth_largest([3, 2, 1, 5, 6, 4], 2) == 5
    assert find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4

def test_median_finder():
    mf = MedianFinder()
    mf.addNum(1)
    mf.addNum(2)
    assert mf.findMedian() == 1.5
    mf.addNum(3)
    assert mf.findMedian() == 2.0
