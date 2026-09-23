"""Unit tests for Chapter 26."""
from __future__ import annotations
from dsa_labs.chapter_26.stream_summary import HyperLogLog
from dsa_labs.chapter_26.leetcode_solutions import ArrayShuffler, ListNode, LinkedListRandomNode, RandomizedCollection

def test_hyperloglog():
    hll = HyperLogLog(precision=10)
    for i in range(100):
        hll.add(str(i))
    assert hll.count() > 50

def test_array_shuffler():
    nums = [1, 2, 3]
    shuffler = ArrayShuffler(nums)
    s = shuffler.shuffle()
    assert sorted(s) == [1, 2, 3]
    assert shuffler.reset() == [1, 2, 3]

def test_linked_list_random_node():
    head = ListNode(10, ListNode(20, ListNode(30)))
    sampler = LinkedListRandomNode(head)
    val = sampler.getRandom()
    assert val in {10, 20, 30}

def test_randomized_collection():
    rc = RandomizedCollection()
    assert rc.insert(1) is True
    assert rc.insert(1) is False
    assert rc.insert(2) is True
    assert rc.getRandom() in {1, 2}
    assert rc.remove(1) is True
    assert rc.getRandom() in {1, 2}
