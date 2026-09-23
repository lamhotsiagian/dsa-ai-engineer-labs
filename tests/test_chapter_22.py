"""Unit tests for Chapter 22."""
from __future__ import annotations
from dsa_labs.chapter_22.workflow_graph import WorkflowGraph
from dsa_labs.chapter_22.leetcode_solutions import flood_fill, num_islands, ladder_length

def test_flood_fill():
    img = [[1,1,1],[1,1,0],[1,0,1]]
    res = flood_fill(img, 1, 1, 2)
    assert res == [[2,2,2],[2,2,0],[2,0,1]]

def test_num_islands():
    grid = [
      ["1","1","1","1","0"],
      ["1","1","0","1","0"],
      ["1","1","0","0","0"],
      ["0","0","0","0","0"]
    ]
    assert num_islands(grid) == 1

def test_ladder_length():
    words = ["hot","dot","dog","lot","log","cog"]
    assert ladder_length("hit", "cog", words) == 5
