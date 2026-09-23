"""Chapter 33: NeetCode 150 - Graphs"""
from __future__ import annotations
import math
import heapq
import bisect
from collections import defaultdict, deque, Counter, OrderedDict
from typing import Optional, List, Dict, Set, Tuple

class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

# ----------------------------------------------------------------------------
# Problem: Number of Islands (LeetCode: number-of-islands)
# ----------------------------------------------------------------------------
def numIslands(grid: list[list[str]]) -> int:
    if not grid:
        return 0
    m, n = len(grid), len(grid[0])
    islands = 0

    def dfs(r: int, c: int) -> None:
        if not (0 <= r < m and 0 <= c < n) or grid[r][c] != '1':
            return
        # Sink the island to '0' to record visited in-place
        grid[r][c] = '0'
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(m):
        for c in range(n):
            if grid[r][c] == '1':
                islands += 1
                dfs(r, c)
    return islands

# ----------------------------------------------------------------------------
# Problem: Clone Graph (LeetCode: clone-graph)
# ----------------------------------------------------------------------------
def cloneGraph(node: 'Node | None') -> 'Node | None':
    if not node:
        return None
    # Map original node -> cloned node
    cloned = {}

    def dfs(curr: 'Node') -> 'Node':
        if curr in cloned:
            return cloned[curr]
        copy = Node(curr.val)
        cloned[curr] = copy
        for neighbor in curr.neighbors:
            copy.neighbors.append(dfs(neighbor))
        return copy

    return dfs(node)

# ----------------------------------------------------------------------------
# Problem: Max Area of Island (LeetCode: max-area-of-island)
# ----------------------------------------------------------------------------
def maxAreaOfIsland(grid: list[list[int]]) -> int:
    ROWS, COLS = len(grid), len(grid[0])
    max_area = 0

    def dfs(r: int, c: int) -> int:
        if not (0 <= r < ROWS and 0 <= c < COLS) or grid[r][c] != 1:
            return 0
        grid[r][c] = 0  # In-place sink
        # 1 (current cell) + 4-directional area
        return 1 + dfs(r + 1, c) + dfs(r - 1, c) + dfs(r, c + 1) + dfs(r, c - 1)

    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == 1:
                max_area = max(max_area, dfs(r, c))
    return max_area

# ----------------------------------------------------------------------------
# Problem: Pacific Atlantic Water Flow (LeetCode: pacific-atlantic-water-flow)
# ----------------------------------------------------------------------------
def pacificAtlantic(heights: list[list[int]]) -> list[list[int]]:
    ROWS, COLS = len(heights), len(heights[0])
    pac, atl = set(), set()

    def dfs(r: int, c: int, visit: set, prev_h: int) -> None:
        if ((r, c) in visit or not (0 <= r < ROWS and 0 <= c < COLS)
                or heights[r][c] < prev_h):
            return
        visit.add((r, c))
        # Flow water uphill into adjacent interior cells
        dfs(r + 1, c, visit, heights[r][c])
        dfs(r - 1, c, visit, heights[r][c])
        dfs(r, c + 1, visit, heights[r][c])
        dfs(r, c - 1, visit, heights[r][c])

    # Seed searches from coastal boundary edges
    for c in range(COLS):
        dfs(0, c, pac, heights[0][c])
        dfs(ROWS - 1, c, atl, heights[ROWS - 1][c])
    for r in range(ROWS):
        dfs(r, 0, pac, heights[r][0])
        dfs(r, COLS - 1, atl, heights[r][COLS - 1])

    # Intersect cells that can reach both oceans
    return list(pac & atl)

# ----------------------------------------------------------------------------
# Problem: Surrounded Regions (LeetCode: surrounded-regions)
# ----------------------------------------------------------------------------
def solve(board: list[list[str]]) -> None:
    ROWS, COLS = len(board), len(board[0])

    def capture(r: int, c: int) -> None:
        if not (0 <= r < ROWS and 0 <= c < COLS) or board[r][c] != "O":
            return
        board[r][c] = "T"  # Mark boundary-connected uncapturable cell
        capture(r + 1, c)
        capture(r - 1, c)
        capture(r, c + 1)
        capture(r, c - 1)

    # Step 1: Protect border 'O's and their connected components
    for r in range(ROWS):
        for c in range(COLS):
            if (r in {0, ROWS - 1} or c in {0, COLS - 1}) and board[r][c] == "O":
                capture(r, c)

    # Step 2: Convert interior 'O's to 'X', and restore 'T's back to 'O'
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == "O":
                board[r][c] = "X"
            elif board[r][c] == "T":
                board[r][c] = "O"

# ----------------------------------------------------------------------------
# Problem: Rotting Oranges (LeetCode: rotting-oranges)
# ----------------------------------------------------------------------------
from collections import deque

def orangesRotting(grid: list[list[int]]) -> int:
    ROWS, COLS = len(grid), len(grid[0])
    q = deque()
    fresh = 0
    # Collect all initially rotten oranges in multi-source BFS queue
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == 1: fresh += 1
            elif grid[r][c] == 2: q.append((r, c))

    time = 0
    while q and fresh > 0:
        for _ in range(len(q)):
            r, c = q.popleft()
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == 1:
                    grid[nr][nc] = 2  # Infect adjacent fresh orange
                    fresh -= 1
                    q.append((nr, nc))
        time += 1
    return time if fresh == 0 else -1

# ----------------------------------------------------------------------------
# Problem: Walls and Gates (LeetCode: walls-and-gates)
# ----------------------------------------------------------------------------
from collections import deque

def wallsAndGates(rooms: list[list[int]]) -> None:
    ROWS, COLS = len(rooms), len(rooms[0])
    q = deque()
    # Find all gates (val == 0) to initialize multi-source BFS
    for r in range(ROWS):
        for c in range(COLS):
            if rooms[r][c] == 0:
                q.append((r, c))

    dist = 0
    while q:
        dist += 1
        for _ in range(len(q)):
            r, c = q.popleft()
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = r + dr, c + dc
                # 2147483647 represents empty room
                if 0 <= nr < ROWS and 0 <= nc < COLS and rooms[nr][nc] == 2147483647:
                    rooms[nr][nc] = dist
                    q.append((nr, nc))

# ----------------------------------------------------------------------------
# Problem: Course Schedule (LeetCode: course-schedule)
# ----------------------------------------------------------------------------
def canFinish(numCourses: int, prerequisites: list[list[int]]) -> bool:
    adj = {i: [] for i in range(numCourses)}
    for crs, pre in prerequisites:
        adj[crs].append(pre)

    visited = set()  # In current DFS recursion path (cycle detection)

    def dfs(crs: int) -> bool:
        if crs in visited:
            return False  # Detected cycle
        if adj[crs] == []:
            return True   # Already verified course
        visited.add(crs)
        for pre in adj[crs]:
            if not dfs(pre):
                return False
        visited.remove(crs)
        adj[crs] = []  # Memoize verified course
        return True

    for crs in range(numCourses):
        if not dfs(crs):
            return False
    return True

# ----------------------------------------------------------------------------
# Problem: Course Schedule II (LeetCode: course-schedule-ii)
# ----------------------------------------------------------------------------
def findOrder(numCourses: int, prerequisites: list[list[int]]) -> list[int]:
    adj = {i: [] for i in range(numCourses)}
    for crs, pre in prerequisites:
        adj[crs].append(pre)

    res = []
    visited = set() # In active DFS path
    cycle = set()   # Fully processed courses

    def dfs(crs: int) -> bool:
        if crs in visited: return False
        if crs in cycle: return True
        visited.add(crs)
        for pre in adj[crs]:
            if not dfs(pre):
                return False
        visited.remove(crs)
        cycle.add(crs)
        res.append(crs)  # Post-order topological append
        return True

    for crs in range(numCourses):
        if not dfs(crs):
            return []
    return res

# ----------------------------------------------------------------------------
# Problem: Redundant Connection (LeetCode: redundant-connection)
# ----------------------------------------------------------------------------
def findRedundantConnection(edges: list[list[int]]) -> list[int]:
    # Disjoint Set Union (DSU) with Path Compression and Union by Rank
    n = len(edges)
    parent = list(range(n + 1))
    rank = [1] * (n + 1)

    def find(node: int) -> int:
        if parent[node] != node:
            parent[node] = find(parent[node])  # Path compression
        return parent[node]

    def union(n1: int, n2: int) -> bool:
        p1, p2 = find(n1), find(n2)
        if p1 == p2:
            return False  # Already in same set: edge is redundant cycle!
        if rank[p1] > rank[p2]:
            parent[p2] = p1
            rank[p1] += rank[p2]
        else:
            parent[p1] = p2
            rank[p2] += rank[p1]
        return True

    for u, v in edges:
        if not union(u, v):
            return [u, v]
    return []

# ----------------------------------------------------------------------------
# Problem: Number of Connected Components in an Undirected Graph (LeetCode: number-of-connected-components-in-an-undirected-graph)
# ----------------------------------------------------------------------------
def countComponents(n: int, edges: list[list[int]]) -> int:
    parent = list(range(n))
    rank = [1] * n

    def find(node: int) -> int:
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]

    def union(n1: int, n2: int) -> int:
        p1, p2 = find(n1), find(n2)
        if p1 == p2:
            return 0  # No reduction in component count
        if rank[p1] > rank[p2]:
            parent[p2] = p1
            rank[p1] += rank[p2]
        else:
            parent[p1] = p2
            rank[p2] += rank[p1]
        return 1

    components = n
    for u, v in edges:
        components -= union(u, v)
    return components

# ----------------------------------------------------------------------------
# Problem: Graph Valid Tree (LeetCode: graph-valid-tree)
# ----------------------------------------------------------------------------
def validTree(n: int, edges: list[list[int]]) -> bool:
    # A valid tree on n nodes must have exactly n - 1 edges and no cycles
    if len(edges) != n - 1:
        return False
    parent = list(range(n))

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    for u, v in edges:
        p1, p2 = find(u), find(v)
        if p1 == p2:
            return False  # Cycle detected
        parent[p1] = p2
    return True

# ----------------------------------------------------------------------------
# Problem: Word Ladder (LeetCode: word-ladder)
# ----------------------------------------------------------------------------
from collections import defaultdict, deque

def ladderLength(beginWord: str, endWord: str, wordList: list[str]) -> int:
    if endWord not in set(wordList):
        return 0
    # Group words by intermediate wildcard pattern, e.g., "h*t" -> ["hot", "hit"]
    patterns = defaultdict(list)
    for word in wordList:
        for j in range(len(word)):
            pat = word[:j] + "*" + word[j+1:]
            patterns[pat].append(word)

    q = deque([(beginWord, 1)])
    visited = {beginWord}
    while q:
        word, level = q.popleft()
        if word == endWord:
            return level
        # Check all single-character variation buckets
        for j in range(len(word)):
            pat = word[:j] + "*" + word[j+1:]
            for neighbor in patterns[pat]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    q.append((neighbor, level + 1))
    return 0

