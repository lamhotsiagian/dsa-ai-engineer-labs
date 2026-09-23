"""LeetCode Solutions for chapter_29."""
from __future__ import annotations

# ----------------------------------------------------------------------------
# Problem: Implement Stack using Queues (LeetCode 225) [\LTwo]
# ----------------------------------------------------------------------------
from collections import deque

class MyStack:
    def __init__(self):
        self.q = deque()

    def push(self, x: int) -> None:
        self.q.append(x)
        for _ in range(len(self.q) - 1):
            self.q.append(self.q.popleft())

    def pop(self) -> int:
        return self.q.popleft()

    def top(self) -> int:
        return self.q[0]

    def empty(self) -> bool:
        return len(self.q) == 0

# ----------------------------------------------------------------------------
# Problem: LRU Cache (LeetCode 146) [\LThree]
# ----------------------------------------------------------------------------
class Node:
    def __init__(self, key: int = 0, val: int = 0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache: dict[int, Node] = {}
        # Dummy sentinels
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node) -> None:
        p, n = node.prev, node.next
        p.next = n
        n.prev = p

    def _add_to_front(self, node: Node) -> None:
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._add_to_front(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        node = Node(key, value)
        self.cache[key] = node
        self._add_to_front(node)

        if len(self.cache) > self.cap:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]

# ----------------------------------------------------------------------------
# Problem: LFU Cache (LeetCode 460) [\LFour]
# ----------------------------------------------------------------------------
from collections import defaultdict, OrderedDict

class LFUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.min_freq = 0
        self.key_to_val_freq = {}  # key -> (val, freq)
        self.freq_to_keys = defaultdict(OrderedDict)

    def _update_freq(self, key: int, val: int) -> None:
        _, freq = self.key_to_val_freq[key]
        del self.freq_to_keys[freq][key]

        if not self.freq_to_keys[freq]:
            del self.freq_to_keys[freq]
            if self.min_freq == freq:
                self.min_freq += 1

        new_freq = freq + 1
        self.key_to_val_freq[key] = (val, new_freq)
        self.freq_to_keys[new_freq][key] = None

    def get(self, key: int) -> int:
        if key not in self.key_to_val_freq:
            return -1
        val, _ = self.key_to_val_freq[key]
        self._update_freq(key, val)
        return val

    def put(self, key: int, value: int) -> None:
        if self.cap <= 0:
            return

        if key in self.key_to_val_freq:
            self._update_freq(key, value)
            return

        if len(self.key_to_val_freq) >= self.cap:
            evict_key, _ = self.freq_to_keys[self.min_freq].popitem(last=False)
            del self.key_to_val_freq[evict_key]

        self.key_to_val_freq[key] = (value, 1)
        self.freq_to_keys[1][key] = None
        self.min_freq = 1

