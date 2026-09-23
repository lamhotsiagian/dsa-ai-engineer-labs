"""LeetCode Solutions for chapter_20."""
from __future__ import annotations

# ----------------------------------------------------------------------------
# Problem: Climbing Stairs (LeetCode 70) [\LTwo]
# ----------------------------------------------------------------------------
def climb_stairs(n: int) -> int:
    if n <= 2:
        return n
    first, second = 1, 2
    for _ in range(3, n + 1):
        first, second = second, first + second
    return second

# ----------------------------------------------------------------------------
# Problem: Coin Change (LeetCode 322) [\LThree]
# ----------------------------------------------------------------------------
def coin_change(coins: list[int], amount: int) -> int:
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0

    for c in coins:
        for i in range(c, amount + 1):
            if dp[i - c] + 1 < dp[i]:
                dp[i] = dp[i - c] + 1

    return dp[amount] if dp[amount] != float("inf") else -1

# ----------------------------------------------------------------------------
# Problem: Edit Distance (LeetCode 72) [\LFour]
# ----------------------------------------------------------------------------
def min_distance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    # 1D row DP optimization
    prev = list(range(n + 1))

    for i in range(1, m + 1):
        curr = [i] + [0] * n
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                curr[j] = prev[j - 1]
            else:
                curr[j] = 1 + min(prev[j], curr[j - 1], prev[j - 1])
        prev = curr

    return prev[n]

