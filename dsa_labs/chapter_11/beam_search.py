"""Module beam_search.py for chapter_11."""
from __future__ import annotations

import heapq
from dataclasses import dataclass, field
from typing import Callable, Sequence

import numpy as np


@dataclass(frozen=True, order=True)
class Beam:
    """One partial hypothesis.

    `score` is the sum of log-probabilities, so it is always <= 0 and
    comparing beams compares scores first. Tokens are a tuple so the beam is
    hashable and immutable -- a mutable beam shared between steps is a
    classic source of aliasing bugs.
    """
    score: float
    tokens: tuple[int, ...] = field(compare=False)
    finished: bool = field(compare=False, default=False)


def length_normalized(score: float, length: int, alpha: float = 0.6) -> float:
    """Google NMT length penalty: score / ((5 + len) / 6) ** alpha.

    Raw log-probability sums are monotonically decreasing in length, so an
    un-normalised beam search systematically prefers SHORT outputs -- it will
    happily emit an early end-of-sequence token. alpha=0 disables the
    penalty; alpha=1 fully divides by length.
    """
    if length <= 0:
        return score
    penalty = ((5.0 + length) / 6.0) ** alpha
    return score / penalty


def beam_search(
    step_fn: Callable[[Sequence[int]], np.ndarray],
    start_token: int,
    eos_token: int,
    beam_width: int = 4,
    max_length: int = 64,
    length_alpha: float = 0.6,
) -> list[Beam]:
    """Beam search over a next-token log-probability function.

    step_fn(tokens) -> (V,) array of log-probabilities for the next token.

    Per step: beam_width * V candidate scores, from which the top
    beam_width are selected. Selection uses argpartition (O(BV)) rather
    than a sort (O(BV log BV)); at V = 128k that is the difference between
    a few hundred microseconds and several milliseconds PER TOKEN.

    Time  O(max_length * beam_width * V)  dominated by scoring, not selection.
    Space O(beam_width * max_length).
    """
    if beam_width < 1:
        raise ValueError("beam_width must be at least 1")

    live = [Beam(score=0.0, tokens=(start_token,))]
    finished: list[Beam] = []          # min-heap on normalised score

    for _ in range(max_length):
        if not live:
            break

        # Score every (beam, next_token) pair.
        all_scores: list[np.ndarray] = []
        for beam in live:
            logprobs = step_fn(beam.tokens)
            all_scores.append(beam.score + logprobs)
        flat = np.concatenate(all_scores)               # (len(live) * V,)
        vocab = all_scores[0].shape[0]

        take = min(beam_width, flat.size)
        top = np.argpartition(-flat, take - 1)[:take]   # O(BV), unordered
        top = top[np.argsort(-flat[top])]               # O(k log k) to order

        next_live: list[Beam] = []
        for flat_index in top:
            beam_index, token = divmod(int(flat_index), vocab)
            parent = live[beam_index]
            candidate = Beam(score=float(flat[flat_index]),
                             tokens=parent.tokens + (token,))
            if token == eos_token:
                norm = length_normalized(candidate.score,
                                         len(candidate.tokens), length_alpha)
                entry = Beam(score=norm, tokens=candidate.tokens, finished=True)
                # Bounded min-heap: keep only the best `beam_width` finished.
                if len(finished) < beam_width:
                    heapq.heappush(finished, entry)
                elif entry.score > finished[0].score:
                    heapq.heapreplace(finished, entry)
            else:
                next_live.append(candidate)

        live = next_live[:beam_width]

        # Early stop: if the best possible live beam cannot beat the worst
        # finished one, further search is wasted. Valid because log-probs are
        # non-positive, so a beam's score can only decrease as it grows.
        if len(finished) >= beam_width and live:
            best_live = length_normalized(live[0].score,
                                          len(live[0].tokens), length_alpha)
            if best_live <= finished[0].score:
                break

    return sorted(finished, key=lambda b: -b.score)
