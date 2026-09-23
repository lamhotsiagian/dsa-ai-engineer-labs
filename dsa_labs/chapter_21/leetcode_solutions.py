"""LeetCode Solutions for chapter_21."""
from __future__ import annotations

# ----------------------------------------------------------------------------
# Problem: Number of 1 Bits (LeetCode 191) [\LTwo]
# ----------------------------------------------------------------------------
def hamming_weight(n: int) -> int:
    count = 0
    while n > 0:
        n &= (n - 1)  # Clear the lowest set bit
        count += 1
    return count

# ----------------------------------------------------------------------------
# Problem: Single Number II (LeetCode 137) [\LThree]
# ----------------------------------------------------------------------------
def single_number(nums: list[int]) -> int:
    ones, twos = 0, 0
    for x in nums:
        # ones holds bits appearing 1 or 4 or 7 times
        ones = (ones ^ x) & ~twos
        # twos holds bits appearing 2 or 5 or 8 times
        twos = (twos ^ x) & ~ones
    return ones

# ----------------------------------------------------------------------------
# Problem: Divide Two Integers (LeetCode 29) [\LFour]
# ----------------------------------------------------------------------------
def divide(dividend: int, divisor: int) -> int:
    INT_MAX = 2**31 - 1
    INT_MIN = -2**31

    # Overflow case
    if dividend == INT_MIN and divisor == -1:
        return INT_MAX

    sign = -1 if (dividend < 0) ^ (divisor < 0) else 1
    dvd, dvs = abs(dividend), abs(divisor)
    quotient = 0

    while dvd >= dvs:
        temp_dvs = dvs
        multiple = 1
        while dvd >= (temp_dvs << 1):
            temp_dvs <<= 1
            multiple <<= 1
        dvd -= temp_dvs
        quotient += multiple

    return max(INT_MIN, min(INT_MAX, sign * quotient))

