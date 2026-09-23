"""LeetCode Solutions for chapter_09."""
from __future__ import annotations

# ----------------------------------------------------------------------------
# Problem: Valid Parentheses (LeetCode 20) [\LTwo]
# ----------------------------------------------------------------------------
def is_valid_parentheses(s: str) -> bool:
    if len(s) % 2 != 0:
        return False

    matching = {')': '(', '}': '{', ']': '['}
    stack = []

    for char in s:
        if char in matching:
            if not stack or stack.pop() != matching[char]:
                return False
        else:
            stack.append(char)

    return len(stack) == 0

# ----------------------------------------------------------------------------
# Problem: Daily Temperatures (LeetCode 739) [\LThree]
# ----------------------------------------------------------------------------
def daily_temperatures(temperatures: list[int]) -> list[int]:
    n = len(temperatures)
    answer = [0] * n
    stack = []  # indices of unresolved days

    for curr_idx, curr_temp in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < curr_temp:
            prev_idx = stack.pop()
            answer[prev_idx] = curr_idx - prev_idx
        stack.append(curr_idx)

    return answer

# ----------------------------------------------------------------------------
# Problem: Largest Rectangle in Histogram (LeetCode 84) [\LFour]
# ----------------------------------------------------------------------------
def largest_rectangle_area(heights: list[int]) -> int:
    stack = []  # index stack
    max_area = 0
    # Append 0 to flush remaining bars at the end
    extended_heights = heights + [0]

    for i, h in enumerate(extended_heights):
        while stack and extended_heights[stack[-1]] > h:
            height = extended_heights[stack.pop()]
            width = i if not stack else (i - stack[-1] - 1)
            max_area = max(max_area, height * width)
        stack.append(i)

    return max_area

