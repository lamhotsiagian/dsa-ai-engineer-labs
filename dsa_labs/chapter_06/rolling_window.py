"""Module rolling_window.py for chapter_06."""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True)
class Decision:
    allowed: bool
    current_tokens: int
    limit: int
    retry_after_s: float        # 0.0 when allowed


class ExactRollingWindow:
    """Exact rolling-window token counter for one key.

    Keeps every (timestamp, tokens) event inside the horizon and evicts from
    the front. Amortised O(1) per call: each event is appended once and
    popped once, so the eviction loop is O(1) amortised even though it is a
    while loop.

    Memory is O(events in window), which is the reason production systems
    often prefer the bucketed approximation below.
    """

    def __init__(self, limit_tokens: int, horizon_s: float) -> None:
        if limit_tokens <= 0 or horizon_s <= 0:
            raise ValueError("limit_tokens and horizon_s must be positive")
        self._limit = limit_tokens
        self._horizon = horizon_s
        self._events: deque[tuple[float, int]] = deque()
        self._total = 0

    def _evict(self, now_s: float) -> None:
        cutoff = now_s - self._horizon
        while self._events and self._events[0][0] <= cutoff:
            _, tokens = self._events.popleft()
            self._total -= tokens

    def try_consume(self, now_s: float, tokens: int) -> Decision:
        """Admit ``tokens`` if the rolling total would stay within the limit."""
        if tokens < 0:
            raise ValueError("tokens must be non-negative")
        self._evict(now_s)

        if self._total + tokens > self._limit:
            # How long until enough of the oldest events age out?
            deficit = self._total + tokens - self._limit
            freed = 0
            retry_at = now_s
            for ts, ev_tokens in self._events:
                freed += ev_tokens
                retry_at = ts + self._horizon
                if freed >= deficit:
                    break
            return Decision(False, self._total, self._limit,
                            max(0.0, retry_at - now_s))

        self._events.append((now_s, tokens))
        self._total += tokens
        return Decision(True, self._total, self._limit, 0.0)


class BucketedRollingWindow:
    """Constant-memory approximation of a rolling window.

    Divides the horizon into ``buckets`` fixed slots and keeps one counter
    each, in a ring. Memory is O(buckets) regardless of event rate; the cost
    is boundary granularity of horizon/buckets seconds.

    With 60 buckets over a 60 s horizon the window is accurate to one second,
    which is almost always sufficient for a rate limiter and uses 60 integers
    instead of millions of events.
    """

    def __init__(self, limit_tokens: int, horizon_s: float, buckets: int = 60) -> None:
        if buckets <= 0:
            raise ValueError("buckets must be positive")
        self._limit = limit_tokens
        self._horizon = horizon_s
        self._width = horizon_s / buckets
        self._counts = [0] * buckets
        self._stamps = [-1] * buckets          # bucket index each slot holds
        self._n = buckets

    def _refresh(self, now_s: float) -> int:
        """Expire slots whose bucket index is outside the current horizon."""
        current = int(now_s // self._width)
        oldest = current - self._n + 1
        for slot in range(self._n):
            if self._stamps[slot] < oldest:
                self._counts[slot] = 0
                self._stamps[slot] = -1
        return current

    def try_consume(self, now_s: float, tokens: int) -> Decision:
        current = self._refresh(now_s)
        total = sum(self._counts)
        if total + tokens > self._limit:
            return Decision(False, total, self._limit, self._width)
        slot = current % self._n
        if self._stamps[slot] != current:
            self._counts[slot] = 0
            self._stamps[slot] = current
        self._counts[slot] += tokens
        return Decision(True, total + tokens, self._limit, 0.0)
