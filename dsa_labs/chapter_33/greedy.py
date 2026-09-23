"""Chapter 33: NeetCode 150 - Greedy"""
from __future__ import annotations
import math
import heapq
import bisect
from collections import defaultdict, deque, Counter, OrderedDict
from typing import Optional, List, Dict, Set, Tuple

# ----------------------------------------------------------------------------
# Problem: Maximum Subarray (LeetCode: maximum-subarray)
# ----------------------------------------------------------------------------
def maxSubArray(nums: list[int]) -> int:
    # Kadane's Algorithm
    max_sum = nums[0]
    cur_sum = 0
    for x in nums:
        # Reset current sum if prefix contribution drops below 0
        cur_sum = max(x, cur_sum + x)
        max_sum = max(max_sum, cur_sum)
    return max_sum

# ----------------------------------------------------------------------------
# Problem: Jump Game (LeetCode: jump-game)
# ----------------------------------------------------------------------------
def canJump(nums: list[int]) -> bool:
    # Work backwards: track leftmost goal post that can reach destination
    goal = len(nums) - 1
    for i in range(len(nums) - 2, -1, -1):
        if i + nums[i] >= goal:
            goal = i  # Shift target leftward
    return goal == 0

# ----------------------------------------------------------------------------
# Problem: Jump Game II (LeetCode: jump-game-ii)
# ----------------------------------------------------------------------------
def jump(nums: list[int]) -> int:
    jumps = 0
    l = r = 0  # Window [l, r] reachable with current number of jumps

    while r < len(nums) - 1:
        farthest = 0
        for i in range(l, r + 1):
            farthest = max(farthest, i + nums[i])
        l = r + 1
        r = farthest
        jumps += 1
    return jumps

# ----------------------------------------------------------------------------
# Problem: Gas Station (LeetCode: gas-station)
# ----------------------------------------------------------------------------
def canCompleteCircuit(gas: list[int], cost: list[int]) -> int:
    # If total fuel is less than total required, circuit is impossible
    if sum(gas) < sum(cost):
        return -1
    total = 0
    start = 0
    for i in range(len(gas)):
        total += gas[i] - cost[i]
        # If tank becomes negative, no station from previous start up to i can work
        if total < 0:
            total = 0
            start = i + 1
    return start

# ----------------------------------------------------------------------------
# Problem: Hand of Straights (LeetCode: hand-of-straights)
# ----------------------------------------------------------------------------
from collections import Counter
import heapq

def isNStraightHand(hand: list[int], groupSize: int) -> bool:
    if len(hand) % groupSize != 0:
        return False
    counts = Counter(hand)
    min_heap = list(counts.keys())
    heapq.heapify(min_heap)

    while min_heap:
        first = min_heap[0]
        # Form group of consecutive cards starting from minimum card
        for card in range(first, first + groupSize):
            if counts[card] == 0:
                return False
            counts[card] -= 1
            if counts[card] == 0:
                if card != min_heap[0]:
                    return False
                heapq.heappop(min_heap)
    return True

# ----------------------------------------------------------------------------
# Problem: Merge Triplets to Form Target Triplet (LeetCode: merge-triplets-to-form-target-triplet)
# ----------------------------------------------------------------------------
def mergeTriplets(triplets: list[list[int]], target: list[int]) -> bool:
    matched = set()  # Tracks component indices [0, 1, 2] satisfied
    for t in triplets:
        # Ignore triplet if any coordinate strictly exceeds target boundary
        if t[0] > target[0] or t[1] > target[1] or t[2] > target[2]:
            continue
        for i in range(3):
            if t[i] == target[i]:
                matched.add(i)
    return len(matched) == 3

# ----------------------------------------------------------------------------
# Problem: Partition Labels (LeetCode: partition-labels)
# ----------------------------------------------------------------------------
def partitionLabels(s: str) -> list[int]:
    # Record the last occurrence index for every character
    last = {c: i for i, c in enumerate(s)}
    res = []
    start = 0
    end = 0

    for i, c in enumerate(s):
        end = max(end, last[c])
        # Current index reached the maximum extent of all characters in partition
        if i == end:
            res.append(end - start + 1)
            start = i + 1
    return res

# ----------------------------------------------------------------------------
# Problem: Valid Parenthesis String (LeetCode: valid-parenthesis-string)
# ----------------------------------------------------------------------------
def checkValidString(s: str) -> bool:
    # Range of possible open parentheses: [cmin, cmax]
    cmin, cmax = 0, 0
    for c in s:
        if c == "(":
            cmin += 1
            cmax += 1
        elif c == ")":
            cmin -= 1
            cmax -= 1
        else: # c == '*' (can be '(', ')', or '')
            cmin -= 1
            cmax += 1
        if cmax < 0:
            return False  # More ')' than '(' possible
        cmin = max(cmin, 0)
    return cmin == 0

