"""Module workflow_graph.py for chapter_22."""
from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field


@dataclass
class WorkflowGraph:
    """Directed graph of agent steps and their dependencies.

    Stored as an adjacency list because real workflows are sparse: a
    hundred steps with a few hundred edges, not ten thousand.
    """
    adjacency: dict[str, list[str]] = field(default_factory=lambda: defaultdict(list))
    nodes: set[str] = field(default_factory=set)

    def add_edge(self, source: str, target: str) -> None:
        """Add a dependency: `source` must complete before `target`. O(1)."""
        if source == target:
            raise ValueError(f"self-loop on {source!r}: a step cannot precede itself")
        self.adjacency[source].append(target)
        self.nodes.add(source)
        self.nodes.add(target)
        self.adjacency.setdefault(target, [])   # sinks must still be nodes

    def reachable_from(self, start: str) -> set[str]:
        """Every step that can run after `start`. BFS, O(V + E)."""
        if start not in self.nodes:
            raise KeyError(f"unknown step {start!r}")
        seen = {start}
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for nxt in self.adjacency.get(node, ()):
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
        return seen

    def distances_from(self, start: str) -> dict[str, int]:
        """Minimum number of steps from `start` to each reachable node.

        In a workflow this is the earliest stage at which a step can run,
        which is the critical-path depth when every step costs the same.
        O(V + E).
        """
        if start not in self.nodes:
            raise KeyError(f"unknown step {start!r}")
        distance = {start: 0}
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for nxt in self.adjacency.get(node, ()):
                if nxt not in distance:
                    distance[nxt] = distance[node] + 1
                    queue.append(nxt)
        return distance

    def find_cycle(self) -> list[str] | None:
        """Return one cycle as a node list, or None.

        Three-colour DFS. Returning the ACTUAL cycle rather than a boolean
        is what makes this useful operationally: 'your workflow has a cycle'
        is not actionable, 'fetch -> parse -> fetch' is.

        Time O(V + E), Space O(V). Iterative: workflow graphs can be deep
        and a recursive version would be a crash on deep input.
        """
        WHITE, GREY, BLACK = 0, 1, 2
        colour = dict.fromkeys(self.nodes, WHITE)
        parent: dict[str, str | None] = {}

        for root in sorted(self.nodes):          # sorted: deterministic output
            if colour[root] != WHITE:
                continue
            colour[root] = GREY
            parent[root] = None
            stack = [(root, iter(self.adjacency.get(root, ())))]
            while stack:
                node, neighbours = stack[-1]
                advanced = False
                for nxt in neighbours:
                    state = colour.get(nxt, WHITE)
                    if state == GREY:
                        # Walk parents back to nxt to materialise the cycle.
                        cycle = [node]
                        while cycle[-1] != nxt:
                            cycle.append(parent[cycle[-1]])
                        cycle.reverse()
                        cycle.append(nxt)
                        return cycle
                    if state == WHITE:
                        colour[nxt] = GREY
                        parent[nxt] = node
                        stack.append((nxt, iter(self.adjacency.get(nxt, ()))))
                        advanced = True
                        break
                if not advanced:
                    colour[node] = BLACK
                    stack.pop()
        return None

    def dead_ends(self, entry_points: list[str]) -> set[str]:
        """Steps that no entry point can reach.

        These are either dead configuration or a missing edge, and both are
        worth surfacing: an unreachable step in a workflow is usually a bug
        that would otherwise be discovered by it silently never running.
        O(V + E).
        """
        reachable: set[str] = set()
        for entry in entry_points:
            reachable |= self.reachable_from(entry)
        return self.nodes - reachable

    def levels(self, entry_points: list[str]) -> list[list[str]]:
        """Group steps by the earliest stage at which they can run.

        Everything within a level is independent and can execute in
        parallel, so this is the parallelisation plan. Multi-source BFS
        from all entry points at once: one pass, not one per entry.
        O(V + E).
        """
        for entry in entry_points:
            if entry not in self.nodes:
                raise KeyError(f"unknown entry point {entry!r}")
        distance = {entry: 0 for entry in entry_points}
        queue = deque(entry_points)
        while queue:
            node = queue.popleft()
            for nxt in self.adjacency.get(node, ()):
                if nxt not in distance:
                    distance[nxt] = distance[node] + 1
                    queue.append(nxt)

        grouped: dict[int, list[str]] = defaultdict(list)
        for node, d in distance.items():
            grouped[d].append(node)
        return [sorted(grouped[d]) for d in sorted(grouped)]
