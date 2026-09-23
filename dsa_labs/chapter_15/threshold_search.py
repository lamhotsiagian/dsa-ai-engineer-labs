"""Module threshold_search.py for chapter_15."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np


@dataclass(frozen=True)
class OperatingPoint:
    threshold: float
    precision: float
    recall: float
    predicted_positive: int
    true_positive: int

    @property
    def f1(self) -> float:
        p, r = self.precision, self.recall
        return 2 * p * r / (p + r) if p + r > 0 else 0.0


def evaluate_at(scores: np.ndarray, labels: np.ndarray,
                threshold: float) -> OperatingPoint:
    """Precision and recall for predictions `scores >= threshold`.

    Time O(n). Vectorised: no Python loop over examples.
    """
    if scores.shape != labels.shape:
        raise ValueError("scores and labels must have the same shape")
    predicted = scores >= threshold
    tp = int(np.count_nonzero(predicted & (labels == 1)))
    pp = int(np.count_nonzero(predicted))
    positives = int(np.count_nonzero(labels == 1))
    return OperatingPoint(
        threshold=float(threshold),
        precision=tp / pp if pp else 1.0,       # vacuously precise when silent
        recall=tp / positives if positives else 0.0,
        predicted_positive=pp,
        true_positive=tp,
    )


def is_monotone(values: list[bool]) -> bool:
    """True if the sequence never goes True then False again.

    Binary search is INVALID on a non-monotone predicate, so this is an
    assertion, not a diagnostic. Time O(n).
    """
    seen_true = False
    for v in values:
        if v:
            seen_true = True
        elif seen_true:
            return False
    return True


def calibrate_threshold(
    scores: np.ndarray,
    labels: np.ndarray,
    target_precision: float,
    *,
    probe_points: int = 25,
    iterations: int = 60,
) -> tuple[OperatingPoint, bool]:
    """Smallest threshold achieving at least `target_precision`.

    Returns (operating point, monotone_ok).

    Why the smallest: precision rises with the threshold while recall falls,
    so the minimum qualifying threshold is the one that meets the precision
    requirement at the HIGHEST recall. Anything larger sacrifices recall for
    precision nobody asked for.

    Time  O(probe_points * n + iterations * n).
    Space O(1) beyond the inputs.

    IMPORTANT: empirical precision is only approximately monotone in the
    threshold. With finite data it can dip when a single false positive is
    excluded before a true positive. The probe checks this and reports it,
    rather than silently returning a meaningless boundary.
    """
    if not 0.0 < target_precision <= 1.0:
        raise ValueError("target_precision must be in (0, 1]")
    if scores.size == 0:
        raise ValueError("empty score array")

    lo, hi = float(scores.min()), float(scores.max())

    # Probe for monotonicity before trusting the search.
    probes = np.linspace(lo, hi, probe_points)
    flags = [evaluate_at(scores, labels, t).precision >= target_precision
             for t in probes]
    monotone_ok = is_monotone(flags)

    if not any(flags):
        # Even the strictest threshold misses the target: report the best
        # available point rather than returning a fabricated boundary.
        best = max((evaluate_at(scores, labels, t) for t in probes),
                   key=lambda op: op.precision)
        return best, monotone_ok

    # Real-valued binary search on a FIXED iteration count.
    for _ in range(iterations):
        mid = lo + (hi - lo) / 2
        if evaluate_at(scores, labels, mid).precision >= target_precision:
            hi = mid
        else:
            lo = mid
    return evaluate_at(scores, labels, hi), monotone_ok


def max_feasible(lo: int, hi: int, feasible: Callable[[int], bool]) -> int:
    """Largest x in [lo, hi] with feasible(x) True; lo - 1 if none.

    The answer-space search used for 'largest batch that fits in memory'
    and similar capacity questions. `feasible` must be monotone decreasing:
    once it fails, it fails for everything larger.

    Time O(log(hi - lo)) calls to `feasible`.
    """
    if hi < lo:
        raise ValueError("hi must be >= lo")
    first_bad = first_true(lo, hi + 1, lambda x: not feasible(x))
    return first_bad - 1
