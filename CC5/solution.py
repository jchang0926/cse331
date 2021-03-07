"""
CC5- Trie
Name: Che-Jui (Jerry), Chang
"""

from __future__ import annotations  # allow self-reference


class TreeNode:
    """Tree Node that contains a value as well as left and right pointers"""
    def __init__(self, val: int = 0, left: TreeNode = None, right: TreeNode = None):
        self.val = val
        self.left = left
        self.right = right


def game_master(root: TreeNode) -> int:
    """
    starts with the root node, we pass it into the helper function.
    also create an attribute call answer where we compare it each
    time in the helper function when the tree is valid.
    :param root: root node
    :return: sum of the biggest subtree
    """
    def helper(node):
        """
        starts with root, keep going all the way to the left and check if each node's subtree
        is valid. If it is, we compare the total sum with answer attribute we create outside the
        helper function.
        :param node: root at first, then go through all the node from left to right.
        :return: lowest value of the tree, highest value of the tree,
        total, if the tree is valid from the root.
        """
        if node is None:
            return 100000, -100000, 0, True
        left_upper, left_lower, left_sum, left_valid = helper(node.left)
        right_upper, right_lower, right_sum, right_valid = helper(node.right)

        if left_valid and right_valid and right_upper > node.val > left_lower:
            tree_valid = True
        else:
            tree_valid = False

        if tree_valid:
            total = left_sum + right_sum + node.val
        else:
            total = -1
        TreeNode.ans = max(TreeNode.ans, total)
        return min(left_upper, node.val), max(right_lower, node.val), total, tree_valid

    TreeNode.ans = 0
    print(helper(root))
    return TreeNode.ans
