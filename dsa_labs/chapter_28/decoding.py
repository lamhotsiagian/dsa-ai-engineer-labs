"""Module decoding.py for chapter_28."""
from __future__ import annotations

import numpy as np


def filter_logits(logits: np.ndarray, temperature: float = 1.0,
                  top_k: int = 0, top_p: float = 1.0) -> np.ndarray:
    """Temperature, then top-k, then top-p. Returns a probability vector.

    Order matters: temperature scales the LOGITS, so it must be applied
    before any probability is formed. Applying it after the softmax is a
    different -- and wrong -- transformation.

    Time  O(V) for top-k alone, O(V log V) when top-p sorts.
    Space O(V).
    """
    if temperature <= 0:
        raise ValueError("temperature must be positive; use greedy for 0")
    scaled = logits / temperature

    if 0 < top_k < scaled.size:
        # Selection, not sorting: O(V) against O(V log V). At V = 128k and
        # one call per generated token this is worth the extra line.
        kth = np.partition(scaled, -top_k)[-top_k]
        scaled = np.where(scaled < kth, -np.inf, scaled)

    shifted = scaled - scaled.max()
    probabilities = np.exp(shifted)
    probabilities /= probabilities.sum()

    if top_p < 1.0:
        order = np.argsort(-probabilities)          # descending
        cumulative = np.cumsum(probabilities[order])
        # searchsorted finds the first index where cumulative >= top_p in
        # O(log V); the +1 keeps the token that crosses the threshold, so
        # the nucleus is never empty even for a very peaked distribution.
        cut = int(np.searchsorted(cumulative, top_p)) + 1
        keep = order[:cut]
        masked = np.zeros_like(probabilities)
        masked[keep] = probabilities[keep]
        probabilities = masked / masked.sum()

    return probabilities


def speculative_accept(draft_tokens: list[int],
                       draft_probs: np.ndarray,
                       target_probs: np.ndarray,
                       rng: np.random.Generator) -> tuple[list[int], int]:
    """Verify a speculative draft. Returns (emitted_tokens, n_accepted).

    draft_probs[i]  -- draft model's distribution at position i
    target_probs[i] -- target model's distribution at the same position,
                       all gamma+1 of them from ONE target forward pass

    Accept token x with probability min(1, p(x)/q(x)). On rejection, draw
    the replacement from the normalised residual max(0, p - q) -- NOT from
    p. Only the residual draw makes the output distribution exactly p,
    which is the entire correctness claim of speculative decoding.

    Time O(gamma * V) worst case, O(gamma) when nothing is rejected.
    """
    emitted: list[int] = []
    for i, token in enumerate(draft_tokens):
        p = float(target_probs[i][token])
        q = float(draft_probs[i][token])
        # q == 0 should be impossible for a token the draft sampled, but a
        # mismatched tokenizer or a stale cache makes it happen, and
        # dividing by zero here would silently accept everything.
        if q <= 0.0 or rng.random() < min(1.0, p / q):
            emitted.append(token)
            continue

        residual = np.maximum(target_probs[i] - draft_probs[i], 0.0)
        total = residual.sum()
        corrected = residual / total if total > 0 else target_probs[i]
        emitted.append(int(rng.choice(len(corrected), p=corrected)))
        return emitted, i          # stop at the first rejection

    # Every draft token accepted: the free bonus token from the extra
    # target position is what makes gamma accepted tokens worth gamma+1.
    bonus = int(rng.choice(len(target_probs[-1]), p=target_probs[-1]))
    emitted.append(bonus)
    return emitted, len(draft_tokens)
