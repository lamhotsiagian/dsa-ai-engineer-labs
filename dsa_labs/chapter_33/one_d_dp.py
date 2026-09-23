"""Chapter 33: NeetCode 150 - 1-D Dynamic Programming"""
from __future__ import annotations
import math
import heapq
import bisect
from collections import defaultdict, deque, Counter, OrderedDict
from typing import Optional, List, Dict, Set, Tuple

# ----------------------------------------------------------------------------
# Problem: Climbing Stairs (LeetCode: climbing-stairs)
# ----------------------------------------------------------------------------
def climbStairs(n: int) -> int:
    # State rolling variables for DP(i) = DP(i-1) + DP(i-2)
    a, b = 1, 1
    for _ in range(n - 1):
        # Shift forward: next step count is sum of previous two
        a, b = b, a + b
    return b

# ----------------------------------------------------------------------------
# Problem: Min Cost Climbing Stairs (LeetCode: min-cost-climbing-stairs)
# ----------------------------------------------------------------------------
def minCostClimbingStairs(cost: list[int]) -> int:
    # Bottom-up DP in-place: work backwards from step n-3 down to 0
    for i in range(len(cost) - 3, -1, -1):
        # Minimum cost from step i is cost[i] plus cheapest of next 1 or 2 steps
        cost[i] += min(cost[i + 1], cost[i + 2])
    # Starting from either index 0 or index 1
    return min(cost[0], cost[1])

# ----------------------------------------------------------------------------
# Problem: House Robber (LeetCode: house-robber)
# ----------------------------------------------------------------------------
def rob(nums: list[int]) -> int:
    # rob1 = max loot up to house i-2; rob2 = max loot up to house i-1
    rob1, rob2 = 0, 0
    for n in nums:
        # Choice: rob current house + rob1, or skip current house (keep rob2)
        new_rob = max(n + rob1, rob2)
        rob1 = rob2
        rob2 = new_rob
    return rob2

# ----------------------------------------------------------------------------
# Problem: House Robber II (LeetCode: house-robber-ii)
# ----------------------------------------------------------------------------
def rob(nums: list[int]) -> int:
    # Houses arranged in a circle: house 1 and house n cannot both be robbed
    if len(nums) == 1:
        return nums[0]

    def simple_rob(arr: list[int]) -> int:
        rob1, rob2 = 0, 0
        for n in arr:
            rob1, rob2 = rob2, max(n + rob1, rob2)
        return rob2

    # Return maximum of excluding first house vs excluding last house
    return max(simple_rob(nums[:-1]), simple_rob(nums[1:]))

# ----------------------------------------------------------------------------
# Problem: Longest Palindromic Substring (LeetCode: longest-palindromic-substring)
# ----------------------------------------------------------------------------
def longestPalindrome(s: str) -> str:
    res = ""
    res_len = 0

    def expand(l: int, r: int) -> None:
        nonlocal res, res_len
        # Expand outwards from center while characters match
        while l >= 0 and r < len(s) and s[l] == s[r]:
            if (r - l + 1) > res_len:
                res = s[l : r + 1]
                res_len = r - l + 1
            l -= 1
            r += 1

    for i in range(len(s)):
        # Odd-length palindromes (single-character center)
        expand(i, i)
        # Even-length palindromes (two-character center)
        expand(i, i + 1)
    return res

# ----------------------------------------------------------------------------
# Problem: Palindromic Substrings (LeetCode: palindromic-substrings)
# ----------------------------------------------------------------------------
def countSubstrings(s: str) -> int:
    count = 0

    def count_pal(l: int, r: int) -> int:
        c = 0
        while l >= 0 and r < len(s) and s[l] == s[r]:
            c += 1
            l -= 1
            r += 1
        return c

    for i in range(len(s)):
        # Accumulate odd-centered and even-centered palindromes
        count += count_pal(i, i)
        count += count_pal(i, i + 1)
    return count

# ----------------------------------------------------------------------------
# Problem: Decode Ways (LeetCode: decode-ways)
# ----------------------------------------------------------------------------
def numDecodings(s: str) -> int:
    # If string starts with '0', no valid decoding exists
    if not s or s[0] == "0":
        return 0
    # dp1 = ways to decode up to i-1, dp2 = ways up to i-2
    dp1, dp2 = 1, 1
    for i in range(1, len(s)):
        curr = 0
        # Single-digit decode ('1' to '9')
        if s[i] != "0":
            curr += dp1
        # Two-digit decode ('10' to '26')
        two_digit = int(s[i - 1 : i + 1])
        if 10 <= two_digit <= 26:
            curr += dp2
        dp2 = dp1
        dp1 = curr
    return dp1

# ----------------------------------------------------------------------------
# Problem: Coin Change (LeetCode: coin-change)
# ----------------------------------------------------------------------------
def coinChange(coins: list[int], amount: int) -> int:
    # dp[a] = minimum coins required to make amount a
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # 0 coins needed for amount 0

    for a in range(1, amount + 1):
        for c in coins:
            if a - c >= 0:
                dp[a] = min(dp[a], 1 + dp[a - c])
    return dp[amount] if dp[amount] != float('inf') else -1

# ----------------------------------------------------------------------------
# Problem: Maximum Product Subarray (LeetCode: maximum-product-subarray)
# ----------------------------------------------------------------------------
def maxProduct(nums: list[int]) -> int:
    res = max(nums)
    cur_min, cur_max = 1, 1

    for n in nums:
        # Negative numbers swap minimum and maximum products
        if n < 0:
            cur_min, cur_max = cur_max, cur_min
        cur_max = max(n, cur_max * n)
        cur_min = min(n, cur_min * n)
        res = max(res, cur_max)
    return res

# ----------------------------------------------------------------------------
# Problem: Word Break (LeetCode: word-break)
# ----------------------------------------------------------------------------
def wordBreak(s: str, wordDict: list[str]) -> bool:
    # dp[i] indicates whether s[i:] can be segmented into dictionary words
    dp = [False] * (len(s) + 1)
    dp[len(s)] = True  # Base case: empty string matches
    words = set(wordDict)

    for i in range(len(s) - 1, -1, -1):
        for w in words:
            if i + len(w) <= len(s) and s[i : i + len(w)] == w:
                if dp[i + len(w)]:
                    dp[i] = True
                    break  # Prune search once valid segmentation found
    return dp[0]

# ----------------------------------------------------------------------------
# Problem: Longest Increasing Subsequence (LeetCode: longest-increasing-subsequence)
# ----------------------------------------------------------------------------
import bisect

def lengthOfLIS(nums: list[int]) -> int:
    # Patience Sorting / Tails array: tails[i] stores smallest tail of LIS of length i+1
    tails = []
    for x in nums:
        idx = bisect.bisect_left(tails, x)
        # If x is strictly greater than all tails, extend the LIS length
        if idx == len(tails):
            tails.append(x)
        # Otherwise, replace existing tail with smaller candidate x
        else:
            tails[idx] = x
    return len(tails)

# ----------------------------------------------------------------------------
# Problem: Partition Equal Subset Sum (LeetCode: partition-equal-subset-sum)
# ----------------------------------------------------------------------------
def canPartition(nums: list[int]) -> bool:
    total = sum(nums)
    # If total sum is odd, cannot partition into two equal integer subsets
    if total % 2 != 0:
        return False
    target = total // 2
    dp = set([0])  # Set storing all achievable subset sums

    for num in nums:
        next_dp = set(dp)
        for t in dp:
            if t + num == target:
                return True
            if t + num < target:
                next_dp.add(t + num)
        dp = next_dp
    return target in dp

