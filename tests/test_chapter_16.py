"""Unit tests for Chapter 16."""
from __future__ import annotations
from dsa_labs.chapter_16.slot_scheduler import SlotScheduler
from dsa_labs.chapter_16.leetcode_solutions import can_attend_meetings, merge_intervals, get_skyline

def test_can_attend_meetings():
    assert can_attend_meetings([[0,30],[5,10],[15,20]]) is False
    assert can_attend_meetings([[7,10],[2,4]]) is True

def test_merge_intervals():
    assert merge_intervals([[1,3],[2,6],[8,10],[15,18]]) == [[1,6],[8,10],[15,18]]
    assert merge_intervals([[1,4],[4,5]]) == [[1,5]]

def test_get_skyline():
    b = [[2,9,10],[3,7,15],[5,12,12],[15,20,10],[19,24,8]]
    skyline = get_skyline(b)
    assert len(skyline) > 0
    assert skyline[0] == [2, 10]
