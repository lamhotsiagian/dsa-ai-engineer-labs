"""Unit tests for Chapter 04."""
from __future__ import annotations
from dsa_labs.chapter_04.batching import Request, Batch, LengthBucketBatcher
from dsa_labs.chapter_04.leetcode_solutions import remove_element, rotate, first_missing_positive

def test_batching():
    batcher = LengthBucketBatcher(max_batch_size=2, max_wait_ms=10.0, buckets=(16, 32))
    b1 = batcher.submit(Request("r1", length=10, arrival_ms=0.0))
    assert b1 is None
    b2 = batcher.submit(Request("r2", length=14, arrival_ms=5.0))
    assert b2 is not None
    assert len(b2.requests) == 2
    assert b2.padded_width == 14

def test_remove_element():
    nums = [3, 2, 2, 3]
    k = remove_element(nums, 3)
    assert k == 2
    assert sorted(nums[:k]) == [2, 2]

def test_rotate():
    nums = [1, 2, 3, 4, 5, 6, 7]
    rotate(nums, 3)
    assert nums == [5, 6, 7, 1, 2, 3, 4]

def test_first_missing_positive():
    assert first_missing_positive([1, 2, 0]) == 3
    assert first_missing_positive([3, 4, -1, 1]) == 2
    assert first_missing_positive([7, 8, 9, 11, 12]) == 1
