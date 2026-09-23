"""LeetCode Solutions for chapter_22."""
from __future__ import annotations

# ----------------------------------------------------------------------------
# Problem: Flood Fill (LeetCode 733) [\LTwo]
# ----------------------------------------------------------------------------
def flood_fill(image: list[list[int]], sr: int, sc: int, color: int) -> list[list[int]]:
    orig = image[sr][sc]
    if orig == color:
        return image

    R, C = len(image), len(image[0])

    def dfs(r: int, c: int) -> None:
        if 0 <= r < R and 0 <= c < C and image[r][c] == orig:
            image[r][c] = color
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)

    dfs(sr, sc)
    return image

# ----------------------------------------------------------------------------
# Problem: Number of Islands (LeetCode 200) [\LThree]
# ----------------------------------------------------------------------------
def num_islands(grid: list[list[str]]) -> int:
    if not grid:
        return 0

    R, C = len(grid), len(grid[0])
    islands = 0

    def sink(r: int, c: int) -> None:
        if 0 <= r < R and 0 <= c < C and grid[r][c] == "1":
            grid[r][c] = "0"
            sink(r + 1, c)
            sink(r - 1, c)
            sink(r, c + 1)
            sink(r, c - 1)

    for r in range(R):
        for c in range(C):
            if grid[r][c] == "1":
                islands += 1
                sink(r, c)

    return islands

# ----------------------------------------------------------------------------
# Problem: Word Ladder (LeetCode 127) [\LFour]
# ----------------------------------------------------------------------------
def ladder_length(begin_word: str, end_word: str, word_list: list[str]) -> int:
    word_set = set(word_list)
    if end_word not in word_set:
        return 0

    begin_set = {begin_word}
    end_set = {end_word}
    length = 1

    while begin_set and end_set:
        # Always expand smaller set
        if len(begin_set) > len(end_set):
            begin_set, end_set = end_set, begin_set

        next_level = set()
        for word in begin_set:
            for i in range(len(word)):
                for c in "abcdefghijklmnopqrstuvwxyz":
                    next_word = word[:i] + c + word[i + 1:]
                    if next_word in end_set:
                        return length + 1
                    if next_word in word_set:
                        next_level.add(next_word)
                        word_set.remove(next_word)

        begin_set = next_level
        length += 1

    return 0

