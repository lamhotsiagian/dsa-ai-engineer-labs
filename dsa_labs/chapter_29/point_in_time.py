"""Point-in-time feature lookup (Chapter 29)."""
from __future__ import annotations
import bisect
from dataclasses import dataclass

@dataclass(frozen=True)
class FeatureRecord:
    valid_from: float
    value: float

class PointInTimeFeatureStore:
    def __init__(self):
        self._history: dict[str, list[FeatureRecord]] = {}

    def put(self, entity_id: str, valid_from: float, value: float) -> None:
        rec = FeatureRecord(valid_from=valid_from, value=value)
        if entity_id not in self._history:
            self._history[entity_id] = [rec]
        else:
            hist = self._history[entity_id]
            idx = bisect.bisect_right([r.valid_from for r in hist], valid_from)
            hist.insert(idx, rec)

    def get(self, entity_id: str, as_of: float) -> float | None:
        hist = self._history.get(entity_id)
        if not hist:
            return None
        timestamps = [r.valid_from for r in hist]
        idx = bisect.bisect_right(timestamps, as_of) - 1
        if idx >= 0:
            return hist[idx].value
        return None
