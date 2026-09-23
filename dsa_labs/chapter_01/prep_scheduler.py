"""Module prep_scheduler.py for chapter_01."""
from __future__ import annotations

import heapq
from dataclasses import dataclass, field
from datetime import date, timedelta

# Spaced-repetition intervals in days. Index = number of successful reviews.
REVIEW_INTERVALS_DAYS: tuple[int, ...] = (1, 3, 7, 16, 35, 70)


@dataclass(order=True)
class Topic:
    """One preparation topic with a self-assessed confidence level.

    Ordering is by ``-priority`` so that the standard min-heap in ``heapq``
    yields the highest-priority topic first. ``sort_index`` is the only field
    used for comparison; everything else is excluded so that two topics with
    equal priority never raise on a tie.
    """

    sort_index: float = field(init=False, repr=False)
    name: str = field(compare=False)
    chapter: int = field(compare=False)
    confidence: int = field(compare=False)        # 1 (shaky) .. 5 (solid)
    frequency_weight: float = field(compare=False)  # how often it is asked, 0..1
    successful_reviews: int = field(compare=False, default=0)
    last_reviewed: date | None = field(compare=False, default=None)

    def __post_init__(self) -> None:
        if not 1 <= self.confidence <= 5:
            raise ValueError(f"confidence must be in 1..5, got {self.confidence}")
        if not 0.0 <= self.frequency_weight <= 1.0:
            raise ValueError("frequency_weight must be in [0.0, 1.0]")
        self.sort_index = -self.priority()

    def priority(self) -> float:
        """Risk score: how much an hour spent here changes the outcome.

        Low confidence and high interview frequency both raise the score, and
        they multiply rather than add: a topic that is shaky *and* frequently
        asked is the single worst place to be, and the score should say so.
        """
        gap = (5 - self.confidence) / 4.0          # 0.0 solid .. 1.0 shaky
        return round(gap * self.frequency_weight, 6)

    def due_on(self) -> date | None:
        """Next review date under the spaced-repetition schedule."""
        if self.last_reviewed is None:
            return None                            # never studied: always due
        idx = min(self.successful_reviews, len(REVIEW_INTERVALS_DAYS) - 1)
        return self.last_reviewed + timedelta(days=REVIEW_INTERVALS_DAYS[idx])

    def is_due(self, today: date) -> bool:
        due = self.due_on()
        return due is None or due <= today


def next_sessions(topics: list[Topic], today: date, count: int) -> list[Topic]:
    """Return the ``count`` highest-risk topics that are due today.

    Uses a bounded heap rather than a full sort: with a few hundred topics the
    difference is irrelevant, but the shape is the one you want in production
    when the candidate set is the whole index and ``count`` is small.
    Time  O(n log count), Space O(count).
    """
    if count <= 0:
        return []
    due = (t for t in topics if t.is_due(today))
    # nsmallest over sort_index == -priority gives the highest priorities.
    return heapq.nsmallest(count, due)
