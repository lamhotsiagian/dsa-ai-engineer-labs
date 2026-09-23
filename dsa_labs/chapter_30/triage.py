"""Module triage.py for chapter_30."""
from __future__ import annotations

from dataclasses import dataclass, field

# Operations per second assumed for the target-complexity estimate. This is
# deliberately conservative: an interpreted language, one core, one second.
OPERATIONS_BUDGET = 100_000_000


@dataclass(frozen=True)
class ComplexityTarget:
    label: str
    approaches: tuple[str, ...]


# Ordered from smallest bound upward; the first row whose bound is >= n wins.
CONSTRAINT_LADDER: list[tuple[int, ComplexityTarget]] = [
    (10, ComplexityTarget("O(n!) or O(2^n * n)",
                          ("permutations", "exhaustive backtracking"))),
    (20, ComplexityTarget("O(2^n)",
                          ("subsets", "bitmask DP over states"))),
    (100, ComplexityTarget("O(n^3)",
                           ("Floyd-Warshall", "interval DP"))),
    (1_000, ComplexityTarget("O(n^2)",
                             ("pairwise DP", "edit distance", "all pairs"))),
    (100_000, ComplexityTarget("O(n log n)",
                               ("sort", "heap", "binary search",
                                "divide and conquer"))),
    (1_000_000, ComplexityTarget("O(n)",
                                 ("one pass", "hash map", "sliding window",
                                  "prefix sums"))),
    (100_000_000, ComplexityTarget("O(n), tight constant",
                                   ("single linear scan",))),
]

FALLBACK = ComplexityTarget("O(log n) or O(1)",
                            ("binary search", "closed form",
                             "streaming sketch"))


def target_for(n: int) -> ComplexityTarget:
    """The complexity an input bound of n is asking for.

    The bound is the most reliable signal in a problem statement, because
    prose can be ambiguous and 10^9 cannot. A small bound is permission to
    be exponential; a large one is a prohibition on nested loops.
    """
    if n <= 0:
        raise ValueError("n must be positive")
    for bound, target in CONSTRAINT_LADDER:
        if n <= bound:
            return target
    return FALLBACK


def feasible(n: int, exponent: float) -> bool:
    """Would an O(n^exponent) algorithm finish inside the budget?

    Used to sanity-check an approach before committing to it: feasible(
    100_000, 2) is False, which is the arithmetic behind 'n up to 1e5 rules
    out the nested loop'.
    """
    return n ** exponent <= OPERATIONS_BUDGET


@dataclass(frozen=True)
class Signal:
    phrase: str
    first_candidate: str
    then_consider: tuple[str, ...] = ()
    trap: str | None = None


SIGNALS: tuple[Signal, ...] = (
    Signal("contiguous subarray", "sliding window",
           ("prefix sums", "Kadane"),
           trap="'subsequence' is NOT contiguous -- that is DP, not a window"),
    Signal("subsequence", "dynamic programming", ("greedy if exchange holds",)),
    Signal("sorted array", "two pointers", ("binary search",),
           trap="'rotated sorted' still admits binary search, modified"),
    Signal("kth largest", "heap of size k",
           ("quickselect", "binary search on the answer"),
           trap="'kth largest' is one element; 'k largest' is a set"),
    Signal("next greater element", "monotonic stack"),
    Signal("number of ways", "dynamic programming", ("combinatorics",)),
    Signal("shortest path unweighted", "BFS", ("bidirectional BFS",)),
    Signal("shortest path weighted", "Dijkstra",
           ("Bellman-Ford for negative edges",)),
    Signal("prerequisites", "topological sort", ("cycle detection",)),
    Signal("connected components", "union-find", ("DFS", "BFS flood fill")),
    Signal("prefix or autocomplete", "trie"),
    Signal("merge intervals", "sort by start", ("sweep line",)),
    Signal("in place O(1) space", "two pointers",
           ("cyclic sort", "index as a hash")),
    Signal("minimise the maximum", "binary search on the answer"),
    Signal("stream too large to store", "heap",
           ("reservoir sampling", "count-min sketch")),
)


def match_signals(statement: str) -> list[Signal]:
    """Signals present in a problem statement, best match first.

    A blunt substring match on purpose: this is a study aid for building the
    reflex, not a parser. The value is in being forced to name the pattern
    before coding, and in seeing the traps attached to near-misses.
    """
    lowered = statement.lower()
    hits = [s for s in SIGNALS if s.phrase in lowered]
    return sorted(hits, key=lambda s: -len(s.phrase))


def triage(statement: str, n: int) -> dict:
    """The three-minute procedure, as data.

    Returns the target complexity implied by the bound, the candidate
    patterns implied by the prose, and any traps attached to them.
    """
    target = target_for(n)
    signals = match_signals(statement)
    return {
        "bound": n,
        "target_complexity": target.label,
        "approaches_for_bound": list(target.approaches),
        "candidates": [s.first_candidate for s in signals],
        "alternatives": [a for s in signals for a in s.then_consider],
        "traps": [s.trap for s in signals if s.trap],
        "nested_loop_feasible": feasible(n, 2),
    }
