"""Chapter 33: NeetCode 150 - Linked List"""
from __future__ import annotations
import math
import heapq
import bisect
from collections import defaultdict, deque, Counter, OrderedDict
from typing import Optional, List, Dict, Set, Tuple

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random

# ----------------------------------------------------------------------------
# Problem: Reverse Linked List (LeetCode: reverse-linked-list)
# ----------------------------------------------------------------------------
def reverseList(root: ListNode | None) -> ListNode | None:
    prev, curr = None, root
    while curr:
        # Stash next node before breaking pointer
        nxt = curr.next
        curr.next = prev  # Invert arrow
        prev = curr       # Shift prev forward
        curr = nxt        # Shift curr forward
    return prev

# ----------------------------------------------------------------------------
# Problem: Merge Two Sorted Lists (LeetCode: merge-two-sorted-lists)
# ----------------------------------------------------------------------------
def mergeTwoLists(list1: ListNode | None, list2: ListNode | None) -> ListNode | None:
    # Dummy head simplifies edge cases when appending first node
    dummy = ListNode()
    tail = dummy
    while list1 and list2:
        if list1.val <= list2.val:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next
        tail = tail.next
    # Attach remaining non-empty tail in O(1)
    tail.next = list1 if list1 else list2
    return dummy.next

# ----------------------------------------------------------------------------
# Problem: Linked List Cycle (LeetCode: linked-list-cycle)
# ----------------------------------------------------------------------------
def hasCycle(head: ListNode | None) -> bool:
    # Floyd's Cycle-Finding Algorithm (Tortoise and Hare)
    slow = fast = head
    while fast and fast.next:
        slow = slow.next        # 1 step
        fast = fast.next.next   # 2 steps
        # If fast catches slow, a cycle is guaranteed
        if slow == fast:
            return True
    return False

# ----------------------------------------------------------------------------
# Problem: Reorder List (LeetCode: reorder-list)
# ----------------------------------------------------------------------------
def reorderList(head: ListNode | None) -> None:
    if not head or not head.next:
        return
    # 1. Split list in half using fast & slow pointers
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    second = slow.next
    slow.next = None  # Sever first half from second half

    # 2. Reverse the second half
    prev = None
    curr = second
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    second = prev

    # 3. Interleave nodes from first and second halves
    first = head
    while second:
        tmp1, tmp2 = first.next, second.next
        first.next = second
        second.next = tmp1
        first, second = tmp1, tmp2

# ----------------------------------------------------------------------------
# Problem: Remove Nth Node From End of List (LeetCode: remove-nth-node-from-end-of-list)
# ----------------------------------------------------------------------------
def removeNthFromEnd(head: ListNode | None, n: int) -> ListNode | None:
    dummy = ListNode(0, head)
    left = dummy
    right = head
    # Advance right pointer n steps forward
    for _ in range(n):
        right = right.next
    # Move both pointers until right reaches past the tail
    while right:
        left = left.next
        right = right.next
    # Left is now positioned directly before the target node to delete
    left.next = left.next.next
    return dummy.next

# ----------------------------------------------------------------------------
# Problem: Copy List with Random Pointer (LeetCode: copy-list-with-random-pointer)
# ----------------------------------------------------------------------------
def copyRandomList(head: 'Node') -> 'Node':
    # Hash map mapping original node -> cloned node
    old_to_new = {None: None}
    curr = head
    # Pass 1: Create all new nodes without wiring pointers
    while curr:
        old_to_new[curr] = Node(curr.val)
        curr = curr.next
    # Pass 2: Connect next and random pointers using lookup table
    curr = head
    while curr:
        old_to_new[curr].next = old_to_new[curr.next]
        old_to_new[curr].random = old_to_new[curr.random]
        curr = curr.next
    return old_to_new[head]

# ----------------------------------------------------------------------------
# Problem: Add Two Numbers (LeetCode: add-two-numbers)
# ----------------------------------------------------------------------------
def addTwoNumbers(l1: ListNode | None, l2: ListNode | None) -> ListNode | None:
    dummy = ListNode()
    curr = dummy
    carry = 0
    # Continue while either list has digits or a carry-over remains
    while l1 or l2 or carry:
        v1 = l1.val if l1 else 0
        v2 = l2.val if l2 else 0
        total = v1 + v2 + carry
        carry = total // 10
        curr.next = ListNode(total % 10)
        curr = curr.next
        if l1: l1 = l1.next
        if l2: l2 = l2.next
    return dummy.next

# ----------------------------------------------------------------------------
# Problem: Find the Duplicate Number (LeetCode: find-the-duplicate-number)
# ----------------------------------------------------------------------------
def findDuplicate(nums: list[int]) -> int:
    # Cycle detection treating value as next pointer: index -> nums[index]
    slow = fast = 0
    # Phase 1: Locate meeting point inside the cycle
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    # Phase 2: Find cycle entrance by resetting slow pointer to start
    slow2 = 0
    while slow != slow2:
        slow = nums[slow]
        slow2 = nums[slow2]
    return slow

# ----------------------------------------------------------------------------
# Problem: LRU Cache (LeetCode: lru-cache)
# ----------------------------------------------------------------------------
class DNode:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = {}  # key -> DNode
        # Sentinel dummy nodes eliminate edge checks on empty list
        self.head, self.tail = DNode(), DNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: DNode) -> None:
        # Unlink node from its current position
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_front(self, node: DNode) -> None:
        # Splice node immediately after dummy head (most recently used)
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add_to_front(node)  # Refresh recency
            return node.val
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            node = self.cache[key]
            node.val = value
            self._remove(node)
            self._add_to_front(node)
        else:
            # If capacity exceeded, evict least recently used (before tail)
            if len(self.cache) >= self.cap:
                lru = self.tail.prev
                self._remove(lru)
                del self.cache[lru.key]
            new_node = DNode(key, value)
            self._add_to_front(new_node)
            self.cache[key] = new_node

# ----------------------------------------------------------------------------
# Problem: Merge k Sorted Lists (LeetCode: merge-k-sorted-lists)
# ----------------------------------------------------------------------------
import heapq

def mergeKLists(lists: list[ListNode | None]) -> ListNode | None:
    # Min-heap storing tuples: (node_value, list_index, node)
    heap = []
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))
            
    dummy = ListNode()
    curr = dummy
    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        # Advance the extracted list and reinsert next node into heap
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    return dummy.next

# ----------------------------------------------------------------------------
# Problem: Reverse Nodes in k-Group (LeetCode: reverse-nodes-in-k-group)
# ----------------------------------------------------------------------------
def reverseKGroup(head: ListNode | None, k: int) -> ListNode | None:
    dummy = ListNode(0, head)
    group_prev = dummy

    def get_kth(curr: ListNode | None, k: int) -> ListNode | None:
        while curr and k > 0:
            curr = curr.next
            k -= 1
        return curr

    while True:
        kth = get_kth(group_prev, k)
        # If fewer than k nodes remain, leave them untouched
        if not kth:
            break
        group_next = kth.next

        # Reverse nodes between group_prev and group_next
        prev, curr = kth.next, group_prev.next
        while curr != group_next:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt

        # Connect previous group tail to newly reversed group head
        tmp = group_prev.next
        group_prev.next = kth
        group_prev = tmp
    return dummy.next

