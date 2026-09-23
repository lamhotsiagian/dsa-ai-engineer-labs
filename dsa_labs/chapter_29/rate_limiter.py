"""Module rate_limiter.py for chapter_29."""
from __future__ import annotations

import threading
import time
from collections import OrderedDict
from dataclasses import dataclass


@dataclass
class Bucket:
    tokens: float
    last_refill: float


class TokenBucketLimiter:
    """Per-key token bucket. O(1) time and O(1) space per tracked key.

    capacity -> the burst that is tolerated
    rate     -> the sustained tokens per second

    There is no timer and no sweeper thread: refill is computed from
    elapsed time on each call, which is what keeps this O(1) and makes it
    safe to have millions of keys.

    The bucket map is an LRU with a hard cap, because a per-key limiter
    over an unbounded key space is a memory leak with a rate limiter
    attached -- the failure mode nobody mentions until it happens.
    """

    def __init__(self, capacity: float, refill_rate_per_second: float,
                 max_tracked_keys: int = 100_000,
                 clock=time.monotonic) -> None:
        if capacity <= 0 or refill_rate_per_second <= 0:
            raise ValueError("capacity and refill rate must be positive")
        self.capacity = float(capacity)
        self.rate = float(refill_rate_per_second)
        self.max_tracked_keys = max_tracked_keys
        self._clock = clock
        self._buckets: OrderedDict[str, Bucket] = OrderedDict()
        self._lock = threading.Lock()

    def allow(self, key: str, cost: float = 1.0) -> bool:
        """True if the request fits in the budget; False to reject.

        `cost` exists because request count is the wrong unit for LLM
        traffic: a 4000-token generation is not one unit of the same thing
        as a 20-token one. Charge estimated tokens, and reconcile with
        actuals afterwards if the estimate can be badly wrong.
        """
        if cost <= 0:
            raise ValueError("cost must be positive")
        now = self._clock()
        with self._lock:
            bucket = self._buckets.get(key)
            if bucket is None:
                bucket = Bucket(tokens=self.capacity, last_refill=now)
                self._buckets[key] = bucket
                self._evict_if_needed()
            else:
                self._buckets.move_to_end(key)

            elapsed = max(0.0, now - bucket.last_refill)
            bucket.tokens = min(self.capacity,
                                bucket.tokens + elapsed * self.rate)
            bucket.last_refill = now

            if bucket.tokens >= cost:
                bucket.tokens -= cost
                return True
            return False

    def retry_after_seconds(self, key: str, cost: float = 1.0) -> float:
        """How long until `cost` tokens are available. Send it in the 429.

        A rejection without a Retry-After invites an immediate retry, which
        is how a rate limiter turns a burst into a sustained overload.
        """
        with self._lock:
            bucket = self._buckets.get(key)
            available = self.capacity if bucket is None else bucket.tokens
        deficit = max(0.0, cost - available)
        return deficit / self.rate

    def _evict_if_needed(self) -> None:
        while len(self._buckets) > self.max_tracked_keys:
            # Evicting the least recently used key resets it to a full
            # bucket, which is generous -- the alternative, rejecting new
            # keys once the map is full, is a denial of service on
            # legitimate traffic. Size the cap so this is rare.
            self._buckets.popitem(last=False)
