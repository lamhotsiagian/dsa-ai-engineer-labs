"""Module quantization.py for chapter_21."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class QuantizedTensor:
    """Grouped symmetric quantisation with packed 4-bit codes."""
    packed: np.ndarray        # uint8, two codes per byte
    scales: np.ndarray        # float32, one per group
    shape: tuple[int, ...]
    bits: int
    group_size: int

    @property
    def bytes_used(self) -> int:
        return self.packed.nbytes + self.scales.nbytes

    def compression_ratio(self, original_dtype: str = "float16") -> float:
        original = int(np.prod(self.shape)) * np.dtype(original_dtype).itemsize
        return original / self.bytes_used


def quantize(weights: np.ndarray, *, bits: int = 4,
             group_size: int = 128) -> QuantizedTensor:
    """Symmetric per-group quantisation with bit packing.

    A SINGLE scale for a whole tensor loses too much accuracy, because one
    outlier weight compresses the range for every other weight. Per-group
    scales bound that damage to `group_size` weights, at the cost of one
    float16 per group -- which is where the extra 0.06 bytes per parameter
    in the memory table comes from.

    Time  O(n), Space O(n * bits / 8 + n / group_size).
    """
    if bits not in (4, 8):
        raise ValueError("only 4- and 8-bit packing is implemented")
    if group_size <= 0 or group_size % 2:
        raise ValueError("group_size must be positive and even")

    flat = weights.reshape(-1).astype(np.float32)
    padded_len = int(np.ceil(flat.size / group_size) * group_size)
    if padded_len != flat.size:
        flat = np.pad(flat, (0, padded_len - flat.size))

    groups = flat.reshape(-1, group_size)
    levels = (1 << bits) - 1
    zero_point = levels // 2

    max_abs = np.abs(groups).max(axis=1)
    # A group of all zeros would divide by zero; scale 1.0 maps it to the
    # zero point, which round-trips exactly.
    scales = np.where(max_abs == 0, 1.0, max_abs / zero_point).astype(np.float32)

    codes = np.clip(np.round(groups / scales[:, None]) + zero_point,
                    0, levels).astype(np.uint8)

    if bits == 8:
        packed = codes.reshape(-1)
    else:
        flat_codes = codes.reshape(-1)
        packed = (flat_codes[0::2] | (flat_codes[1::2] << 4)).astype(np.uint8)

    return QuantizedTensor(packed, scales, weights.shape, bits, group_size)


def dequantize(q: QuantizedTensor) -> np.ndarray:
    """Reconstruct an approximation of the original weights. Time O(n)."""
    levels = (1 << q.bits) - 1
    zero_point = levels // 2

    if q.bits == 8:
        codes = q.packed.astype(np.int16)
    else:
        low = (q.packed & 0x0F).astype(np.int16)
        high = ((q.packed >> 4) & 0x0F).astype(np.int16)
        codes = np.empty(q.packed.size * 2, dtype=np.int16)
        codes[0::2] = low
        codes[1::2] = high

    groups = codes.reshape(-1, q.group_size).astype(np.float32)
    values = (groups - zero_point) * q.scales[:, None]
    return values.reshape(-1)[: int(np.prod(q.shape))].reshape(q.shape)


def quantization_error(weights: np.ndarray, **kwargs) -> dict[str, float]:
    """Measure what quantisation cost, rather than assuming it is fine.

    Reports relative Frobenius error and cosine similarity: the first is
    the magnitude of the distortion, the second is how much of the
    DIRECTION survived, which is what matters for a matmul.
    """
    q = quantize(weights, **kwargs)
    restored = dequantize(q)
    diff = np.linalg.norm(weights - restored)
    base = np.linalg.norm(weights)
    a, b = weights.reshape(-1), restored.reshape(-1)
    cosine = float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12))
    return {
        "relative_error": float(diff / base) if base else 0.0,
        "cosine_similarity": cosine,
        "compression_ratio": q.compression_ratio(),
        "bytes_used": float(q.bytes_used),
    }


def hamming_topk(query: np.ndarray, corpus: np.ndarray, k: int
                 ) -> tuple[np.ndarray, np.ndarray]:
    """Top-k by Hamming distance over packed binary embeddings.

    query, corpus are uint8 arrays of packed bits. XOR then popcount is
    roughly two orders of magnitude cheaper than a float dot product, which
    is why binary embeddings are used as a FIRST-STAGE filter before exact
    re-ranking on the survivors.

    Time O(n * d / 8), Space O(n).
    """
    if query.ndim != 1 or corpus.ndim != 2:
        raise ValueError("query must be 1-D and corpus 2-D")
    if query.shape[0] != corpus.shape[1]:
        raise ValueError("packed widths must match")
    xor = np.bitwise_xor(corpus, query[None, :])
    # np.unpackbits then sum is portable; a native popcount is faster where
    # available, and the two agree exactly.
    distances = np.unpackbits(xor, axis=1).sum(axis=1)
    take = min(k, distances.shape[0])
    best = np.argpartition(distances, take - 1)[:take]
    best = best[np.argsort(distances[best])]
    return best, distances[best]
