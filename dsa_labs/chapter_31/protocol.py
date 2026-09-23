"""Module protocol.py for chapter_31."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum


class Signal(IntEnum):
    """The four-point scale most interview rubrics reduce to."""
    NO_EVIDENCE = 0
    WEAK = 1
    SOLID = 2
    STRONG = 3


@dataclass(frozen=True)
class Step:
    number: int
    name: str
    minute_window: tuple[int, int]
    observable: str           # what the interviewer must be able to WRITE DOWN
    weight: float


PROTOCOL: tuple[Step, ...] = (
    Step(1, "Restate the problem", (0, 1),
         "candidate restated it in their own words and got confirmation",
         0.5),
    Step(2, "Clarifying questions", (1, 3),
         "asked questions whose answers change the algorithm", 1.0),
    Step(3, "Hand-trace an example", (3, 5),
         "produced the expected output by hand before coding", 0.5),
    Step(4, "Brute force stated", (5, 6),
         "named the naive approach and its cost", 0.5),
    Step(5, "Found the redundant work", (6, 9),
         "identified what the inner loop recomputes", 1.5),
    Step(6, "Approach agreed", (9, 11),
         "proposed the approach and paused for agreement", 1.0),
    Step(7, "Complexity before coding", (11, 12),
         "stated time and space as a prediction", 1.0),
    Step(8, "Implementation", (12, 28),
         "skeleton first; narrated decisions, not keystrokes", 2.0),
    Step(9, "Traced the finished code", (28, 33),
         "walked a concrete input line by line, aloud", 1.5),
    Step(10, "Edge cases", (33, 38),
         "enumerated by category and tested the risky ones", 1.5),
    Step(11, "Trade-offs and production", (38, 45),
         "compared on a dimension other than big-O", 1.0),
)

TOTAL_WEIGHT = sum(step.weight for step in PROTOCOL)


@dataclass
class SessionScore:
    """Self-assessment of one practice session.

    Scoring yourself against an explicit rubric is the only way to get a
    feedback signal when practising alone. The absolute number matters far
    less than which steps are consistently weak across sessions.
    """
    problem: str
    minutes: int
    solved: bool
    marks: dict[int, Signal] = field(default_factory=dict)
    notes: dict[int, str] = field(default_factory=dict)

    def record(self, step_number: int, signal: Signal,
               note: str = "") -> None:
        if not any(s.number == step_number for s in PROTOCOL):
            raise ValueError(f"no step {step_number} in the protocol")
        self.marks[step_number] = signal
        if note:
            self.notes[step_number] = note

    @property
    def weighted_score(self) -> float:
        """0.0 to 1.0. Unrecorded steps count as NO_EVIDENCE on purpose:
        a step the interviewer could not observe did not happen."""
        earned = sum(
            step.weight * self.marks.get(step.number, Signal.NO_EVIDENCE)
            for step in PROTOCOL)
        return earned / (TOTAL_WEIGHT * Signal.STRONG)

    def weakest(self, count: int = 3) -> list[Step]:
        """The steps to drill next: lowest signal, highest weight first."""
        return sorted(
            PROTOCOL,
            key=lambda s: (self.marks.get(s.number, Signal.NO_EVIDENCE),
                           -s.weight),
        )[:count]

    def summary(self) -> str:
        verdict = "solved" if self.solved else "not solved"
        lines = [f"{self.problem}: {verdict} in {self.minutes} min, "
                 f"protocol {self.weighted_score:.0%}"]
        for step in self.weakest():
            mark = self.marks.get(step.number, Signal.NO_EVIDENCE)
            lines.append(f"  drill step {step.number} ({step.name}): "
                         f"{mark.name} -- {step.observable}")
        return "\n".join(lines)


def aggregate(sessions: list[SessionScore]) -> dict[int, float]:
    """Mean signal per step across sessions.

    One bad session is noise; a step that is weak across ten is the thing
    to practise. This is the whole point of keeping the log -- the pattern
    is invisible from inside any single session.
    """
    if not sessions:
        return {}
    return {
        step.number: sum(
            s.marks.get(step.number, Signal.NO_EVIDENCE) for s in sessions
        ) / len(sessions)
        for step in PROTOCOL
    }
