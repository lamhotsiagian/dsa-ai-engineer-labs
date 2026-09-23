"""MinHash signatures and the LSH banding scheme.
Canonical reference for Chapter 24.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass


def shingles(text: str, k: int = 5) -> set[int]:
    """Hashed k-grams of words. Hashing keeps memory constant per shingle.

    Word k-grams rather than character k-grams: word-level is far less
    sensitive to formatting noise, and k=5 is a common choice for web text.
    Smaller k inflates apparent similarity (more collisions between
    unrelated documents); larger k makes near-duplicates look distinct.
    """
    if k < 1:
        raise ValueError("k must be positive")
    words = text.split()
    if len(words) < k:
        return {_stable_hash(" ".join(words))} if words else set()
    return {_stable_hash(" ".join(words[i:i + k]))
            for i in range(len(words) - k + 1)}


def _stable_hash(text: str) -> int:
    """64-bit digest, stable across processes -- unlike hash(), which is
    randomised per process and must never be persisted."""
    return int.from_bytes(
        hashlib.blake2b(text.encode("utf-8"), digest_size=8).digest(), "big")


_MERSENNE = (1 << 61) - 1


@dataclass(frozen=True)
class MinHasher:
    """Fixed-width MinHash signatures.

    Uses the Kirsch-Mitzenmacher trick: instead of P independent hash
    functions, derive P hashes from two via h_i(x) = (a_i*x + b_i) mod p.
    That is P multiplications rather than P full digests, which is the
    difference between a tractable and an intractable corpus pass.
    """
    permutations: int = 128
    seed: int = 0

    def _coefficients(self) -> list[tuple[int, int]]:
        rng_state = self.seed or 1
        out = []
        for _ in range(self.permutations):
            rng_state = (rng_state * 6364136223846793005 + 1442695040888963407) % (1 << 64)
            a = (rng_state % (_MERSENNE - 1)) + 1        # a must be non-zero
            rng_state = (rng_state * 6364136223846793005 + 1442695040888963407) % (1 << 64)
            b = rng_state % _MERSENNE
            out.append((a, b))
        return out

    def signature(self, shingle_set: set[int]) -> tuple[int, ...]:
        """Time O(|shingles| * P), Space O(P).

        The signature size is INDEPENDENT of the document length, which is
        the whole point: a 10-word and a 10,000-word document both reduce
        to P integers.
        """
        if not shingle_set:
            return tuple([_MERSENNE] * self.permutations)
        coefficients = self._coefficients()
        mins = [_MERSENNE] * self.permutations
        for shingle in shingle_set:
            for i, (a, b) in enumerate(coefficients):
                value = (a * shingle + b) % _MERSENNE
                if value < mins[i]:
                    mins[i] = value
        return tuple(mins)

    @staticmethod
    def estimate_jaccard(a: tuple[int, ...], b: tuple[int, ...]) -> float:
        """Fraction of agreeing positions. Time O(P).

        Standard error is roughly 1/sqrt(P): with P=128 that is about 0.09,
        so a single estimate is noisy and a threshold near the estimate's
        error should be verified exactly.
        """
        if len(a) != len(b):
            raise ValueError("signatures must have the same length")
        return sum(x == y for x, y in zip(a, b)) / len(a)
