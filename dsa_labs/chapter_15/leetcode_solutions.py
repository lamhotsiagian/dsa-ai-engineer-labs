"""LeetCode Solutions for chapter_15."""
from __future__ import annotations

# ----------------------------------------------------------------------------
# Problem: Binary Search (LeetCode 704) [\LTwo]
# ----------------------------------------------------------------------------
def search(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# ----------------------------------------------------------------------------
# Problem: Search in Rotated Sorted Array (LeetCode 33) [\LThree]
# ----------------------------------------------------------------------------
def search_rotated(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid

        # Left half is normally sorted
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        # Right half is normally sorted
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1

    return -1

# ----------------------------------------------------------------------------
# Problem: Median of Two Sorted Arrays (LeetCode 4) [\LFour]
# ----------------------------------------------------------------------------
def find_median_sorted_arrays(nums1: list[int], nums2: list[int]) -> float:
    # Always binary search on smaller array
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    m, n = len(nums1), len(nums2)
    left, right = 0, m

    while left <= right:
        part1 = (left + right) // 2
        part2 = (m + n + 1) // 2 - part1

        max_left1 = float("-inf") if part1 == 0 else nums1[part1 - 1]
        min_right1 = float("inf") if part1 == m else nums1[part1]

        max_left2 = float("-inf") if part2 == 0 else nums2[part2 - 1]
        min_right2 = float("inf") if part2 == n else nums2[part2]

        if max_left1 <= min_right2 and max_left2 <= min_right1:
            if (m + n) % 2 == 1:
                return float(max(max_left1, max_left2))
            return (max(max_left1, max_left2) + min(min_right1, min_right2)) / 2.0
        elif max_left1 > min_right2:
            right = part1 - 1
        else:
            left = part1 + 1

    return 0.0

