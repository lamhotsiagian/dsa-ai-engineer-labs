"""Module viterbi_tokenizer.py for chapter_20."""
from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Segmentation:
    pieces: tuple[str, ...]
    token_ids: tuple[int, ...]
    log_probability: float

    @property
    def piece_count(self) -> int:
        return len(self.pieces)


class UnigramTokenizer:
    """Optimal subword segmentation by Viterbi over character positions.

    This is the algorithm behind SentencePiece's Unigram model. Greedy
    longest-match (Chapter 12) is fast and NOT optimal: it can commit to a
    long piece that strands an expensive remainder. Viterbi considers every
    segmentation implicitly and returns the maximum-probability one.

    State:      best[i] = log-probability of the best segmentation of the
                first i characters.
    Transition: best[i] = max over pieces p ending at i of
                          best[i - len(p)] + logp[p]
    Base:       best[0] = 0.0
    Answer:     best[n], with pieces recovered from back-pointers.

    Time  O(n * L) where L is the longest vocabulary piece, because for each
          position we only consider pieces that could end there.
    Space O(n) for the table and the back-pointers.
    """

    def __init__(self, vocabulary: dict[str, float],
                 *, unk_log_probability: float = -20.0) -> None:
        """`vocabulary` maps piece -> log-probability (negative)."""
        if not vocabulary:
            raise ValueError("vocabulary must be non-empty")
        if any(lp > 0 for lp in vocabulary.values()):
            raise ValueError("values must be LOG-probabilities (<= 0)")
        self._logp = dict(vocabulary)
        self._ids = {piece: i for i, piece in enumerate(sorted(vocabulary))}
        self._max_piece = max(len(p) for p in vocabulary)
        self._unk_logp = unk_log_probability

    def segment(self, text: str) -> Segmentation:
        """Maximum-log-probability segmentation of `text`."""
        if not text:
            return Segmentation((), (), 0.0)

        n = len(text)
        best = [-math.inf] * (n + 1)
        best[0] = 0.0
        back: list[tuple[int, str] | None] = [None] * (n + 1)

        for end in range(1, n + 1):
            # Only look back as far as the longest vocabulary piece: this is
            # what makes the algorithm O(n*L) rather than O(n^2).
            lowest = max(0, end - self._max_piece)
            for start in range(lowest, end):
                if best[start] == -math.inf:
                    continue                       # unreachable prefix
                piece = text[start:end]
                logp = self._logp.get(piece)
                if logp is None:
                    # Single characters fall back to UNK so that any string
                    # is segmentable. Without this, a string containing one
                    # out-of-vocabulary character would have NO segmentation
                    # and the table would stay at -inf.
                    if end - start != 1:
                        continue
                    logp = self._unk_logp
                score = best[start] + logp
                if score > best[end]:
                    best[end] = score
                    back[end] = (start, piece)

        pieces: list[str] = []
        position = n
        while position > 0:
            step = back[position]
            if step is None:                       # should be unreachable
                raise RuntimeError(f"no segmentation reaches position {position}")
            start, piece = step
            pieces.append(piece)
            position = start
        pieces.reverse()

        ids = tuple(self._ids.get(p, -1) for p in pieces)
        return Segmentation(tuple(pieces), ids, best[n])

    def segment_greedy(self, text: str) -> Segmentation:
        """Greedy longest-match, for comparison. Time O(n * L).

        Kept in the library specifically so the optimality gap can be
        measured rather than asserted.
        """
        pieces: list[str] = []
        total = 0.0
        i = 0
        while i < len(text):
            for length in range(min(self._max_piece, len(text) - i), 0, -1):
                candidate = text[i:i + length]
                if candidate in self._logp:
                    pieces.append(candidate)
                    total += self._logp[candidate]
                    i += length
                    break
            else:
                pieces.append(text[i])
                total += self._unk_logp
                i += 1
        ids = tuple(self._ids.get(p, -1) for p in pieces)
        return Segmentation(tuple(pieces), ids, total)
