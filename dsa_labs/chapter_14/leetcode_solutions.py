"""LeetCode Solutions for chapter_14."""
from __future__ import annotations

# ----------------------------------------------------------------------------
# Problem: Merge Sorted Array (LeetCode 88) [\LTwo]
# ----------------------------------------------------------------------------
def merge_sorted_array(nums1: list[int], m: int, nums2: list[int], n: int) -> None:
    p1 = m - 1
    p2 = n - 1
    p = m + n - 1

    while p1 >= 0 and p2 >= 0:
        if nums1[p1] > nums2[p2]:
            nums1[p] = nums1[p1]
            p1 -= 1
        else:
            nums1[p] = nums2[p2]
            p2 -= 1
        p -= 1

    # Copy any remaining elements from nums2
    while p2 >= 0:
        nums1[p] = nums2[p2]
        p2 -= 1
        p -= 1

# ----------------------------------------------------------------------------
# Problem: Sort Colors (LeetCode 75) [\LThree]
# ----------------------------------------------------------------------------
def sort_colors(nums: list[int]) -> None:
    low, mid, high = 0, 0, len(nums) - 1

    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1

# ----------------------------------------------------------------------------
# Problem: Maximum Gap (LeetCode 164) [\LFour]
# ----------------------------------------------------------------------------
import math

def maximum_gap(nums: list[int]) -> int:
    if len(nums) < 2:
        return 0

    min_val, max_val = min(nums), max(nums)
    if min_val == max_val:
        return 0

    n = len(nums)
    bucket_size = max(1, (max_val - min_val) // (n - 1))
    bucket_count = (max_val - min_val) // bucket_size + 1

    buckets_min = [float("inf")] * bucket_count
    buckets_max = [float("-inf")] * bucket_count

    for num in nums:
        idx = (num - min_val) // bucket_size
        buckets_min[idx] = min(buckets_min[idx], num)
        buckets_max[idx] = max(buckets_max[idx], num)

    max_gap = 0
    prev_max = min_val

    for i in range(bucket_count):
        if buckets_min[i] == float("inf"):
            continue
        max_gap = max(max_gap, buckets_min[i] - prev_max)
        prev_max = buckets_max[i]

    return max_gap

