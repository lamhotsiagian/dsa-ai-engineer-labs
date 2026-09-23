"""Module external_sort.py for chapter_14."""
from __future__ import annotations

import heapq
import os
import tempfile
from dataclasses import dataclass
from typing import Callable, Iterable, Iterator, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class SortStats:
    records: int
    runs: int
    bytes_read: int
    bytes_written: int
    merge_passes: int


def _write_run(records: list[str], directory: str, index: int) -> tuple[str, int]:
    path = os.path.join(directory, f"run_{index:05d}.txt")
    written = 0
    with open(path, "w", encoding="utf-8") as fh:
        for record in records:
            line = record + "\n"
            fh.write(line)
            written += len(line.encode("utf-8"))
    return path, written


def _read_run(path: str) -> Iterator[str]:
    """Stream a run file one record at a time -- O(1) memory per run,
    which is what makes the merge fan-in a memory decision rather than a
    dataset-size decision."""
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            yield line.rstrip("\n")


def external_sort(
    source: Iterable[str],
    output_path: str,
    *,
    key: Callable[[str], object] = lambda r: r,
    run_size: int = 100_000,
    fan_in: int = 64,
    work_dir: str | None = None,
) -> SortStats:
    """Sort a stream larger than memory into `output_path`.

    Phase 1 (sort):  read `run_size` records, sort in memory, spill to disk.
    Phase 2 (merge): k-way merge the runs with a heap of size `fan_in`.

    Time  O(N log N) comparisons, but I/O is the real cost model:
          2N * ceil(log_fan_in(runs)) bytes moved.
    Space O(run_size) during phase 1, O(fan_in) during phase 2.

    `fan_in` is the parameter that matters: large enough to merge in ONE
    pass and every byte is read and written exactly twice. Too small and
    the dataset is rewritten once per extra pass.
    """
    if run_size < 1 or fan_in < 2:
        raise ValueError("run_size >= 1 and fan_in >= 2 are required")

    owns_dir = work_dir is None
    work_dir = work_dir or tempfile.mkdtemp(prefix="extsort_")
    run_paths: list[str] = []
    records = written = 0

    try:
        # ---- Phase 1: create sorted runs -----------------------------------
        buffer: list[str] = []
        for record in source:
            buffer.append(record)
            records += 1
            if len(buffer) >= run_size:
                buffer.sort(key=key)                 # in-memory, stable
                path, size = _write_run(buffer, work_dir, len(run_paths))
                run_paths.append(path)
                written += size
                buffer.clear()
        if buffer:
            buffer.sort(key=key)
            path, size = _write_run(buffer, work_dir, len(run_paths))
            run_paths.append(path)
            written += size
            buffer.clear()

        if not run_paths:                            # empty input
            open(output_path, "w").close()
            return SortStats(0, 0, 0, 0, 0)

        # ---- Phase 2: merge, possibly in several passes ---------------------
        passes = 0
        while len(run_paths) > fan_in:
            passes += 1
            merged: list[str] = []
            for start in range(0, len(run_paths), fan_in):
                group = run_paths[start:start + fan_in]
                path = os.path.join(work_dir, f"merge_{passes}_{start:05d}.txt")
                with open(path, "w", encoding="utf-8") as out:
                    for record in heapq.merge(*(_read_run(p) for p in group),
                                              key=key):
                        out.write(record + "\n")
                merged.append(path)
                for p in group:
                    os.remove(p)                     # reclaim as we go
            run_paths = merged

        passes += 1
        with open(output_path, "w", encoding="utf-8") as out:
            for record in heapq.merge(*(_read_run(p) for p in run_paths), key=key):
                out.write(record + "\n")
        for p in run_paths:
            os.remove(p)

        return SortStats(records=records, runs=len(run_paths),
                         bytes_read=written, bytes_written=written,
                         merge_passes=passes)
    finally:
        if owns_dir:
            try:
                os.rmdir(work_dir)
            except OSError:
                pass                                  # leftover files: leave them
