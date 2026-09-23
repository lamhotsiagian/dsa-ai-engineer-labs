"""Module context_packing.py for chapter_19."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    tokens: int
    score: float                  # relevance, higher is better

    @property
    def density(self) -> float:
        return self.score / self.tokens if self.tokens else 0.0


@dataclass(frozen=True)
class Packing:
    chosen: tuple[str, ...]
    total_tokens: int
    total_score: float
    budget: int

    @property
    def utilisation(self) -> float:
        return self.total_tokens / self.budget if self.budget else 0.0


def pack_greedy(chunks: list[Chunk], budget: int) -> Packing:
    """Greedy by score-per-token, skipping anything that does not fit.

    Time  O(n log n) for the sort, O(n) for the sweep.
    Space O(1) beyond the output.

    NOT optimal: this is 0/1 knapsack. The sort key includes chunk_id so
    that equal densities order deterministically -- without it, identical
    inputs can produce different prompts, which breaks prompt caching and
    makes A/B results noisy.
    """
    if budget < 0:
        raise ValueError("budget must be non-negative")
    remaining = budget
    chosen: list[str] = []
    total_score = 0.0

    for chunk in sorted(chunks, key=lambda c: (-c.density, c.chunk_id)):
        if chunk.tokens <= remaining:
            chosen.append(chunk.chunk_id)
            remaining -= chunk.tokens
            total_score += chunk.score
    return Packing(tuple(chosen), budget - remaining, total_score, budget)


def pack_optimal(chunks: list[Chunk], budget: int,
                 *, score_scale: int = 1000) -> Packing:
    """Exact 0/1 knapsack by dynamic programming over the token budget.

    Time  O(n * budget), Space O(budget).

    Scores are scaled to integers so the DP compares exactly; comparing
    floats in a DP table accumulates error and can pick the wrong subset.

    This is the ORACLE, not the production path: at budget = 32000 and
    n = 500 it is 16 million cells, which is far too slow per request.
    Its job is to measure how much greedy loses, offline.
    """
    if budget < 0:
        raise ValueError("budget must be non-negative")
    best = [0] * (budget + 1)
    keep: list[list[bool]] = []

    for chunk in chunks:
        row = [False] * (budget + 1)
        gain = int(round(chunk.score * score_scale))
        for capacity in range(budget, chunk.tokens - 1, -1):
            candidate = best[capacity - chunk.tokens] + gain
            if candidate > best[capacity]:
                best[capacity] = candidate
                row[capacity] = True
        keep.append(row)

    # Reconstruct the chosen set by walking the decisions backwards.
    chosen: list[str] = []
    capacity = budget
    for i in range(len(chunks) - 1, -1, -1):
        if keep[i][capacity]:
            chosen.append(chunks[i].chunk_id)
            capacity -= chunks[i].tokens
    chosen.reverse()

    by_id = {c.chunk_id: c for c in chunks}
    used = sum(by_id[c].tokens for c in chosen)
    score = sum(by_id[c].score for c in chosen)
    return Packing(tuple(chosen), used, score, budget)


def optimality_gap(chunks: list[Chunk], budget: int) -> float:
    """Fraction of the optimal score that greedy leaves on the table.

    Run this offline on sampled real inputs. A design that says "greedy is
    good enough" without this number is an assertion; with it, it is a
    measurement.
    """
    greedy = pack_greedy(chunks, budget)
    optimal = pack_optimal(chunks, budget)
    if optimal.total_score == 0:
        return 0.0
    return (optimal.total_score - greedy.total_score) / optimal.total_score
