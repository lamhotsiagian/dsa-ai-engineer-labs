"""Unit tests for Chapter 13."""
from __future__ import annotations
from dsa_labs.chapter_13.dedup_clusters import ArrayUnionFind, cluster_pairs
from dsa_labs.chapter_13.leetcode_solutions import valid_path, find_redundant_connection, num_islands_2

def test_cluster_union_find():
    uf = ArrayUnionFind(5)
    uf.union(0, 1)
    uf.union(1, 2)
    assert uf.find(0) == uf.find(2)
    assert uf.find(0) != uf.find(3)

def test_valid_path():
    edges = [[0,1],[1,2],[2,0]]
    assert valid_path(3, edges, 0, 2) is True
    assert valid_path(6, [[0,1],[0,2],[3,5],[5,4],[4,3]], 0, 5) is False

def test_find_redundant_connection():
    assert find_redundant_connection([[1,2],[1,3],[2,3]]) == [2,3]
    assert find_redundant_connection([[1,2],[2,3],[3,4],[1,4],[1,5]]) == [1,4]

def test_num_islands_2():
    assert num_islands_2(3, 3, [[0,0],[0,1],[1,2],[2,1]]) == [1, 1, 2, 3]
