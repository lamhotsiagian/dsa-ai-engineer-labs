"""Session logger (Chapter 31)."""
from __future__ import annotations
from dsa_labs.chapter_31.protocol import PROTOCOL, SessionScore, Signal, aggregate

class SessionLogger:
    def __init__(self):
        self.sessions: list[SessionScore] = []

    def log(self, session: SessionScore) -> None:
        self.sessions.append(session)

    def report(self) -> dict[int, float]:
        return aggregate(self.sessions)
