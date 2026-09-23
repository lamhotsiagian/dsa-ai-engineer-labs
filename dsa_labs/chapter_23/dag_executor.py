"""Module dag_executor.py for chapter_23."""
from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable


class StepState(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"        # a dependency failed; this can never run


@dataclass(frozen=True)
class Step:
    name: str
    duration_s: float = 1.0
    depends_on: tuple[str, ...] = ()


@dataclass
class ExecutionReport:
    states: dict[str, StepState] = field(default_factory=dict)
    levels: list[list[str]] = field(default_factory=list)
    critical_path: list[str] = field(default_factory=list)
    critical_path_seconds: float = 0.0
    sequential_seconds: float = 0.0

    @property
    def theoretical_speedup(self) -> float:
        return (self.sequential_seconds / self.critical_path_seconds
                if self.critical_path_seconds else 1.0)


class DagExecutor:
    """Execute a step DAG in dependency order, parallel where possible.

    Validates the graph BEFORE running anything: unknown references,
    self-loops and cycles are configuration errors and should be rejected
    at submission rather than discovered as a hang at execution time.

    Validation O(V + E); execution O(V + E) plus the steps themselves.
    """

    def __init__(self, steps: list[Step]) -> None:
        self._steps = {s.name: s for s in steps}
        if len(self._steps) != len(steps):
            raise ValueError("duplicate step names")
        self._validate()
        self._dependents: dict[str, list[str]] = defaultdict(list)
        for step in steps:
            for dep in step.depends_on:
                self._dependents[dep].append(step.name)

    def _validate(self) -> None:
        for step in self._steps.values():
            for dep in step.depends_on:
                if dep == step.name:
                    raise ValueError(f"step {step.name!r} depends on itself")
                if dep not in self._steps:
                    raise ValueError(
                        f"step {step.name!r} depends on unknown step {dep!r}")
        if (cycle := self._find_cycle()) is not None:
            raise ValueError("dependency cycle: " + " -> ".join(cycle))

    def _find_cycle(self) -> list[str] | None:
        """Kahn: whatever is not emitted lies on or after a cycle.

        Reporting the involved steps is what makes the error actionable.
        """
        in_degree = {n: len(s.depends_on) for n, s in self._steps.items()}
        dependents: dict[str, list[str]] = defaultdict(list)
        for name, step in self._steps.items():
            for dep in step.depends_on:
                dependents[dep].append(name)

        ready = deque(sorted(n for n, d in in_degree.items() if d == 0))
        emitted = 0
        while ready:
            node = ready.popleft()
            emitted += 1
            for nxt in dependents[node]:
                in_degree[nxt] -= 1
                if in_degree[nxt] == 0:
                    ready.append(nxt)
        if emitted == len(self._steps):
            return None
        return sorted(n for n, d in in_degree.items() if d > 0)

    def levels(self) -> list[list[str]]:
        """Steps grouped by execution stage. Everything in a level is
        independent and may run concurrently. O(V + E)."""
        in_degree = {n: len(s.depends_on) for n, s in self._steps.items()}
        current = sorted(n for n, d in in_degree.items() if d == 0)
        out: list[list[str]] = []
        while current:
            out.append(current)
            nxt: list[str] = []
            for node in current:
                for dependent in self._dependents[node]:
                    in_degree[dependent] -= 1
                    if in_degree[dependent] == 0:
                        nxt.append(dependent)
            current = sorted(nxt)
        return out

    def critical_path(self) -> tuple[list[str], float]:
        """Longest-duration dependency chain.

        Longest path is NP-hard in general graphs and linear in a DAG:
        process in topological order and each node's earliest finish is its
        duration plus the maximum finish among its predecessors.

        This is the only chain worth optimising -- shortening anything off
        it changes nothing about total runtime.
        O(V + E).
        """
        finish: dict[str, float] = {}
        predecessor: dict[str, str | None] = {}
        for level in self.levels():
            for name in level:
                step = self._steps[name]
                best_dep, best_time = None, 0.0
                for dep in step.depends_on:
                    if finish[dep] > best_time:
                        best_dep, best_time = dep, finish[dep]
                finish[name] = best_time + step.duration_s
                predecessor[name] = best_dep

        if not finish:
            return [], 0.0
        end = max(finish, key=lambda n: finish[n])
        path = [end]
        while (prev := predecessor[path[-1]]) is not None:
            path.append(prev)
        path.reverse()
        return path, finish[end]

    def run(self, execute: Callable[[Step], bool]) -> ExecutionReport:
        """Run every step whose dependencies succeeded.

        `execute` returns True on success. When a step fails, every step
        downstream of it is marked SKIPPED rather than left PENDING --
        leaving them pending is what makes an executor hang, and marking
        them FAILED would misreport what happened.
        """
        states = {name: StepState.PENDING for name in self._steps}
        remaining = {n: len(s.depends_on) for n, s in self._steps.items()}
        ready = deque(sorted(n for n, d in remaining.items() if d == 0))

        while ready:
            name = ready.popleft()
            if states[name] is StepState.SKIPPED:
                continue
            states[name] = StepState.RUNNING
            ok = execute(self._steps[name])
            states[name] = StepState.COMPLETED if ok else StepState.FAILED

            if ok:
                for dependent in self._dependents[name]:
                    remaining[dependent] -= 1
                    if remaining[dependent] == 0:
                        ready.append(dependent)
            else:
                # Propagate the failure: BFS over everything downstream.
                queue = deque(self._dependents[name])
                while queue:
                    node = queue.popleft()
                    if states[node] is StepState.SKIPPED:
                        continue
                    states[node] = StepState.SKIPPED
                    queue.extend(self._dependents[node])

        levels = self.levels()
        path, path_seconds = self.critical_path()
        return ExecutionReport(
            states=states,
            levels=levels,
            critical_path=path,
            critical_path_seconds=path_seconds,
            sequential_seconds=sum(s.duration_s for s in self._steps.values()),
        )
