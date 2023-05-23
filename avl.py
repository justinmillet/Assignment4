# Name: Justin Millet
# OSU Email: milletj@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 4- Bst and AVL
# Due Date: 5/22/2023
# Description: Implement AVL tree and add or remove nodes from the tree

import random
from queue_and_stack import Queue, Stack
from bst import BSTNode, BST


class AVLNode(BSTNode):
    """
    AVL Tree Node class. Inherits from BSTNode
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(value)
        # new variables needed for AVL
        self.parent = None
        self.height = 0

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'AVL Node: {}'.format(self.value)


class AVL(BST):
    """
    AVL Tree class. Inherits from BST
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(start_tree)

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        super()._str_helper(self._root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.
        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                # check for correct height (relative to children)
                left = node.left.height if node.left else -1
                right = node.right.height if node.right else -1
                if node.height != 1 + max(left, right):
                    return False
                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                    else:
                        # NULL parent is only allowed on the root of the tree
                        if node != self._root:
                            return False
                    stack.push(node.right)
                    stack.push(node.left)
        return True

    def add(self, value: object) -> None:
        """
        Add a new node to an AVL tree
        """
        new_node = AVLNode(value)
        if self._root is None:  # determines if the tree is empty
            self._root = new_node  # sets new node to the root
        else:
            parent = None
            current = self._root
            while current:
                if value < current.value:
                    parent = current
                    current = current.left  # determines the value is less than the current nodes value, so goes left in
                    # the tree
                elif value > current.value:
                    parent = current
                    current = current.right  # determines the value is greater than the current nodes value, so goes
                    # right in the tree
                else:
                    return  # no change since the node exists in tree
            new_node.parent = parent  # Insert new node
            if value < parent.value:
                parent.left = new_node  # inserts as left child if the value is less than the parent value
            else:
                parent.right = new_node  # inserts as right child if value is greater than parent value
            self._update_height(new_node)
            self._rebalance(new_node)

    def remove(self, value: object) -> bool:
        """
        Removes a node from an AVLTree
        """
        if self._root is None:
            return False  # returns false if the tree is empty

        node = self._root  # finds the node for removal
        parent = None
        while node:
            if value == node.value:
                break  # breaks the loop once the node is found
            parent = node  # sets the parent value to the node
            if value < node.value:
                node = node.left  # determines the value is less than the parent value, goes left in tree
            else:
                node = node.right  # determines the value is greater than the parent value, goes right
        else:
            return False  # Node not found
        if node.left is None and node.right is None:
            if parent is None:
                self._root = None  # determines the node is the root
            elif parent.left == node:  # determines the node is the left child to the parent
                parent.left = None
            else:
                parent.right = None  # determines the node is the right child
        elif node.left is None or node.right is None:
            if parent is None:
                if node.left:
                    self._root = node.left
                else:
                    self._root = node.right
            elif parent.left == node:
                if node.left:
                    parent.left = node.left
                else:
                    parent.left = node.right
            else:
                if node.left:
                    parent.right = node.left
                else:
                    parent.right = node.right
        else:  # used when there are to child nodes to be removed
            successor_parent = node
            successor = node.right
            while successor.left:
                successor_parent = successor
                successor = successor.left
            node.value = successor.value  # replaces value with successor value
            if successor_parent.left == successor:  # update left
                if successor.right:
                    successor_parent.left = successor.right
                else:
                    successor_parent.left = None
            else:
                if successor.right:  # update right
                    successor_parent.right = successor.right
                else:
                    successor_parent.right = None

        # Update heights and perform AVL rotations
        self._update_height(parent)
        self._rebalance(parent)

        return True

    def _update_height(self, node: AVLNode) -> None:
        while node:
            node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
            node = node.parent

    def _rebalance(self, node: AVLNode) -> None:
        while node:
            balance = self._get_balance(node)
            if balance > 1:  # determines if the left subtree is taller than the right
                if self._get_balance(node.left) < 0:
                    self._rotate_left(node.left)  # left to right rotation
                self._rotate_right(node)  # left to left rotation
            elif balance < -1:  # right subtree is taller than left
                if self._get_balance(node.right) > 0:
                    self._rotate_right(node.right)  # right to left rotation
                self._rotate_left(node)  # right to right rotation
            node = node.parent

    def _get_height(self, node: AVLNode) -> int:
        if node is None:
            return -1
        return node.height

    def _get_balance(self, node: AVLNode) -> int:
        return self._get_height(node.left) - self._get_height(node.right)

    def _rotate_left(self, node: AVLNode) -> None:
        pivot = node.right  # set pivot point as right child of current node
        node.right = pivot.left  # pivot left subtree at pivot point
        if pivot.left:
            pivot.left.parent = node  # updates left parent subtree
        pivot.parent = node.parent  # update parent
        if node.parent is None:
            self._root = pivot
        elif node == node.parent.left:
            node.parent.left = pivot  # if node is left child it updates the left childs nodes parent
        else:
            node.parent.right = pivot  # if node is right it updates the right childs nodes parent
        pivot.left = node  # moves node to the left of pivot
        node.parent = pivot  # update parent node
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))  # updates the heights of
        # the nodes and pivots
        pivot.height = 1 + max(self._get_height(pivot.left), self._get_height(pivot.right))

    def _rotate_right(self, node: AVLNode) -> None:
        pivot = node.left  # set pivot point as left child of current node
        node.left = pivot.right  # pivot right subtree at point
        if pivot.right:
            pivot.right.parent = node  # updates right parent subtree
        pivot.parent = node.parent
        if node.parent is None:
            self._root = pivot
        elif node == node.parent.left:
            node.parent.left = pivot  # if node is left child it updates the left child nodes parent
        else:
            node.parent.right = pivot  # if node is right child it updates the right child nodes parent
        pivot.right = node  # moves node to the right of the pivot
        node.parent = pivot  # updates parent node
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        pivot.height = 1 + max(self._get_height(pivot.left), self._get_height(pivot.right))
