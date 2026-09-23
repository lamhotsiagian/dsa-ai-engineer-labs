"""Chapter 33: NeetCode 150 - Intervals"""
from __future__ import annotations
import math
import heapq
import bisect
from collections import defaultdict, deque, Counter, OrderedDict
from typing import Optional, List, Dict, Set, Tuple

# ----------------------------------------------------------------------------
# Problem: Meeting Rooms (LeetCode: meeting-rooms)
# ----------------------------------------------------------------------------
def canAttendMeetings(intervals: list[list[int]]) -> bool:
    intervals.sort(key=lambda x: x[0])
    for i in range(len(intervals) - 1):
        # If next meeting starts before current meeting finishes, conflict exists
        if intervals[i + 1][0] < intervals[i][1]:
            return False
    return True

# ----------------------------------------------------------------------------
# Problem: Insert Interval (LeetCode: insert-interval)
# ----------------------------------------------------------------------------
def insert(intervals: list[list[int]], newInterval: list[int]) -> list[list[int]]:
    res = []
    for i, interval in enumerate(intervals):
        # Case 1: newInterval strictly before current interval
        if newInterval[1] < interval[0]:
            res.append(newInterval)
            return res + intervals[i:]
        # Case 2: newInterval strictly after current interval
        elif newInterval[0] > interval[1]:
            res.append(interval)
        # Case 3: Overlap encountered; merge boundaries
        else:
            newInterval = [
                min(newInterval[0], interval[0]),
                max(newInterval[1], interval[1])
            ]
    res.append(newInterval)
    return res

# ----------------------------------------------------------------------------
# Problem: Merge Intervals (LeetCode: merge-intervals)
# ----------------------------------------------------------------------------
def merge(intervals: list[list[int]]) -> list[list[int]]:
    # Sort intervals by starting time
    intervals.sort(key=lambda x: x[0])
    res = [intervals[0]]

    for start, end in intervals[1:]:
        last_end = res[-1][1]
        # If current interval overlaps with previous, extend the end time
        if start <= last_end:
            res[-1][1] = max(last_end, end)
        else:
            res.append([start, end])
    return res

# ----------------------------------------------------------------------------
# Problem: Non-overlapping Intervals (LeetCode: non-overlapping-intervals)
# ----------------------------------------------------------------------------
def eraseOverlapIntervals(intervals: list[list[int]]) -> int:
    # Sort intervals by end time to greedily maximize remaining non-overlapping slots
    intervals.sort(key=lambda x: x[1])
    removals = 0
    prev_end = intervals[0][1]

    for start, end in intervals[1:]:
        if start < prev_end:
            # Overlap detected; greedily drop interval with later end
            removals += 1
        else:
            prev_end = end
    return removals

# ----------------------------------------------------------------------------
# Problem: Meeting Rooms II (LeetCode: meeting-rooms-ii)
# ----------------------------------------------------------------------------
def minMeetingRooms(intervals: list[list[int]]) -> int:
    # Separate and sort start and end timelines independently
    starts = sorted([i[0] for i in intervals])
    ends = sorted([i[1] for i in intervals])
    res = 0
    count = 0
    s, e = 0, 0

    while s < len(intervals):
        if starts[s] < ends[e]:
            count += 1  # Meeting started before previous ended, need room
            s += 1
        else:
            count -= 1  # Room freed up
            e += 1
        res = max(res, count)
    return res

# ----------------------------------------------------------------------------
# Problem: Minimum Interval to Include Each Query (LeetCode: minimum-interval-to-include-each-query)
# ----------------------------------------------------------------------------
import heapq

def minInterval(intervals: list[list[int]], queries: list[int]) -> list[int]:
    intervals.sort(key=lambda x: x[0])
    # Min-heap storing: (interval_length, interval_end)
    min_heap = []
    res = {}
    i = 0

    # Sort queries while maintaining original associations
    for q in sorted(queries):
        # Push all intervals starting at or before query q
        while i < len(intervals) and intervals[i][0] <= q:
            l, r = intervals[i]
            heapq.heappush(min_heap, (r - l + 1, r))
            i += 1
        # Evict stale intervals whose end point is before query q
        while min_heap and min_heap[0][1] < q:
            heapq.heappop(min_heap)
        res[q] = min_heap[0][0] if min_heap else -1

    return [res[q] for q in queries]

