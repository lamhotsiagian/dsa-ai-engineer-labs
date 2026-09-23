"""Module dedup.py for chapter_07."""
from __future__ import annotations

import hashlib
import math
from collections import OrderedDict
from dataclasses import dataclass


def content_digest(text: str, *, bits: int = 128) -> int:
    """Stable content digest, independent of PYTHONHASHSEED.

    128 bits by default: over 10^9 documents the birthday-bound collision
    probability is ~1.5e-21, i.e. negligible. A 64-bit digest at the same
    scale is ~3%, which would silently drop real documents.
    """
    if bits % 8 or not 32 <= bits <= 512:
        raise ValueError("bits must be a multiple of 8 in [32, 512]")
    raw = hashlib.blake2b(text.encode("utf-8"), digest_size=bits // 8).digest()
    return int.from_bytes(raw, "big")


@dataclass
class DedupStats:
    seen: int = 0
    duplicates: int = 0
    evicted: int = 0

    @property
    def duplicate_rate(self) -> float:
        return self.duplicates / self.seen if self.seen else 0.0


class ExactDeduplicator:
    """Exact deduplication with a bounded LRU of recent digests.

    Unbounded exact dedup over a large corpus does not fit in memory, so the
    capacity is explicit and the trade is stated: a document whose duplicate
    fell out of the window is admitted again. For a streaming pipeline with
    temporal locality this is usually fine; for a one-shot corpus build,
    sort by digest and dedupe in a streaming pass instead.

    is_duplicate: O(1) expected time, O(capacity) memory.
    """

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._capacity = capacity
        self._seen: OrderedDict[int, None] = OrderedDict()
        self.stats = DedupStats()

    def is_duplicate(self, text: str) -> bool:
        digest = content_digest(text)
        self.stats.seen += 1
        if digest in self._seen:
            self._seen.move_to_end(digest)          # refresh recency
            self.stats.duplicates += 1
            return True
        self._seen[digest] = None
        if len(self._seen) > self._capacity:
            self._seen.popitem(last=False)          # evict least recent
            self.stats.evicted += 1
        return False


class BloomDeduplicator:
    """Approximate deduplication in a fixed bit array.

    No false negatives: a document reported as new IS new. False positives
    discard a legitimate document at the configured rate, so the rate is a
    data-loss budget and must be chosen deliberately.

    Memory: m bits for n expected items at false-positive rate p, with
        m = -n ln p / (ln 2)^2 ,   k = (m/n) ln 2 .
    At n = 1e8 and p = 0.01 that is ~114 MB and k = 7.
    """

    def __init__(self, expected_items: int, false_positive_rate: float = 0.01) -> None:
        if expected_items <= 0:
            raise ValueError("expected_items must be positive")
        if not 0.0 < false_positive_rate < 1.0:
            raise ValueError("false_positive_rate must be in (0, 1)")
        ln2 = math.log(2)
        self._m = max(8, int(-expected_items * math.log(false_positive_rate) / ln2 ** 2))
        self._k = max(1, round(self._m / expected_items * ln2))
        self._bits = bytearray((self._m + 7) // 8)
        self.stats = DedupStats()

    @property
    def size_bytes(self) -> int:
        return len(self._bits)

    def _positions(self, digest: int):
        """Kirsch-Mitzenmacher: derive k indices from two independent halves
        of one digest instead of computing k separate hashes."""
        h1 = digest & 0xFFFFFFFFFFFFFFFF
        h2 = (digest >> 64) | 1              # odd, so it strides the table
        for i in range(self._k):
            yield (h1 + i * h2) % self._m

    def is_duplicate(self, text: str) -> bool:
        digest = content_digest(text, bits=128)
        self.stats.seen += 1
        all_set = True
        positions = list(self._positions(digest))
        for pos in positions:
            if not (self._bits[pos >> 3] >> (pos & 7)) & 1:
                all_set = False
                break
        if all_set:
            self.stats.duplicates += 1
            return True
        for pos in positions:
            self._bits[pos >> 3] |= 1 << (pos & 7)
        return False
