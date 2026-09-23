"""LeetCode Solutions for chapter_10."""
from __future__ import annotations

# ----------------------------------------------------------------------------
# Problem: Maximum Depth of Binary Tree (LeetCode 104) [\LTwo]
# ----------------------------------------------------------------------------
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def max_depth(root: TreeNode) -> int:
    if not root:
        return 0
    left_depth = max_depth(root.left)
    right_depth = max_depth(root.right)
    return 1 + max(left_depth, right_depth)

# ----------------------------------------------------------------------------
# Problem: Lowest Common Ancestor of a Binary Tree (LeetCode 236) [\LThree]
# ----------------------------------------------------------------------------
def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    if not root or root == p or root == q:
        return root

    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)

    if left and right:
        return root
    return left if left else right

# ----------------------------------------------------------------------------
# Problem: Binary Tree Maximum Path Sum (LeetCode 124) [\LFour]
# ----------------------------------------------------------------------------
def max_path_sum(root: TreeNode) -> int:
    max_sum = float("-inf")

    def max_gain(node: TreeNode) -> int:
        nonlocal max_sum
        if not node:
            return 0

        # Ignore negative contributions
        left_gain = max(0, max_gain(node.left))
        right_gain = max(0, max_gain(node.right))

        # Price of new path with current node as the highest vertex
        curr_path_sum = node.val + left_gain + right_gain
        max_sum = max(max_sum, curr_path_sum)

        # Return maximum contribution to parent
        return node.val + max(left_gain, right_gain)

    max_gain(root)
    return max_sum

