"""Unit tests for Chapter 09."""
from __future__ import annotations
from dsa_labs.chapter_09.request_queue import BoundedRequestQueue, QueuedRequest
from dsa_labs.chapter_09.leetcode_solutions import is_valid_parentheses, daily_temperatures, largest_rectangle_area

def test_bounded_queue():
    from dsa_labs.chapter_09.request_queue import Rejection
    q = BoundedRequestQueue(max_depth=5, max_queued_tokens=100)
    req1 = QueuedRequest("r1", enqueued_ms=0.0, deadline_ms=100.0, estimated_tokens=30)
    assert q.offer(req1, now_ms=0.0) == Rejection.NONE
    assert len(q) == 1
    assert q.poll(now_ms=10.0) == req1

def test_is_valid_parentheses():
    assert is_valid_parentheses("()") is True
    assert is_valid_parentheses("()[]{}") is True
    assert is_valid_parentheses("(]") is False

def test_daily_temperatures():
    assert daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]
    assert daily_temperatures([30, 40, 50, 60]) == [1, 1, 1, 0]

def test_largest_rectangle_area():
    assert largest_rectangle_area([2, 1, 5, 6, 2, 3]) == 10
    assert largest_rectangle_area([2, 4]) == 4
