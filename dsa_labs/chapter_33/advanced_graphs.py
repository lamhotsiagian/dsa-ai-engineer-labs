"""Chapter 33: NeetCode 150 - Advanced Graphs"""
from __future__ import annotations
import math
import heapq
import bisect
from collections import defaultdict, deque, Counter, OrderedDict
from typing import Optional, List, Dict, Set, Tuple

# ----------------------------------------------------------------------------
# Problem: Min Cost to Connect All Points (LeetCode: min-cost-to-connect-all-points)
# ----------------------------------------------------------------------------
import heapq

def minCostConnectPoints(points: list[list[int]]) -> int:
    # Prim's Algorithm for Minimum Spanning Tree
    n = len(points)
    adj = {i: [] for i in range(n)}
    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]
            dist = abs(x1 - x2) + abs(y1 - y2)
            adj[i].append((dist, j))
            adj[j].append((dist, i))

    total_cost = 0
    visited = set()
    min_heap = [(0, 0)]  # (cost, node)

    while len(visited) < n:
        cost, node = heapq.heappop(min_heap)
        if node in visited:
            continue
        visited.add(node)
        total_cost += cost
        for edge_cost, neighbor in adj[node]:
            if neighbor not in visited:
                heapq.heappush(min_heap, (edge_cost, neighbor))
    return total_cost

# ----------------------------------------------------------------------------
# Problem: Network Delay Time (LeetCode: network-delay-time)
# ----------------------------------------------------------------------------
import heapq
from collections import defaultdict

def networkDelayTime(times: list[list[int]], n: int, k: int) -> int:
    # Dijkstra's Algorithm for Single-Source Shortest Path
    adj = defaultdict(list)
    for u, v, w in times:
        adj[u].append((v, w))

    min_heap = [(0, k)]  # (distance, node)
    visited = {}

    while min_heap:
        d, node = heapq.heappop(min_heap)
        if node in visited:
            continue
        visited[node] = d
        for neighbor, weight in adj[node]:
            if neighbor not in visited:
                heapq.heappush(min_heap, (d + weight, neighbor))

    return max(visited.values()) if len(visited) == n else -1

# ----------------------------------------------------------------------------
# Problem: Cheapest Flights Within K Stops (LeetCode: cheapest-flights-within-k-stops)
# ----------------------------------------------------------------------------
def findCheapestPrice(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
    # Bellman-Ford Algorithm executed for k + 1 iterations
    prices = [float('inf')] * n
    prices[src] = 0

    for _ in range(k + 1):
        tmp_prices = prices.copy()
        for u, v, p in flights:
            if prices[u] == float('inf'):
                continue
            if prices[u] + p < tmp_prices[v]:
                tmp_prices[v] = prices[u] + p
        prices = tmp_prices

    return int(prices[dst]) if prices[dst] != float('inf') else -1

# ----------------------------------------------------------------------------
# Problem: Reconstruct Itinerary (LeetCode: reconstruct-itinerary)
# ----------------------------------------------------------------------------
from collections import defaultdict

def findItinerary(tickets: list[list[str]]) -> list[str]:
    # Hierholzer's Algorithm for Eulerian Path
    adj = defaultdict(list)
    # Sort destinations in reverse lexical order so we can pop from the back in O(1)
    for src, dst in sorted(tickets, reverse=True):
        adj[src].append(dst)

    res = []
    def dfs(airport: str):
        while adj[airport]:
            next_dest = adj[airport].pop()
            dfs(next_dest)
        res.append(airport)

    dfs("JFK")
    return res[::-1]

# ----------------------------------------------------------------------------
# Problem: Swim in Rising Water (LeetCode: swim-in-rising-water)
# ----------------------------------------------------------------------------
import heapq

def swimInWater(grid: list[list[int]]) -> int:
    # Modified Dijkstra: minimize maximum elevation along path
    n = len(grid)
    visited = set([(0, 0)])
    min_heap = [(grid[0][0], 0, 0)]  # (max_elevation, r, c)

    while min_heap:
        elev, r, c = heapq.heappop(min_heap)
        if r == n - 1 and c == n - 1:
            return elev
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in visited:
                visited.add((nr, nc))
                heapq.heappush(min_heap, (max(elev, grid[nr][nc]), nr, nc))
    return 0

# ----------------------------------------------------------------------------
# Problem: Alien Dictionary (LeetCode: alien-dictionary)
# ----------------------------------------------------------------------------
def alienOrder(words: list[str]) -> str:
    # Build adjacency set for all unique characters
    adj = {c: set() for w in words for c in w}
    # Derive edge constraints from adjacent word prefix differences
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        min_len = min(len(w1), len(w2))
        # Edge case: prefix violation ("apple" before "app" is invalid)
        if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
            return ""
        for j in range(min_len):
            if w1[j] != w2[j]:
                adj[w1[j]].add(w2[j])
                break

    visited = {}  # False = in active path (cycle), True = verified
    res = []

    def dfs(c: str) -> bool:
        if c in visited:
            return visited[c]
        visited[c] = False
        for neighbor in adj[c]:
            if not dfs(neighbor):
                return False
        visited[c] = True
        res.append(c)  # Post-order append
        return True

    for c in adj:
        if not dfs(c):
            return ""
    # Reverse post-order produces topological sort
    return "".join(res[::-1])

