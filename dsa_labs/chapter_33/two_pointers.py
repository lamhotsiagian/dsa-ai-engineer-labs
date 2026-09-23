"""Chapter 33: NeetCode 150 - Two Pointers"""
from __future__ import annotations
import math
import heapq
import bisect
from collections import defaultdict, deque, Counter, OrderedDict
from typing import Optional, List, Dict, Set, Tuple

# ----------------------------------------------------------------------------
# Problem: Valid Palindrome (LeetCode: valid-palindrome)
# ----------------------------------------------------------------------------
def isPalindrome(s: str) -> bool:
    # Converging two pointers from opposite ends
    l, r = 0, len(s) - 1
    while l < r:
        # Advance left pointer over non-alphanumeric characters
        while l < r and not s[l].isalnum():
            l += 1
        # Decrement right pointer over non-alphanumeric characters
        while l < r and not s[r].isalnum():
            r -= 1
        # Compare normalized lowercase characters
        if s[l].lower() != s[r].lower():
            return False
        l += 1
        r -= 1
    return True

# ----------------------------------------------------------------------------
# Problem: Two Sum II - Input Array Is Sorted (LeetCode: two-sum-ii-input-array-is-sorted)
# ----------------------------------------------------------------------------
def twoSum(numbers: list[int], target: int) -> list[int]:
    # Since array is sorted, narrow window from both ends
    l, r = 0, len(numbers) - 1
    while l < r:
        curr_sum = numbers[l] + numbers[r]
        if curr_sum == target:
            # 1-indexed response required by problem specification
            return [l + 1, r + 1]
        elif curr_sum < target:
            l += 1  # Need larger sum, move left pointer right
        else:
            r -= 1  # Need smaller sum, move right pointer left
    return []

# ----------------------------------------------------------------------------
# Problem: 3Sum (LeetCode: 3sum)
# ----------------------------------------------------------------------------
def threeSum(nums: list[int]) -> list[list[int]]:
    nums.sort()  # Sort to enable two-pointer scans and duplicate skipping
    res = []
    n = len(nums)
    for i in range(n - 2):
        # Optimization: if smallest number > 0, sum cannot equal 0
        if nums[i] > 0:
            break
        # Skip duplicate values for the first element
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        l, r = i + 1, n - 1
        while l < r:
            s = nums[i] + nums[l] + nums[r]
            if s == 0:
                res.append([nums[i], nums[l], nums[r]])
                # Skip duplicate values for left and right pointers
                while l < r and nums[l] == nums[l + 1]:
                    l += 1
                while l < r and nums[r] == nums[r - 1]:
                    r -= 1
                l += 1
                r -= 1
            elif s < 0:
                l += 1
            else:
                r -= 1
    return res

# ----------------------------------------------------------------------------
# Problem: Container With Most Water (LeetCode: container-with-most-water)
# ----------------------------------------------------------------------------
def maxArea(height: list[int]) -> int:
    l, r = 0, len(height) - 1
    max_water = 0
    while l < r:
        width = r - l
        # Volume bounded by the shorter line
        h = min(height[l], height[r])
        max_water = max(max_water, width * h)
        # Greedily discard the shorter wall (it cannot support larger area)
        if height[l] < height[r]:
            l += 1
        else:
            r -= 1
    return max_water

# ----------------------------------------------------------------------------
# Problem: Trapping Rain Water (LeetCode: trapping-rain-water)
# ----------------------------------------------------------------------------
def trap(height: list[int]) -> int:
    if not height:
        return 0
    l, r = 0, len(height) - 1
    max_l, max_r = height[l], height[r]
    water = 0
    while l < r:
        # Water level is always constrained by the smaller boundary maximum
        if max_l <= max_r:
            l += 1
            max_l = max(max_l, height[l])
            water += max_l - height[l]  # Trapped water above bar l
        else:
            r -= 1
            max_r = max(max_r, height[r])
            water += max_r - height[r]  # Trapped water above bar r
    return water

