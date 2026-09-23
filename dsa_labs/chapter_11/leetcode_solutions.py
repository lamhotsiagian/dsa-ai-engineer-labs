"""LeetCode Solutions for chapter_11."""
from __future__ import annotations

# ----------------------------------------------------------------------------
# Problem: Kth Largest Element in a Stream (LeetCode 703) [\LTwo]
# ----------------------------------------------------------------------------
import heapq

class KthLargest:
    def __init__(self, k: int, nums: list[int]):
        self.k = k
        self.min_heap = nums
        heapq.heapify(self.min_heap)
        while len(self.min_heap) > k:
            heapq.heappop(self.min_heap)

    def add(self, val: int) -> int:
        heapq.heappush(self.min_heap, val)
        if len(self.min_heap) > self.k:
            heapq.heappop(self.min_heap)
        return self.min_heap[0]

# ----------------------------------------------------------------------------
# Problem: Kth Largest Element in an Array (LeetCode 215) [\LThree]
# ----------------------------------------------------------------------------
import random

def find_kth_largest(nums: list[int], k: int) -> int:
    target_idx = len(nums) - k

    def quickselect(left: int, right: int) -> int:
        pivot_idx = random.randint(left, right)
        pivot = nums[pivot_idx]
        nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]

        store_idx = left
        for i in range(left, right):
            if nums[i] < pivot:
                nums[store_idx], nums[i] = nums[i], nums[store_idx]
                store_idx += 1
        nums[store_idx], nums[right] = nums[right], nums[store_idx]

        if store_idx == target_idx:
            return nums[store_idx]
        elif store_idx < target_idx:
            return quickselect(store_idx + 1, right)
        else:
            return quickselect(left, store_idx - 1)

    return quickselect(0, len(nums) - 1)

# ----------------------------------------------------------------------------
# Problem: Find Median from Data Stream (LeetCode 295) [\LFour]
# ----------------------------------------------------------------------------
import heapq

class MedianFinder:
    def __init__(self):
        self.small = []  # max-heap (invert signs)
        self.large = []  # min-heap

    def addNum(self, num: int) -> None:
        # Push to max-heap, then balance to min-heap
        heapq.heappush(self.small, -num)
        heapq.heappush(self.large, -heapq.heappop(self.small))

        # Maintain size invariant: small can have at most 1 more item than large
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2.0

