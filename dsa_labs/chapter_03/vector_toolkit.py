"""Module vector_toolkit.py for chapter_03."""
from __future__ import annotations

import numpy as np

_EPS = 1e-12


def l2_normalize(matrix: np.ndarray) -> np.ndarray:
    """Row-normalise to unit length, tolerating all-zero rows.

    Zero rows would divide by zero and produce NaN, which then poisons every
    downstream similarity. Clipping the norm leaves a zero row as a zero row,
    whose similarity to everything is 0 -- a defensible, non-crashing answer.
    """
    if matrix.ndim != 2:
        raise ValueError(f"expected a 2-D (n, d) array, got shape {matrix.shape}")
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    return matrix / np.clip(norms, _EPS, None)


def top_k_cosine(
    queries: np.ndarray,
    corpus: np.ndarray,
    k: int,
    *,
    corpus_is_normalized: bool = False,
) -> tuple[np.ndarray, np.ndarray]:
    """Return (indices, scores) of the ``k`` most cosine-similar corpus rows.

    Shapes: queries (q, d), corpus (n, d) -> indices (q, k), scores (q, k),
    both sorted by descending score within each row.

    Time   O(q*n*d) for the matmul + O(q*n) for the partition + O(q*k log k).
    Space  O(q*n) for the score matrix.

    The partition is the point: a full sort of n scores is O(n log n) per
    query, while argpartition is O(n) and we only pay log k on the k we keep.
    At n = 10^6 and k = 10 that is a ~20x reduction in the selection step.
    """
    if queries.ndim != 2 or corpus.ndim != 2:
        raise ValueError("queries and corpus must both be 2-D")
    if queries.shape[1] != corpus.shape[1]:
        raise ValueError(
            f"dimension mismatch: queries d={queries.shape[1]}, "
            f"corpus d={corpus.shape[1]}")
    n = corpus.shape[0]
    if n == 0:
        raise ValueError("corpus is empty")
    k = min(k, n)                       # asking for more than exists is not an error
    if k <= 0:
        raise ValueError(f"k must be positive, got {k}")

    q = l2_normalize(queries.astype(np.float32, copy=False))
    c = corpus.astype(np.float32, copy=False)
    if not corpus_is_normalized:
        c = l2_normalize(c)

    scores = q @ c.T                                   # (q, n), each in [-1, 1]

    # argpartition puts the k largest in the first k slots, unordered, in O(n).
    part = np.argpartition(-scores, kth=k - 1, axis=1)[:, :k]
    part_scores = np.take_along_axis(scores, part, axis=1)

    # Order just those k.
    order = np.argsort(-part_scores, axis=1)
    return np.take_along_axis(part, order, axis=1), \
           np.take_along_axis(part_scores, order, axis=1)
