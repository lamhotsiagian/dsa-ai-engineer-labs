"""Module tree_reduce.py for chapter_17."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Sequence, TypeVar

import numpy as np

T = TypeVar("T")


@dataclass(frozen=True)
class ReduceReport:
    inputs: int
    rounds: int
    combines: int


def tree_reduce(
    values: Sequence[T],
    combine: Callable[[T, T], T],
    *,
    identity: T | None = None,
) -> tuple[T, ReduceReport]:
    """Pairwise-combine values in a fixed, deterministic tree.

    Requires `combine` to be ASSOCIATIVE. It need not be commutative,
    because the tree preserves left-to-right order at every level -- which
    is exactly the property that makes the result reproducible.

    Rounds  ceil(log2(n))  -- the parallel critical path.
    Combines n - 1         -- the same total work as a sequential fold.
    """
    if not values:
        if identity is None:
            raise ValueError("empty input and no identity element")
        return identity, ReduceReport(0, 0, 0)

    level = list(values)
    rounds = combines = 0
    while len(level) > 1:
        nxt: list[T] = []
        for i in range(0, len(level) - 1, 2):
            nxt.append(combine(level[i], level[i + 1]))
            combines += 1
        if len(level) % 2:                   # odd one out is carried forward
            nxt.append(level[-1])
        level = nxt
        rounds += 1
    return level[0], ReduceReport(len(values), rounds, combines)


def sequential_reduce(values: Sequence[T],
                      combine: Callable[[T, T], T]) -> T:
    """Left fold. Same result as tree_reduce for exact arithmetic; a
    DIFFERENT result for floats, because float addition is not associative."""
    result = values[0]
    for v in values[1:]:
        result = combine(result, v)
    return result


def float_reduction_gap(values: Sequence[float]) -> float:
    """How far apart a tree reduction and a sequential fold land.

    This is not a bug in either one: float addition is not associative, so
    the two orderings genuinely produce different sums. The gap grows with
    n and with the spread of magnitudes, and it is the reason a distributed
    training run is not bit-reproducible across different worker counts.
    """
    tree, _ = tree_reduce(list(values), lambda a, b: a + b)
    return abs(tree - sequential_reduce(list(values), lambda a, b: a + b))


class DeterministicAllReduce:
    """Gradient aggregation with a FIXED reduction order.

    The reduction tree is determined by worker rank, not by arrival order,
    so the same gradients always sum in the same sequence and the run is
    bit-reproducible. Aggregating in arrival order would be faster (no
    waiting for a specific partner) and would make every run different.

    That is the trade this class exists to make explicit: determinism costs
    latency, and which one you want is a decision, not a default.
    """

    def __init__(self, world_size: int, *, accumulate_in_float64: bool = True):
        if world_size < 1:
            raise ValueError("world_size must be positive")
        self.world_size = world_size
        self.accumulate_in_float64 = accumulate_in_float64
        self._buffers: dict[int, np.ndarray] = {}

    def submit(self, rank: int, gradient: np.ndarray) -> None:
        if not 0 <= rank < self.world_size:
            raise ValueError(f"rank {rank} outside 0..{self.world_size - 1}")
        if rank in self._buffers:
            raise ValueError(f"rank {rank} already submitted this step")
        self._buffers[rank] = gradient

    def reduce(self) -> np.ndarray:
        """Sum all submitted gradients in rank order. O(world_size * d)."""
        missing = set(range(self.world_size)) - self._buffers.keys()
        if missing:
            raise RuntimeError(f"missing gradients from ranks {sorted(missing)}")

        ordered = [self._buffers[r] for r in range(self.world_size)]
        shapes = {g.shape for g in ordered}
        if len(shapes) != 1:
            raise ValueError(f"gradient shape mismatch across ranks: {shapes}")

        if self.accumulate_in_float64:
            # Accumulating in higher precision shrinks the ordering-dependent
            # error by orders of magnitude for a small cost, which is usually
            # the right trade for a reduction over thousands of workers.
            ordered = [g.astype(np.float64, copy=False) for g in ordered]

        total, _ = tree_reduce(ordered, lambda a, b: a + b)
        self._buffers.clear()
        return total.astype(np.float32, copy=False)
