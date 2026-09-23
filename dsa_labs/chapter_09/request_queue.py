"""Module request_queue.py for chapter_09."""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from enum import Enum


class Rejection(Enum):
    NONE = "accepted"
    QUEUE_FULL = "queue_full"
    ALREADY_EXPIRED = "already_expired"


@dataclass(frozen=True)
class QueuedRequest:
    request_id: str
    enqueued_ms: float
    deadline_ms: float          # absolute time after which the answer is useless
    estimated_tokens: int


@dataclass
class QueueStats:
    accepted: int = 0
    rejected_full: int = 0
    dropped_expired: int = 0
    served: int = 0


class BoundedRequestQueue:
    """FIFO admission queue with a hard bound and deadline-aware dropping.

    Design decisions, each stated because each is a trade:
      * BOUNDED: an unbounded queue converts overload into unbounded latency
        and eventually an OOM. A bound converts it into a fast rejection,
        which clients can retry or degrade on.
      * DEADLINE DROP ON DEQUEUE: a request whose deadline has passed is
        discarded without being served, so GPU time is never spent producing
        an answer nobody is waiting for.
      * TAIL DROP: new arrivals are rejected when full, rather than evicting
        queued requests. This favours requests that have already waited,
        which is the fair default; see `pop_newest_first` for the overload
        alternative.

    All operations are O(1) amortised.
    """

    def __init__(self, max_depth: int, max_queued_tokens: int) -> None:
        if max_depth <= 0 or max_queued_tokens <= 0:
            raise ValueError("bounds must be positive")
        self._max_depth = max_depth
        self._max_tokens = max_queued_tokens
        self._q: deque[QueuedRequest] = deque()
        self._queued_tokens = 0
        self.stats = QueueStats()

    def __len__(self) -> int:
        return len(self._q)

    @property
    def queued_tokens(self) -> int:
        return self._queued_tokens

    def offer(self, request: QueuedRequest, now_ms: float) -> Rejection:
        """Admit a request, or say why not. O(1)."""
        if request.deadline_ms <= now_ms:
            self.stats.dropped_expired += 1
            return Rejection.ALREADY_EXPIRED
        # Bound on BOTH count and work: 32 requests of 4k tokens each is a
        # very different queue from 32 requests of 50 tokens each, and only
        # the token bound reflects the actual wait a new arrival faces.
        if (len(self._q) >= self._max_depth
                or self._queued_tokens + request.estimated_tokens > self._max_tokens):
            self.stats.rejected_full += 1
            return Rejection.QUEUE_FULL
        self._q.append(request)
        self._queued_tokens += request.estimated_tokens
        self.stats.accepted += 1
        return Rejection.NONE

    def poll(self, now_ms: float) -> QueuedRequest | None:
        """Take the next servable request, discarding expired ones. O(1) amortised."""
        while self._q:
            head = self._q.popleft()
            self._queued_tokens -= head.estimated_tokens
            if head.deadline_ms <= now_ms:
                self.stats.dropped_expired += 1
                continue                     # never serve a dead request
            self.stats.served += 1
            return head
        return None

    def poll_newest_first(self, now_ms: float) -> QueuedRequest | None:
        """LIFO variant for saturated conditions.

        Under sustained overload the oldest queued requests are the most
        likely to have already been abandoned client-side, so serving the
        newest maximises the fraction of answers that still matter. It
        starves the tail, so it is an overload mode, not a default.
        """
        while self._q:
            newest = self._q.pop()
            self._queued_tokens -= newest.estimated_tokens
            if newest.deadline_ms <= now_ms:
                self.stats.dropped_expired += 1
                continue
            self.stats.served += 1
            return newest
        return None
