"""Module vocab_trie.py for chapter_12."""
from __future__ import annotations

import unicodedata
from dataclasses import dataclass, field

import numpy as np


@dataclass
class VocabNode:
    children: dict[str, "VocabNode"] = field(default_factory=dict)
    token_id: int | None = None        # not None => a complete vocabulary entry
    subtree_count: int = 0             # entries at or below this node


class VocabularyTrie:
    """Prefix structure over a token vocabulary.

    Supports the three operations a tokenizer and a constrained decoder need:
      * longest_match  -- greedy segmentation, O(L) per position
      * completions    -- ranked continuations for autocomplete, O(L + k)
      * allowed_mask   -- legal next tokens given a prefix, O(#children)

    Keys are NFC-normalised on both insert and query, so visually identical
    strings always take the same path. Doing this in one place is what stops
    the two sides drifting apart.
    """

    def __init__(self, unk_id: int = 0) -> None:
        self.root = VocabNode()
        self.unk_id = unk_id
        self._id_to_token: dict[int, str] = {}

    @staticmethod
    def _normalize(text: str) -> str:
        return unicodedata.normalize("NFC", text)

    def add(self, token: str, token_id: int) -> None:
        """Insert one vocabulary entry. Time O(L)."""
        if not token:
            raise ValueError("cannot insert an empty token")
        if token_id < 0:
            raise ValueError("token_id must be non-negative")
        token = self._normalize(token)
        node = self.root
        node.subtree_count += 1
        for ch in token:
            node = node.children.setdefault(ch, VocabNode())
            node.subtree_count += 1
        node.token_id = token_id
        self._id_to_token[token_id] = token

    def add_many(self, vocab: dict[str, int]) -> None:
        for token, token_id in vocab.items():
            self.add(token, token_id)

    def _walk(self, prefix: str) -> VocabNode | None:
        node = self.root
        for ch in self._normalize(prefix):
            node = node.children.get(ch)
            if node is None:
                return None
        return node

    def longest_match(self, text: str, start: int = 0) -> tuple[int, int | None]:
        """Longest vocabulary entry matching text[start:].

        Returns (end_index, token_id). end_index == start means no match.
        Time O(L) for the longest matching entry -- one walk.
        """
        text = self._normalize(text)
        node = self.root
        best_end, best_id = start, None
        for i in range(start, len(text)):
            node = node.children.get(text[i])
            if node is None:
                break
            if node.token_id is not None:
                best_end, best_id = i + 1, node.token_id
        return best_end, best_id

    def tokenize_greedy(self, text: str) -> list[int]:
        """Greedy longest-match segmentation.

        Time O(n * L). Not optimal -- see the chapter text -- but it is the
        algorithm WordPiece-style tokenizers use, and it is deterministic,
        which matters more in production than optimality.
        """
        text = self._normalize(text)
        out: list[int] = []
        i = 0
        while i < len(text):
            end, token_id = self.longest_match(text, i)
            if token_id is None:
                out.append(self.unk_id)
                i += 1
            else:
                out.append(token_id)
                i = end
        return out

    def completions(self, prefix: str, limit: int = 10) -> list[str]:
        """Vocabulary entries beginning with `prefix`.

        Time O(L + number of results explored). The subtree_count field lets
        the traversal skip empty branches immediately.
        """
        node = self._walk(prefix)
        if node is None:
            return []
        out: list[str] = []

        def collect(current: VocabNode, suffix: str) -> None:
            if len(out) >= limit:
                return
            if current.token_id is not None:
                out.append(self._normalize(prefix) + suffix)
            for ch, child in sorted(current.children.items()):
                if len(out) >= limit:
                    return
                if child.subtree_count > 0:
                    collect(child, suffix + ch)

        collect(node, "")
        return out

    def allowed_mask(self, prefix: str, vocab_size: int) -> np.ndarray:
        """Boolean mask over token ids that may legally follow `prefix`.

        Used for constrained decoding: set logits[~mask] = -inf before the
        softmax so the surviving distribution stays normalised.
        Time O(#children at this node).
        """
        mask = np.zeros(vocab_size, dtype=bool)
        node = self._walk(prefix)
        if node is None:
            return mask
        for child in node.children.values():
            if child.token_id is not None and 0 <= child.token_id < vocab_size:
                mask[child.token_id] = True
        return mask

    def memory_report(self) -> dict[str, int]:
        """Node and edge counts -- the trie's weak point, so measure it."""
        nodes = edges = words = 0
        stack = [self.root]
        while stack:
            node = stack.pop()
            nodes += 1
            edges += len(node.children)
            words += node.token_id is not None
            stack.extend(node.children.values())
        return {"nodes": nodes, "edges": edges, "entries": words}
