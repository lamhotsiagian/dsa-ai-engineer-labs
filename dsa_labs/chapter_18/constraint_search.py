"""Module constraint_search.py for chapter_18."""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Callable, Iterable, Sequence, TypeVar

S = TypeVar("S")            # a partial solution
C = TypeVar("C")            # a single choice


@dataclass
class SearchBudget:
    """Hard limits. A search without these is an outage waiting to happen."""
    max_nodes: int = 100_000
    max_depth: int = 64
    max_seconds: float = 1.0


@dataclass
class SearchReport:
    solutions: int = 0
    nodes_explored: int = 0
    nodes_pruned: int = 0
    max_depth_reached: int = 0
    truncated: bool = False
    reason: str = ""

    @property
    def prune_rate(self) -> float:
        total = self.nodes_explored + self.nodes_pruned
        return self.nodes_pruned / total if total else 0.0


class BudgetExhausted(Exception):
    """Raised internally to unwind the search when a limit is hit."""


def bounded_search(
    initial: S,
    is_complete: Callable[[S], bool],
    candidates: Callable[[S], Iterable[C]],
    is_valid: Callable[[S, C], bool],
    apply: Callable[[S, C], None],
    undo: Callable[[S, C], None],
    snapshot: Callable[[S], object],
    *,
    budget: SearchBudget | None = None,
    max_solutions: int | None = None,
) -> tuple[list[object], SearchReport]:
    """Backtracking search with hard limits and an honest report.

    Returns (solutions, report). `report.truncated` says whether the search
    was cut short -- so a caller can distinguish "no solutions exist" from
    "we ran out of budget", which are very different answers and are
    routinely conflated.

    Time  O(nodes explored x work per node), bounded by the budget.
    Space O(max_depth) recursion plus the solutions.
    """
    budget = budget or SearchBudget()
    results: list[object] = []
    report = SearchReport()
    deadline = time.perf_counter() + budget.max_seconds

    def explore(state: S, depth: int) -> None:
        report.nodes_explored += 1
        report.max_depth_reached = max(report.max_depth_reached, depth)

        # Check limits on every node, not only at the top: a single branch
        # can run away, and the deadline is what makes this safe to call
        # from a request path.
        if report.nodes_explored > budget.max_nodes:
            report.truncated, report.reason = True, "node limit"
            raise BudgetExhausted
        if time.perf_counter() > deadline:
            report.truncated, report.reason = True, "time limit"
            raise BudgetExhausted

        if is_complete(state):
            results.append(snapshot(state))
            report.solutions += 1
            if max_solutions is not None and len(results) >= max_solutions:
                report.reason = "solution limit"
                raise BudgetExhausted
            return

        if depth >= budget.max_depth:
            report.truncated, report.reason = True, "depth limit"
            return                          # prune this branch, keep searching

        for choice in candidates(state):
            if not is_valid(state, choice):
                report.nodes_pruned += 1
                continue
            apply(state, choice)
            try:
                explore(state, depth + 1)
            finally:
                undo(state, choice)         # undo even when unwinding

    try:
        explore(initial, 0)
    except BudgetExhausted:
        pass
    return results, report


# ---------------------------------------------------------------------------
# A concrete instance: tool-call sequences with preconditions and effects.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Tool:
    name: str
    requires: frozenset[str] = field(default_factory=frozenset)
    provides: frozenset[str] = field(default_factory=frozenset)
    cost: float = 1.0


def plan_tool_sequence(
    tools: Sequence[Tool],
    initial_facts: frozenset[str],
    goal_facts: frozenset[str],
    *,
    budget: SearchBudget | None = None,
    max_plans: int = 5,
) -> tuple[list[list[str]], SearchReport]:
    """Find tool-call sequences that reach the goal from the initial facts.

    Pruning: a tool whose preconditions are unmet is skipped without
    recursing, and a tool that adds nothing new is skipped as well -- a
    no-op step can only lengthen a plan, never enable one.

    The 'adds nothing new' rule is what keeps the search finite: without it,
    a tool with no effects could be applied forever.
    """
    facts = set(initial_facts)
    sequence: list[str] = []

    def complete(_state) -> bool:
        return goal_facts <= facts

    def available(_state):
        # Most-constrained-first: try tools that provide the most NEW facts,
        # which reaches the goal sooner and fails faster when it cannot.
        return sorted(tools,
                      key=lambda t: (-len(t.provides - facts), t.cost, t.name))

    def valid(_state, tool: Tool) -> bool:
        if not tool.requires <= facts:
            return False
        return bool(tool.provides - facts)      # must make progress

    def do(_state, tool: Tool) -> None:
        sequence.append(tool.name)
        tool_new = tool.provides - facts
        facts.update(tool_new)
        _applied.append(tool_new)

    def undo(_state, _tool: Tool) -> None:
        sequence.pop()
        facts.difference_update(_applied.pop())

    _applied: list[set[str]] = []
    return bounded_search(
        initial=None, is_complete=complete, candidates=available,
        is_valid=valid, apply=do, undo=undo,
        snapshot=lambda _s: list(sequence),
        budget=budget, max_solutions=max_plans,
    )
