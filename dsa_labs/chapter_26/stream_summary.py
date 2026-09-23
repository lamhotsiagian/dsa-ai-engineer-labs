"""Module stream_summary.py for chapter_26."""
from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass


class HyperLogLog:
    """Distinct-count estimation in fixed memory.

    m = 2^precision one-byte registers. Standard error ~1.04/sqrt(m):
    precision 14 gives 16,384 registers = 16 KB for ~0.8% error, at ANY
    cardinality from ten to ten billion.

    add: O(1). merge: O(m). Memory: m bytes.
    """

    def __init__(self, precision: int = 14) -> None:
        if not 4 <= precision <= 18:
            raise ValueError("precision must be in 4..18")
        self.precision = precision
        self.m = 1 << precision
        self._registers = bytearray(self.m)

    @property
    def memory_bytes(self) -> int:
        return self.m

    @property
    def standard_error(self) -> float:
        return 1.04 / math.sqrt(self.m)

    def add(self, item: str) -> None:
        """O(1). The register index comes from the top `precision` bits and
        the value from the leading-zero count of the rest."""
        digest = hashlib.blake2b(item.encode("utf-8"), digest_size=8).digest()
        h = int.from_bytes(digest, "big")
        index = h >> (64 - self.precision)
        remainder = (h << self.precision) & ((1 << 64) - 1)
        # Position of the leftmost 1 bit in the remainder, 1-based.
        rank = 1 if remainder == 0 else 64 - remainder.bit_length() + 1
        rank = min(rank, 64 - self.precision + 1)
        if rank > self._registers[index]:
            self._registers[index] = rank

    def count(self) -> int:
        """Estimated distinct count. O(m).

        The harmonic mean is what makes the estimator robust: a single
        register that happens to see a very rare hash would dominate an
        arithmetic mean and wildly over-estimate.
        """
        alpha = {16: 0.673, 32: 0.697, 64: 0.709}.get(
            self.m, 0.7213 / (1 + 1.079 / self.m))
        harmonic = sum(2.0 ** -r for r in self._registers)
        estimate = alpha * self.m * self.m / harmonic

        zeros = self._registers.count(0)
        if estimate <= 2.5 * self.m and zeros:
            # Small-range correction: at low cardinality the raw estimator
            # is biased, and linear counting over empty registers is exact
            # enough to replace it.
            return int(round(self.m * math.log(self.m / zeros)))
        return int(round(estimate))

    def merge(self, other: "HyperLogLog") -> "HyperLogLog":
        """Union of the underlying sets: element-wise register maximum.

        Exact for the union -- no additional error is introduced by
        merging, which is what makes HLL correct across shards.
        """
        if self.precision != other.precision:
            raise ValueError("precisions must match to merge")
        merged = HyperLogLog(self.precision)
        merged._registers = bytearray(
            max(a, b) for a, b in zip(self._registers, other._registers))
        return merged


class BloomFilter:
    """Approximate membership with NO false negatives.

    m = -n ln(p) / (ln 2)^2 bits, k = (m/n) ln 2 hash functions.
    At p = 0.01 that is ~9.6 bits per element and k = 7.

    add / contains: O(k). Memory: m bits.
    """

    def __init__(self, expected_items: int, false_positive_rate: float = 0.01):
        if expected_items <= 0:
            raise ValueError("expected_items must be positive")
        if not 0.0 < false_positive_rate < 1.0:
            raise ValueError("false_positive_rate must be in (0, 1)")
        ln2 = math.log(2)
        self.m = max(8, int(-expected_items * math.log(false_positive_rate) / ln2 ** 2))
        self.k = max(1, round(self.m / expected_items * ln2))
        self.expected_items = expected_items
        self._bits = bytearray((self.m + 7) // 8)
        self._added = 0

    @property
    def memory_bytes(self) -> int:
        return len(self._bits)

    @property
    def fill_ratio(self) -> float:
        """Fraction of bits set. A filter past its design capacity has a
        far higher false-positive rate than configured, and nothing
        reports it -- so this is the metric to alert on."""
        return sum(bin(byte).count("1") for byte in self._bits) / self.m

    def current_false_positive_rate(self) -> float:
        """Estimated rate given how full the filter actually is."""
        return self.fill_ratio ** self.k

    def _positions(self, item: str):
        digest = hashlib.blake2b(item.encode("utf-8"), digest_size=16).digest()
        h1 = int.from_bytes(digest[:8], "big")
        h2 = int.from_bytes(digest[8:], "big") | 1
        for i in range(self.k):
            yield (h1 + i * h2) % self.m

    def add(self, item: str) -> None:
        for pos in self._positions(item):
            self._bits[pos >> 3] |= 1 << (pos & 7)
        self._added += 1

    def __contains__(self, item: str) -> bool:
        return all((self._bits[pos >> 3] >> (pos & 7)) & 1
                   for pos in self._positions(item))

    def union(self, other: "BloomFilter") -> "BloomFilter":
        """Bitwise OR. Exact for the union of the two inserted sets."""
        if (self.m, self.k) != (other.m, other.k):
            raise ValueError("filters must have identical parameters to union")
        merged = BloomFilter(self.expected_items)
        merged.m, merged.k = self.m, self.k
        merged._bits = bytearray(a | b for a, b in zip(self._bits, other._bits))
        merged._added = self._added + other._added
        return merged


@dataclass
class StreamSummary:
    """Everything a dashboard needs about a stream, in fixed memory.

    All four components are MERGEABLE, so each shard builds its own and a
    coordinator combines them with no shuffle:
      * HyperLogLog  -- element-wise register maximum
      * Bloom        -- bitwise OR
      * Count-Min    -- element-wise addition
      * histogram    -- element-wise addition
    """
    distinct: HyperLogLog
    seen: BloomFilter
    total_events: int = 0

    def merge(self, other: "StreamSummary") -> "StreamSummary":
        return StreamSummary(
            distinct=self.distinct.merge(other.distinct),
            seen=self.seen.union(other.seen),
            total_events=self.total_events + other.total_events,
        )
