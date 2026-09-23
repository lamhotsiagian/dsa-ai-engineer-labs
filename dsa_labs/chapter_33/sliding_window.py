"""Chapter 33: NeetCode 150 - Sliding Window"""
from __future__ import annotations
import math
import heapq
import bisect
from collections import defaultdict, deque, Counter, OrderedDict
from typing import Optional, List, Dict, Set, Tuple

# ----------------------------------------------------------------------------
# Problem: Best Time to Buy and Sell Stock (LeetCode: best-time-to-buy-and-sell-stock)
# ----------------------------------------------------------------------------
def maxProfit(prices: list[int]) -> int:
    min_price = float('inf')  # Lowest buy price seen so far
    max_p = 0                 # Highest achievable profit
    for p in prices:
        if p < min_price:
            min_price = p     # Establish new optimal buy point
        elif p - min_price > max_p:
            max_p = p - min_price  # Evaluate profit if selling today
    return max_p

# ----------------------------------------------------------------------------
# Problem: Longest Substring Without Repeating Characters (LeetCode: longest-substring-without-repeating-characters)
# ----------------------------------------------------------------------------
def lengthOfLongestSubstring(s: str) -> int:
    # Maps character -> last seen index to jump left pointer in O(1)
    seen = {}
    l = 0
    max_len = 0
    for r, c in enumerate(s):
        # If character repeated inside current window, jump left pointer
        if c in seen and seen[c] >= l:
            l = seen[c] + 1
        seen[c] = r
        max_len = max(max_len, r - l + 1)
    return max_len

# ----------------------------------------------------------------------------
# Problem: Longest Repeating Character Replacement (LeetCode: longest-repeating-character-replacement)
# ----------------------------------------------------------------------------
from collections import defaultdict

def characterReplacement(s: str, k: int) -> int:
    counts = defaultdict(int)
    max_freq = 0  # Frequency of most frequent character in current window
    l = 0
    max_len = 0
    for r in range(len(s)):
        counts[s[r]] += 1
        max_freq = max(max_freq, counts[s[r]])
        # If required replacements (window_len - max_freq) exceeds k, shrink window
        while (r - l + 1) - max_freq > k:
            counts[s[l]] -= 1
            l += 1
        max_len = max(max_len, r - l + 1)
    return max_len

# ----------------------------------------------------------------------------
# Problem: Permutation in String (LeetCode: permutation-in-string)
# ----------------------------------------------------------------------------
def checkInclusion(s1: str, s2: str) -> bool:
    if len(s1) > len(s2):
        return False
    c1, c2 = [0] * 26, [0] * 26
    # Populate frequency counts for s1 and initial window of s2
    for i in range(len(s1)):
        c1[ord(s1[i]) - ord('a')] += 1
        c2[ord(s2[i]) - ord('a')] += 1
    
    matches = sum(1 for i in range(26) if c1[i] == c2[i])
    for i in range(len(s1), len(s2)):
        if matches == 26:
            return True
        # Slide window right: add incoming character
        r = ord(s2[i]) - ord('a')
        c2[r] += 1
        if c2[r] == c1[r]:
            matches += 1
        elif c2[r] == c1[r] + 1:
            matches -= 1
        # Evict outgoing character from left
        l = ord(s2[i - len(s1)]) - ord('a')
        c2[l] -= 1
        if c2[l] == c1[l]:
            matches += 1
        elif c2[l] == c1[l] - 1:
            matches -= 1
    return matches == 26

# ----------------------------------------------------------------------------
# Problem: Minimum Window Substring (LeetCode: minimum-window-substring)
# ----------------------------------------------------------------------------
from collections import Counter

def minWindow(s: str, t: str) -> str:
    if not t or not s:
        return ""
    target_counts = Counter(t)
    window_counts = {}
    have, need = 0, len(target_counts)
    res, res_len = [-1, -1], float('inf')
    l = 0

    for r in range(len(s)):
        c = s[r]
        window_counts[c] = window_counts.get(c, 0) + 1
        if c in target_counts and window_counts[c] == target_counts[c]:
            have += 1
        # Contract window from left while all requirements are fulfilled
        while have == need:
            if (r - l + 1) < res_len:
                res = [l, r]
                res_len = r - l + 1
            left_char = s[l]
            window_counts[left_char] -= 1
            if left_char in target_counts and window_counts[left_char] < target_counts[left_char]:
                have -= 1
            l += 1
    l, r = res
    return s[l : r + 1] if res_len != float('inf') else ""

# ----------------------------------------------------------------------------
# Problem: Sliding Window Maximum (LeetCode: sliding-window-maximum)
# ----------------------------------------------------------------------------
from collections import deque

def maxSlidingWindow(nums: list[int], k: int) -> list[int]:
    # Monotonic queue storing indices; elements are kept in strictly decreasing order
    q = deque()
    res = []
    for r in range(len(nums)):
        # Maintain monotonic property: pop smaller elements from the back
        while q and nums[q[-1]] < nums[r]:
            q.pop()
        q.append(r)
        # Evict elements that fell outside the sliding window boundary
        if q[0] < r - k + 1:
            q.popleft()
        # Record maximum (head of deque) once first window is formed
        if r >= k - 1:
            res.append(nums[q[0]])
    return res

