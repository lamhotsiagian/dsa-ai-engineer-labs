"""Problem Template Library (Chapter 30)."""
from __future__ import annotations

class Templates:
    @staticmethod
    def binary_search(nums: list[int], target: int) -> int:
        lo, hi = 0, len(nums) - 1
        while lo <= hi:
            mid = lo + (hi - lo) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return -1

    @staticmethod
    def sliding_window(s: str, k: int) -> int:
        best = 0
        cur = 0
        for i, ch in enumerate(s):
            cur += 1
            if i >= k:
                cur -= 1
            best = max(best, cur)
        return best
