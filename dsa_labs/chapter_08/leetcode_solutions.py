"""LeetCode Solutions for chapter_08."""
from __future__ import annotations

# ----------------------------------------------------------------------------
# Problem: Reverse Linked List (LeetCode 206) [\LTwo]
# ----------------------------------------------------------------------------
class ListNode:
    def __init__(self, val: int = 0, next: 'ListNode' = None):
        self.val = val
        self.next = next

def reverse_list(head: ListNode) -> ListNode:
    prev = None
    curr = head
    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    return prev

# ----------------------------------------------------------------------------
# Problem: Linked List Cycle II (LeetCode 142) [\LThree]
# ----------------------------------------------------------------------------
def detect_cycle(head: ListNode) -> ListNode:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            # Cycle detected; find entrance
            entry = head
            while entry != slow:
                entry = entry.next
                slow = slow.next
            return entry
    return None

# ----------------------------------------------------------------------------
# Problem: Reverse Nodes in k-Group (LeetCode 25) [\LFour]
# ----------------------------------------------------------------------------
def reverse_k_group(head: ListNode, k: int) -> ListNode:
    dummy = ListNode(0, head)
    group_prev = dummy

    while True:
        # Check if k nodes exist ahead
        kth = group_prev
        for _ in range(k):
            kth = kth.next
            if not kth:
                return dummy.next

        group_next = kth.next
        # Reverse group: [group_prev.next ... kth]
        prev = group_next
        curr = group_prev.next
        while curr != group_next:
            temp = curr.next
            curr.next = prev
            prev = curr
            curr = temp

        next_group_prev = group_prev.next
        group_prev.next = kth
        group_prev = next_group_prev

