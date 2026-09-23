"""LeetCode Solutions for chapter_23."""
from __future__ import annotations

# ----------------------------------------------------------------------------
# Problem: Find Center of Star Graph (LeetCode 1791) [\LTwo]
# ----------------------------------------------------------------------------
def find_center(edges: list[list[int]]) -> int:
    if edges[0][0] in (edges[1][0], edges[1][1]):
        return edges[0][0]
    return edges[0][1]

# ----------------------------------------------------------------------------
# Problem: Course Schedule (LeetCode 207) [\LThree]
# ----------------------------------------------------------------------------
from collections import deque, defaultdict

def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    adj = defaultdict(list)
    in_degrees = [0] * num_courses

    for course, prereq in prerequisites:
        adj[prereq].append(course)
        in_degrees[course] += 1

    queue = deque([i for i in range(num_courses) if in_degrees[i] == 0])
    processed = 0

    while queue:
        curr = queue.popleft()
        processed += 1
        for neighbor in adj[curr]:
            in_degrees[neighbor] -= 1
            if in_degrees[neighbor] == 0:
                queue.append(neighbor)

    return processed == num_courses

# ----------------------------------------------------------------------------
# Problem: Network Delay Time (LeetCode 743) [\LFour]
# ----------------------------------------------------------------------------
import heapq
from collections import defaultdict

def network_delay_time(times: list[list[int]], n: int, k: int) -> int:
    adj = defaultdict(list)
    for u, v, w in times:
        adj[u].append((v, w))

    min_heap = [(0, k)]
    distances = {}

    while min_heap:
        time, node = heapq.heappop(min_heap)
        if node in distances:
            continue
        distances[node] = time

        for neighbor, weight in adj[node]:
            if neighbor not in distances:
                heapq.heappush(min_heap, (time + weight, neighbor))

    if len(distances) == n:
        return max(distances.values())
    return -1

