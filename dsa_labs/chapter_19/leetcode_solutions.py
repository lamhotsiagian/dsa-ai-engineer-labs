"""LeetCode Solutions for chapter_19."""
from __future__ import annotations

# ----------------------------------------------------------------------------
# Problem: Best Time to Buy and Sell Stock (LeetCode 121) [\LTwo]
# ----------------------------------------------------------------------------
def max_profit(prices: list[int]) -> int:
    min_price = float("inf")
    best_profit = 0

    for p in prices:
        if p < min_price:
            min_price = p
        elif p - min_price > best_profit:
            best_profit = p - min_price

    return best_profit

# ----------------------------------------------------------------------------
# Problem: Jump Game (LeetCode 55) [\LThree]
# ----------------------------------------------------------------------------
def can_jump(nums: list[int]) -> bool:
    max_reach = 0
    for i, jump in enumerate(nums):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + jump)
        if max_reach >= len(nums) - 1:
            return True
    return True

# ----------------------------------------------------------------------------
# Problem: Candy (LeetCode 135) [\LFour]
# ----------------------------------------------------------------------------
def candy(ratings: list[int]) -> int:
    n = len(ratings)
    candies = [1] * n

    # Left to right pass
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            candies[i] = candies[i - 1] + 1

    # Right to left pass
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            candies[i] = max(candies[i], candies[i + 1] + 1)

    return sum(candies)

