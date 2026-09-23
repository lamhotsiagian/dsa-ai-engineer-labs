"""LeetCode Solutions for chapter_13."""
from __future__ import annotations

# ----------------------------------------------------------------------------
# Problem: Find if Path Exists in Graph (LeetCode 1971) [\LTwo]
# ----------------------------------------------------------------------------
def valid_path(n: int, edges: list[list[int]], source: int, destination: int) -> bool:
    parent = list(range(n))
    rank = [0] * n

    def find(i: int) -> int:
        if parent[i] != i:
            parent[i] = find(parent[i])  # path compression
        return parent[i]

    def union(i: int, j: int) -> None:
        root_i, root_j = find(i), find(j)
        if root_i != root_j:
            if rank[root_i] < rank[root_j]:
                root_i, root_j = root_j, root_i
            parent[root_j] = root_i
            if rank[root_i] == rank[root_j]:
                rank[root_i] += 1

    for u, v in edges:
        union(u, v)

    return find(source) == find(destination)

# ----------------------------------------------------------------------------
# Problem: Redundant Connection (LeetCode 684) [\LThree]
# ----------------------------------------------------------------------------
def find_redundant_connection(edges: list[list[int]]) -> list[int]:
    n = len(edges)
    parent = list(range(n + 1))

    def find(i: int) -> int:
        if parent[i] != i:
            parent[i] = find(parent[i])
        return parent[i]

    for u, v in edges:
        root_u = find(u)
        root_v = find(v)
        if root_u == root_v:
            return [u, v]
        parent[root_u] = root_v

    return []

# ----------------------------------------------------------------------------
# Problem: Number of Islands II (LeetCode 305) [\LFour]
# ----------------------------------------------------------------------------
def num_islands_2(m: int, n: int, positions: list[list[int]]) -> list[int]:
    parent: dict[int, int] = {}
    rank: dict[int, int] = {}
    count = 0
    result = []

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x: int, y: int) -> bool:
        rx, ry = find(x), find(y)
        if rx == ry:
            return False
        if rank[rx] < rank[ry]:
            rx, ry = ry, rx
        parent[ry] = rx
        if rank[rx] == rank[ry]:
            rank[rx] += 1
        return True

    for r, c in positions:
        idx = r * n + c
        if idx in parent:
            result.append(count)
            continue

        parent[idx] = idx
        rank[idx] = 0
        count += 1

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            n_idx = nr * n + nc
            if 0 <= nr < m and 0 <= nc < n and n_idx in parent:
                if union(idx, n_idx):
                    count -= 1

        result.append(count)

    return result

