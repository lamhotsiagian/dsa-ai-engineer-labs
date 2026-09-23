"""Chapter 33: NeetCode 150 - Heap & Priority Queue"""
from __future__ import annotations
import math
import heapq
import bisect
from collections import defaultdict, deque, Counter, OrderedDict
from typing import Optional, List, Dict, Set, Tuple

# ----------------------------------------------------------------------------
# Problem: Kth Largest Element in a Stream (LeetCode: kth-largest-element-in-a-stream)
# ----------------------------------------------------------------------------
import heapq

class KthLargest:
    def __init__(self, k: int, nums: list[int]):
        self.k = k
        self.min_heap = nums
        heapq.heapify(self.min_heap)
        # Evict smallest elements until heap size is bounded at exactly k
        while len(self.min_heap) > k:
            heapq.heappop(self.min_heap)

    def add(self, val: int) -> int:
        heapq.heappush(self.min_heap, val)
        if len(self.min_heap) > self.k:
            heapq.heappop(self.min_heap)
        # Root of min-heap of size k is the k-th largest element
        return self.min_heap[0]

# ----------------------------------------------------------------------------
# Problem: Last Stone Weight (LeetCode: last-stone-weight)
# ----------------------------------------------------------------------------
import heapq

def lastStoneWeight(stones: list[int]) -> int:
    # Invert signs to simulate a max-heap using Python heapq
    max_heap = [-s for s in stones]
    heapq.heapify(max_heap)

    while len(max_heap) > 1:
        s1 = -heapq.heappop(max_heap)
        s2 = -heapq.heappop(max_heap)
        # If stones have different weights, smash and push difference back
        if s1 != s2:
            heapq.heappush(max_heap, -(s1 - s2))
    return -max_heap[0] if max_heap else 0

# ----------------------------------------------------------------------------
# Problem: K Closest Points to Origin (LeetCode: k-closest-points-to-origin)
# ----------------------------------------------------------------------------
import heapq

def kClosest(points: list[list[int]], k: int) -> list[list[int]]:
    # Max-heap of size k storing: (-dist_squared, x, y)
    max_heap = []
    for x, y in points:
        dist = x * x + y * y
        heapq.heappush(max_heap, (-dist, x, y))
        # Keep heap bounded to k points; furthest point evicted at root
        if len(max_heap) > k:
            heapq.heappop(max_heap)
    return [[x, y] for _, x, y in max_heap]

# ----------------------------------------------------------------------------
# Problem: Kth Largest Element in an Array (LeetCode: kth-largest-element-in-an-array)
# ----------------------------------------------------------------------------
import heapq

def findKthLargest(nums: list[int], k: int) -> int:
    # Maintain a min-heap of size k
    min_heap = []
    for num in nums:
        heapq.heappush(min_heap, num)
        if len(min_heap) > k:
            heapq.heappop(min_heap)
    # The smallest among the k largest elements is the k-th largest overall
    return min_heap[0]

# ----------------------------------------------------------------------------
# Problem: Task Scheduler (LeetCode: task-scheduler)
# ----------------------------------------------------------------------------
from collections import Counter, deque
import heapq

def leastInterval(tasks: list[str], n: int) -> int:
    counts = Counter(tasks)
    # Max-heap tracking task frequencies
    max_heap = [-cnt for cnt in counts.values()]
    heapq.heapify(max_heap)
    
    time = 0
    # Cooldown queue storing pairs: [remaining_count, available_time]
    q = deque()
    while max_heap or q:
        time += 1
        if max_heap:
            cnt = 1 + heapq.heappop(max_heap)
            if cnt != 0:
                q.append([cnt, time + n])
        # Re-queue task once cooling interval n has elapsed
        if q and q[0][1] == time:
            heapq.heappush(max_heap, q.popleft()[0])
    return time

# ----------------------------------------------------------------------------
# Problem: Design Twitter (LeetCode: design-twitter)
# ----------------------------------------------------------------------------
from collections import defaultdict
import heapq

class Twitter:
    def __init__(self):
        self.time = 0
        self.tweets = defaultdict(list)    # userId -> list of [time, tweetId]
        self.following = defaultdict(set)  # userId -> set of followeeIds

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.tweets[userId].append([self.time, tweetId])
        self.time -= 1  # Decrementing time creates natural min-heap ordering

    def getNewsFeed(self, userId: int) -> list[int]:
        res = []
        min_heap = []
        self.following[userId].add(userId)  # Candidate sees their own tweets

        for followee in self.following[userId]:
            if followee in self.tweets and self.tweets[followee]:
                idx = len(self.tweets[followee]) - 1
                t, tid = self.tweets[followee][idx]
                min_heap.append((t, tid, followee, idx - 1))
        heapq.heapify(min_heap)

        # Merge k sorted tweet streams
        while min_heap and len(res) < 10:
            t, tid, followee, idx = heapq.heappop(min_heap)
            res.append(tid)
            if idx >= 0:
                nxt_t, nxt_tid = self.tweets[followee][idx]
                heapq.heappush(min_heap, (nxt_t, nxt_tid, followee, idx - 1))
        return res

    def follow(self, followerId: int, followeeId: int) -> None:
        self.following[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        if followeeId in self.following[followerId]:
            self.following[followerId].remove(followeeId)

# ----------------------------------------------------------------------------
# Problem: Find Median from Data Stream (LeetCode: find-median-from-data-stream)
# ----------------------------------------------------------------------------
import heapq

class MedianFinder:
    def __init__(self):
        # small: max-heap (negated) storing lower half of numbers
        # large: min-heap storing upper half of numbers
        self.small = []
        self.large = []

    def addNum(self, num: int) -> None:
        # Step 1: Push to lower half max-heap
        heapq.heappush(self.small, -num)
        # Step 2: Ensure all small elements <= all large elements
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        # Step 3: Rebalance sizes so len(small) == len(large) or len(small) == len(large) + 1
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        elif len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2.0

