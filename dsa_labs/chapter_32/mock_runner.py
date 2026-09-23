"""Mock Interview Runner (Chapter 32)."""
from __future__ import annotations
from dsa_labs.chapter_32.rubric import LoopReport, RoundScore, Dimension

class MockRunner:
    def __init__(self, candidate_name: str):
        self.report = LoopReport(candidate=candidate_name)

    def add_round(self, round_score: RoundScore) -> None:
        self.report.rounds.append(round_score)

    def evaluate(self) -> str:
        return self.report.recommendation()
