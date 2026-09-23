"""LeetCode Solutions for chapter_25."""
from __future__ import annotations

# ----------------------------------------------------------------------------
# Problem: Range Sum Query via Binary Indexed Tree (LeetCode 303/Fenwick) [\LTwo]
# ----------------------------------------------------------------------------
class NumArrayFenwick:
    def __init__(self, nums: list[int]):
        self.n = len(nums)
        self.tree = [0] * (self.n + 1)
        for i, val in enumerate(nums):
            self._add(i + 1, val)

    def _add(self, idx: int, val: int) -> None:
        while idx <= self.n:
            self.tree[idx] += val
            idx += idx & (-idx)

    def _prefix_sum(self, idx: int) -> int:
        s = 0
        while idx > 0:
            s += self.tree[idx]
            idx -= idx & (-idx)
        return s

    def sumRange(self, left: int, right: int) -> int:
        return self._prefix_sum(right + 1) - self._prefix_sum(left)

# ----------------------------------------------------------------------------
# Problem: Range Sum Query --- Mutable (LeetCode 307) [\LThree]
# ----------------------------------------------------------------------------
class NumArray:
    def __init__(self, nums: list[int]):
        self.n = len(nums)
        self.nums = nums[:]
        self.tree = [0] * (self.n + 1)
        for i, val in enumerate(nums):
            self._add(i + 1, val)

    def _add(self, idx: int, delta: int) -> None:
        while idx <= self.n:
            self.tree[idx] += delta
            idx += idx & (-idx)

    def _query(self, idx: int) -> int:
        total = 0
        while idx > 0:
            total += self.tree[idx]
            idx -= idx & (-idx)
        return total

    def update(self, index: int, val: int) -> None:
        delta = val - self.nums[index]
        self.nums[index] = val
        self._add(index + 1, delta)

    def sumRange(self, left: int, right: int) -> int:
        return self._query(right + 1) - self._query(left)

# ----------------------------------------------------------------------------
# Problem: Count of Smaller Numbers After Self (LeetCode 315) [\LFour]
# ----------------------------------------------------------------------------
def count_smaller(nums: list[int]) -> list[int]:
    # Coordinate compression
    sorted_unique = sorted(set(nums))
    rank_map = {val: i + 1 for i, val in enumerate(sorted_unique)}
    m = len(sorted_unique)

    tree = [0] * (m + 1)

    def add(idx: int, val: int) -> None:
        while idx <= m:
            tree[idx] += val
            idx += idx & (-idx)

    def query(idx: int) -> int:
        total = 0
        while idx > 0:
            total += tree[idx]
            idx -= idx & (-idx)
        return total

    counts = []
    # Traverse from right to left
    for num in reversed(nums):
        r = rank_map[num]
        counts.append(query(r - 1))
        add(r, 1)

    return counts[::-1]

