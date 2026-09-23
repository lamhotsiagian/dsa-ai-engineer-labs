"""Module weighted_sampler.py for chapter_25."""
from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass(frozen=True)
class SamplerStats:
    items: int
    total_weight: int
    zero_weight_items: int


class WeightedSampler:
    """Sample indices proportional to weights, with O(log n) updates.

    A static prefix-sum array plus bisect samples in O(log n) but costs
    O(n) per weight change -- unusable when priorities are revised after
    every draw, which is exactly what prioritised replay does.

    A Fenwick tree over the weights gives O(log n) for BOTH, and the sample
    is a single tree descent rather than a binary search over an array.

    Weights are integers in a fixed unit: float weights accumulate drift
    through repeated add/subtract, and a sampler whose total silently
    diverges from the sum of its parts is very hard to debug.
    """

    SCALE = 1_000_000            # weights are stored as micro-units

    def __init__(self, weights: list[float], *, seed: int | None = None) -> None:
        if any(w < 0 for w in weights):
            raise ValueError("weights must be non-negative")
        self._weights = [int(round(w * self.SCALE)) for w in weights]
        self._tree = FenwickTree(self._weights)
        self._rng = random.Random(seed)

    def __len__(self) -> int:
        return len(self._weights)

    @property
    def total_weight(self) -> int:
        return self._tree.prefix_sum(len(self._weights))

    def set_weight(self, index: int, weight: float) -> None:
        """Change one item's weight. O(log n)."""
        if weight < 0:
            raise ValueError("weight must be non-negative")
        if not 0 <= index < len(self._weights):
            raise IndexError(f"index {index} outside 0..{len(self._weights) - 1}")
        scaled = int(round(weight * self.SCALE))
        self._tree.add(index, scaled - self._weights[index])
        self._weights[index] = scaled

    def sample(self) -> int:
        """Draw an index with probability proportional to its weight.

        O(log n): one uniform draw plus one tree descent. No prefix array
        is materialised and no binary search over one is performed.
        """
        total = self.total_weight
        if total <= 0:
            raise ValueError("cannot sample: all weights are zero")
        target = self._rng.randrange(total) + 1      # 1..total inclusive
        return self._tree.find_by_prefix(target)

    def sample_many(self, count: int) -> list[int]:
        """`count` independent draws with replacement. O(count log n)."""
        return [self.sample() for _ in range(count)]

    def stats(self) -> SamplerStats:
        return SamplerStats(
            items=len(self._weights),
            total_weight=self.total_weight,
            zero_weight_items=sum(1 for w in self._weights if w == 0),
        )


class PrioritisedReplayBuffer:
    """Fixed-capacity buffer sampling proportional to priority^alpha.

    The RL use case that makes this structure worth the complexity:
    priorities change after every single sampled transition, so an O(n)
    update per change would dominate training entirely.

    add / update_priority / sample: all O(log n).
    """

    def __init__(self, capacity: int, *, alpha: float = 0.6,
                 seed: int | None = None) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        if not 0.0 <= alpha <= 1.0:
            raise ValueError("alpha must be in [0, 1]")
        self._capacity = capacity
        self._alpha = alpha
        self._items: list[object] = [None] * capacity
        self._sampler = WeightedSampler([0.0] * capacity, seed=seed)
        self._next = 0
        self._size = 0
        self._max_priority = 1.0

    def __len__(self) -> int:
        return self._size

    def add(self, item: object, priority: float | None = None) -> int:
        """Insert, overwriting the oldest slot when full. O(log n).

        A new item gets the maximum observed priority so that it is
        sampled at least once before its true priority is known --
        otherwise a transition with an unknown error might never be
        visited at all.
        """
        slot = self._next
        self._items[slot] = item
        p = self._max_priority if priority is None else priority
        self._sampler.set_weight(slot, p ** self._alpha)
        self._next = (self._next + 1) % self._capacity
        self._size = min(self._size + 1, self._capacity)
        return slot

    def update_priority(self, slot: int, priority: float) -> None:
        """Revise a slot's priority after using it. O(log n)."""
        if priority < 0:
            raise ValueError("priority must be non-negative")
        self._max_priority = max(self._max_priority, priority)
        self._sampler.set_weight(slot, priority ** self._alpha)

    def sample(self, batch_size: int) -> list[tuple[int, object]]:
        """Draw a batch proportional to priority^alpha. O(batch log n)."""
        if self._size == 0:
            raise ValueError("buffer is empty")
        return [(slot, self._items[slot])
                for slot in self._sampler.sample_many(batch_size)]
