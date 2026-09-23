"""Chapter 33: NeetCode 150 - Stack"""
from __future__ import annotations
import math
import heapq
import bisect
from collections import defaultdict, deque, Counter, OrderedDict
from typing import Optional, List, Dict, Set, Tuple

# ----------------------------------------------------------------------------
# Problem: Valid Parentheses (LeetCode: valid-parentheses)
# ----------------------------------------------------------------------------
def isValid(s: str) -> bool:
    if len(s) % 2 != 0:
        return False
    stack = []
    # Map closing bracket to its required matching opening bracket
    pairs = {')': '(', '}': '{', ']': '['}
    for c in s:
        if c in pairs:
            # Check if top of stack matches the expected opener
            if not stack or stack[-1] != pairs[c]:
                return False
            stack.pop()
        else:
            # Push opening bracket onto stack
            stack.append(c)
    # Stack must be completely empty if all brackets closed properly
    return not stack

# ----------------------------------------------------------------------------
# Problem: Min Stack (LeetCode: min-stack)
# ----------------------------------------------------------------------------
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []  # Tracks minimum value at corresponding height

    def push(self, val: int) -> None:
        self.stack.append(val)
        # Record new minimum (either current val or previous min)
        curr_min = min(val, self.min_stack[-1] if self.min_stack else val)
        self.min_stack.append(curr_min)

    def pop(self) -> None:
        self.stack.pop()
        self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]

# ----------------------------------------------------------------------------
# Problem: Evaluate Reverse Polish Notation (LeetCode: evaluate-reverse-polish-notation)
# ----------------------------------------------------------------------------
def evalRPN(tokens: list[str]) -> int:
    stack = []
    for token in tokens:
        if token in {"+", "-", "*", "/"}:
            # Pop operands in reverse order (b was second operand)
            b = stack.pop()
            a = stack.pop()
            if token == "+": stack.append(a + b)
            elif token == "-": stack.append(a - b)
            elif token == "*": stack.append(a * b)
            else: stack.append(int(a / b))  # Truncate toward zero
        else:
            stack.append(int(token))
    return stack[0]

# ----------------------------------------------------------------------------
# Problem: Generate Parentheses (LeetCode: generate-parentheses)
# ----------------------------------------------------------------------------
def generateParenthesis(n: int) -> list[str]:
    res = []
    stack = []

    def backtrack(open_c: int, close_c: int) -> None:
        # Base case: valid string of length 2n constructed
        if open_c == close_c == n:
            res.append("".join(stack))
            return
        # Choice 1: Add opening parenthesis if budget remains
        if open_c < n:
            stack.append("(")
            backtrack(open_c + 1, close_c)
            stack.pop()
        # Choice 2: Add closing parenthesis only if it doesn't exceed open brackets
        if close_c < open_c:
            stack.append(")")
            backtrack(open_c, close_c + 1)
            stack.pop()

    backtrack(0, 0)
    return res

# ----------------------------------------------------------------------------
# Problem: Daily Temperatures (LeetCode: daily-temperatures)
# ----------------------------------------------------------------------------
def dailyTemperatures(temperatures: list[int]) -> list[int]:
    n = len(temperatures)
    res = [0] * n
    # Monotonic decreasing stack storing indices: [index]
    stack = []
    for i, t in enumerate(temperatures):
        # Resolve wait time for all previous days colder than today
        while stack and temperatures[stack[-1]] < t:
            prev_idx = stack.pop()
            res[prev_idx] = i - prev_idx
        stack.append(i)
    return res

# ----------------------------------------------------------------------------
# Problem: Car Fleet (LeetCode: car-fleet)
# ----------------------------------------------------------------------------
def carFleet(target: int, position: list[int], speed: list[int]) -> int:
    # Pair position with speed and sort in descending order of starting position
    cars = sorted(zip(position, speed), reverse=True)
    stack = []  # Stores arrival times of distinct car fleets
    for pos, spd in cars:
        time = (target - pos) / spd
        # If car arrives strictly later than fleet ahead, it forms a new fleet
        if not stack or time > stack[-1]:
            stack.append(time)
        # Otherwise, it catches up and merges into the existing fleet ahead
    return len(stack)

# ----------------------------------------------------------------------------
# Problem: Largest Rectangle in Histogram (LeetCode: largest-rectangle-in-histogram)
# ----------------------------------------------------------------------------
def largestRectangleArea(heights: list[int]) -> int:
    max_area = 0
    # Monotonic increasing stack storing pairs of (start_index, height)
    stack = []
    for i, h in enumerate(heights):
        start = i
        # Pop bars taller than current bar and calculate their maximum rectangle
        while stack and stack[-1][1] > h:
            prev_idx, prev_h = stack.pop()
            max_area = max(max_area, prev_h * (i - prev_idx))
            start = prev_idx  # Current bar can extend back to popped bar's start
        stack.append((start, h))
    
    # Process remaining bars in stack that extend to the rightmost boundary
    n = len(heights)
    for idx, h in stack:
        max_area = max(max_area, h * (n - idx))
    return max_area

