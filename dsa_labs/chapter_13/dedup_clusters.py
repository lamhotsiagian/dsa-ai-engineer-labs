"""Module dedup_clusters.py for chapter_13."""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Iterable, Iterator

import numpy as np


class ArrayUnionFind:
    """Union-Find over int32 NumPy arrays, for large element counts.

    At n = 5e8 this is two int32 arrays = 4 GB, against roughly 60 GB for
    Python lists of ints. The algorithm is identical; only the storage
    changes, and the storage is what decides whether it runs at all.
    """

    def __init__(self, n: int) -> None:
        if not 0 <= n < 2 ** 31:
            raise ValueError("n must fit in int32")
        self.parent = np.arange(n, dtype=np.int32)
        self.rank = np.zeros(n, dtype=np.int8)     # height <= log2(n) < 64
        self.components = n

    def find(self, x: int) -> int:
        parent = self.parent
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:                   # compress
            parent[x], x = root, parent[x]
        return int(root)

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        self.components -= 1
        return True


@dataclass(frozen=True)
class ClusterReport:
    total_documents: int
    clusters: int
    duplicates_removed: int
    largest_cluster: int
    singleton_clusters: int

    @property
    def reduction(self) -> float:
        return self.duplicates_removed / self.total_documents if self.total_documents else 0.0


def cluster_pairs(
    n_documents: int,
    candidate_pairs: Iterable[tuple[int, int]],
    *,
    max_cluster_size: int | None = None,
) -> tuple[np.ndarray, ClusterReport]:
    """Turn pairwise near-duplicate candidates into clusters.

    Returns (cluster_id per document, report).

    Time  O(P * alpha(n)) for P pairs, plus O(n) to materialise labels.
    Space O(n).

    `max_cluster_size` is a guard against transitive over-merging: with a
    loose similarity threshold, chains of pairwise-similar documents can
    collapse a huge fraction of the corpus into one cluster. Refusing a
    union that would exceed the cap keeps the damage local and makes the
    problem visible instead of silent.
    """
    uf = ArrayUnionFind(n_documents)
    size = np.ones(n_documents, dtype=np.int64)
    refused = 0

    for a, b in candidate_pairs:
        if not (0 <= a < n_documents and 0 <= b < n_documents):
            raise IndexError(f"pair ({a}, {b}) outside 0..{n_documents - 1}")
        if a == b:
            continue
        ra, rb = uf.find(a), uf.find(b)
        if ra == rb:
            continue
        if max_cluster_size is not None and size[ra] + size[rb] > max_cluster_size:
            refused += 1
            continue
        merged = size[ra] + size[rb]
        uf.union(a, b)
        size[uf.find(a)] = merged

    labels = np.fromiter((uf.find(i) for i in range(n_documents)),
                         dtype=np.int64, count=n_documents)
    counts = Counter(labels.tolist())
    report = ClusterReport(
        total_documents=n_documents,
        clusters=len(counts),
        duplicates_removed=n_documents - len(counts),
        largest_cluster=max(counts.values()) if counts else 0,
        singleton_clusters=sum(1 for c in counts.values() if c == 1),
    )
    return labels, report


def representatives(labels: np.ndarray, quality: np.ndarray) -> np.ndarray:
    """Pick one document per cluster: the highest-quality member.

    Which representative is kept changes the corpus composition, so it is a
    decision, not a detail. Length, source authority and a quality score are
    all defensible; picking the first-seen is not, because it encodes crawl
    order into the dataset.

    Time O(n), Space O(clusters).
    """
    if labels.shape != quality.shape:
        raise ValueError("labels and quality must have the same shape")
    best: dict[int, int] = {}
    for index, (label, score) in enumerate(zip(labels.tolist(), quality.tolist())):
        current = best.get(label)
        if current is None or score > quality[current]:
            best[label] = index
    return np.array(sorted(best.values()), dtype=np.int64)


def cross_split_leakage(
    labels: np.ndarray, split: np.ndarray
) -> Iterator[tuple[int, set]]:
    """Yield (cluster_id, splits) for clusters spanning more than one split.

    A near-duplicate cluster containing both a training and a test document
    means the evaluation is contaminated. This is the single highest-value
    check this structure enables, and it is cheap: one pass.

    Time O(n).
    """
    by_cluster: dict[int, set] = {}
    for label, which in zip(labels.tolist(), split.tolist()):
        by_cluster.setdefault(label, set()).add(which)
    for label, splits in by_cluster.items():
        if len(splits) > 1:
            yield label, splits
