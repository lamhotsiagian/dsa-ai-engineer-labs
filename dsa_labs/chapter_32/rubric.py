"""Module rubric.py for chapter_32."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum


class Dimension(IntEnum):
    PROBLEM_SOLVING = 0
    CODING = 1
    COMPLEXITY = 2
    VERIFICATION = 3
    COMMUNICATION = 4
    JUDGEMENT = 5
    RECOVERY = 6


# Weights reflect how loops actually decide. Verification and recovery are
# weighted like coding, which is the part candidates consistently
# underestimate -- and they are also the two most often left blank.
WEIGHTS: dict[Dimension, float] = {
    Dimension.PROBLEM_SOLVING: 1.5,
    Dimension.CODING: 1.5,
    Dimension.COMPLEXITY: 1.0,
    Dimension.VERIFICATION: 1.5,
    Dimension.COMMUNICATION: 1.5,
    Dimension.JUDGEMENT: 1.0,
    Dimension.RECOVERY: 1.5,
}

BAR = 3.0          # "solid: meets the bar"


@dataclass
class RoundScore:
    """One interview round.

    A dimension with no score is NOT neutral: it is unobserved, and an
    interviewer cannot write down what they did not see. `covered` makes
    that distinction explicit so a loop report can say 'never exercised'
    instead of silently averaging it away.
    """
    name: str
    scores: dict[Dimension, int] = field(default_factory=dict)
    evidence: dict[Dimension, str] = field(default_factory=dict)

    def record(self, dimension: Dimension, score: int,
               evidence: str = "") -> None:
        if not 1 <= score <= 4:
            raise ValueError("scores run 1 (weak) to 4 (strong)")
        if not evidence:
            # Enforced on purpose: a score with no evidence behind it is
            # an impression, and impressions are what rubrics exist to
            # replace.
            raise ValueError(f"{dimension.name} needs one line of evidence")
        self.scores[dimension] = score
        self.evidence[dimension] = evidence

    @property
    def covered(self) -> set[Dimension]:
        return set(self.scores)

    @property
    def weighted(self) -> float:
        """Mean over OBSERVED dimensions only; 0.0 if nothing observed."""
        if not self.scores:
            return 0.0
        total = sum(WEIGHTS[d] for d in self.scores)
        earned = sum(WEIGHTS[d] * s for d, s in self.scores.items())
        return earned / total


@dataclass
class LoopReport:
    candidate: str
    rounds: list[RoundScore] = field(default_factory=list)

    @property
    def blind_spots(self) -> list[Dimension]:
        """Dimensions no round exercised. These decide close calls: an
        unexercised dimension means a later round carries all its weight,
        and one bad moment there has nothing to balance it."""
        seen: set[Dimension] = set()
        for round_ in self.rounds:
            seen |= round_.covered
        return sorted(set(Dimension) - seen)

    def per_dimension(self) -> dict[Dimension, float | None]:
        """Mean per dimension across the rounds that observed it."""
        out: dict[Dimension, float | None] = {}
        for dimension in Dimension:
            observed = [r.scores[dimension] for r in self.rounds
                        if dimension in r.scores]
            out[dimension] = (sum(observed) / len(observed)
                              if observed else None)
        return out

    def recommendation(self) -> str:
        if not self.rounds:
            return "no signal"
        means = self.per_dimension()
        weak = [d for d, m in means.items() if m is not None and m < 2.0]
        if weak:
            return "no hire: " + ", ".join(d.name.lower() for d in weak)
        overall = sum(r.weighted for r in self.rounds) / len(self.rounds)
        if overall >= 3.5:
            return "strong hire"
        if overall >= BAR:
            return "hire"
        return "no hire: below the bar overall"
