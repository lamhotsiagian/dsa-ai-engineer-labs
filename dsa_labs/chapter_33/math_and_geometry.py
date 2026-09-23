"""Chapter 33: NeetCode 150 - Math & Geometry"""
from __future__ import annotations
import math
import heapq
import bisect
from collections import defaultdict, deque, Counter, OrderedDict
from typing import Optional, List, Dict, Set, Tuple

# ----------------------------------------------------------------------------
# Problem: Happy Number (LeetCode: happy-number)
# ----------------------------------------------------------------------------
def isHappy(n: int) -> bool:
    def get_sum(num: int) -> int:
        s = 0
        while num > 0:
            digit = num % 10
            s += digit * digit
            num //= 10
        return s

    # Floyd's Cycle Detection on digit square sums
    slow, fast = n, get_sum(n)
    while fast != 1 and slow != fast:
        slow = get_sum(slow)
        fast = get_sum(get_sum(fast))
    return fast == 1

# ----------------------------------------------------------------------------
# Problem: Plus One (LeetCode: plus-one)
# ----------------------------------------------------------------------------
def plusOne(digits: list[int]) -> list[int]:
    # Work right to left adding carry
    for i in range(len(digits) - 1, -1, -1):
        if digits[i] < 9:
            digits[i] += 1
            return digits
        digits[i] = 0
    # If all digits were 9 (e.g., [9, 9] -> [1, 0, 0])
    return [1] + digits

# ----------------------------------------------------------------------------
# Problem: Rotate Image (LeetCode: rotate-image)
# ----------------------------------------------------------------------------
def rotate(matrix: list[list[int]]) -> None:
    # Rotate 90 degrees clockwise in-place:
    # 1. Transpose the matrix across the main diagonal
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    # 2. Reverse each row horizontally
    for i in range(n):
        matrix[i].reverse()

# ----------------------------------------------------------------------------
# Problem: Spiral Matrix (LeetCode: spiral-matrix)
# ----------------------------------------------------------------------------
def spiralOrder(matrix: list[list[int]]) -> list[int]:
    res = []
    top, bottom = 0, len(matrix)
    left, right = 0, len(matrix[0])

    while left < right and top < bottom:
        # Traverse top row left -> right
        for c in range(left, right): res.append(matrix[top][c])
        top += 1
        # Traverse right column top -> bottom
        for r in range(top, bottom): res.append(matrix[r][right - 1])
        right -= 1
        if not (left < right and top < bottom): break
        # Traverse bottom row right -> left
        for c in range(right - 1, left - 1, -1): res.append(matrix[bottom - 1][c])
        bottom -= 1
        # Traverse left column bottom -> top
        for r in range(bottom - 1, top - 1, -1): res.append(matrix[r][left])
        left += 1
    return res

# ----------------------------------------------------------------------------
# Problem: Set Matrix Zeroes (LeetCode: set-matrix-zeroes)
# ----------------------------------------------------------------------------
def setZeroes(matrix: list[list[int]]) -> None:
    ROWS, COLS = len(matrix), len(matrix[0])
    row_zero = False  # Track if first row needs zeroing

    # Use first row and column as marker storage to achieve O(1) space
    for r in range(ROWS):
        for c in range(COLS):
            if matrix[r][c] == 0:
                matrix[0][c] = 0
                if r > 0: matrix[r][0] = 0
                else: row_zero = True

    # Zero interior cells using markers
    for r in range(1, ROWS):
        for c in range(1, COLS):
            if matrix[0][c] == 0 or matrix[r][0] == 0:
                matrix[r][c] = 0

    # Zero first column if marked
    if matrix[0][0] == 0:
        for r in range(ROWS): matrix[r][0] = 0
    # Zero first row if marked
    if row_zero:
        for c in range(COLS): matrix[0][c] = 0

# ----------------------------------------------------------------------------
# Problem: Pow(x, n) (LeetCode: powx-n)
# ----------------------------------------------------------------------------
def myPow(x: float, n: int) -> float:
    # Binary Exponentiation (Exponentiation by Squaring) in O(log n)
    if n < 0:
        x = 1 / x
        n = -n
    res = 1.0
    curr = x
    while n > 0:
        if n % 2 == 1:
            res *= curr
        curr *= curr  # Square base
        n //= 2       # Halve exponent
    return res

# ----------------------------------------------------------------------------
# Problem: Multiply Strings (LeetCode: multiply-strings)
# ----------------------------------------------------------------------------
def multiply(num1: str, num2: str) -> str:
    if num1 == "0" or num2 == "0":
        return "0"
    m, n = len(num1), len(num2)
    # Result array of max possible length m + n
    res = [0] * (m + n)

    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            mul = int(num1[i]) * int(num2[j])
            p1, p2 = i + j, i + j + 1
            total = mul + res[p2]
            res[p2] = total % 10
            res[p1] += total // 10

    # Skip leading zeros
    i = 0
    while i < len(res) and res[i] == 0:
        i += 1
    return "".join(map(str, res[i:]))

# ----------------------------------------------------------------------------
# Problem: Detect Squares (LeetCode: detect-squares)
# ----------------------------------------------------------------------------
from collections import defaultdict

class DetectSquares:
    def __init__(self):
        self.pts_count = defaultdict(int)
        self.pts = []

    def add(self, point: list[int]) -> None:
        self.pts_count[tuple(point)] += 1
        self.pts.append(point)

    def count(self, point: list[int]) -> int:
        res = 0
        px, py = point
        # For every diagonal point (x, y) that forms a square with (px, py)
        for x, y in self.pts:
            if abs(px - x) != abs(py - y) or px == x or py == y:
                continue
            # Multiply counts of other two corners to form complete square
            res += self.pts_count[(x, py)] * self.pts_count[(px, y)]
        return res

