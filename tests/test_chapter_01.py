"""Unit tests for Chapter 01."""
from __future__ import annotations
from datetime import date, timedelta
from dsa_labs.chapter_01.prep_scheduler import Topic, next_sessions, REVIEW_INTERVALS_DAYS

def test_topic_priority():
    t1 = Topic(name="DP", chapter=20, confidence=1, frequency_weight=1.0)
    t2 = Topic(name="Bit", chapter=21, confidence=5, frequency_weight=0.5)
    assert t1.priority() > t2.priority()
    assert t1.sort_index < t2.sort_index

def test_next_sessions():
    today = date(2026, 9, 22)
    t1 = Topic(name="DP", chapter=20, confidence=1, frequency_weight=1.0)
    t2 = Topic(name="Bit", chapter=21, confidence=4, frequency_weight=0.5, last_reviewed=today, successful_reviews=1)
    topics = [t1, t2]
    sessions = next_sessions(topics, today, count=1)
    assert len(sessions) == 1
    assert sessions[0].name == "DP"
