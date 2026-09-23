"""Union-Find with both optimisations (union by rank and path compression).
Canonical reference for Chapter 13.
"""
from __future__ import annotations


class UnionFind:
    """Disjoint-set forest with union by rank and path compression.

    find  O(alpha(n)) amortised -- alpha is the inverse Ackermann function,
          which is at most 4 for any n that fits in the observable universe.
          Treat it as constant, but know the name.
    union O(alpha(n)) amortised.

    Both optimisations are needed for that bound: union by rank alone gives
    O(log n); path compression alone gives O(log n) amortised; together they
    give O(alpha(n)).
    """

    def __init__(self, n: int) -> None:
        if n < 0:
            raise ValueError("n must be non-negative")
        self._parent = list(range(n))
        self._rank = [0] * n          # upper bound on tree height
        self._size = [1] * n          # elements in the tree rooted here
        self.components = n

    def find(self, x: int) -> int:
        """Representative of x's group, compressing the path on the way.

        Iterative rather than recursive: on a degenerate input the recursive
        version blows the stack, and this is exactly the structure whose
        inputs can be adversarial.
        """
        root = x
        while self._parent[root] != root:
            root = self._parent[root]
        # Second pass: point everything on the path directly at the root.
        while self._parent[x] != root:
            self._parent[x], x = root, self._parent[x]
        return root

    def union(self, a: int, b: int) -> bool:
        """Merge the groups of a and b. Returns False if already together."""
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                     # already connected: no-op
        # Attach the shorter tree under the taller one.
        if self._rank[ra] < self._rank[rb]:
            ra, rb = rb, ra
        self._parent[rb] = ra
        self._size[ra] += self._size[rb]
        if self._rank[ra] == self._rank[rb]:
            self._rank[ra] += 1              # height grows only on a tie
        self.components -= 1
        return True

    def connected(self, a: int, b: int) -> bool:
        return self.find(a) == self.find(b)

    def size_of(self, x: int) -> int:
        """Number of elements in x's group. O(alpha(n))."""
        return self._size[self.find(x)]

    def groups(self) -> dict[int, list[int]]:
        """Materialise the partition. O(n * alpha(n))."""
        out: dict[int, list[int]] = {}
        for x in range(len(self._parent)):
            out.setdefault(self.find(x), []).append(x)
        return out
