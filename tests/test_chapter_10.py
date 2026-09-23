"""Unit tests for Chapter 10."""
from __future__ import annotations
import numpy as np
from dsa_labs.chapter_10.hierarchical_index import HierarchicalIndex
from dsa_labs.chapter_10.leetcode_solutions import TreeNode, max_depth, lowest_common_ancestor, max_path_sum

def test_hierarchical_index():
    vectors = np.array([[1.0, 0.0], [0.9, 0.1], [0.0, 1.0]], dtype=np.float32)
    idx = HierarchicalIndex(branching=2, leaf_size=2)
    idx.build(vectors)
    ids, dists = idx.query(np.array([1.0, 0.0], dtype=np.float32), k=1)
    assert len(ids) == 1
    assert ids[0] == 0

def test_tree_depth():
    r = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
    assert max_depth(r) == 3

def test_lca():
    p = TreeNode(5)
    q = TreeNode(1)
    root = TreeNode(3, p, q)
    assert lowest_common_ancestor(root, p, q) == root

def test_max_path_sum():
    r = TreeNode(-10, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
    assert max_path_sum(r) == 42
