"""Unit tests for Chapter 23."""
from __future__ import annotations
from dsa_labs.chapter_23.dag_executor import Step, DagExecutor, StepState
from dsa_labs.chapter_23.leetcode_solutions import find_center, can_finish, network_delay_time

def test_dag_executor():
    steps = [Step("s1", duration_s=0.01), Step("s2", duration_s=0.01, depends_on=("s1",))]
    executor = DagExecutor(steps)
    rep = executor.run(execute=lambda s: True)
    assert rep.states["s1"] == StepState.COMPLETED
    assert rep.states["s2"] == StepState.COMPLETED

def test_find_center():
    assert find_center([[1,2],[2,3],[4,2]]) == 2

def test_can_finish():
    assert can_finish(2, [[1,0]]) is True
    assert can_finish(2, [[1,0],[0,1]]) is False

def test_network_delay_time():
    times = [[2,1,1],[2,3,1],[3,4,1]]
    assert network_delay_time(times, 4, 2) == 2
