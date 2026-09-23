"""Module batching.py for chapter_04."""
from __future__ import annotations

import bisect
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Request:
    request_id: str
    length: int                       # token count
    arrival_ms: float


@dataclass
class Batch:
    requests: list[Request] = field(default_factory=list)

    @property
    def padded_width(self) -> int:
        return max((r.length for r in self.requests), default=0)

    @property
    def useful_tokens(self) -> int:
        return sum(r.length for r in self.requests)

    @property
    def padded_tokens(self) -> int:
        return len(self.requests) * self.padded_width

    @property
    def efficiency(self) -> float:
        """Fraction of tensor slots that carry real tokens, in [0, 1]."""
        return self.useful_tokens / self.padded_tokens if self.requests else 1.0


# Bucket boundaries chosen so that within-bucket padding waste is bounded:
# consecutive boundaries differ by at most ~2x, so worst-case efficiency
# inside a bucket is ~50% and typical efficiency is far better.
DEFAULT_BUCKETS: tuple[int, ...] = (16, 32, 64, 128, 256, 512, 1024, 2048, 4096)


class LengthBucketBatcher:
    """Group requests of similar length so padded tensors stay dense.

    A single sorted bucket-boundary array plus ``bisect`` turns bucket
    selection into an O(log B) lookup rather than a linear scan, which matters
    when this runs on the request path at thousands of QPS.
    """

    def __init__(self, max_batch_size: int = 32,
                 max_wait_ms: float = 20.0,
                 buckets: tuple[int, ...] = DEFAULT_BUCKETS) -> None:
        if max_batch_size <= 0:
            raise ValueError("max_batch_size must be positive")
        if list(buckets) != sorted(buckets) or len(set(buckets)) != len(buckets):
            raise ValueError("buckets must be strictly increasing")
        self.max_batch_size = max_batch_size
        self.max_wait_ms = max_wait_ms
        self.buckets = buckets
        self._pending: dict[int, list[Request]] = {b: [] for b in buckets}

    def _bucket_for(self, length: int) -> int:
        """Smallest bucket boundary >= length; the largest bucket absorbs the
        overflow so an over-long request is never silently dropped."""
        idx = bisect.bisect_left(self.buckets, length)
        return self.buckets[min(idx, len(self.buckets) - 1)]

    def submit(self, request: Request) -> Batch | None:
        """Enqueue a request; return a Batch when one becomes ready."""
        if request.length <= 0:
            raise ValueError(f"length must be positive, got {request.length}")
        queue = self._pending[self._bucket_for(request.length)]
        queue.append(request)
        if len(queue) >= self.max_batch_size:
            return self._drain(queue)
        return None

    def flush_expired(self, now_ms: float) -> list[Batch]:
        """Emit any bucket whose oldest request has exceeded the deadline.

        This is what bounds tail latency: without it a rare length bucket
        could wait forever for neighbours that never arrive.
        """
        ready: list[Batch] = []
        for queue in self._pending.values():
            if queue and now_ms - queue[0].arrival_ms >= self.max_wait_ms:
                ready.append(self._drain(queue))
        return ready

    def _drain(self, queue: list[Request]) -> Batch:
        taken = queue[: self.max_batch_size]
        del queue[: self.max_batch_size]
        return Batch(requests=taken)
