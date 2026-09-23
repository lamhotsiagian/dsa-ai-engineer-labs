"""LeetCode Solutions for chapter_04."""
from __future__ import annotations

# ----------------------------------------------------------------------------
# Problem: Remove Element (LeetCode 27) [\LTwo]
# ----------------------------------------------------------------------------
def remove_element(nums: list[int], val: int) -> int:
    """Remove all occurrences of val in-place.
    
    Time O(n), Space O(1).
    """
    write_index = 0
    for read_index in range(len(nums)):
        if nums[read_index] != val:
            nums[write_index] = nums[read_index]
            write_index += 1
    return write_index

# ----------------------------------------------------------------------------
# Problem: Rotate Array (LeetCode 189) [\LThree]
# ----------------------------------------------------------------------------
def rotate(nums: list[int], k: int) -> None:
    """Rotate array to the right by k steps in-place.
    
    Time O(n), Space O(1).
    """
    n = len(nums)
    k = k % n
    if k == 0:
        return

    def reverse_range(left: int, right: int) -> None:
        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1

    reverse_range(0, n - 1)      # 1. Reverse entire array
    reverse_range(0, k - 1)      # 2. Reverse first k elements
    reverse_range(k, n - 1)      # 3. Reverse remaining n-k elements

# ----------------------------------------------------------------------------
# Problem: First Missing Positive (LeetCode 41) [\LFour]
# ----------------------------------------------------------------------------
def first_missing_positive(nums: list[int]) -> int:
    """Find the smallest missing positive integer.
    
    Time O(n), Space O(1).
    """
    n = len(nums)
    for i in range(n):
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            correct_idx = nums[i] - 1
            nums[i], nums[correct_idx] = nums[correct_idx], nums[i]

    for i in range(n):
        if nums[i] != i + 1:
            return i + 1

    return n + 1

