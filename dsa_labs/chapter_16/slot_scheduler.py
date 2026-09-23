"""Module slot_scheduler.py for chapter_16."""
from __future__ import annotations

import heapq
from dataclasses import dataclass, field
from enum import Enum


class Admission(Enum):
    ADMITTED = "admitted"
    NO_SLOT = "no_slot"
    NO_MEMORY = "no_memory"
    DEADLINE_UNREACHABLE = "deadline_unreachable"


@dataclass(frozen=True)
class Job:
    job_id: str
    arrival_ms: float
    estimated_duration_ms: float
    kv_blocks: int                  # memory footprint while running
    deadline_ms: float


@dataclass(order=True)
class _Running:
    """Heap entry ordered by projected finish time."""
    finish_ms: float
    sequence: int = field(compare=True)
    job: Job = field(compare=False)


@dataclass
class SchedulerStats:
    admitted: int = 0
    rejected_no_slot: int = 0
    rejected_no_memory: int = 0
    rejected_deadline: int = 0
    overruns: int = 0


class SlotScheduler:
    """Admission control for a fixed pool of inference slots.

    Two independent capacity constraints, which is what distinguishes this
    from the textbook meeting-rooms problem:
      * slot count   -- the batch dimension the engine supports
      * KV blocks    -- GPU memory, which different jobs consume unequally

    A job is admitted only if BOTH permit it. Running jobs are held in a
    min-heap keyed by projected finish time, so reclaiming capacity is
    O(log n) per completion and checking the earliest completion is O(1).

    admit / release: O(log n). Memory O(slots).
    """

    def __init__(self, max_slots: int, max_kv_blocks: int) -> None:
        if max_slots <= 0 or max_kv_blocks <= 0:
            raise ValueError("capacities must be positive")
        self.max_slots = max_slots
        self.max_kv_blocks = max_kv_blocks
        self._running: list[_Running] = []
        self._kv_used = 0
        self._sequence = 0
        self.stats = SchedulerStats()

    @property
    def free_slots(self) -> int:
        return self.max_slots - len(self._running)

    @property
    def free_kv_blocks(self) -> int:
        return self.max_kv_blocks - self._kv_used

    def _reap(self, now_ms: float) -> None:
        """Release jobs whose projected finish time has passed. O(k log n)."""
        while self._running and self._running[0].finish_ms <= now_ms:
            done = heapq.heappop(self._running)
            self._kv_used -= done.job.kv_blocks

    def earliest_free_slot(self, now_ms: float) -> float:
        """When a slot next becomes available. O(1) given a reaped heap."""
        if len(self._running) < self.max_slots:
            return now_ms
        return self._running[0].finish_ms if self._running else now_ms

    def admit(self, job: Job, now_ms: float) -> Admission:
        """Decide whether to start `job` now."""
        if job.estimated_duration_ms < 0 or job.kv_blocks <= 0:
            raise ValueError("duration must be non-negative and kv_blocks positive")
        self._reap(now_ms)

        # Reject up front if even an immediate start misses the deadline.
        # Admitting a doomed job wastes the scarcest resource in the system.
        if now_ms + job.estimated_duration_ms > job.deadline_ms:
            self.stats.rejected_deadline += 1
            return Admission.DEADLINE_UNREACHABLE

        if len(self._running) >= self.max_slots:
            self.stats.rejected_no_slot += 1
            return Admission.NO_SLOT
        if job.kv_blocks > self.free_kv_blocks:
            self.stats.rejected_no_memory += 1
            return Admission.NO_MEMORY

        self._sequence += 1
        heapq.heappush(self._running,
                       _Running(finish_ms=now_ms + job.estimated_duration_ms,
                                sequence=self._sequence, job=job))
        self._kv_used += job.kv_blocks
        self.stats.admitted += 1
        return Admission.ADMITTED

    def report_actual_finish(self, job_id: str, actual_ms: float) -> None:
        """Correct a finish time when the estimate was wrong.

        LLM output length is not known at admission, so estimates are
        routinely wrong in both directions. Leaving the heap keyed on a stale
        estimate silently corrupts capacity accounting, so the scheduler must
        accept corrections rather than assume its predictions.

        Time O(n) to locate plus O(n) to re-heapify -- acceptable because the
        heap is bounded by the slot count, which is small.
        """
        for entry in self._running:
            if entry.job.job_id == job_id:
                if actual_ms > entry.finish_ms:
                    self.stats.overruns += 1
                entry.finish_ms = actual_ms
                heapq.heapify(self._running)
                return
        raise KeyError(f"job {job_id} is not running")


def peak_concurrency(jobs: list[Job]) -> int:
    """Offline: how many slots WOULD have been needed for this trace.

    Replaying a production trace through this function gives the capacity
    requirement directly, which is a far better basis for a replica count
    than a guess. Time O(n log n), Space O(n).
    """
    events: list[tuple[float, int]] = []
    for job in jobs:
        events.append((job.arrival_ms, +1))
        events.append((job.arrival_ms + job.estimated_duration_ms, -1))
    events.sort()
    current = peak = 0
    for _, delta in events:
        current += delta
        peak = max(peak, current)
    return peak
