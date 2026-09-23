"""Unit tests for Chapter 32."""
from __future__ import annotations
from dsa_labs.chapter_32.rubric import Dimension, RoundScore, LoopReport
from dsa_labs.chapter_32.mock_runner import MockRunner

def test_loop_scoring():
    r1 = RoundScore("coding")
    r1.record(Dimension.PROBLEM_SOLVING, 4, "Optimal approach identified in 4 min")
    r1.record(Dimension.CODING, 4, "Clean syntax and modular design")
    r1.record(Dimension.COMPLEXITY, 4, "Accurately stated trade-offs")
    r1.record(Dimension.VERIFICATION, 3, "Traced through edge cases")
    assert r1.weighted >= 3.5

    runner = MockRunner(candidate_name="Alice")
    runner.add_round(r1)
    eval_res = runner.evaluate()
    assert "hire" in eval_res
