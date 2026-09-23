"""Module near_duplicates.py for chapter_24."""
from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass


def choose_bands(permutations: int, threshold: float) -> tuple[int, int]:
    """Pick (bands, rows) so the LSH S-curve is steepest near `threshold`.

    The candidate probability for similarity s is 1 - (1 - s^r)^b, whose
    inflection sits near (1/b)^(1/r). Choosing b and r IS choosing the
    threshold -- a post-filter can raise precision but can never recover
    recall that the banding failed to generate.

    Time O(permutations) over the divisor search.
    """
    if not 0.0 < threshold < 1.0:
        raise ValueError("threshold must be in (0, 1)")
    best = (permutations, 1)
    best_gap = float("inf")
    for rows in range(1, permutations + 1):
        if permutations % rows:
            continue
        bands = permutations // rows
        approx = (1.0 / bands) ** (1.0 / rows)
        gap = abs(approx - threshold)
        if gap < best_gap:
            best_gap, best = gap, (bands, rows)
    return best


def candidate_probability(similarity: float, bands: int, rows: int) -> float:
    """Probability that a pair at this similarity becomes an LSH candidate."""
    return 1.0 - (1.0 - similarity ** rows) ** bands


@dataclass
class DedupReport:
    documents: int
    candidate_pairs: int
    verified_pairs: int
    clusters: int
    duplicates_removed: int
    largest_cluster: int

    @property
    def precision(self) -> float:
        """Fraction of LSH candidates that survived exact verification."""
        return self.verified_pairs / self.candidate_pairs if self.candidate_pairs else 1.0


class NearDuplicateIndex:
    """MinHash + LSH + union-find near-duplicate clustering.

    Build     O(n * |shingles| * P)   -- dominated by signature construction
    Banding   O(n * bands)
    Verify    O(candidates * P)
    Cluster   O(candidates * alpha(n))

    The verification step is not optional: a band collision means the
    signatures agreed on r positions, which is evidence of similarity, not
    proof of it. Skipping it is how a deduplication pass merges unrelated
    documents and reports a spectacular removal rate.
    """

    def __init__(self, *, permutations: int = 128, threshold: float = 0.8,
                 shingle_size: int = 5, max_cluster_size: int | None = 10_000):
        from dsa_labs.chapter_24.minhash import MinHasher

        self.threshold = threshold
        self.shingle_size = shingle_size
        self.max_cluster_size = max_cluster_size
        self.hasher = MinHasher(permutations=permutations)
        self.bands, self.rows = choose_bands(permutations, threshold)

    def build(self, documents: list[str]) -> tuple[list[int], DedupReport]:
        """Return (cluster label per document, report)."""
        from dsa_labs.chapter_13.union_find import UnionFind
        from dsa_labs.chapter_24.minhash import shingles

        n = len(documents)
        if n == 0:
            return [], DedupReport(0, 0, 0, 0, 0, 0)

        signatures = [self.hasher.signature(shingles(doc, self.shingle_size))
                      for doc in documents]

        # Banding: two documents are candidates if any band matches exactly.
        buckets: defaultdict[tuple, list[int]] = defaultdict(list)
        for doc_id, signature in enumerate(signatures):
            for band in range(self.bands):
                start = band * self.rows
                key = (band, signature[start:start + self.rows])
                buckets[key].append(doc_id)

        candidates: set[tuple[int, int]] = set()
        for members in buckets.values():
            if len(members) < 2:
                continue
            # A huge bucket means the band key is degenerate -- usually
            # boilerplate shared by every document. Emitting its full
            # quadratic pair set would dominate the whole run.
            if len(members) > 1_000:
                continue
            for i in range(len(members)):
                for j in range(i + 1, len(members)):
                    candidates.add((members[i], members[j]))

        uf = UnionFind(n)
        sizes = [1] * n
        verified = 0
        for a, b in candidates:
            estimate = self.hasher.estimate_jaccard(signatures[a], signatures[b])
            if estimate < self.threshold:
                continue                       # candidate, not a duplicate
            verified += 1
            ra, rb = uf.find(a), uf.find(b)
            if ra == rb:
                continue
            if (self.max_cluster_size is not None
                    and sizes[ra] + sizes[rb] > self.max_cluster_size):
                continue                       # refuse runaway transitive merge
            merged = sizes[ra] + sizes[rb]
            uf.union(a, b)
            sizes[uf.find(a)] = merged

        labels = [uf.find(i) for i in range(n)]
        distinct = len(set(labels))
        counts: defaultdict[int, int] = defaultdict(int)
        for label in labels:
            counts[label] += 1

        return labels, DedupReport(
            documents=n,
            candidate_pairs=len(candidates),
            verified_pairs=verified,
            clusters=distinct,
            duplicates_removed=n - distinct,
            largest_cluster=max(counts.values()),
        )
