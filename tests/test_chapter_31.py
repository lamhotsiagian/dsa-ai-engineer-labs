"""Unit tests for Chapter 31."""
from __future__ import annotations
from dsa_labs.chapter_31.protocol import SessionScore, Signal, Step, PROTOCOL
from dsa_labs.chapter_31.session_log import SessionLogger

def test_protocol_scoring():
    session = SessionScore(problem="Two Sum", minutes=20, solved=True)
    session.record(1, Signal.STRONG)
    session.record(2, Signal.SOLID)
    assert session.weighted_score > 0.0
    summary = session.summary()
    assert "Two Sum: solved" in summary

def test_session_logger():
    logger = SessionLogger()
    s = SessionScore(problem="LRU", minutes=25, solved=True)
    s.record(1, Signal.STRONG)
    logger.log(s)
    rep = logger.report()
    assert 1 in rep
    assert rep[1] == 3.0
