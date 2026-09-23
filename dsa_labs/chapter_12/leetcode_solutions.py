"""LeetCode Solutions for chapter_12."""
from __future__ import annotations

# ----------------------------------------------------------------------------
# Problem: Implement Trie (Prefix Tree) (LeetCode 208) [\LTwo]
# ----------------------------------------------------------------------------
class TrieNode:
    def __init__(self):
        self.children: dict[str, TrieNode] = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        curr = self.root
        for c in word:
            if c not in curr.children:
                curr.children[c] = TrieNode()
            curr = curr.children[c]
        curr.is_end = True

    def search(self, word: str) -> bool:
        curr = self._find(word)
        return curr is not None and curr.is_end

    def startsWith(self, prefix: str) -> bool:
        return self._find(prefix) is not None

    def _find(self, prefix: str) -> TrieNode:
        curr = self.root
        for c in prefix:
            if c not in curr.children:
                return None
            curr = curr.children[c]
        return curr

# ----------------------------------------------------------------------------
# Problem: Design Add and Search Words Data Structure (LeetCode 211) [\LThree]
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
        def dfs(idx: int, node: TrieNode) -> bool:
            if idx == len(word):
                return node.is_end
            c = word[idx]
            if c == '.':
                for child in node.children.values():
                    if dfs(idx + 1, child):
                        return True
                return False
            else:
                if c not in node.children:
                    return False
                return dfs(idx + 1, node.children[c])

        return dfs(0, self.root)

# ----------------------------------------------------------------------------
# Problem: Word Search II (LeetCode 212) [\LFour]
# ----------------------------------------------------------------------------
def find_words(board: list[list[str]], words: list[str]) -> list[str]:
    # Build trie with word stored at leaf
    trie = {}
    for word in words:
        curr = trie
        for c in word:
            curr = curr.setdefault(c, {})
        curr['#'] = word  # terminal marker

    R, C = len(board), len(board[0])
    found_words = []

    def backtrack(r: int, c: int, parent_node: dict):
        char = board[r][c]
        curr_node = parent_node[char]

        # Check if complete word found
        if '#' in curr_node:
            found_words.append(curr_node.pop('#'))

        # Mark cell as visited
        board[r][c] = '*'
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and board[nr][nc] in curr_node:
                backtrack(nr, nc, curr_node)
        board[r][c] = char  # unmark

        # Leaf pruning optimization
        if not curr_node:
            parent_node.pop(char)

    for r in range(R):
        for c in range(C):
            if board[r][c] in trie:
                backtrack(r, c, trie)

    return found_words

