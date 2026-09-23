"""LeetCode Solutions for chapter_16."""
from __future__ import annotations

# ----------------------------------------------------------------------------
# Problem: Meeting Rooms (LeetCode 252) [\LTwo]
# ----------------------------------------------------------------------------
def can_attend_meetings(intervals: list[list[int]]) -> bool:
    intervals.sort(key=lambda x: x[0])
    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i - 1][1]:
            return False
    return True

# ----------------------------------------------------------------------------
# Problem: Merge Intervals (LeetCode 56) [\LThree]
# ----------------------------------------------------------------------------
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    intervals.sort(key=lambda x: x[0])
    merged = []

    for interval in intervals:
        if not merged or merged[-1][1] < interval[0]:
            merged.append(interval)
        else:
            merged[-1][1] = max(merged[-1][1], interval[1])

    return merged

# ----------------------------------------------------------------------------
# Problem: The Skyline Problem (LeetCode 218) [\LFour]
# ----------------------------------------------------------------------------
import heapq

def get_skyline(buildings: list[list[int]]) -> list[list[int]]:
    events = []
    for L, R, H in buildings:
        events.append((L, -H, R))  # start event (-H for max-heap tiebreaker)
        events.append((R, 0, 0))   # end event

    events.sort(key=lambda x: (x[0], x[1]))

    result = [[0, 0]]
    # Max-heap storing (-height, end_x)
    live = [(0, float("inf"))]

    for x, neg_h, R in events:
        if neg_h != 0:
            heapq.heappush(live, (neg_h, R))

        # Lazy deletion of expired buildings
        while live[0][1] <= x:
            heapq.heappop(live)

        curr_height = -live[0][0]
        if result[-1][1] != curr_height:
            result.append([x, curr_height])

    return result[1:]

