"""Chapter 33: NeetCode 150 - Binary Search"""
from __future__ import annotations
import math
import heapq
import bisect
from collections import defaultdict, deque, Counter, OrderedDict
from typing import Optional, List, Dict, Set, Tuple

# ----------------------------------------------------------------------------
# Problem: Binary Search (LeetCode: binary-search)
# ----------------------------------------------------------------------------
def search(nums: list[int], target: int) -> int:
    l, r = 0, len(nums) - 1
    while l <= r:
        # Avoid potential integer overflow with midpoint formula
        mid = l + (r - l) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            l = mid + 1  # Target is in the right half
        else:
            r = mid - 1  # Target is in the left half
    return -1

# ----------------------------------------------------------------------------
# Problem: Search a 2D Matrix (LeetCode: search-a-2d-matrix)
# ----------------------------------------------------------------------------
def searchMatrix(matrix: list[list[int]], target: int) -> bool:
    if not matrix or not matrix[0]:
        return False
    m, n = len(matrix), len(matrix[0])
    l, r = 0, m * n - 1
    # Treat 2D matrix as a virtual 1D flattened sorted array
    while l <= r:
        mid = l + (r - l) // 2
        row, col = mid // n, mid % n
        mid_val = matrix[row][col]
        if mid_val == target:
            return True
        elif mid_val < target:
            l = mid + 1
        else:
            r = mid - 1
    return False

# ----------------------------------------------------------------------------
# Problem: Koko Eating Bananas (LeetCode: koko-eating-bananas)
# ----------------------------------------------------------------------------
import math

def minEatingSpeed(piles: list[int], h: int) -> int:
    # Binary search on eating speed k: range [1, max(piles)]
    l, r = 1, max(piles)
    res = r
    while l <= r:
        k = l + (r - l) // 2
        # Calculate total hours needed at speed k
        total_hours = sum(math.ceil(pile / k) for pile in piles)
        if total_hours <= h:
            res = k      # Valid speed, try to find a slower viable speed
            r = k - 1
        else:
            l = k + 1    # Too slow, need to eat faster
    return res

# ----------------------------------------------------------------------------
# Problem: Find Minimum in Rotated Sorted Array (LeetCode: find-minimum-in-rotated-sorted-array)
# ----------------------------------------------------------------------------
def findMin(nums: list[int]) -> int:
    l, r = 0, len(nums) - 1
    # Pivot condition: stop when search range narrows to single minimum
    while l < r:
        mid = l + (r - l) // 2
        # If mid element is strictly greater than right element,
        # the inflection (minimum) must reside in right half
        if nums[mid] > nums[r]:
            l = mid + 1
        else:
            # Minimum is at mid or in left half
            r = mid
    return nums[l]

# ----------------------------------------------------------------------------
# Problem: Search in Rotated Sorted Array (LeetCode: search-in-rotated-sorted-array)
# ----------------------------------------------------------------------------
def search(nums: list[int], target: int) -> int:
    l, r = 0, len(nums) - 1
    while l <= r:
        mid = l + (r - l) // 2
        if nums[mid] == target:
            return mid
        # Check if left half is monotonically sorted
        if nums[l] <= nums[mid]:
            # Check if target falls strictly within sorted left half
            if nums[l] <= target < nums[mid]:
                r = mid - 1
            else:
                l = mid + 1
        # Otherwise, right half must be sorted
        else:
            # Check if target falls strictly within sorted right half
            if nums[mid] < target <= nums[r]:
                l = mid + 1
            else:
                r = mid - 1
    return -1

# ----------------------------------------------------------------------------
# Problem: Time Based Key-Value Store (LeetCode: time-based-key-value-store)
# ----------------------------------------------------------------------------
from collections import defaultdict

class TimeMap:
    def __init__(self):
        # Maps key -> list of (timestamp, value) pairs
        self.store = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        # Timestamps are strictly increasing, so list is naturally sorted
        self.store[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        values = self.store.get(key, [])
        l, r = 0, len(values) - 1
        res = ""
        # Binary search for greatest timestamp <= query timestamp
        while l <= r:
            mid = l + (r - l) // 2
            if values[mid][0] <= timestamp:
                res = values[mid][1]
                l = mid + 1  # Look for closer/larger timestamp
            else:
                r = mid - 1
        return res

# ----------------------------------------------------------------------------
# Problem: Median of Two Sorted Arrays (LeetCode: median-of-two-sorted-arrays)
# ----------------------------------------------------------------------------
def findMedianSortedArrays(nums1: list[int], nums2: list[int]) -> float:
    # Ensure binary search is performed on the smaller array for O(log(min(m, n)))
    A, B = nums1, nums2
    if len(A) > len(B):
        A, B = B, A
    total = len(A) + len(B)
    half = total // 2
    l, r = 0, len(A)

    while l <= r:
        i = (l + r) // 2  # Partition size for array A
        j = half - i      # Corresponding partition size for array B
        # Boundary sentinels for edge partitions
        A_left = A[i - 1] if i > 0 else float('-inf')
        A_right = A[i] if i < len(A) else float('inf')
        B_left = B[j - 1] if j > 0 else float('-inf')
        B_right = B[j] if j < len(B) else float('inf')
        
        # Proper partition condition: all left elements <= all right elements
        if A_left <= B_right and B_left <= A_right:
            if total % 2 != 0:
                return float(min(A_right, B_right))
            return (max(A_left, B_left) + min(A_right, B_right)) / 2.0
        elif A_left > B_right:
            r = i - 1  # Too many elements from A; shrink A's partition
        else:
            l = i + 1  # Too few elements from A; expand A's partition
    return 0.0

