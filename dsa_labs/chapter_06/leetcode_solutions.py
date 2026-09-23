"""LeetCode Solutions for chapter_06."""
from __future__ import annotations

# ----------------------------------------------------------------------------
# Problem: Valid Palindrome (LeetCode 125) [\LTwo]
# ----------------------------------------------------------------------------
def is_palindrome(s: str) -> bool:
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True

# ----------------------------------------------------------------------------
# Problem: Longest Substring Without Repeating Characters (LeetCode 3) [\LThree]
# ----------------------------------------------------------------------------
def length_of_longest_substring(s: str) -> int:
    last_seen: dict[str, int] = {}
    left = 0
    max_length = 0

    for right, char in enumerate(s):
        if char in last_seen and last_seen[char] >= left:
            left = last_seen[char] + 1
        last_seen[char] = right
        max_length = max(max_length, right - left + 1)

    return max_length

# ----------------------------------------------------------------------------
# Problem: Minimum Window Substring (LeetCode 76) [\LFour]
# ----------------------------------------------------------------------------
from collections import Counter

def min_window(s: str, t: str) -> str:
    if not s or not t:
        return ""

    target_counts = Counter(t)
    required = len(target_counts)
    window_counts: dict[str, int] = {}

    formed = 0
    left = 0
    best_len = float("inf")
    best_window = (0, 0)

    for right, char in enumerate(s):
        window_counts[char] = window_counts.get(char, 0) + 1
        if char in target_counts and window_counts[char] == target_counts[char]:
            formed += 1

        while left <= right and formed == required:
            curr_len = right - left + 1
            if curr_len < best_len:
                best_len = curr_len
                best_window = (left, right)

            discard = s[left]
            window_counts[discard] -= 1
            if discard in target_counts and window_counts[discard] < target_counts[discard]:
                formed -= 1
            left += 1

    return "" if best_len == float("inf") else s[best_window[0]:best_window[1] + 1]

