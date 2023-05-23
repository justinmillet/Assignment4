# Name: Justin Millet
# Osu Email: milletj@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 4, bst and AVL
# Due date: 5/22/2023
# Description: Uses different operations to explore a BST. Including Add, remove, contains, traverse, min, max, empty

import random
from queue_and_stack import Queue, Stack


class BSTNode:
    """
    Binary Search Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new BST node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value  # to store node's data
        self.left = None  # pointer to root of left subtree
        self.right = None  # pointer to root of right subtree

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'BST Node: {}'.format(self.value)


class BST:
    """
    Binary Search Tree class
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize new Binary Search Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._root = None
        # populate BST with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Override string method; display in pre-order
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self._root, values)
        return "BST pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, node: BSTNode, values: []) -> None:
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if not node:
            return
        values.append(str(node.value))
        self._str_helper(node.left, values)
        self._str_helper(node.right, values)

    def get_root(self) -> BSTNode:
        """
        Return root of tree, or None if empty
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._root

    def is_valid_bst(self) -> bool:
        """
        Perform pre-order traversal of the tree.
        Return False if nodes don't adhere to the bst ordering property.
        This is intended to be a troubleshooting method to help find any
        inconsistencies in the tree after the add() or remove() operations.
        A return of True from this method doesn't guarantee that your tree
        is the 'correct' result, just that it satisfies bst ordering.
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
        if node:
            if node.left and node.left.value >= node.value:
                return False
        if node.right and node.right.value < node.value:
            return False
        stack.push(node.right)
        stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #
    def add(self, value: object) -> None:
        """
        Adds a new value to the tree
        """
        node = BSTNode(value)
        x = self._root
        y = None
        while x is not None:
            y = x
            if value < x.value:
                x = x.left
            else:
                x = x.right
        if y is None:
            y = node
            self._root = y
        elif value < y.value:
            y.left = node
        else:
            y.right = node

    def remove(self, value: object) -> bool:
        """
        Removes a node in the tree, the other methods for no child, one child and two child are included here and have
        been removed from the code list.
        """
        if self._root is None:
            return False
        parent = None
        node = self._root
        is_child_left = False
        found = False
        while node is not None and not found:  # searches for the node to be removed
            if value == node.value:
                found = True  # we have found the node and set it to true
            else:
                parent = node  # changes the node to the parent if not found
                if value < node.value:
                    node = node.left
                    is_child_left = True
                else:
                    node = node.right
                    is_child_left = False
        if not found:
            return False
        if node.left is None and node.right is None:  # checks if the node has no children
            if parent is None:
                self._root = None  # sets the root to none if the node is the root
            elif is_child_left:
                parent.left = None  # the node is left child
            else:
                parent.right = None  # node is right child
        elif node.left is None:  # checks if the node has one child
            if parent is None:
                self._root = node.right  # determines the node is the root
            elif is_child_left:
                parent.left = node.right  # determines the node is a left child
            else:
                parent.right = node.right  # determines the node is a left child
        elif node.right is None:
            if parent is None:
                self._root = node.left
            elif is_child_left:
                parent.left = node.left
            else:
                parent.right = node.left
        else:  # checks if the node has two children
            successor_parent = node  # changes the previous parent variable
            successor = node.right
            while successor.left is not None:  # searches for the left most node
                successor_parent = successor
                successor = successor.left
            if successor_parent != node:
                successor_parent.left = successor.right  # updates the left child to the right
                successor.right = node.right  # assigns the subtree of the node to the right
            if parent is None:
                self._root = successor
            elif is_child_left:
                parent.left = successor
            else:
                parent.right = successor
            successor.left = node.left
        return True

    def contains(self, value: object) -> bool:
        """
        Determines whether a node is contained within the tree
        """
        if self._root is None:
            return False
        stack = [self._root]  # creates a new stack for the root node
        while stack:
            node = stack.pop()  # pops a node from the stack using the pop() function
            if node.value == value:  # checks if the node value matches
                return True
            if node.left is not None and value < node.value:  # checks if value is less than the target, checks left
                # tree
                stack.append(node.left)
            if node.right is not None and value > node.value:  # checks if value is greater than the target, checks
                # right tree
                stack.append(node.right)
        return False  # returns false if the value is not found

    def inorder_traversal(self) -> Queue:
        """
        Returns a tree in order from smallest to largest value
        """
        if self._root is None:
            return Queue()   # returns empty if tree is empty
        traversal_queue = Queue()  # creates queue to store values
        stack = []  # creates empty stack
        current = self._root  # starts at root node
        while True:
            if current is not None:
                stack.append(current)  # adds current node to the stack
                current = current.left  # moves to the left
            elif stack:
                current = stack.pop()  # pops a node from the stack
                traversal_queue.enqueue(current.value)  # enqueue the value of the node
                current = current.right  # moves to the right
            else:
                break
        return traversal_queue  # returns the previous empty queue with the new queue

    def find_min(self) -> object:
        """
        Finds the minimum value in a tree
        """
        if self._root is None:
            return None
        current = self._root
        while current.left is not None:
            current = current.left  # traverses to the left most node
        return current.value  # returns the value

    def find_max(self) -> object:
        """
        Finds the max value in a tree
        """
        if self._root is None:
            return None
        current = self._root
        while current.right is not None:
            current = current.right  # traverses to the right most node
        return current.value  # returns the value

    def is_empty(self) -> bool:
        """
        Returns true if the tree is empty, false if it has nodes
        """
        return self._root is None

    def make_empty(self) -> None:
        """
        Removes all nodes from the tree
        """
        self._root = None
