"""LeetCode Solutions for chapter_07."""
from __future__ import annotations

# ----------------------------------------------------------------------------
# Problem: Valid Anagram (LeetCode 242) [\LTwo]
# ----------------------------------------------------------------------------
def is_anagram(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False

    counts = [0] * 26
    for char_s, char_t in zip(s, t):
        counts[ord(char_s) - ord('a')] += 1
        counts[ord(char_t) - ord('a')] -= 1

    return all(c == 0 for c in counts)

# ----------------------------------------------------------------------------
# Problem: Group Anagrams (LeetCode 49) [\LThree]
# ----------------------------------------------------------------------------
from collections import defaultdict

def group_anagrams(strs: list[str]) -> list[list[str]]:
    groups = defaultdict(list)
    for s in strs:
        # 26-element character count tuple as canonical key
        char_counts = [0] * 26
        for c in s:
            char_counts[ord(c) - ord('a')] += 1
        groups[tuple(char_counts)].append(s)

    return list(groups.values())

# ----------------------------------------------------------------------------
# Problem: Longest Consecutive Sequence (LeetCode 128) [\LFour]
# ----------------------------------------------------------------------------
def longest_consecutive(nums: list[int]) -> int:
    num_set = set(nums)
    longest_streak = 0

    for num in num_set:
        # Only start counting if num is the beginning of a sequence
        if num - 1 not in num_set:
            current_num = num
            current_streak = 1

            while current_num + 1 in num_set:
                current_num += 1
                current_streak += 1

            longest_streak = max(longest_streak, current_streak)

    return longest_streak

