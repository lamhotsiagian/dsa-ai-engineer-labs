"""Unit tests for Chapter 33: NeetCode 150 Practice Compendium.
Tests cover all 150 problems across 18 algorithmic domains.
"""
from __future__ import annotations
import pytest

from dsa_labs.chapter_33 import (
    arrays_and_hashing,
    two_pointers,
    sliding_window,
    stack,
    binary_search,
    linked_list,
    trees,
    tries,
    heap,
    backtracking,
    graphs,
    advanced_graphs,
    one_d_dp,
    two_d_dp,
    greedy,
    intervals,
    math_and_geometry,
    bit_manipulation,
)

# ============================================================================
# 1. Arrays & Hashing (9 problems)
# ============================================================================
def test_contains_duplicate():
    assert arrays_and_hashing.containsDuplicate([1, 2, 3, 1]) is True
    assert arrays_and_hashing.containsDuplicate([1, 2, 3, 4]) is False

def test_valid_anagram():
    assert arrays_and_hashing.isAnagram("anagram", "nagaram") is True
    assert arrays_and_hashing.isAnagram("rat", "car") is False

def test_two_sum():
    assert arrays_and_hashing.twoSum([2, 7, 11, 15], 9) == [0, 1]
    assert arrays_and_hashing.twoSum([3, 2, 4], 6) == [1, 2]

def test_group_anagrams():
    res = arrays_and_hashing.group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    sorted_res = sorted([sorted(g) for g in res])
    assert sorted_res == [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]

def test_top_k_frequent():
    res = arrays_and_hashing.topKFrequent([1, 1, 1, 2, 2, 3], 2)
    assert sorted(res) == [1, 2]

def test_encode_decode():
    codec = arrays_and_hashing.Codec()
    strs = ["neet", "code", "love", "you"]
    encoded = codec.encode(strs)
    assert codec.decode(encoded) == strs

def test_product_except_self():
    assert arrays_and_hashing.productExceptSelf([1, 2, 3, 4]) == [24, 12, 8, 6]
    assert arrays_and_hashing.productExceptSelf([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]

def test_valid_sudoku():
    board = [
        ["5","3",".",".","7",".",".",".","."],
        ["6",".",".","1","9","5",".",".","."],
        [".","9","8",".",".",".",".","6","."],
        ["8",".",".",".","6",".",".",".","3"],
        ["4",".",".","8",".","3",".",".","1"],
        ["7",".",".",".","2",".",".",".","6"],
        [".","6",".",".",".",".","2","8","."],
        [".",".",".","4","1","9",".",".","5"],
        [".",".",".",".","8",".",".","7","9"]
    ]
    assert arrays_and_hashing.isValidSudoku(board) is True

def test_longest_consecutive_sequence():
    assert arrays_and_hashing.longestConsecutive([100, 4, 200, 1, 3, 2]) == 4
    assert arrays_and_hashing.longestConsecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9

# ============================================================================
# 2. Two Pointers (5 problems)
# ============================================================================
def test_valid_palindrome():
    assert two_pointers.isPalindrome("A man, a plan, a canal: Panama") is True
    assert two_pointers.isPalindrome("race a car") is False

def test_two_sum_ii():
    assert two_pointers.twoSum([2, 7, 11, 15], 9) == [1, 2]

def test_three_sum():
    res = two_pointers.threeSum([-1, 0, 1, 2, -1, -4])
    sorted_res = sorted([sorted(t) for t in res])
    assert sorted_res == [[-1, -1, 2], [-1, 0, 1]]

def test_container_with_most_water():
    assert two_pointers.maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    assert two_pointers.maxArea([1, 1]) == 1

def test_trapping_rain_water():
    assert two_pointers.trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
    assert two_pointers.trap([4, 2, 0, 3, 2, 5]) == 9

# ============================================================================
# 3. Sliding Window (6 problems)
# ============================================================================
def test_best_time_stock():
    assert sliding_window.maxProfit([7, 1, 5, 3, 6, 4]) == 5
    assert sliding_window.maxProfit([7, 6, 4, 3, 1]) == 0

def test_longest_substring_without_repeating():
    assert sliding_window.lengthOfLongestSubstring("abcabcbb") == 3
    assert sliding_window.lengthOfLongestSubstring("bbbbb") == 1
    assert sliding_window.lengthOfLongestSubstring("pwwkew") == 3

def test_longest_repeating_character_replacement():
    assert sliding_window.characterReplacement("ABAB", 2) == 4
    assert sliding_window.characterReplacement("AABABBA", 1) == 4

def test_permutation_in_string():
    assert sliding_window.checkInclusion("ab", "eidbaooo") is True
    assert sliding_window.checkInclusion("ab", "eidboaoo") is False

def test_minimum_window_substring():
    assert sliding_window.minWindow("ADOBECODEBANC", "ABC") == "BANC"
    assert sliding_window.minWindow("a", "a") == "a"
    assert sliding_window.minWindow("a", "aa") == ""

def test_sliding_window_maximum():
    assert sliding_window.maxSlidingWindow([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
    assert sliding_window.maxSlidingWindow([1], 1) == [1]

# ============================================================================
# 4. Stack (7 problems)
# ============================================================================
def test_valid_parentheses():
    assert stack.isValid("()") is True
    assert stack.isValid("()[]{}") is True
    assert stack.isValid("(]") is False

def test_min_stack():
    ms = stack.MinStack()
    ms.push(-2)
    ms.push(0)
    ms.push(-3)
    assert ms.getMin() == -3
    ms.pop()
    assert ms.top() == 0
    assert ms.getMin() == -2

def test_eval_rpn():
    assert stack.evalRPN(["2", "1", "+", "3", "*"]) == 9
    assert stack.evalRPN(["4", "13", "5", "/", "+"]) == 6

def test_generate_parentheses():
    assert sorted(stack.generateParenthesis(3)) == sorted(["((()))", "(()())", "(())()", "()(())", "()()()"])

def test_daily_temperatures():
    assert stack.dailyTemperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]

def test_car_fleet():
    assert stack.carFleet(12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]) == 3
    assert stack.carFleet(10, [3], [3]) == 1

def test_largest_rectangle_histogram():
    assert stack.largestRectangleArea([2, 1, 5, 6, 2, 3]) == 10
    assert stack.largestRectangleArea([2, 4]) == 4

# ============================================================================
# 5. Binary Search (7 problems)
# ============================================================================
def test_binary_search():
    assert binary_search.search([-1, 0, 3, 5, 9, 12], 9) == 4
    assert binary_search.search([-1, 0, 3, 5, 9, 12], 2) == -1

def test_search_2d_matrix():
    matrix = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
    assert binary_search.searchMatrix(matrix, 3) is True
    assert binary_search.searchMatrix(matrix, 13) is False

def test_koko_eating_bananas():
    assert binary_search.minEatingSpeed([3, 6, 7, 11], 8) == 4
    assert binary_search.minEatingSpeed([30, 11, 23, 4, 20], 5) == 30

def test_find_min_rotated():
    assert binary_search.findMin([3, 4, 5, 1, 2]) == 1
    assert binary_search.findMin([4, 5, 6, 7, 0, 1, 2]) == 0

def test_search_rotated():
    assert binary_search.search([4, 5, 6, 7, 0, 1, 2], 0) == 4
    assert binary_search.search([4, 5, 6, 7, 0, 1, 2], 3) == -1

def test_time_based_store():
    tm = binary_search.TimeMap()
    tm.set("foo", "bar", 1)
    assert tm.get("foo", 1) == "bar"
    assert tm.get("foo", 3) == "bar"
    tm.set("foo", "bar2", 4)
    assert tm.get("foo", 4) == "bar2"
    assert tm.get("foo", 5) == "bar2"

def test_median_two_sorted_arrays():
    assert binary_search.findMedianSortedArrays([1, 3], [2]) == 2.0
    assert binary_search.findMedianSortedArrays([1, 2], [3, 4]) == 2.5

# ============================================================================
# 6. Linked List (11 problems)
# ============================================================================
def to_list(head):
    res = []
    curr = head
    while curr:
        res.append(curr.val)
        curr = curr.next
    return res

def from_list(vals):
    dummy = linked_list.ListNode(0)
    curr = dummy
    for v in vals:
        curr.next = linked_list.ListNode(v)
        curr = curr.next
    return dummy.next

def test_reverse_linked_list():
    l = from_list([1, 2, 3, 4, 5])
    assert to_list(linked_list.reverseList(l)) == [5, 4, 3, 2, 1]

def test_merge_two_sorted_lists():
    l1 = from_list([1, 2, 4])
    l2 = from_list([1, 3, 4])
    assert to_list(linked_list.mergeTwoLists(l1, l2)) == [1, 1, 2, 3, 4, 4]

def test_reorder_list():
    l = from_list([1, 2, 3, 4])
    linked_list.reorderList(l)
    assert to_list(l) == [1, 4, 2, 3]

def test_remove_nth_from_end():
    l = from_list([1, 2, 3, 4, 5])
    assert to_list(linked_list.removeNthFromEnd(l, 2)) == [1, 2, 3, 5]

def test_copy_random_list():
    n1 = linked_list.Node(7)
    n2 = linked_list.Node(13)
    n1.next = n2
    n2.random = n1
    cp = linked_list.copyRandomList(n1)
    assert cp.val == 7
    assert cp.next.val == 13
    assert cp.next.random.val == 7

def test_add_two_numbers():
    l1 = from_list([2, 4, 3])
    l2 = from_list([5, 6, 4])
    assert to_list(linked_list.addTwoNumbers(l1, l2)) == [7, 0, 8]

def test_has_cycle():
    n1 = linked_list.ListNode(1)
    n2 = linked_list.ListNode(2)
    n1.next = n2
    assert linked_list.hasCycle(n1) is False
    n2.next = n1
    assert linked_list.hasCycle(n1) is True

def test_find_duplicate():
    assert linked_list.findDuplicate([1, 3, 4, 2, 2]) == 2
    assert linked_list.findDuplicate([3, 1, 3, 4, 2]) == 3

def test_lru_cache():
    cache = linked_list.LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1
    cache.put(3, 3) # evicts key 2
    assert cache.get(2) == -1
    cache.put(4, 4) # evicts key 1
    assert cache.get(1) == -1
    assert cache.get(3) == 3
    assert cache.get(4) == 4

def test_merge_k_lists():
    lists = [from_list([1, 4, 5]), from_list([1, 3, 4]), from_list([2, 6])]
    assert to_list(linked_list.mergeKLists(lists)) == [1, 1, 2, 3, 4, 4, 5, 6]

def test_reverse_k_group():
    l = from_list([1, 2, 3, 4, 5])
    assert to_list(linked_list.reverseKGroup(l, 2)) == [2, 1, 4, 3, 5]

# ============================================================================
# 7. Trees (15 problems)
# ============================================================================
def test_trees_suite():
    # Helper tree builder
    #       4
    #      /     #     2   7
    #    / \ /     #   1  3 6  9
    root = trees.TreeNode(4)
    root.left = trees.TreeNode(2, trees.TreeNode(1), trees.TreeNode(3))
    root.right = trees.TreeNode(7, trees.TreeNode(6), trees.TreeNode(9))

    # 1. Invert Tree
    inv = trees.invertTree(trees.TreeNode(2, trees.TreeNode(1), trees.TreeNode(3)))
    assert inv.left.val == 3 and inv.right.val == 1

    # 2. Max Depth
    assert trees.maxDepth(root) == 3

    # 3. Diameter
    assert trees.diameterOfBinaryTree(root) == 4

    # 4. Balanced
    assert trees.isBalanced(root) is True

    # 5. Same Tree
    assert trees.isSameTree(root, root) is True
    assert trees.isSameTree(root, None) is False

    # 6. Subtree
    sub = trees.TreeNode(2, trees.TreeNode(1), trees.TreeNode(3))
    assert trees.isSubtree(root, sub) is True

    # 7. LCA in BST
    p = root.left.left   # 1
    q = root.left.right  # 3
    assert trees.lowestCommonAncestor(root, p, q).val == 2

    # 8. Level Order
    assert trees.levelOrder(root) == [[4], [2, 7], [1, 3, 6, 9]]

    # 9. Right Side View
    assert trees.rightSideView(root) == [4, 7, 9]

    # 10. Good Nodes (nodes 4, 7, 9 have val >= path max)
    assert trees.goodNodes(root) == 3

    # 11. Valid BST
    assert trees.isValidBST(root) is True

    # 12. Kth Smallest
    assert trees.kthSmallest(root, 3) == 3

    # 13. Build Tree
    preorder = [3, 9, 20, 15, 7]
    inorder = [9, 3, 15, 20, 7]
    b_tree = trees.buildTree(preorder, inorder)
    assert b_tree.val == 3 and b_tree.left.val == 9 and b_tree.right.val == 20

    # 14. Max Path Sum
    # -10, 9, 20, 15, 7 -> max is 15 + 20 + 7 = 42
    r_mps = trees.TreeNode(-10, trees.TreeNode(9), trees.TreeNode(20, trees.TreeNode(15), trees.TreeNode(7)))
    assert trees.maxPathSum(r_mps) == 42

    # 15. Codec Serialize / Deserialize
    codec = trees.Codec()
    ser = codec.serialize(root)
    deser = codec.deserialize(ser)
    assert trees.isSameTree(root, deser) is True

# ============================================================================
# 8. Tries (3 problems)
# ============================================================================
def test_tries_suite():
    # 1. Trie
    t = tries.Trie()
    t.insert("apple")
    assert t.search("apple") is True
    assert t.search("app") is False
    assert t.startsWith("app") is True

    # 2. WordDictionary
    wd = tries.WordDictionary()
    wd.addWord("bad")
    wd.addWord("dad")
    wd.addWord("mad")
    assert wd.search("pad") is False
    assert wd.search("bad") is True
    assert wd.search(".ad") is True
    assert wd.search("b..") is True

    # 3. Word Search II
    board = [
        ["o","a","a","n"],
        ["e","t","a","e"],
        ["i","h","k","r"],
        ["i","f","l","v"]
    ]
    words = ["oath","pea","eat","rain"]
    res = tries.findWords(board, words)
    assert sorted(res) == sorted(["eat", "oath"])

# ============================================================================
# 9. Heap & Priority Queue (7 problems)
# ============================================================================
def test_heap_suite():
    # 1. KthLargest
    kl = heap.KthLargest(3, [4, 5, 8, 2])
    assert kl.add(3) == 4
    assert kl.add(5) == 5

    # 2. Last Stone Weight
    assert heap.lastStoneWeight([2, 7, 4, 1, 8, 1]) == 1

    # 3. K Closest Points
    assert heap.kClosest([[1, 3], [-2, 2]], 1) == [[-2, 2]]

    # 4. Kth Largest in Array
    assert heap.findKthLargest([3, 2, 1, 5, 6, 4], 2) == 5

    # 5. Task Scheduler
    assert heap.leastInterval(["A", "A", "A", "B", "B", "B"], 2) == 8

    # 6. Twitter
    tw = heap.Twitter()
    tw.postTweet(1, 5)
    assert tw.getNewsFeed(1) == [5]
    tw.follow(1, 2)
    tw.postTweet(2, 6)
    assert tw.getNewsFeed(1) == [6, 5]
    tw.unfollow(1, 2)
    assert tw.getNewsFeed(1) == [5]

    # 7. MedianFinder
    mf = heap.MedianFinder()
    mf.addNum(1)
    mf.addNum(2)
    assert mf.findMedian() == 1.5
    mf.addNum(3)
    assert mf.findMedian() == 2.0

# ============================================================================
# 10. Backtracking (9 problems)
# ============================================================================
def test_backtracking_suite():
    # 1. Subsets
    res = backtracking.subsets([1, 2, 3])
    assert len(res) == 8

    # 2. Combination Sum
    assert backtracking.combinationSum([2, 3, 6, 7], 7) == [[2, 2, 3], [7]]

    # 3. Permutations
    assert len(backtracking.permute([1, 2, 3])) == 6

    # 4. Subsets II
    assert len(backtracking.subsetsWithDup([1, 2, 2])) == 6

    # 5. Combination Sum II
    res = backtracking.combinationSum2([10, 1, 2, 7, 6, 1, 5], 8)
    sorted_res = sorted([sorted(c) for c in res])
    assert sorted_res == sorted([[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]])

    # 6. Word Search
    board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]
    assert backtracking.exist(board, "ABCCED") is True
    assert backtracking.exist(board, "SEE") is True
    assert backtracking.exist(board, "ABCB") is False

    # 7. Palindrome Partitioning
    res = backtracking.partition("aab")
    assert res == [["a", "a", "b"], ["aa", "b"]]

    # 8. Letter Combinations
    assert sorted(backtracking.letterCombinations("23")) == sorted(["ad","ae","af","bd","be","bf","cd","ce","cf"])

    # 9. N-Queens
    assert len(backtracking.solveNQueens(4)) == 2

# ============================================================================
# 11. Graphs (13 problems)
# ============================================================================
def test_graphs_suite():
    # 1. Number of Islands
    grid = [
        ["1","1","1","1","0"],
        ["1","1","0","1","0"],
        ["1","1","0","0","0"],
        ["0","0","0","0","0"]
    ]
    assert graphs.numIslands(grid) == 1

    # 2. Clone Graph
    n1 = graphs.Node(1)
    n2 = graphs.Node(2)
    n1.neighbors.append(n2)
    n2.neighbors.append(n1)
    cg = graphs.cloneGraph(n1)
    assert cg.val == 1 and cg.neighbors[0].val == 2

    # 3. Max Area of Island
    grid2 = [[0, 1], [1, 1]]
    assert graphs.maxAreaOfIsland(grid2) == 3

    # 4. Pacific Atlantic
    heights = [[1, 2, 2, 3, 5], [3, 2, 3, 4, 4], [2, 4, 5, 3, 1], [6, 7, 1, 4, 5], [5, 1, 1, 2, 4]]
    res = graphs.pacificAtlantic(heights)
    assert (0, 4) in res and (1, 4) in res

    # 5. Surrounded Regions
    board = [["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]]
    graphs.solve(board)
    assert board == [["X","X","X","X"],["X","X","X","X"],["X","X","X","X"],["X","O","X","X"]]

    # 6. Rotting Oranges
    assert graphs.orangesRotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4

    # 7. Walls and Gates
    INF = 2147483647
    rooms = [[INF, -1, 0, INF], [INF, INF, INF, -1], [INF, -1, INF, -1], [0, -1, INF, INF]]
    graphs.wallsAndGates(rooms)
    assert rooms[0][0] == 3 and rooms[0][2] == 0

    # 8. Course Schedule
    assert graphs.canFinish(2, [[1, 0]]) is True
    assert graphs.canFinish(2, [[1, 0], [0, 1]]) is False

    # 9. Course Schedule II
    assert graphs.findOrder(2, [[1, 0]]) == [0, 1]

    # 10. Redundant Connection
    assert graphs.findRedundantConnection([[1, 2], [1, 3], [2, 3]]) == [2, 3]

    # 11. Connected Components
    assert graphs.countComponents(5, [[0, 1], [1, 2], [3, 4]]) == 2

    # 12. Graph Valid Tree
    assert graphs.validTree(5, [[0, 1], [0, 2], [0, 3], [1, 4]]) is True
    assert graphs.validTree(5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]) is False

    # 13. Word Ladder
    assert graphs.ladderLength("hit", "cog", ["hot","dot","dog","lot","log","cog"]) == 5

# ============================================================================
# 12. Advanced Graphs (6 problems)
# ============================================================================
def test_advanced_graphs_suite():
    # 1. Reconstruct Itinerary
    tickets = [["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]]
    assert advanced_graphs.findItinerary(tickets) == ["JFK", "MUC", "LHR", "SFO", "SJC"]

    # 2. Min Cost Connect Points
    assert advanced_graphs.minCostConnectPoints([[0,0],[2,2],[3,10],[5,2],[7,0]]) == 20

    # 3. Network Delay Time
    times = [[2, 1, 1], [2, 3, 1], [3, 4, 1]]
    assert advanced_graphs.networkDelayTime(times, 4, 2) == 2

    # 4. Swim in Rising Water
    grid = [[0, 2], [1, 3]]
    assert advanced_graphs.swimInWater(grid) == 3

    # 5. Alien Dictionary
    words = ["wrt", "wrf", "er", "ett", "rftt"]
    assert advanced_graphs.alienOrder(words) == "wertf"

    # 6. Cheapest Flights Within K Stops
    flights = [[0, 1, 100], [1, 2, 100], [0, 2, 500]]
    assert advanced_graphs.findCheapestPrice(3, flights, 0, 2, 1) == 200

# ============================================================================
# 13. 1-D Dynamic Programming (12 problems)
# ============================================================================
def test_one_d_dp_suite():
    # 1. Climbing Stairs
    assert one_d_dp.climbStairs(2) == 2
    assert one_d_dp.climbStairs(3) == 3

    # 2. Min Cost Climbing Stairs
    assert one_d_dp.minCostClimbingStairs([10, 15, 20]) == 15

    # 3. House Robber
    assert one_d_dp.rob([1, 2, 3, 1]) == 4

    # 4. House Robber II
    assert one_d_dp.rob([2, 3, 2]) == 3

    # 5. Longest Palindromic Substring
    assert one_d_dp.longestPalindrome("babad") in {"bab", "aba"}

    # 6. Palindromic Substrings
    assert one_d_dp.countSubstrings("abc") == 3
    assert one_d_dp.countSubstrings("aaa") == 6

    # 7. Decode Ways
    assert one_d_dp.numDecodings("12") == 2
    assert one_d_dp.numDecodings("226") == 3
    assert one_d_dp.numDecodings("06") == 0

    # 8. Coin Change
    assert one_d_dp.coinChange([1, 2, 5], 11) == 3
    assert one_d_dp.coinChange([2], 3) == -1

    # 9. Maximum Product Subarray
    assert one_d_dp.maxProduct([2, 3, -2, 4]) == 6

    # 10. Word Break
    assert one_d_dp.wordBreak("leetcode", ["leet", "code"]) is True

    # 11. Longest Increasing Subsequence
    assert one_d_dp.lengthOfLIS([10, 9, 2, 5, 3, 7, 101, 18]) == 4

    # 12. Partition Equal Subset Sum
    assert one_d_dp.canPartition([1, 5, 11, 5]) is True
    assert one_d_dp.canPartition([1, 2, 3, 5]) is False

# ============================================================================
# 14. 2-D Dynamic Programming (11 problems)
# ============================================================================
def test_two_d_dp_suite():
    # 1. Unique Paths
    assert two_d_dp.uniquePaths(3, 7) == 28

    # 2. Longest Common Subsequence
    assert two_d_dp.longestCommonSubsequence("abcde", "ace") == 3

    # 3. Stock with Cooldown
    assert two_d_dp.maxProfit([1, 2, 3, 0, 2]) == 3

    # 4. Coin Change II
    assert two_d_dp.change(5, [1, 2, 5]) == 4

    # 5. Target Sum
    assert two_d_dp.findTargetSumWays([1, 1, 1, 1, 1], 3) == 5

    # 6. Interleaving String
    assert two_d_dp.isInterleave("aabcc", "dbbca", "aadbbcbcac") is True

    # 7. Longest Increasing Path
    matrix = [[9, 9, 4], [6, 6, 8], [2, 1, 1]]
    assert two_d_dp.longestIncreasingPath(matrix) == 4

    # 8. Distinct Subsequences
    assert two_d_dp.numDistinct("rabbbit", "rabbit") == 3

    # 9. Edit Distance
    assert two_d_dp.minDistance("horse", "ros") == 3

    # 10. Burst Balloons
    assert two_d_dp.maxCoins([3, 1, 5, 8]) == 167

    # 11. Regular Expression Matching
    assert two_d_dp.isMatch("aa", "a") is False
    assert two_d_dp.isMatch("aa", "a*") is True
    assert two_d_dp.isMatch("ab", ".*") is True

# ============================================================================
# 15. Greedy (8 problems)
# ============================================================================
def test_greedy_suite():
    # 1. Maximum Subarray
    assert greedy.maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6

    # 2. Jump Game
    assert greedy.canJump([2, 3, 1, 1, 4]) is True
    assert greedy.canJump([3, 2, 1, 0, 4]) is False

    # 3. Jump Game II
    assert greedy.jump([2, 3, 1, 1, 4]) == 2

    # 4. Gas Station
    assert greedy.canCompleteCircuit([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]) == 3

    # 5. Hand of Straights
    assert greedy.isNStraightHand([1, 2, 3, 6, 2, 3, 4, 7, 8], 3) is True

    # 6. Merge Triplets
    assert greedy.mergeTriplets([[2, 5, 3], [1, 8, 4], [1, 7, 5]], [2, 7, 5]) is True

    # 7. Partition Labels
    assert greedy.partitionLabels("ababcbacadefegdehijhklij") == [9, 7, 8]

    # 8. Valid Parenthesis String
    assert greedy.checkValidString("()") is True
    assert greedy.checkValidString("(*)") is True
    assert greedy.checkValidString("(*))") is True

# ============================================================================
# 16. Intervals (6 problems)
# ============================================================================
def test_intervals_suite():
    # 1. Meeting Rooms
    assert intervals.canAttendMeetings([[0, 30], [5, 10], [15, 20]]) is False
    assert intervals.canAttendMeetings([[7, 10], [2, 4]]) is True

    # 2. Insert Interval
    assert intervals.insert([[1, 3], [6, 9]], [2, 5]) == [[1, 5], [6, 9]]

    # 3. Merge Intervals
    assert intervals.merge([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]

    # 4. Non-overlapping Intervals
    assert intervals.eraseOverlapIntervals([[1, 2], [2, 3], [3, 4], [1, 3]]) == 1

    # 5. Meeting Rooms II
    assert intervals.minMeetingRooms([[0, 30], [5, 10], [15, 20]]) == 2

    # 6. Minimum Interval to Include Each Query
    assert intervals.minInterval([[1, 4], [2, 4], [3, 6], [4, 4]], [2, 3, 4, 5]) == [3, 3, 1, 4]

# ============================================================================
# 17. Math & Geometry (8 problems)
# ============================================================================
def test_math_and_geometry_suite():
    # 1. Happy Number
    assert math_and_geometry.isHappy(19) is True
    assert math_and_geometry.isHappy(2) is False

    # 2. Plus One
    assert math_and_geometry.plusOne([1, 2, 3]) == [1, 2, 4]
    assert math_and_geometry.plusOne([9]) == [1, 0]

    # 3. Rotate Image
    mat = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    math_and_geometry.rotate(mat)
    assert mat == [[7, 4, 1], [8, 5, 2], [9, 6, 3]]

    # 4. Spiral Matrix
    mat2 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    assert math_and_geometry.spiralOrder(mat2) == [1, 2, 3, 6, 9, 8, 7, 4, 5]

    # 5. Set Matrix Zeroes
    mat3 = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    math_and_geometry.setZeroes(mat3)
    assert mat3 == [[1, 0, 1], [0, 0, 0], [1, 0, 1]]

    # 6. Pow(x, n)
    assert abs(math_and_geometry.myPow(2.0, 10) - 1024.0) < 1e-5
    assert abs(math_and_geometry.myPow(2.0, -2) - 0.25) < 1e-5

    # 7. Multiply Strings
    assert math_and_geometry.multiply("2", "3") == "6"
    assert math_and_geometry.multiply("123", "456") == "56088"

    # 8. Detect Squares
    ds = math_and_geometry.DetectSquares()
    ds.add([3, 10])
    ds.add([11, 2])
    ds.add([3, 2])
    assert ds.count([11, 10]) == 1
    assert ds.count([14, 8]) == 0
    ds.add([11, 2])
    assert ds.count([11, 10]) == 2

# ============================================================================
# 18. Bit Manipulation (7 problems)
# ============================================================================
def test_bit_manipulation_suite():
    # 1. Single Number
    assert bit_manipulation.singleNumber([2, 2, 1]) == 1

    # 2. Number of 1 Bits
    assert bit_manipulation.hammingWeight(11) == 3

    # 3. Counting Bits
    assert bit_manipulation.countBits(2) == [0, 1, 1]
    assert bit_manipulation.countBits(5) == [0, 1, 1, 2, 1, 2]

    # 4. Reverse Bits
    assert bit_manipulation.reverseBits(43261596) == 964176192

    # 5. Missing Number
    assert bit_manipulation.missingNumber([3, 0, 1]) == 2

    # 6. Sum of Two Integers
    assert bit_manipulation.getSum(1, 2) == 3
    assert bit_manipulation.getSum(2, 3) == 5

    # 7. Reverse Integer
    assert bit_manipulation.reverse(123) == 321
    assert bit_manipulation.reverse(-123) == -321
    assert bit_manipulation.reverse(120) == 21
