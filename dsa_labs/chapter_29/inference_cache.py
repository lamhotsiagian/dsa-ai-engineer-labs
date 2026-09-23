"""Module inference_cache.py for chapter_29."""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Hashable


@dataclass
class CacheEntry:
    """One cached value plus the accounting eviction needs."""
    key: Hashable
    value: Any
    size_bytes: int
    recompute_cost: float          # seconds, or any consistent unit
    expires_at: float | None
    previous: "CacheEntry | None" = None
    next: "CacheEntry | None" = None


class InferenceCache:
    """LRU over a byte budget, with TTL, single-flight, and metrics.

    Composition:
      _index  dict[key] -> CacheEntry     O(1) lookup
      list    doubly linked, MRU first    O(1) promote and evict
    Invariant: _index.values() are exactly the real nodes between the
    sentinels, and _used_bytes is their summed size_bytes.

    get / put are O(1) amortised; a put may evict several entries, but
    each eviction is O(1) and every entry is evicted at most once.
    """

    def __init__(self, capacity_bytes: int,
                 default_ttl_seconds: float | None = None,
                 clock: Callable[[], float] = time.monotonic) -> None:
        if capacity_bytes <= 0:
            raise ValueError("capacity_bytes must be positive")
        self.capacity_bytes = capacity_bytes
        self.default_ttl_seconds = default_ttl_seconds
        self._clock = clock

        self._index: dict[Hashable, CacheEntry] = {}
        self._used_bytes = 0

        # Sentinels. Every unlink and insert is then three assignments with
        # no None checks -- which is where roughly half of all LRU bugs live.
        self._head = CacheEntry(key=None, value=None, size_bytes=0,
                                recompute_cost=0.0, expires_at=None)
        self._tail = CacheEntry(key=None, value=None, size_bytes=0,
                                recompute_cost=0.0, expires_at=None)
        self._head.next = self._tail
        self._tail.previous = self._head

        self._lock = threading.RLock()
        self._in_flight: dict[Hashable, threading.Event] = {}
        self.hits = self.misses = self.evictions = self.expirations = 0

    # -- list surgery -----------------------------------------------------
    def _unlink(self, entry: CacheEntry) -> None:
        entry.previous.next = entry.next
        entry.next.previous = entry.previous
        entry.previous = entry.next = None

    def _push_front(self, entry: CacheEntry) -> None:
        entry.next = self._head.next
        entry.previous = self._head
        self._head.next.previous = entry
        self._head.next = entry

    # -- public API -------------------------------------------------------
    def get(self, key: Hashable) -> Any | None:
        with self._lock:
            entry = self._index.get(key)
            if entry is None:
                self.misses += 1
                return None
            if entry.expires_at is not None and self._clock() >= entry.expires_at:
                # Expiry is checked lazily on read. A background sweeper is
                # only worth it when expired entries would otherwise pin a
                # lot of memory for a long time.
                self._remove(entry)
                self.expirations += 1
                self.misses += 1
                return None
            self._unlink(entry)
            self._push_front(entry)
            self.hits += 1
            return entry.value

    def put(self, key: Hashable, value: Any, size_bytes: int,
            recompute_cost: float = 1.0,
            ttl_seconds: float | None = None) -> None:
        if size_bytes <= 0:
            raise ValueError("size_bytes must be positive")
        with self._lock:
            existing = self._index.get(key)
            if existing is not None:
                self._remove(existing)          # replace, do not duplicate

            if size_bytes > self.capacity_bytes:
                # Refusing is correct: admitting it would evict the entire
                # cache to store one entry that cannot fit anyway.
                return

            ttl = ttl_seconds if ttl_seconds is not None \
                else self.default_ttl_seconds
            entry = CacheEntry(
                key=key, value=value, size_bytes=size_bytes,
                recompute_cost=recompute_cost,
                expires_at=None if ttl is None else self._clock() + ttl)

            while self._used_bytes + size_bytes > self.capacity_bytes:
                self._evict_one()

            self._index[key] = entry
            self._push_front(entry)
            self._used_bytes += size_bytes

    def _remove(self, entry: CacheEntry) -> None:
        self._unlink(entry)
        del self._index[entry.key]
        self._used_bytes -= entry.size_bytes

    def _evict_one(self) -> None:
        victim = self._tail.previous
        if victim is self._head:                # empty: cannot happen if
            raise RuntimeError("cache underflow")   # the accounting is right
        self._remove(victim)
        self.evictions += 1

    def get_or_compute(self, key: Hashable, compute: Callable[[], Any],
                       size_bytes: int, recompute_cost: float = 1.0) -> Any:
        """Single-flight: N concurrent misses on one key do ONE compute.

        Without this, a cold start on a popular key sends N identical
        requests to the model service -- the thundering herd, and the
        reason a cache can make an outage worse instead of better.
        """
        cached = self.get(key)
        if cached is not None:
            return cached

        with self._lock:
            waiter = self._in_flight.get(key)
            if waiter is None:
                waiter = threading.Event()
                self._in_flight[key] = waiter
                leader = True
            else:
                leader = False

        if not leader:
            waiter.wait(timeout=30.0)
            cached = self.get(key)
            # A None here means the leader failed. Computing it ourselves is
            # the right fallback: it is slower than waiting, and correct.
            return cached if cached is not None else compute()

        try:
            value = compute()
            self.put(key, value, size_bytes, recompute_cost)
            return value
        finally:
            with self._lock:
                self._in_flight.pop(key, None)
            waiter.set()

    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total else 0.0
