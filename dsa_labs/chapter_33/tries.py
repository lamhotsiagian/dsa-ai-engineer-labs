"""Chapter 33: NeetCode 150 - Tries"""
from __future__ import annotations
import math
import heapq
import bisect
from collections import defaultdict, deque, Counter, OrderedDict
from typing import Optional, List, Dict, Set, Tuple

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class WordSearchTrieNode:
    def __init__(self):
        self.children = {}
        self.word = None

# ----------------------------------------------------------------------------
# Problem: Implement Trie (Prefix Tree) (LeetCode: implement-trie-prefix-tree)
# ----------------------------------------------------------------------------
class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        curr = self.root
        for c in word:
            if c not in curr.children:
                curr.children[c] = TrieNode()
            curr = curr.children[c]
        curr.is_end = True  # Mark terminal character

    def search(self, word: str) -> bool:
        curr = self.root
        for c in word:
            if c not in curr.children:
                return False
            curr = curr.children[c]
        return curr.is_end

    def startsWith(self, prefix: str) -> bool:
        curr = self.root
        for c in prefix:
            if c not in curr.children:
                return False
            curr = curr.children[c]
        return True

# ----------------------------------------------------------------------------
# Problem: Design Add and Search Words Data Structure (LeetCode: design-add-and-search-words-data-structure)
# ----------------------------------------------------------------------------
class WordDictionary:
    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word: str) -> None:
        curr = self.root
        for c in word:
            if c not in curr.children:
                curr.children[c] = TrieNode()
            curr = curr.children[c]
        curr.is_end = True

    def search(self, word: str) -> bool:
        def dfs(j: int, root: TrieNode) -> bool:
            curr = root
            for i in range(j, len(word)):
                c = word[i]
                if c == ".":
                    # Wildcard: recursively branch through all existing children
                    for child in curr.children.values():
                        if dfs(i + 1, child):
                            return True
                    return False
                else:
                    if c not in curr.children:
                        return False
                    curr = curr.children[c]
            return curr.is_end

        return dfs(0, self.root)

# ----------------------------------------------------------------------------
# Problem: Word Search II (LeetCode: word-search-ii)
# ----------------------------------------------------------------------------
def findWords(board: list[list[str]], words: list[str]) -> list[str]:
    # Build Prefix Trie from word dictionary
    root = WordSearchTrieNode()
    for w in words:
        curr = root
        for c in w:
            if c not in curr.children:
                curr.children[c] = WordSearchTrieNode()
            curr = curr.children[c]
        curr.word = w

    ROWS, COLS = len(board), len(board[0])
    res = []

    def dfs(r: int, c: int, node: WordSearchTrieNode):
        char = board[r][c]
        if char not in node.children:
            return
        curr_node = node.children[char]
        # Match found: collect word and prune to prevent duplicate outputs
        if curr_node.word:
            res.append(curr_node.word)
            curr_node.word = None
        
        # Mark cell as visited in-place
        board[r][c] = "#"
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] != "#":
                dfs(nr, nc, curr_node)
        board[r][c] = char  # Backtrack restore
        
        # Leaf pruning optimization: remove empty trie branches
        if not curr_node.children:
            del node.children[char]

    for r in range(ROWS):
        for c in range(COLS):
            dfs(r, c, root)
    return res

