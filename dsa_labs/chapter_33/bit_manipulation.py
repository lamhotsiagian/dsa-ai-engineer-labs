"""Chapter 33: NeetCode 150 - Bit Manipulation"""
from __future__ import annotations
import math
import heapq
import bisect
from collections import defaultdict, deque, Counter, OrderedDict
from typing import Optional, List, Dict, Set, Tuple

# ----------------------------------------------------------------------------
# Problem: Single Number (LeetCode: single-number)
# ----------------------------------------------------------------------------
def singleNumber(nums: list[int]) -> int:
    # XOR cancellation property: x ^ x = 0 and x ^ 0 = x
    res = 0
    for x in nums:
        res ^= x
    return res

# ----------------------------------------------------------------------------
# Problem: Number of 1 Bits (LeetCode: number-of-1-bits)
# ----------------------------------------------------------------------------
def hammingWeight(n: int) -> int:
    count = 0
    while n:
        # Brian Kernighan's Algorithm: n & (n - 1) clears the lowest set bit
        n &= (n - 1)
        count += 1
    return count

# ----------------------------------------------------------------------------
# Problem: Counting Bits (LeetCode: counting-bits)
# ----------------------------------------------------------------------------
def countBits(n: int) -> list[int]:
    # DP with bit shift: dp[i] = dp[i >> 1] + (i & 1)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i >> 1] + (i & 1)
    return dp

# ----------------------------------------------------------------------------
# Problem: Reverse Bits (LeetCode: reverse-bits)
# ----------------------------------------------------------------------------
def reverseBits(n: int) -> int:
    res = 0
    for _ in range(32):
        # Shift res left and append least significant bit of n
        res = (res << 1) | (n & 1)
        n >>= 1
    return res

# ----------------------------------------------------------------------------
# Problem: Missing Number (LeetCode: missing-number)
# ----------------------------------------------------------------------------
def missingNumber(nums: list[int]) -> int:
    n = len(nums)
    res = n
    # XOR all array indices and array values; missing number remains
    for i, x in enumerate(nums):
        res ^= i ^ x
    return res

# ----------------------------------------------------------------------------
# Problem: Sum of Two Integers (LeetCode: sum-of-two-integers)
# ----------------------------------------------------------------------------
def getSum(a: int, b: int) -> int:
    # 32-bit integer mask for Python two's complement emulation
    mask = 0xFFFFFFFF
    while b != 0:
        carry = (a & b) << 1
        a = (a ^ b) & mask      # Sum without carry
        b = carry & mask        # Shifted carry
    # Handle negative numbers beyond 32-bit boundary
    return a if a <= 0x7FFFFFFF else ~(a ^ mask)

# ----------------------------------------------------------------------------
# Problem: Reverse Integer (LeetCode: reverse-integer)
# ----------------------------------------------------------------------------
def reverse(x: int) -> int:
    sign = -1 if x < 0 else 1
    x = abs(x)
    res = 0
    # 32-bit signed limits: [-2^31, 2^31 - 1]
    MAX_INT = 2**31 - 1

    while x != 0:
        digit = x % 10
        x //= 10
        # Check for 32-bit overflow before multiplying
        if res > MAX_INT // 10 or (res == MAX_INT // 10 and digit > 7):
            return 0
        res = res * 10 + digit
    return sign * res

