"""
Project 3 (Fall 2020) - Red/Black Trees
Name: Che-Jui (Jerry), Chang
"""

from __future__ import annotations
from typing import TypeVar, Generic, Callable, Generator
from Project3.RBnode import RBnode as Node
from copy import deepcopy
import queue

T = TypeVar('T')


class RBtree:
    """
    A Red/Black Tree class
    :root: Root Node of the tree
    :size: Number of Nodes
    """

    __slots__ = ['root', 'size']

    def __init__(self, root: Node = None):
        """ Initializer for an RBtree """
        # this alllows us to initialize by copying an existing tree
        self.root = deepcopy(root)
        if self.root:
            self.root.parent = None
        self.size = 0 if not self.root else self.root.subtree_size()

    def __eq__(self, other: RBtree) -> bool:
        """ Equality Comparator for RBtrees """
        comp = lambda n1, n2: n1 == n2 and (
            (comp(n1.left, n2.left) and comp(n1.right, n2.right)) if (n1 and n2) else True)
        return comp(self.root, other.root) and self.size == other.size

    def __str__(self) -> str:
        """ represents Red/Black tree as string """

        if not self.root:
            return 'Empty RB Tree'

        root, bfs_queue, height = self.root, queue.SimpleQueue(), self.root.subtree_height()
        track = {i: [] for i in range(height + 1)}
        bfs_queue.put((root, 0, root.parent))

        while bfs_queue:
            n = bfs_queue.get()
            if n[1] > height:
                break
            track[n[1]].append(n)
            if n[0] is None:
                bfs_queue.put((None, n[1] + 1, None))
                bfs_queue.put((None, n[1] + 1, None))
                continue
            bfs_queue.put((None, n[1] + 1, None) if not n[0].left else (n[0].left, n[1] + 1, n[0]))
            bfs_queue.put((None, n[1] + 1, None) if not n[0].right else (n[0].right, n[1] + 1, n[0]))

        spaces = 12 * (2 ** (height))
        ans = '\n' + '\t\tVisual Level Order Traversal of RBtree'.center(spaces) + '\n\n'
        for i in range(height):
            ans += f"Level {i + 1}: "
            for n in track[i]:
                space = int(round(spaces / (2 ** i)))
                if not n[0]:
                    ans += ' ' * space
                    continue
                ans += "{} ({})".format(n[0], n[2].value if n[2] else None).center(space, " ")
            ans += '\n'
        return ans

    def __repr__(self) -> str:
        return self.__str__()

    ################################################################
    ################### Complete Functions Below ###################
    ################################################################

    ######################## Static Methods ########################
    # These methods are static as they operate only on nodes, without explicitly referencing an RBtree instance

    @staticmethod
    def set_child(parent: Node, child: Node, is_left: bool) -> None:
        """
        Check if is_left is true, if is true, then we change the left to new node
        Otherwise, we set the right to new node
        """
        if is_left is True:
            parent.left = child
        else:
            parent.right = child

    @staticmethod
    def replace_child(parent: Node, current_child: Node, new_child: Node) -> None:
        """
        if the current_child is parent.left, set the child to parent.left
        if the current_child is parent.right, set the child to parent.right
        """
        if parent is None:
            return None
        elif parent.left == current_child:
            RBtree.set_child(parent, new_child, True)
        else:
            RBtree.set_child(parent, new_child, False)

    @staticmethod
    def get_sibling(node: Node) -> Node:
        """
        if the node is none or has no parents, we return none.
        if node is node.parent.left, we return node.parent.right.
        if node is node.parent.right, we return node.parent.left.
        """
        if node is None:
            return None
        if node.parent is None:
            return None
        elif node.parent.left is node:
            return node.parent.right
        else:
            return node.parent.left

    @staticmethod
    def get_grandparent(node: Node) -> Node:
        """
        if node is none or has no parent, we return none.
        otherwise, we return node.parent.parent
        """
        if node is None:
            return None
        if node.parent is None:
            return None
        else:
            return node.parent.parent

    @staticmethod
    def get_uncle(node: Node) -> Node:
        """
        if node.parent is not none, we set grand parent to node.parent.parent
        if grand parent is none, we return none.
        if grand parent.left is node.parent, we return grand parent.right
        if grand parent.right is node.parent, we return grand parent.left
        """
        grandparent = None
        if node.parent is not None:
            grandparent = node.parent.parent
        if grandparent is None:
            return None
        if grandparent.left == node.parent:
            return grandparent.right
        else:
            return grandparent.left

    ######################## Misc Utilities ##########################

    def min(self, node: Node) -> Node:
        """
        find the smallest value inside the tree, which is keep looking for
        node.left. if it does not exist, we return node.
        :param node: the root
        :return: return the node with smallest value
        """
        if self.root is None:
            return None
        if node.left is not None:
            return self.min(node.left)
        else:
            return node

    def max(self, node: Node) -> Node:
        """
        find the biggest value inside the tree, which is keep looking for
        node.right. if it does not exist, we return node.
        :param node: the root
        :return: return the node with biggest value
        """
        if self.root is None:
            return None
        if node.right is not None:
            return self.max(node.right)
        else:
            return node

    def search(self, node: Node, val: Generic[T]) -> Node:
        """
        look for the node with same value that's passed in to this function.
        if Node(val) does not exist in tree, return none
        :param node: root at first, then base on val to decide root.left or root.right
        :param val: the value we looking for
        :return: the node with same value or none
        """
        if node is None:
            return None
        if node.value == val:
            return node
        elif val < node.value and node.left is not None:
            return self.search(node.left, val)
        elif val > node.value and node.right is not None:
            return self.search(node.right, val)
        return node

    ######################## Tree Traversals #########################

    def inorder(self, node: Node) -> Generator[Node, None, None]:
        """
        yield the left side of the tree first, then the root, then the right part.
        if root is none, return
        :param node: root
        :return: yield the inorder tree traversals
        """
        if self.root is None:
            return
        if node.left is not None:
            for val in self.inorder(node.left):
                yield val
        yield node
        if node.right is not None:
            for other in self.inorder(node.right):
                yield other

    def preorder(self, node: Node) -> Generator[Node, None, None]:
        """
        yield the root first, then left side of the tree, then right side.
        if root is none, return
        :param node: root
        :return: yield the preorder tree traversals
        """
        if self.root is None:
            return
        yield node
        if node.left is not None:
            for val in self.preorder(node.left):
                yield val
        if node.right is not None:
            for other in self.preorder(node.right):
                yield other

    def postorder(self, node: Node) -> Generator[Node, None, None]:
        """
        yield the left side of the tree first, then the right side, then the root.
        if root is none, return
        :param node: root
        :return: yield the postorder tree traversals
        """
        if self.root is None:
            return
        if node.left is not None:
            for val in self.postorder(node.left):
                yield val
        if node.right is not None:
            for other in self.postorder(node.right):
                yield other
        yield node

    def bfs(self, node: Node) -> Generator[Node, None, None]:
        """
        use a queue to travel all the nodes by going through it level by level
        :param node: root
        :return: yield the bfs tree traversals
        """
        if node is None:
            node = self.root
        bfs = queue.SimpleQueue()
        bfs.put(node)
        while not bfs.empty():
            current = bfs.get()
            yield current
            if current.left is not None:
                bfs.put(current.left)
            if current.right is not None:
                bfs.put(current.right)

    ################### Rebalancing Utilities ######################

    def left_rotate(self, node: Node) -> None:
        """
        if the node is none, return none.
        rotate some part of the tree counter clockwise.
        :param node: the node that's going to rotate counter clockwise
        :return: none
        """
        if node is None:
            return None
        new_tip = node.right
        node.right = new_tip.left
        if new_tip.left is not None:
            new_tip.left.parent = node

        new_tip.parent = node.parent
        if node.parent is None:
            self.root = new_tip
        elif node is node.parent.left:
            node.parent.left = new_tip
        else:
            node.parent.right = new_tip
        new_tip.left = node
        node.parent = new_tip

    def right_rotate(self, node: Node) -> None:
        """
        if node is none, return none.
        rotate some part of the tree clockwise.
        :param node: the node that's going to rotate clockwise
        :return: none
        """
        if node is None:
            return None

        new_tip = node.left
        node.left = new_tip.right
        if new_tip.right is not None:
            new_tip.right.parent = node

        new_tip.parent = node.parent
        if node.parent is None:
            self.root = new_tip
        elif node is node.parent.left:
            node.parent.left = new_tip
        else:
            node.parent.right = new_tip
        new_tip.right = node
        node.parent = new_tip

    def insertion_repair(self, node: Node) -> None:
        """
        after each insertion, we need to check if the tree is balanced or not
        if not, we need to rotate the tree to the right or to the left and change
        some attribute for the node.
        :param node: the node that's being inserted
        :return: none
        """
        if node.parent is None:
            node.is_red = False
            return None
        if node.parent.is_red is False:
            return None
        parents = node.parent
        gp = self.get_grandparent(node)
        unc = self.get_uncle(node)

        if unc is not None and unc.is_red is True:
            unc.is_red = False
            parents.is_red = False
            gp.is_red = True
            self.insertion_repair(gp)
            return None

        if parents is gp.right and node is parents.left:
            self.right_rotate(parents)
            node = parents
            parents = node.parent
        elif parents is gp.left and node is parents.right:
            self.left_rotate(parents)
            node = parents
            parents = node.parent
        gp.is_red = True
        parents.is_red = False
        if node is parents.left:
            self.right_rotate(gp)
        else:
            self.left_rotate(gp)

    def prepare_removal(self, node: Node) -> None:
        """
        check the balance of the tree after remove the node to make sure
        the balance and the connection between node with different other nodes.
        also check the condition of trees and see the node matches which
        remove case and do some changes for other nodes.
        :param node: the node that's going to be removed
        :return: none
        """
        def tree_not_none_and_red(root: Node):
            if root is None:
                return False
            if root.is_red is True:
                return True
            return False

        def tree_null_or_black(root: Node):
            if root is None:
                return True
            if root.is_red is False:
                return True
            return False

        def both_child_black(root: Node):
            if root.left is not None and root.left.is_red is True:
                return False
            if root.right is not None and root.right.is_red is True:
                return False
            return True

        def remove_case1(node: Node):
            if node.is_red is True or node.parent is None:
                return True
            return False

        def remove_case2(node: Node, sibling: Node):
            if sibling.is_red:
                node.parent.is_red = True
                sibling.is_red = False
                if node is node.parent.left:
                    self.left_rotate(node.parent)
                else:
                    self.right_rotate(node.parent)
                return True
            return False

        def remove_case3(node: Node, sibling: Node):
            if node.parent.is_red is False and both_child_black(sibling):
                sibling.is_red = True
                self.prepare_removal(node.parent)
                return True
            return False

        def remove_case4(node: Node, sibling: Node):
            if node.parent.is_red and both_child_black(sibling):
                node.parent.is_red = False
                sibling.is_red = True
                return True
            return False

        def remove_case5(node: Node, sibling: Node):
            if tree_not_none_and_red(sibling.left) and tree_null_or_black(sibling.right):
                if node is node.parent.left:
                    sibling.is_red = True
                    sibling.left.is_red = False
                    self.right_rotate(sibling)
                    return True
            return False

        def remove_case6(node: Node, sibling: Node):
            if tree_null_or_black(sibling.left) and tree_not_none_and_red(sibling.right):
                if node is node.parent.right:
                    sibling.is_red = True
                    sibling.right.is_red = False
                    self.left_rotate(sibling)
                    return True
            return False

        sibling = self.get_sibling(node)
        if remove_case1(node):
            return
        if remove_case2(node, sibling):
            sibling = RBtree.get_sibling(node)
        if remove_case3(node, sibling):
            return
        if remove_case4(node, sibling):
            return
        if remove_case5(node, sibling):
            sibling = self.get_sibling(node)
        if remove_case6(node, sibling):
            sibling = self.get_sibling(node)

        sibling.is_red = node.parent.is_red
        node.parent.is_red = False
        if node is node.parent.left:
            sibling.right.is_red = False
            self.left_rotate(node.parent)
        else:
            sibling.left.is_red = False
            self.right_rotate(node.parent)

    ##################### Insertion and Removal #########################

    def insert(self, node: Node, val: Generic[T]) -> None:
        """
        insert the node to the right place. after finish insert, we call
        insertion repair to repair the tree and the nodes.
        :param node: root first, then call it recursively with node = node.left or node.right
        based on value
        :param val: the value for the new node
        :return: none
        """
        if self.root is None:
            self.root = Node(val)
            self.insertion_repair(self.root)
            self.size += 1
            return
        prev = node
        if val < node.value:
            if node.left is not None:
                self.insert(node.left, val)
            else:
                node.left = Node(val)
                node.left.parent = prev
                self.size += 1
                self.insertion_repair(node.left)
        elif val > node.value:
            if node.right is not None:
                self.insert(node.right, val)
            else:
                node.right = Node(val)
                node.right.parent = prev
                self.size += 1
                self.insertion_repair(node.right)
        else:
            return None

    def remove(self, node: Node, val: Generic[T]) -> None:
        """
        check if the root is none. if it's not, call remove_tree function
        :param node: root
        :param val: the node with the value that's getting removed.
        :return: none
        """
        if node is not None:
            self.remove_tree(node, val)

    def remove_tree(self, node, value) -> None:
        """
        if there's no node with the same value, we return.
        call this function recursively to get the node that's getting removed.
        after finding the node, we call prepare removal with the node we find to
        make sure the tree is not unbalance or not in the right order after remove.
        :param node: root first, predecessor if there's only 2 node left, search if the
        node has 2 children
        :param value: the value that's getting remove
        :return: none
        """
        search = self.search(node, value)
        if search is None:
            return

        if node.left is not None and node.right is None:
            predecessor = node.left
            predecessor_val = predecessor.value
            self.remove_tree(predecessor, predecessor_val)
            node.value = predecessor_val
            return
        if search.right is not None and search.left is not None:
            predecessor = self.predecessor(search)
            predecessor_val = predecessor.value
            self.remove_tree(node, predecessor_val)
            search.value = predecessor_val
            return
        if search.is_red is False:
            self.prepare_removal(search)
        self.bstremove(node, search.value)

    def predecessor(self, node: Node) -> Node:
        """
        get the node with biggest value that's smaller than root.
        :param node: root
        :return: node that's smaller than root but with the biggest value.
        """
        node = node.left
        while node.right is not None:
            node = node.right
        return node

    def bstremove(self, node: Node, val) -> None:
        """
        actually remove the node. we have different conditions. after checking those
        conditions, we do some changes with the tree and finish remove.
        :param node: root first, then the node that's bigger than val but smaller than other node.
        :param val: the value that's getting removed.
        :return: none
        """
        found_node = self.search(node, val)
        if found_node is None or found_node.value != val:
            return
        if found_node.right is None and found_node.left is None:
            previous = found_node.parent
            if previous is None:
                self.root = None
            elif previous.right is not None and previous.right.value == val:
                previous.right = None
            else:
                previous.left = None
            self.size -= 1
            return
        if found_node.right is None or found_node.left is None:
            pre = found_node.parent
            if found_node.right is not None:
                child = found_node.right
            else:
                child = found_node.left
            if pre is None:
                self.root = child
                self.root.is_red = False
            elif pre.right is not None and pre.right.value == val:
                pre.right = child
            else:
                pre.left = child
            child.parent = pre
            self.size -= 1
            return
        min_right = self.min(found_node.right)
        self.bstremove(min_right.value)
        found_node.value = min_right.value

