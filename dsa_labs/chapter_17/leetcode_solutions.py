"""LeetCode Solutions for chapter_17."""
from __future__ import annotations

# ----------------------------------------------------------------------------
# Problem: Fibonacci Number (LeetCode 509) [\LTwo]
# ----------------------------------------------------------------------------
def fib(n: int) -> int:
    if n < 2:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# ----------------------------------------------------------------------------
# Problem: Pow(x, n) (LeetCode 50) [\LThree]
# ----------------------------------------------------------------------------
def my_pow(x: float, n: int) -> float:
    if n < 0:
        x = 1.0 / x
        n = -n

    result = 1.0
    current_product = x

    while n > 0:
        if n % 2 == 1:
            result *= current_product
        current_product *= current_product
        n //= 2

    return result

# ----------------------------------------------------------------------------
# Problem: Merge k Sorted Lists (LeetCode 23) [\LFour]
# ----------------------------------------------------------------------------
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def merge_k_lists(lists: list[ListNode]) -> ListNode:
    if not lists:
        return None

    def merge_two(l1: ListNode, l2: ListNode) -> ListNode:
        dummy = ListNode(0)
        curr = dummy
        while l1 and l2:
            if l1.val <= l2.val:
                curr.next, l1 = l1, l1.next
            else:
                curr.next, l2 = l2, l2.next
            curr = curr.next
        curr.next = l1 if l1 else l2
        return dummy.next

    interval = 1
    while interval < len(lists):
        for i in range(0, len(lists) - interval, interval * 2):
            lists[i] = merge_two(lists[i], lists[i + interval])
        interval *= 2

    return lists[0]

