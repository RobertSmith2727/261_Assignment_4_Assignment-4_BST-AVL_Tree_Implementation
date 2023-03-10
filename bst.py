# Name: Robert Smith
# OSU Email: Smithro8@oregonstate.edu
# Course:       CS261 - Data Structures
# Assignment: 4
# Due Date: 02/27/2023
# Description: Creates a BST Tree with add, remove, min/max, contains, is empty and make empty methods

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
        Adds a passed value to a BST
        Creates tree if empty
        """
        parent = None
        node = self._root
        # if empty
        if self._root is None:
            self._root = BSTNode(value)
            return
        # iterates to end node
        while node is not None:
            parent = node
            if value < node.value:
                node = node.left
            else:
                node = node.right
        # assigns proper node
        if value < parent.value:
            parent.left = BSTNode(value)
        else:
            parent.right = BSTNode(value)

    def remove(self, value: object) -> bool:
        """
        Removes a passed value and returns ture if removed
        Else returns false
        """
        # if empty
        if self._root is None:
            return False
        # calls find remove node and parent
        remove_node, remove_parent = self.find_remove_node(value)
        # if value not found in tree
        if remove_node is None:
            return False
        # no children
        if remove_node.left is None and remove_node.right is None:
            self._remove_no_subtrees(remove_parent, remove_node)
            return True
        # one subtree
        if remove_node.left is not None and remove_node.right is None or \
                remove_node.left is None and remove_node.right is not None:
            self._remove_one_subtree(remove_parent, remove_node)
            return True
        # two subtrees
        if remove_node.left is not None and remove_node.right is not None:
            self._remove_two_subtrees(remove_parent, remove_node)
            return True
        else:
            return False

    def find_remove_node(self, value):
        """
        Returns the node to be removed and its parent
        """
        # if root
        if self._root.value == value:
            return self._root, None
        node = self._root
        remove_node = None
        remove_parent = None
        while node is not None:
            # finds node to be removed
            if node.value == value:
                remove_node = node
                break
            # finds parent of node to be removed
            if node.right is not None:
                if node.right.value == value:
                    remove_parent = node
            if node.left is not None:
                if node.left.value == value:
                    remove_parent = node
            # iterates to value
            if value < node.value:
                node = node.left
            else:
                node = node.right
        return remove_node, remove_parent

    def _remove_no_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        Removes passed node with no subtrees
        """
        # assigns none to parent pointing to node being removed
        if remove_parent is None:
            self._root = None
            return
        # deletes node by making it None
        if remove_parent.left is remove_node:
            remove_parent.left = None
        if remove_parent.right is remove_node:
            remove_parent.right = None
        return

    def _remove_one_subtree(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        Removes passed node with one subtree
        Reassigns subtree to proper parent
        """
        # if root
        if remove_parent is None:
            # sets r/l node to new root
            if self._root.left is None and self._root.right is not None:
                self._root = self._root.right
                return

            if self._root.left is not None and self._root.right is None:
                self._root = self._root.left
            return

        # sets node to parent pointer
        if remove_node.left is None:
            if remove_parent.value > remove_node.value:
                remove_parent.left = remove_node.right
                if remove_node.left is not None:
                    remove_node.left.parent = remove_node
            else:
                remove_parent.right = remove_node.right
                if remove_node.right is not None:
                    remove_node.right.parent = remove_node

        if remove_node.right is None:
            if remove_parent.value > remove_node.value:
                remove_parent.left = remove_node.left
            else:
                remove_parent.right = remove_node.left

        return

    def _remove_two_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        Removes node that has two subtrees
        Reassigns subtrees to proper parent
        """

        # calls finds successor and parent
        successor, successor_parent = self.find_successor(remove_node)

        # if root
        if self._root == remove_node:
            # if root successor is roots right node
            if self._root.right == successor:
                self._root.value = successor.value
                self._root.right = successor.right
                return
            if self._root.right != successor:
                self._root.value = successor.value
                successor_parent.left = successor.right
                successor.right = None
            return
        # assigns remove left to successor left
        successor.left = remove_node.left
        if successor != remove_node.right:
            # replaces successor with its right
            successor_parent.left = successor.right
            successor.right = remove_node.right
        # assigns successor to proper parent node
        if remove_parent.value < successor.value:
            remove_parent.right = successor
        else:
            remove_parent.left = successor
        return

    def find_successor(self, remove_node: BSTNode):
        """
        Returns the successor and it parent
        """
        node = remove_node
        successor = None
        successor_parent = None
        node = node.right

        # iterates to successor
        while node is not None:
            successor = node
            node = node.left
        temp_node = remove_node.right
        # iterates to successor parent
        while temp_node != successor:
            successor_parent = temp_node
            temp_node = temp_node.left
        return successor, successor_parent

    def contains(self, value: object) -> bool:
        """
        Returns true if BST has value in it
        Else returns false
        """
        # if empty
        if self._root is None:
            return False

        # finds val if in tree
        node = self._root
        while node is not None:
            if node.value == value:
                return True
            if value < node.value:
                node = node.left
            else:
                node = node.right
        return False

    def inorder_traversal(self) -> Queue:
        """
        Returns an in order queue of BST
        Calls helper method
        """
        ordered_queue = Queue()
        node = self._root
        self.rec_inorder_traversal(node, ordered_queue)
        return ordered_queue

    def rec_inorder_traversal(self, node, queue):
        """
        Recursion helper method
        Recursively traverses left then right
        """
        if node is not None:
            self.rec_inorder_traversal(node.left, queue)
            queue.enqueue(node.value)
            self.rec_inorder_traversal(node.right, queue)
        return

    def find_min(self) -> object:
        """
        Returns the min value of the BST
        """
        # if empty
        if self._root is None:
            return None

        # if root is min
        node = self._root
        if node.left is None:
            return node.value
        # iterate to far left(min)
        while node is not None:
            min_node = node
            node = node.left
        return min_node.value

    def find_max(self) -> object:
        """
        Returns the max value of the BST
        """
        # if empty
        if self._root is None:
            return None
        # if root is max
        node = self._root
        if node.right is None:
            return node.value
        # iterate far right(max)
        while node is not None:
            max_node = node
            node = node.right
        return max_node.value

    def is_empty(self) -> bool:
        """
        Returns true if BST is empty
        Else returns false
        """
        if self._root == None:
            return True
        return False

    def make_empty(self) -> None:
        """
        Makes BST empty
        """
        self._root = None


# ------------------- BASIC TESTING -----------------------------------------
if __name__ == '__main__':
    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),
        (3, 2, 1),
        (1, 3, 2),
        (3, 1, 2),
    )
    for case in test_cases:
        tree = BST(case)
        print(tree)
    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),
        (10, 20, 30, 50, 40),
        (30, 20, 10, 5, 1),
        (30, 20, 10, 1, 5),
        (5, 4, 6, 3, 7, 2, 8),
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = BST(case)
        print('INPUT  :', case)
        print('RESULT :', tree)
    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = BST()
        for value in case:
            tree.add(value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')
    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((-9, -19, -12, -19, -12, -5, -7, -9, -8, -9, 19, 11, 10, -5, -3, -5, -3, 13, 13, 15, 14, 16, 17), -3),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)
    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)
    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = BST(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)
    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = BST(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)
    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = BST([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))
    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = BST()
    print(tree.contains(0))
    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())
    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())
    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())
    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())
    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())
    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())
    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())
    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree is empty:", tree.is_empty())
    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
