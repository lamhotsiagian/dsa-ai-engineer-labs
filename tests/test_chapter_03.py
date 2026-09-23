"""Unit tests for Chapter 03."""
from __future__ import annotations
import numpy as np
from dsa_labs.chapter_03.vector_toolkit import l2_normalize, top_k_cosine

def test_l2_normalize():
    mat = np.array([[3.0, 4.0], [0.0, 0.0]], dtype=np.float32)
    normed = l2_normalize(mat)
    assert np.isclose(np.linalg.norm(normed[0]), 1.0)
    assert np.allclose(normed[1], [0.0, 0.0])

def test_top_k_cosine():
    queries = np.array([[1.0, 0.0]], dtype=np.float32)
    corpus = np.array([[1.0, 0.0], [0.0, 1.0], [-1.0, 0.0]], dtype=np.float32)
    indices, scores = top_k_cosine(queries, corpus, k=2)
    assert indices[0, 0] == 0
    assert np.isclose(scores[0, 0], 1.0)
    assert indices[0, 1] == 1
