"""LeetCode Solutions for chapter_05."""
from __future__ import annotations

# ----------------------------------------------------------------------------
# Problem: Range Sum Query --- Immutable (LeetCode 303) [\LTwo]
# ----------------------------------------------------------------------------
class NumArray:
    def __init__(self, nums: list[int]):
        self.prefix = [0] * (len(nums) + 1)
        for i, val in enumerate(nums):
            self.prefix[i + 1] = self.prefix[i] + val

    def sumRange(self, left: int, right: int) -> int:
        return self.prefix[right + 1] - self.prefix[left]

# ----------------------------------------------------------------------------
# Problem: Subarray Sum Equals K (LeetCode 560) [\LThree]
# ----------------------------------------------------------------------------
def subarray_sum(nums: list[int], k: int) -> int:
    count = 0
    current_sum = 0
    prefix_counts: dict[int, int] = {0: 1}

    for num in nums:
        current_sum += num
        needed = current_sum - k
        if needed in prefix_counts:
            count += prefix_counts[needed]
        prefix_counts[current_sum] = prefix_counts.get(current_sum, 0) + 1

    return count

# ----------------------------------------------------------------------------
# Problem: Number of Submatrices That Sum to Target (LeetCode 1074) [\LFour]
# ----------------------------------------------------------------------------
def num_submatrix_sum_target(matrix: list[list[int]], target: int) -> int:
    R, C = len(matrix), len(matrix[0])
    for r in range(R):
        for c in range(1, C):
            matrix[r][c] += matrix[r][c - 1]

    total_count = 0
    for c1 in range(C):
        for c2 in range(c1, C):
            prefix_counts = {0: 1}
            current_sum = 0
            for r in range(R):
                row_val = matrix[r][c2] - (matrix[r][c1 - 1] if c1 > 0 else 0)
                current_sum += row_val
                total_count += prefix_counts.get(current_sum - target, 0)
                prefix_counts[current_sum] = prefix_counts.get(current_sum, 0) + 1

    return total_count

