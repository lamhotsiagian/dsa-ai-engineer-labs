"""Module linked.py for chapter_08."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ListNode:
    val: int
    next: "ListNode | None" = None


def from_iterable(values) -> ListNode | None:
    """Build a list from any iterable. O(n)."""
    dummy = ListNode(0)
    tail = dummy
    for value in values:
        tail.next = ListNode(value)
        tail = tail.next
    return dummy.next


def to_list(head: ListNode | None, *, limit: int = 10_000) -> list[int]:
    """Materialise to a Python list, refusing to hang on a cycle.

    The limit is a safety valve: a test helper that follows `next` forever
    turns a logic bug into a hung test suite, which is much harder to debug
    than an exception.
    """
    out: list[int] = []
    node = head
    while node is not None:
        out.append(node.val)
        if len(out) > limit:
            raise RuntimeError("cycle detected or list longer than limit")
        node = node.next
    return out


def has_cycle(head: ListNode | None) -> bool:
    """Floyd's algorithm. Time O(n), Space O(1)."""
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next            # type: ignore[union-attr]
        fast = fast.next.next
        if slow is fast:
            return True
    return False


def reverse_between(head: ListNode | None, left: int, right: int) -> ListNode | None:
    """Reverse the sublist from position `left` to `right`, 1-indexed.

    Time O(n), Space O(1). The dummy head is what makes left == 1 ordinary
    rather than a special case.
    """
    if head is None or left >= right:
        return head
    if left < 1:
        raise ValueError("positions are 1-indexed")

    dummy = ListNode(0, head)
    before = dummy
    for _ in range(left - 1):
        if before.next is None:
            raise IndexError("left is past the end of the list")
        before = before.next

    # Head-insert each subsequent node directly after `before`, which
    # reverses the segment in one pass without a second traversal.
    tail_of_segment = before.next
    for _ in range(right - left):
        if tail_of_segment is None or tail_of_segment.next is None:
            raise IndexError("right is past the end of the list")
        moved = tail_of_segment.next
        tail_of_segment.next = moved.next
        moved.next = before.next
        before.next = moved

    return dummy.next
