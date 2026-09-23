"""Chapter 33: NeetCode 150 - 2-D Dynamic Programming"""
from __future__ import annotations
import math
import heapq
import bisect
from collections import defaultdict, deque, Counter, OrderedDict
from typing import Optional, List, Dict, Set, Tuple

# ----------------------------------------------------------------------------
# Problem: Unique Paths (LeetCode: unique-paths)
# ----------------------------------------------------------------------------
def uniquePaths(m: int, n: int) -> int:
    # 1D space-optimized DP representing previous row
    row = [1] * n
    for _ in range(m - 1):
        new_row = [1] * n
        # new_row[j] = paths from above (row[j]) + paths from left (new_row[j-1])
        for j in range(1, n):
            new_row[j] = new_row[j - 1] + row[j]
        row = new_row
    return row[-1]

# ----------------------------------------------------------------------------
# Problem: Longest Common Subsequence (LeetCode: longest-common-subsequence)
# ----------------------------------------------------------------------------
def longestCommonSubsequence(text1: str, text2: str) -> int:
    m, n = len(text1), len(text2)
    # 2D table where dp[i][j] = LCS of text1[i:] and text2[j:]
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            if text1[i] == text2[j]:
                dp[i][j] = 1 + dp[i + 1][j + 1]  # Diagonal transition
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j + 1])
    return dp[0][0]

# ----------------------------------------------------------------------------
# Problem: Best Time to Buy and Sell Stock with Cooldown (LeetCode: best-time-to-buy-and-sell-stock-with-cooldown)
# ----------------------------------------------------------------------------
def maxProfit(prices: list[int]) -> int:
    # Finite State Machine:
    # held: currently holding a stock
    # sold: sold stock today (forces mandatory 1-day cooldown)
    # rest: ready to buy
    held = float('-inf')
    sold = 0
    rest = 0

    for p in prices:
        prev_sold = sold
        sold = held + p             # Sell held stock
        held = max(held, rest - p)  # Buy new stock from rest state
        rest = max(rest, prev_sold) # Rest or recover from cooldown
    return max(sold, rest)

# ----------------------------------------------------------------------------
# Problem: Coin Change II (LeetCode: coin-change-ii)
# ----------------------------------------------------------------------------
def change(amount: int, coins: list[int]) -> int:
    # dp[a] = combinations of coins to make amount a
    dp = [0] * (amount + 1)
    dp[0] = 1  # 1 way to make amount 0 (choose no coins)

    for c in coins:
        # Loop forward to allow unlimited usage of coin c
        for a in range(c, amount + 1):
            dp[a] += dp[a - c]
    return dp[amount]

# ----------------------------------------------------------------------------
# Problem: Target Sum (LeetCode: target-sum)
# ----------------------------------------------------------------------------
from collections import defaultdict

def findTargetSumWays(nums: list[int], target: int) -> int:
    # dp maps sum -> number of ways to achieve it
    dp = defaultdict(int)
    dp[0] = 1

    for n in nums:
        next_dp = defaultdict(int)
        for cur_sum, count in dp.items():
            next_dp[cur_sum + n] += count
            next_dp[cur_sum - n] += count
        dp = next_dp
    return dp[target]

# ----------------------------------------------------------------------------
# Problem: Interleaving String (LeetCode: interleaving-string)
# ----------------------------------------------------------------------------
def isInterleave(s1: str, s2: str, s3: str) -> bool:
    if len(s1) + len(s2) != len(s3):
        return False
    # 2D DP grid: dp[i][j] checks if s1[:i] and s2[:j] interleave into s3[:i+j]
    dp = [[False] * (len(s2) + 1) for _ in range(len(s1) + 1)]
    dp[0][0] = True

    for i in range(len(s1) + 1):
        for j in range(len(s2) + 1):
            if i > 0 and s1[i - 1] == s3[i + j - 1] and dp[i - 1][j]:
                dp[i][j] = True
            if j > 0 and s2[j - 1] == s3[i + j - 1] and dp[i][j - 1]:
                dp[i][j] = True
    return dp[len(s1)][len(s2)]

# ----------------------------------------------------------------------------
# Problem: Longest Increasing Path in a Matrix (LeetCode: longest-increasing-path-in-a-matrix)
# ----------------------------------------------------------------------------
def longestIncreasingPath(matrix: list[list[int]]) -> int:
    ROWS, COLS = len(matrix), len(matrix[0])
    memo = {}  # (r, c) -> longest increasing path starting at (r, c)

    def dfs(r: int, c: int) -> int:
        if (r, c) in memo:
            return memo[(r, c)]
        res = 1
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and matrix[nr][nc] > matrix[r][c]:
                res = max(res, 1 + dfs(nr, nc))
        memo[(r, c)] = res
        return res

    for r in range(ROWS):
        for c in range(COLS):
            dfs(r, c)
    return max(memo.values())

# ----------------------------------------------------------------------------
# Problem: Distinct Subsequences (LeetCode: distinct-subsequences)
# ----------------------------------------------------------------------------
def numDistinct(s: str, t: str) -> int:
    m, n = len(s), len(t)
    # dp[i][j] = distinct subsequences of s[i:] matching t[j:]
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][n] = 1  # Base case: empty t matches any suffix

    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            # Skip character s[i]
            dp[i][j] = dp[i + 1][j]
            # Match character s[i] with t[j]
            if s[i] == t[j]:
                dp[i][j] += dp[i + 1][j + 1]
    return dp[0][0]

# ----------------------------------------------------------------------------
# Problem: Edit Distance (LeetCode: edit-distance)
# ----------------------------------------------------------------------------
def minDistance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    # dp[i][j] = min operations to convert word1[i:] to word2[j:]
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1): dp[i][n] = m - i
    for j in range(n + 1): dp[m][j] = n - j

    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            if word1[i] == word2[j]:
                dp[i][j] = dp[i + 1][j + 1]  # Characters match, 0 cost
            else:
                # 1 + min(Insert: dp[i][j+1], Delete: dp[i+1][j], Replace: dp[i+1][j+1])
                dp[i][j] = 1 + min(dp[i][j + 1], dp[i + 1][j], dp[i + 1][j + 1])
    return dp[0][0]

# ----------------------------------------------------------------------------
# Problem: Burst Balloons (LeetCode: burst-balloons)
# ----------------------------------------------------------------------------
def maxCoins(nums: list[int]) -> int:
    # Pad boundaries with 1s: [1] + nums + [1]
    A = [1] + [x for x in nums if x > 0] + [1]
    n = len(A)
    # dp[l][r] = max coins from bursting all balloons strictly between index l and r
    dp = [[0] * n for _ in range(n)]

    # Iterate over window lengths from 2 up to n
    for length in range(2, n):
        for l in range(0, n - length):
            r = l + length
            # k is the LAST balloon burst in subarray (l, r)
            for k in range(l + 1, r):
                coins = A[l] * A[k] * A[r] + dp[l][k] + dp[k][r]
                if coins > dp[l][r]:
                    dp[l][r] = coins
    return dp[0][n - 1]

# ----------------------------------------------------------------------------
# Problem: Regular Expression Matching (LeetCode: regular-expression-matching)
# ----------------------------------------------------------------------------
def isMatch(s: str, p: str) -> bool:
    memo = {}

    def dfs(i: int, j: int) -> bool:
        if (i, j) in memo:
            return memo[(i, j)]
        if i >= len(s) and j >= len(p):
            return True
        if j >= len(p):
            return False

        match = i < len(s) and (s[i] == p[j] or p[j] == ".")
        if (j + 1) < len(p) and p[j + 1] == "*":
            # Branch 1: Skip '*' and previous char (0 occurrences)
            # Branch 2: Consume 1 occurrence of matching char
            ans = dfs(i, j + 2) or (match and dfs(i + 1, j))
        else:
            ans = match and dfs(i + 1, j + 1)

        memo[(i, j)] = ans
        return ans

    return dfs(0, 0)

