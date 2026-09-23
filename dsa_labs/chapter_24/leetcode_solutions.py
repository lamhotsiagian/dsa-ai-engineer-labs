"""LeetCode Solutions for chapter_24."""
from __future__ import annotations

# ----------------------------------------------------------------------------
# Problem: Find the Index of First Occurrence (LeetCode 28) [\LTwo]
# ----------------------------------------------------------------------------
def str_str(haystack: str, needle: str) -> int:
    if not needle:
        return 0
    m, n = len(needle), len(haystack)
    if m > n:
        return -1

    # Precompute LPS table for needle
    lps = [0] * m
    prev_lps, i = 0, 1
    while i < m:
        if needle[i] == needle[prev_lps]:
            prev_lps += 1
            lps[i] = prev_lps
            i += 1
        elif prev_lps > 0:
            prev_lps = lps[prev_lps - 1]
        else:
            lps[i] = 0
            i += 1

    # Scan haystack
    h_idx = n_idx = 0
    while h_idx < n:
        if haystack[h_idx] == needle[n_idx]:
            h_idx += 1
            n_idx += 1
            if n_idx == m:
                return h_idx - m
        elif n_idx > 0:
            n_idx = lps[n_idx - 1]
        else:
            h_idx += 1

    return -1

# ----------------------------------------------------------------------------
# Problem: Repeated DNA Sequences (LeetCode 187) [\LThree]
# ----------------------------------------------------------------------------
def find_repeated_dna_sequences(s: str) -> list[str]:
    L = 10
    if len(s) <= L:
        return []

    mapping = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    mask = (1 << (2 * L)) - 1

    bit_hash = 0
    for i in range(L):
        bit_hash = (bit_hash << 2) | mapping[s[i]]

    seen = {bit_hash}
    repeated = set()

    for i in range(L, len(s)):
        bit_hash = ((bit_hash << 2) & mask) | mapping[s[i]]
        if bit_hash in seen:
            repeated.add(s[i - L + 1:i + 1])
        else:
            seen.add(bit_hash)

    return list(repeated)

# ----------------------------------------------------------------------------
# Problem: Shortest Palindrome (LeetCode 214) [\LFour]
# ----------------------------------------------------------------------------
def shortest_palindrome(s: str) -> str:
    rev = s[::-1]
    combined = s + "#" + rev

    # Compute LPS table
    lps = [0] * len(combined)
    for i in range(1, len(combined)):
        j = lps[i - 1]
        while j > 0 and combined[i] != combined[j]:
            j = lps[j - 1]
        if combined[i] == combined[j]:
            j += 1
        lps[i] = j

    longest_pal_prefix = lps[-1]
    add_on = rev[:len(s) - longest_pal_prefix]
    return add_on + s

