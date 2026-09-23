"""Unit tests for Chapter 28."""
from __future__ import annotations
import numpy as np
from dsa_labs.chapter_28.ann_index import NavigableSmallWorldIndex
from dsa_labs.chapter_28.decoding import filter_logits

def test_filter_logits():
    logits = np.array([1.0, 2.0, 3.0, 4.0])
    probs = filter_logits(logits, temperature=1.0, top_k=2)
    assert np.isclose(probs.sum(), 1.0)
    assert probs[0] == 0.0
    assert probs[1] == 0.0
    assert probs[3] > probs[2]

def test_nsw_index():
    idx = NavigableSmallWorldIndex(dimension=4, max_degree=4, ef_construction=10)
    v1 = np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float32)
    v2 = np.array([0.0, 1.0, 0.0, 0.0], dtype=np.float32)
    idx.add(v1)
    idx.add(v2)
    res = idx.search(v1, k=1, ef_search=5)
    assert len(res) == 1
    assert res[0][1] == 0
