"""Unit tests for Chapter 08."""
from __future__ import annotations
from dsa_labs.chapter_08.linked import ListNode as LabNode, from_iterable, to_list, has_cycle
from dsa_labs.chapter_08.leetcode_solutions import ListNode, reverse_list, detect_cycle, reverse_k_group

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

def test_lab_linked():
    head = from_iterable([1, 2, 3])
    assert to_list(head) == [1, 2, 3]
    assert has_cycle(head) is False

def test_reverse_list():
    head = _make_list([1, 2, 3, 4, 5])
    rev = reverse_list(head)
    assert _to_vals(rev) == [5, 4, 3, 2, 1]

def test_detect_cycle():
    n1 = ListNode(3)
    n2 = ListNode(2)
    n3 = ListNode(0)
    n4 = ListNode(-4)
    n1.next, n2.next, n3.next, n4.next = n2, n3, n4, n2
    assert detect_cycle(n1) == n2
    assert detect_cycle(_make_list([1, 2])) is None

def test_reverse_k_group():
    head = _make_list([1, 2, 3, 4, 5])
    res = reverse_k_group(head, 2)
    assert _to_vals(res) == [2, 1, 4, 3, 5]
