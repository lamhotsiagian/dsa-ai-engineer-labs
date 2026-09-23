"""Module context_budget.py for chapter_05."""
from __future__ import annotations

import bisect
from dataclasses import dataclass
from itertools import accumulate


@dataclass(frozen=True)
class Turn:
    role: str                 # "user" or "assistant"
    tokens: int


@dataclass(frozen=True)
class BudgetPlan:
    kept_turns: int           # how many of the most recent turns survive
    dropped_turns: int
    prompt_tokens: int        # system + kept turns + retrieved context
    generation_reserve: int
    total_tokens: int
    fits: bool


class ContextBudget:
    """Decide how much conversation history fits in a context window.

    Builds a suffix-cumulative array over turn token counts so that
    "what do the last t turns cost" is one lookup, and the largest affordable
    t is a binary search.

    Build  O(m).
    Plan   O(log m) per request.
    """

    def __init__(self, turns: list[Turn]) -> None:
        self._turns = turns
        # suffix_cost[t] = tokens used by the LAST t turns.
        reversed_tokens = [t.tokens for t in reversed(turns)]
        self._suffix_cost = [0, *accumulate(reversed_tokens)]

    def cost_of_last(self, t: int) -> int:
        """Tokens consumed by the most recent ``t`` turns. O(1)."""
        if not 0 <= t <= len(self._turns):
            raise IndexError(f"t must be in [0, {len(self._turns)}]")
        return self._suffix_cost[t]

    def plan(
        self,
        context_limit: int,
        system_tokens: int,
        retrieved_tokens: int,
        generation_reserve: int,
    ) -> BudgetPlan:
        """Keep as many recent turns as fit, dropping the oldest first."""
        fixed = system_tokens + retrieved_tokens + generation_reserve
        available = context_limit - fixed

        if available < 0:
            # Even with zero history the request does not fit. Report it
            # rather than silently truncating something the caller needs.
            return BudgetPlan(0, len(self._turns), system_tokens + retrieved_tokens,
                              generation_reserve, fixed, fits=False)

        # suffix_cost is non-decreasing, so bisect_right finds the largest t
        # with suffix_cost[t] <= available in O(log m).
        kept = bisect.bisect_right(self._suffix_cost, available) - 1
        kept = max(0, min(kept, len(self._turns)))

        history = self._suffix_cost[kept]
        prompt = system_tokens + retrieved_tokens + history
        return BudgetPlan(
            kept_turns=kept,
            dropped_turns=len(self._turns) - kept,
            prompt_tokens=prompt,
            generation_reserve=generation_reserve,
            total_tokens=prompt + generation_reserve,
            fits=True,
        )
