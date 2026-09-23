"""Chapter 33: NeetCode 150 - Trees"""
from __future__ import annotations
import math
import heapq
import bisect
from collections import defaultdict, deque, Counter, OrderedDict
from typing import Optional, List, Dict, Set, Tuple

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# ----------------------------------------------------------------------------
# Problem: Invert Binary Tree (LeetCode: invert-binary-tree)
# ----------------------------------------------------------------------------
def invertTree(root: TreeNode | None) -> TreeNode | None:
    # Base case: empty subtree requires no operation
    if not root:
        return None
    # Post-order inversion: recursively invert subtrees and swap pointers
    root.left, root.right = invertTree(root.right), invertTree(root.left)
    return root

# ----------------------------------------------------------------------------
# Problem: Maximum Depth of Binary Tree (LeetCode: maximum-depth-of-binary-tree)
# ----------------------------------------------------------------------------
def maxDepth(root: TreeNode | None) -> int:
    # Base case: depth of null tree is 0
    if not root:
        return 0
    # Maximum depth is 1 (current node) + maximum depth of child subtrees
    return 1 + max(maxDepth(root.left), maxDepth(root.right))

# ----------------------------------------------------------------------------
# Problem: Diameter of Binary Tree (LeetCode: diameter-of-binary-tree)
# ----------------------------------------------------------------------------
def diameterOfBinaryTree(root: TreeNode | None) -> int:
    max_d = 0

    def height(node: TreeNode | None) -> int:
        nonlocal max_d
        if not node:
            return 0
        left_h = height(node.left)
        right_h = height(node.right)
        # Longest path through this node is sum of left and right branch heights
        max_d = max(max_d, left_h + right_h)
        # Return height of subtree to parent
        return 1 + max(left_h, right_h)

    height(root)
    return max_d

# ----------------------------------------------------------------------------
# Problem: Balanced Binary Tree (LeetCode: balanced-binary-tree)
# ----------------------------------------------------------------------------
def isBalanced(root: TreeNode | None) -> bool:
    def dfs(node: TreeNode | None) -> int:
        if not node:
            return 0
        left = dfs(node.left)
        if left == -1: return -1  # Left subtree unbalanced
        right = dfs(node.right)
        if right == -1: return -1 # Right subtree unbalanced
        # If height difference exceeds 1, propagate -1 failure flag upward
        if abs(left - right) > 1:
            return -1
        return 1 + max(left, right)

    return dfs(root) != -1

# ----------------------------------------------------------------------------
# Problem: Same Tree (LeetCode: same-tree)
# ----------------------------------------------------------------------------
def isSameTree(p: TreeNode | None, q: TreeNode | None) -> bool:
    # Both nodes null: structural match
    if not p and not q:
        return True
    # One null or mismatched values: not identical
    if not p or not q or p.val != q.val:
        return False
    # Recursively check both left and right child subtrees
    return isSameTree(p.left, q.left) and isSameTree(p.right, q.right)

# ----------------------------------------------------------------------------
# Problem: Subtree of Another Tree (LeetCode: subtree-of-another-tree)
# ----------------------------------------------------------------------------
def isSubtree(root: TreeNode | None, subRoot: TreeNode | None) -> bool:
    if not subRoot: return True
    if not root: return False

    def is_same(p, q):
        if not p and not q: return True
        if not p or not q or p.val != q.val: return False
        return is_same(p.left, q.left) and is_same(p.right, q.right)

    # Either trees match at current root or subRoot is nested in left/right child
    if is_same(root, subRoot):
        return True
    return isSubtree(root.left, subRoot) or isSubtree(root.right, subRoot)

# ----------------------------------------------------------------------------
# Problem: Lowest Common Ancestor of a Binary Search Tree (LeetCode: lowest-common-ancestor-of-a-binary-search-tree)
# ----------------------------------------------------------------------------
def lowestCommonAncestor(root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
    curr = root
    while curr:
        # If both targets are greater, LCA must lie in the right subtree
        if p.val > curr.val and q.val > curr.val:
            curr = curr.right
        # If both targets are smaller, LCA must lie in the left subtree
        elif p.val < curr.val and q.val < curr.val:
            curr = curr.left
        # Split point encountered: curr is the lowest common ancestor
        else:
            return curr
    return root

# ----------------------------------------------------------------------------
# Problem: Binary Tree Level Order Traversal (LeetCode: binary-tree-level-order-traversal)
# ----------------------------------------------------------------------------
from collections import deque

def levelOrder(root: TreeNode | None) -> list[list[int]]:
    if not root:
        return []
    res = []
    q = deque([root])
    # BFS layer by layer
    while q:
        level_size = len(q)
        level_vals = []
        for _ in range(level_size):
            node = q.popleft()
            level_vals.append(node.val)
            if node.left: q.append(node.left)
            if node.right: q.append(node.right)
        res.append(level_vals)
    return res

# ----------------------------------------------------------------------------
# Problem: Binary Tree Right Side View (LeetCode: binary-tree-right-side-view)
# ----------------------------------------------------------------------------
from collections import deque

def rightSideView(root: TreeNode | None) -> list[int]:
    if not root:
        return []
    res = []
    q = deque([root])
    while q:
        level_len = len(q)
        for i in range(level_len):
            node = q.popleft()
            # The last element encountered in each BFS level is visible from right
            if i == level_len - 1:
                res.append(node.val)
            if node.left: q.append(node.left)
            if node.right: q.append(node.right)
    return res

# ----------------------------------------------------------------------------
# Problem: Count Good Nodes in Binary Tree (LeetCode: count-good-nodes-in-binary-tree)
# ----------------------------------------------------------------------------
def goodNodes(root: TreeNode) -> int:
    def dfs(node: TreeNode | None, max_val: int) -> int:
        if not node:
            return 0
        # Node is good if its value is >= maximum value along root-to-node path
        good = 1 if node.val >= max_val else 0
        new_max = max(max_val, node.val)
        return good + dfs(node.left, new_max) + dfs(node.right, new_max)

    return dfs(root, root.val)

# ----------------------------------------------------------------------------
# Problem: Validate Binary Search Tree (LeetCode: validate-binary-search-tree)
# ----------------------------------------------------------------------------
def isValidBST(root: TreeNode | None) -> bool:
    def validate(node: TreeNode | None, low: float, high: float) -> bool:
        if not node:
            return True
        # Current node value must be strictly within (low, high) bounds
        if not (low < node.val < high):
            return False
        # Left child bounded by (low, node.val); Right child by (node.val, high)
        return validate(node.left, low, node.val) and validate(node.right, node.val, high)

    return validate(root, float('-inf'), float('inf'))

# ----------------------------------------------------------------------------
# Problem: Kth Smallest Element in a BST (LeetCode: kth-smallest-element-in-a-bst)
# ----------------------------------------------------------------------------
def kthSmallest(root: TreeNode | None, k: int) -> int:
    # In-order traversal of BST visits nodes in strictly increasing order
    stack = []
    curr = root
    while curr or stack:
        # Traverse down left spine
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        k -= 1
        if k == 0:
            return curr.val
        curr = curr.right
    return -1

# ----------------------------------------------------------------------------
# Problem: Construct Binary Tree from Preorder and Inorder Traversal (LeetCode: construct-binary-tree-from-preorder-and-inorder-traversal)
# ----------------------------------------------------------------------------
def buildTree(preorder: list[int], inorder: list[int]) -> TreeNode | None:
    # Preorder: [Root, Left Subtree, Right Subtree]
    # Inorder:  [Left Subtree, Root, Right Subtree]
    in_map = {val: idx for idx, val in enumerate(inorder)}
    pre_idx = 0

    def helper(l: int, r: int) -> TreeNode | None:
        nonlocal pre_idx
        if l > r:
            return None
        # Root value is determined by next element in preorder traversal
        root_val = preorder[pre_idx]
        pre_idx += 1
        root = TreeNode(root_val)
        mid = in_map[root_val]

        # Construct left subtree before right subtree to match preorder sequence
        root.left = helper(l, mid - 1)
        root.right = helper(mid + 1, r)
        return root

    return helper(0, len(inorder) - 1)

# ----------------------------------------------------------------------------
# Problem: Binary Tree Maximum Path Sum (LeetCode: binary-tree-maximum-path-sum)
# ----------------------------------------------------------------------------
def maxPathSum(root: TreeNode | None) -> int:
    max_sum = float('-inf')

    def max_gain(node: TreeNode | None) -> int:
        nonlocal max_sum
        if not node:
            return 0
        # Discard negative contributions by flooring gains at 0
        left_gain = max(0, max_gain(node.left))
        right_gain = max(0, max_gain(node.right))
        # Path arching through current node connecting both branches
        price_newpath = node.val + left_gain + right_gain
        max_sum = max(max_sum, price_newpath)
        # Return maximum single-branch contribution to parent
        return node.val + max(left_gain, right_gain)

    max_gain(root)
    return int(max_sum)

# ----------------------------------------------------------------------------
# Problem: Serialize and Deserialize Binary Tree (LeetCode: serialize-and-deserialize-binary-tree)
# ----------------------------------------------------------------------------
class Codec:
    def serialize(self, root: TreeNode | None) -> str:
        # Preorder traversal encoding null markers as 'N'
        vals = []
        def dfs(node):
            if not node:
                vals.append("N")
                return
            vals.append(str(node.val))
            dfs(node.left)
            dfs(node.right)
        dfs(root)
        return ",".join(vals)

    def deserialize(self, data: str) -> TreeNode | None:
        vals = data.split(",")
        idx = 0
        def dfs():
            nonlocal idx
            if vals[idx] == "N":
                idx += 1
                return None
            node = TreeNode(int(vals[idx]))
            idx += 1
            node.left = dfs()
            node.right = dfs()
            return node
        return dfs()

