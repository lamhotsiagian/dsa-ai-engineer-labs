"""Module ann_index.py for chapter_28."""
from __future__ import annotations

import heapq
import math
import random
from dataclasses import dataclass, field

import numpy as np


@dataclass
class NavigableSmallWorldIndex:
    """A single-file HNSW-style index: layered proximity graph + beam search.

    Teaching implementation. It has the structure of a production index --
    geometric level assignment, greedy descent, bounded best-first search at
    level 0 -- without the SIMD kernels, memory pooling or thread safety a
    real one needs. Use a library in production; know this to debug one.

    Build   O(n * ef_construction * M * d)
    Query   O(ef_search * M * d * log n) expected
    Memory  O(n * d) vectors + O(n * M) edges
    """
    dimension: int
    max_degree: int = 16                 # M: neighbours per node per level
    ef_construction: int = 100           # build-time beam width
    level_multiplier: float = 1 / math.log(2.0)
    seed: int = 0

    vectors: list[np.ndarray] = field(default_factory=list)
    graph: list[dict[int, list[int]]] = field(default_factory=list)
    entry_point: int | None = None
    _rng: random.Random = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._rng = random.Random(self.seed)

    def _distance(self, a: np.ndarray, b: np.ndarray) -> float:
        """Squared L2. Monotone in L2, so the ordering is identical and the
        square root -- one per comparison, millions per query -- is saved."""
        diff = a - b
        return float(diff @ diff)

    def _random_level(self) -> int:
        """Geometric level assignment: P(level >= l) decays by a constant
        factor per level, so the top level holds O(log n) nodes. This is the
        skip-list coin flip, and it is what makes the descent logarithmic."""
        return int(-math.log(self._rng.random()) * self.level_multiplier)

    def add(self, vector: np.ndarray) -> int:
        if vector.shape != (self.dimension,):
            raise ValueError(
                f"expected shape ({self.dimension},), got {vector.shape}")

        node_id = len(self.vectors)
        self.vectors.append(np.asarray(vector, dtype=np.float32))
        level = self._random_level()
        while len(self.graph) <= level:
            self.graph.append({})

        if self.entry_point is None:
            for l in range(level + 1):
                self.graph[l][node_id] = []
            self.entry_point = node_id
            return node_id

        # Descend from the top with a beam of 1 -- coarse navigation only.
        current = self.entry_point
        for l in range(len(self.graph) - 1, level, -1):
            current = self._greedy_descend(vector, current, l)

        # From here down, search properly and wire up the neighbours.
        for l in range(min(level, len(self.graph) - 1), -1, -1):
            candidates = self._search_layer(
                vector, [current], l, self.ef_construction)
            neighbours = [n for _, n in heapq.nsmallest(
                self.max_degree, candidates)]
            self.graph[l][node_id] = neighbours
            for neighbour in neighbours:
                # Bidirectional edge, then prune. Without the prune, popular
                # nodes accumulate unbounded degree and both memory and query
                # cost drift upward over the life of the index.
                self.graph[l].setdefault(neighbour, []).append(node_id)
                self._prune(neighbour, l)
            if candidates:
                current = min(candidates)[1]

        if level >= len(self.graph) - 1:
            self.entry_point = node_id
        return node_id

    def _prune(self, node: int, level: int) -> None:
        edges = self.graph[level][node]
        if len(edges) <= self.max_degree:
            return
        base = self.vectors[node]
        edges.sort(key=lambda other: self._distance(base, self.vectors[other]))
        del edges[self.max_degree:]

    def _greedy_descend(self, query: np.ndarray, start: int,
                        level: int) -> int:
        """Hill-climbing with beam 1: move to the closest neighbour until no
        neighbour improves. Cheap, and good enough for the upper levels."""
        current = start
        current_distance = self._distance(query, self.vectors[current])
        improved = True
        while improved:
            improved = False
            for neighbour in self.graph[level].get(current, ()):
                d = self._distance(query, self.vectors[neighbour])
                if d < current_distance:
                    current, current_distance, improved = neighbour, d, True
        return current

    def _search_layer(self, query: np.ndarray, entries: list[int],
                      level: int, ef: int) -> list[tuple[float, int]]:
        """Bounded best-first search. Returns at most `ef` (distance, id).

        Two heaps, as always for a bounded best-first search:
          candidates -- min-heap, what to expand next (closest first)
          results    -- max-heap via negated distance, the best ef so far

        The stopping rule is the part that is easy to get wrong: stop when
        the nearest unexpanded candidate is FURTHER than the worst kept
        result, because nothing reachable through it can improve the set.
        Stopping merely because `results` is full loses recall silently.
        """
        visited: set[int] = set(entries)
        candidates: list[tuple[float, int]] = []
        results: list[tuple[float, int]] = []

        for entry in entries:
            d = self._distance(query, self.vectors[entry])
            heapq.heappush(candidates, (d, entry))
            heapq.heappush(results, (-d, entry))

        while candidates:
            distance, node = heapq.heappop(candidates)
            if results and distance > -results[0][0] and len(results) >= ef:
                break
            for neighbour in self.graph[level].get(node, ()):
                if neighbour in visited:
                    continue
                visited.add(neighbour)
                d = self._distance(query, self.vectors[neighbour])
                if len(results) < ef or d < -results[0][0]:
                    heapq.heappush(candidates, (d, neighbour))
                    heapq.heappush(results, (-d, neighbour))
                    if len(results) > ef:
                        heapq.heappop(results)
        return [(-d, node) for d, node in results]

    def search(self, query: np.ndarray, k: int = 10,
               ef_search: int | None = None) -> list[tuple[float, int]]:
        """Return the k nearest (distance, id), closest first.

        ef_search is the recall/latency knob, clamped to >= k: a beam
        narrower than the requested result count cannot fill it.
        """
        if self.entry_point is None:
            return []
        ef = max(k, ef_search if ef_search is not None else max(k, 50))

        current = self.entry_point
        for level in range(len(self.graph) - 1, 0, -1):
            current = self._greedy_descend(query, current, level)

        found = self._search_layer(query, [current], 0, ef)
        return heapq.nsmallest(k, found)
