"""Chapter 33: NeetCode 150 - Arrays & Hashing"""
from __future__ import annotations
import math
import heapq
import bisect
from collections import defaultdict, deque, Counter, OrderedDict
from typing import Optional, List, Dict, Set, Tuple

# ----------------------------------------------------------------------------
# Problem: Contains Duplicate (LeetCode: contains-duplicate)
# ----------------------------------------------------------------------------
def containsDuplicate(nums: list[int]) -> bool:
    # Hash set gives O(1) expected lookups for seen numbers
    seen = set()
    for x in nums:
        # If already recorded, we found a duplicate
        if x in seen:
            return True
        seen.add(x)
    # Scanned entire array with all unique elements
    return False

# ----------------------------------------------------------------------------
# Problem: Valid Anagram (LeetCode: valid-anagram)
# ----------------------------------------------------------------------------
def isAnagram(s: str, t: str) -> bool:
    # Anagrams must have identical length
    if len(s) != len(t):
        return False
    # Fixed-size frequency table for 26 lowercase English letters
    count = [0] * 26
    for i in range(len(s)):
        count[ord(s[i]) - ord('a')] += 1  # Increment for s
        count[ord(t[i]) - ord('a')] -= 1  # Decrement for t
    # If all character frequencies balance to 0, they are anagrams
    return all(c == 0 for c in count)

# ----------------------------------------------------------------------------
# Problem: Two Sum (LeetCode: two-sum)
# ----------------------------------------------------------------------------
def twoSum(nums: list[int], target: int) -> list[int]:
    # Maps number value -> its original index in nums
    seen = {}
    for i, x in enumerate(nums):
        complement = target - x
        # Check if the needed complement was already encountered
        if complement in seen:
            return [seen[complement], i]
        seen[x] = i
    return []

# ----------------------------------------------------------------------------
# Problem: Group Anagrams (LeetCode: group-anagrams)
# ----------------------------------------------------------------------------
from collections import defaultdict

def group_anagrams(strs: list[str]) -> list[list[str]]:
    # Map 26-element character count tuple -> list of anagrams
    groups = defaultdict(list)
    for s in strs:
        # Build frequency array as a canonical hashable signature
        counts = [0] * 26
        for c in s:
            counts[ord(c) - ord('a')] += 1
        # Convert list to tuple so it can serve as a dict key
        groups[tuple(counts)].append(s)
    return list(groups.values())

# ----------------------------------------------------------------------------
# Problem: Top K Frequent Elements (LeetCode: top-k-frequent-elements)
# ----------------------------------------------------------------------------
from collections import Counter

def topKFrequent(nums: list[int], k: int) -> list[int]:
    count = Counter(nums)
    # Buckets where index represents frequency (0 to n)
    buckets = [[] for _ in range(len(nums) + 1)]
    for val, freq in count.items():
        buckets[freq].append(val)
    
    res = []
    # Gather elements starting from highest frequency bucket down to lowest
    for freq in range(len(nums), 0, -1):
        for val in buckets[freq]:
            res.append(val)
            if len(res) == k:
                return res
    return res

# ----------------------------------------------------------------------------
# Problem: Encode and Decode Strings (LeetCode: encode-and-decode-strings)
# ----------------------------------------------------------------------------
class Codec:
    def encode(self, strs: list[str]) -> str:
        # Prefix each string with its length followed by a delimiter '#'
        # Example: ["neet", "code"] -> "4#neet4#code"
        res = []
        for s in strs:
            res.append(f"{len(s)}#{s}")
        return "".join(res)

    def decode(self, s: str) -> list[str]:
        res = []
        i = 0
        while i < len(s):
            # Locate the '#' delimiter separating length and content
            j = s.find('#', i)
            length = int(s[i:j])
            # Extract exactly `length` characters
            res.append(s[j + 1 : j + 1 + length])
            # Advance pointer past the extracted word
            i = j + 1 + length
        return res

# ----------------------------------------------------------------------------
# Problem: Product of Array Except Self (LeetCode: product-of-array-except-self)
# ----------------------------------------------------------------------------
def productExceptSelf(nums: list[int]) -> list[int]:
    n = len(nums)
    res = [1] * n
    # Prefix pass: res[i] contains product of all elements to the left of i
    prefix = 1
    for i in range(n):
        res[i] = prefix
        prefix *= nums[i]
    # Suffix pass: multiply with accumulated product of elements to the right of i
    postfix = 1
    for i in range(n - 1, -1, -1):
        res[i] *= postfix
        postfix *= nums[i]
    return res

# ----------------------------------------------------------------------------
# Problem: Valid Sudoku (LeetCode: valid-sudoku)
# ----------------------------------------------------------------------------
def isValidSudoku(board: list[list[str]]) -> bool:
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]  # 3x3 sub-grids indexed 0 to 8

    for r in range(9):
        for c in range(9):
            val = board[r][c]
            if val == '.':
                continue
            box_idx = (r // 3) * 3 + (c // 3)
            # Check for duplicate in row, column, or 3x3 block
            if val in rows[r] or val in cols[c] or val in boxes[box_idx]:
                return False
            rows[r].add(val)
            cols[c].add(val)
            boxes[box_idx].add(val)
    return True

# ----------------------------------------------------------------------------
# Problem: Longest Consecutive Sequence (LeetCode: longest-consecutive-sequence)
# ----------------------------------------------------------------------------
def longestConsecutive(nums: list[int]) -> int:
    num_set = set(nums)
    longest = 0
    for x in num_set:
        # Only start counting if x is the true beginning of a streak
        if x - 1 not in num_set:
            curr = x
            streak = 1
            # Expand consecutive streak upwards
            while curr + 1 in num_set:
                curr += 1
                streak += 1
            longest = max(longest, streak)
    return longest

