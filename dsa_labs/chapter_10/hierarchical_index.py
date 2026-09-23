"""Module hierarchical_index.py for chapter_10."""
from __future__ import annotations

import heapq
from dataclasses import dataclass, field

import numpy as np


@dataclass
class IndexNode:
    """One node of a hierarchical centroid tree.

    Internal nodes hold a centroid and children; leaves hold the ids and
    vectors of the documents assigned to them.
    """
    centroid: np.ndarray
    children: list["IndexNode"] = field(default_factory=list)
    leaf_ids: np.ndarray | None = None        # (m,) int64, leaves only
    leaf_vectors: np.ndarray | None = None    # (m, d) float32, leaves only

    @property
    def is_leaf(self) -> bool:
        return not self.children


class HierarchicalIndex:
    """Tree-structured approximate nearest-neighbour index.

    Build: recursively k-means the vectors into `branching` clusters until a
    node holds at most `leaf_size` vectors.
    Query: descend, keeping the `beam` most promising nodes at each level,
    then exhaustively score the vectors in the reached leaves.

    Build  O(n * d * branching * iters * depth)
    Query  O(beam * branching * d * depth + beam * leaf_size * d)

    The beam is the accuracy dial. beam=1 is a pure greedy descent and is
    fast and lossy: the nearest neighbour can sit in a sibling cluster whose
    centroid is further away. Widening the beam recovers recall linearly in
    cost, and the right value is MEASURED against exact search, never assumed.
    """

    def __init__(self, branching: int = 8, leaf_size: int = 64,
                 kmeans_iters: int = 10, seed: int = 0) -> None:
        if branching < 2:
            raise ValueError("branching must be at least 2")
        if leaf_size < 1:
            raise ValueError("leaf_size must be positive")
        self.branching = branching
        self.leaf_size = leaf_size
        self.kmeans_iters = kmeans_iters
        self._rng = np.random.default_rng(seed)
        self.root: IndexNode | None = None
        self._dim: int | None = None

    def build(self, vectors: np.ndarray, ids: np.ndarray | None = None) -> None:
        if vectors.ndim != 2 or vectors.shape[0] == 0:
            raise ValueError("vectors must be a non-empty (n, d) array")
        vectors = np.ascontiguousarray(vectors, dtype=np.float32)
        ids = np.arange(len(vectors), dtype=np.int64) if ids is None else ids
        self._dim = vectors.shape[1]
        self.root = self._build_node(vectors, ids, depth=0)

    def _build_node(self, vectors: np.ndarray, ids: np.ndarray,
                    depth: int) -> IndexNode:
        centroid = vectors.mean(axis=0)
        if len(vectors) <= self.leaf_size or depth > 32:
            return IndexNode(centroid=centroid, leaf_ids=ids, leaf_vectors=vectors)

        labels, centroids = self._kmeans(vectors, min(self.branching, len(vectors)))
        node = IndexNode(centroid=centroid)
        for c in range(len(centroids)):
            mask = labels == c
            if not mask.any():
                continue                       # empty cluster: skip, do not recurse
            node.children.append(
                self._build_node(vectors[mask], ids[mask], depth + 1))
        # Degenerate split (everything landed in one cluster): make it a leaf
        # rather than recursing forever on the same data.
        if len(node.children) <= 1:
            return IndexNode(centroid=centroid, leaf_ids=ids, leaf_vectors=vectors)
        return node

    def _kmeans(self, vectors: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray]:
        idx = self._rng.choice(len(vectors), size=k, replace=False)
        centroids = vectors[idx].copy()
        labels = np.zeros(len(vectors), dtype=np.int64)
        for _ in range(self.kmeans_iters):
            # ||a-b||^2 expansion: one matmul, no (n, k, d) intermediate.
            d2 = ((vectors ** 2).sum(1)[:, None]
                  - 2 * vectors @ centroids.T
                  + (centroids ** 2).sum(1)[None, :])
            new_labels = d2.argmin(axis=1)
            if np.array_equal(new_labels, labels):
                break                          # converged
            labels = new_labels
            for c in range(k):
                mask = labels == c
                if mask.any():
                    centroids[c] = vectors[mask].mean(axis=0)
        return labels, centroids

    def query(self, vector: np.ndarray, k: int = 10, beam: int = 4
              ) -> tuple[np.ndarray, np.ndarray]:
        """Return (ids, distances) of approximately the k nearest vectors."""
        if self.root is None:
            raise RuntimeError("index has not been built")
        if vector.shape != (self._dim,):
            raise ValueError(f"expected a ({self._dim},) query vector")
        q = np.ascontiguousarray(vector, dtype=np.float32)

        frontier = [self.root]
        leaves: list[IndexNode] = []
        while frontier:
            candidates: list[IndexNode] = []
            for node in frontier:
                if node.is_leaf:
                    leaves.append(node)
                else:
                    candidates.extend(node.children)
            if not candidates:
                break
            scored = [(float(np.dot(c.centroid - q, c.centroid - q)), i, c)
                      for i, c in enumerate(candidates)]
            frontier = [c for _, _, c in heapq.nsmallest(beam, scored)]

        if not leaves:
            leaves = [self.root]
        ids = np.concatenate([lf.leaf_ids for lf in leaves])
        vecs = np.concatenate([lf.leaf_vectors for lf in leaves])
        d2 = ((vecs - q) ** 2).sum(axis=1)
        take = min(k, len(ids))
        best = np.argpartition(d2, take - 1)[:take]
        best = best[np.argsort(d2[best])]
        return ids[best], d2[best]
