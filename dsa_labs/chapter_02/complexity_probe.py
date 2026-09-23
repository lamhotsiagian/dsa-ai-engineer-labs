"""Module complexity_probe.py for chapter_02."""
from __future__ import annotations

import math
import time
from dataclasses import dataclass
from typing import Callable, Sequence


@dataclass(frozen=True)
class ScalingReport:
    sizes: tuple[int, ...]
    seconds: tuple[float, ...]
    exponent: float          # fitted p in  t ~ n**p
    label: str               # nearest textbook complexity class

    def __str__(self) -> str:
        rows = "\n".join(f"  n={n:<10,d} {t*1e3:9.3f} ms"
                         for n, t in zip(self.sizes, self.seconds))
        return f"{rows}\n  fitted exponent p = {self.exponent:.2f}  ->  {self.label}"


def _classify(exponent: float) -> str:
    """Map a fitted exponent onto the complexity class it is closest to."""
    for threshold, name in ((0.25, "O(1) or O(log n)"), (1.15, "O(n)"),
                            (1.45, "O(n log n)"), (2.25, "O(n^2)"),
                            (3.25, "O(n^3)")):
        if exponent < threshold:
            return name
    return "worse than O(n^3) -- likely exponential"


def measure_scaling(
    func: Callable[[Sequence[int]], object],
    make_input: Callable[[int], Sequence[int]],
    sizes: Sequence[int] = (1_000, 2_000, 4_000, 8_000, 16_000),
    repeats: int = 3,
) -> ScalingReport:
    """Time ``func`` across growing inputs and fit the scaling exponent.

    The exponent is fitted by ordinary least squares on (log n, log t), which
    is exact for a pure power law and robust enough to separate the classes
    that matter. Inputs are built outside the timed region so that input
    construction is never measured.

    Time  O(sum of func's own cost over all sizes).
    """
    if len(sizes) < 2:
        raise ValueError("need at least two sizes to fit a slope")

    seconds: list[float] = []
    for n in sizes:
        payload = make_input(n)
        best = math.inf
        for _ in range(max(1, repeats)):
            start = time.perf_counter()
            func(payload)
            best = min(best, time.perf_counter() - start)  # min rejects noise
        seconds.append(best)

    # Least-squares slope of log(t) against log(n).
    xs = [math.log(n) for n in sizes]
    ys = [math.log(max(t, 1e-9)) for t in seconds]
    x_mean, y_mean = sum(xs) / len(xs), sum(ys) / len(ys)
    numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys))
    denominator = sum((x - x_mean) ** 2 for x in xs)
    exponent = numerator / denominator if denominator else 0.0

    return ScalingReport(tuple(sizes), tuple(seconds),
                         round(exponent, 3), _classify(exponent))
