"""Unit tests for Chapter 17."""
from __future__ import annotations
from dsa_labs.chapter_17.tree_reduce import tree_reduce, sequential_reduce
from dsa_labs.chapter_17.leetcode_solutions import fib, my_pow, ListNode, merge_k_lists

def _make_list(vals):
    dummy = ListNode(0)
    curr = dummy
    for v in vals:
        curr.next = ListNode(v)
        curr = curr.next
    return dummy.next

def _to_vals(head):
    res = []
    while head:
        res.append(head.val)
        head = head.next
    return res

def test_tree_reduce():
    nums = [1, 2, 3, 4, 5, 6, 7, 8]
    val, rep = tree_reduce(nums, lambda a, b: a + b)
    assert val == 36
    assert rep.rounds == 3

def test_fib():
    assert fib(2) == 1
    assert fib(4) == 3

def test_my_pow():
    assert abs(my_pow(2.0, 10) - 1024.0) < 1e-6
    assert abs(my_pow(2.0, -2) - 0.25) < 1e-6

def test_merge_k_lists():
    l1 = _make_list([1, 4, 5])
    l2 = _make_list([1, 3, 4])
    l3 = _make_list([2, 6])
    merged = merge_k_lists([l1, l2, l3])
    assert _to_vals(merged) == [1, 1, 2, 3, 4, 4, 5, 6]
