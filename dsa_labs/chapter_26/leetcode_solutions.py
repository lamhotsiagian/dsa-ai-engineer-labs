"""LeetCode Solutions for chapter_26."""
from __future__ import annotations

# ----------------------------------------------------------------------------
# Problem: Shuffle an Array (LeetCode 384) [\LTwo]
# ----------------------------------------------------------------------------
import random

class ArrayShuffler:
    def __init__(self, nums: list[int]):
        self.original = nums[:]
        self.nums = nums[:]

    def reset(self) -> list[int]:
        self.nums = self.original[:]
        return self.nums

    def shuffle(self) -> list[int]:
        n = len(self.nums)
        for i in range(n - 1, 0, -1):
            j = random.randint(0, i)
            self.nums[i], self.nums[j] = self.nums[j], self.nums[i]
        return self.nums

# ----------------------------------------------------------------------------
# Problem: Linked List Random Node (LeetCode 382) [\LThree]
# ----------------------------------------------------------------------------
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class LinkedListRandomNode:
    def __init__(self, head: ListNode):
        self.head = head

    def getRandom(self) -> int:
        chosen = self.head.val
        curr = self.head.next
        i = 2

        while curr:
            if random.randint(1, i) == 1:
                chosen = curr.val
            curr = curr.next
            i += 1

        return chosen

# ----------------------------------------------------------------------------
# Problem: Insert Delete GetRandom O(1) --- Duplicates allowed (LeetCode 381) [\LFour]
# ----------------------------------------------------------------------------
from collections import defaultdict
import random

class RandomizedCollection:
    def __init__(self):
        self.nums = []
        self.val_to_indices = defaultdict(set)

    def insert(self, val: int) -> bool:
        not_present = len(self.val_to_indices[val]) == 0
        self.val_to_indices[val].add(len(self.nums))
        self.nums.append(val)
        return not_present

    def remove(self, val: int) -> bool:
        if not self.val_to_indices[val]:
            return False

        # Get an index of val and the last element
        remove_idx = self.val_to_indices[val].pop()
        last_val = self.nums[-1]
        last_idx = len(self.nums) - 1

        if remove_idx != last_idx:
            self.nums[remove_idx] = last_val
            self.val_to_indices[last_val].remove(last_idx)
            self.val_to_indices[last_val].add(remove_idx)

        self.nums.pop()
        return True

    def getRandom(self) -> int:
        return random.choice(self.nums)

