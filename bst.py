# Name: Robert Smith
# OSU Email: Smithro8@oregonstate.edu
# Course:       CS261 - Data Structures
# Assignment: 4
# Due Date: 02/27/2023
# Description:

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
        TODO: Write your implementation, empty, root no children
        """
        # parent = None
        # successor = None
        # node = self._root
        # # if tree just a root
        # if node.left is None and node.right is None:
        #     self._root = None
        #     return True
        # # if value is root
        # if node.value == value:
        #     suc_right = node.right
        #     suc_left = node.left
        #     if node.right is not None:
        #         node = node.right
        #     while node is not None:
        #         successor = node
        #         node = node.left
        #     node = suc_right
        #     parent_node = node
        #     if node.left is not None:
        #         while node.left != successor:
        #             parent_node = node
        #             if value < node.value:
        #                 node = node.left
        #             else:
        #                 node = node.right
        #     parent_node.left = successor.right
        #     self._root.value = successor.value
        #     self._root.left = suc_left
        #     self._root.right = suc_right
        #     return True
        #
        # # finds if value is in tree
        # found_value = None
        # while node is not None:
        #     if node.value == value:
        #         found_value = value
        #     if value < node.value:
        #         node = node.left
        #     else:
        #         node = node.right
        # # if value not found in tree
        # if found_value is None:
        #     return False
        #
        # node = self._root
        # # find parent node of node being removed
        # while node.value != value:
        #     parent = node
        #     if value < node.value:
        #         node = node.left
        #     else:
        #         node = node.right
        # remove_node = node
        # # find successor
        # node = node.right
        # while node is not None:
        #     successor = node
        #     node = node.left
        # # if successor none make left node successor
        # if successor is None:
        #     successor = remove_node.left
        #     # if successor still none (leaf)
        #     if successor is None:
        #         # deletes leaf
        #         if parent.value > value:
        #             parent.left = None
        #         else:
        #             parent.right = None
        #         return True
        #     # assign successor (left node) to parent
        #     if successor.value < parent.value:
        #         parent.left = successor
        #     else:
        #         parent.right = successor
        #     return True
        # # assign successor (right node) to parent
        # if successor.value > parent.value:
        #     parent.right = successor
        # else:
        #     parent.left = successor
        #     successor.left = remove_node.left
        # return True
        remove_parent = None
        successor = None
        node = self._root

        # finds root successor
        node = node.right
        root_successor = None
        while node is not None:
            root_successor = node
            node = node.left

        # check if val in tree, get successor and remove node's parent
        node = self._root
        remove_node = None
        root_successor_parent = None
        remove_parent = None
        while node is not None:
            # finds roots successor parent
            if node.right == root_successor:
                root_successor_parent = node
            if node.left == root_successor:
                root_successor_parent = node

            # finds parent of node to be removed for root
            if self._root.value == value:
                if node.right == value:
                    remove_parent = node
                if node.left == value:
                    remove_parent = node
            # finds parent of node to be removed for non root
            if self._root.value != value:
                if node.right is not None:
                    if node.right.value == value:
                        remove_parent = node
                if node.left is not None:
                    if node.left.value == value:
                        remove_parent = node
            # finds node to be removed
            if node.value == value:
                remove_node = node
            if value < node.value:
                node = node.left
            else:
                node = node.right
        # if value not found in tree
        if remove_node is None:
            return False

        node = self._root
        # if tree just a root
        if node.left is None and node.right is None:
            self._root = None
            return True
        # if value is root
        if node.value == value:
            # if root successor is roots right node
            if self._root.right == root_successor:
                self._root.value = root_successor.value
                self._root.right = root_successor.right
                self._root.left = root_successor.left
                return True
            else:
                self._root.value = root_successor.value
                root_successor_parent.left = root_successor.right
                root_successor.right = None
                return True

        # finds successor and parent
        node = remove_node
        successor_parent = node
        node = node.right
        while node is not None:
            successor = node
            # finds successor parent
            if node.right == successor:
                successor_parent = node
            if node.left == successor:
                successor_parent = node
            node = node.left

        if successor is None:
            successor = remove_node.left
            # if successor still none (leaf)
            if successor is None:
                # deletes leaf
                if remove_parent.value > value:
                    remove_parent.left = None
                else:
                    remove_parent.right = None
                return True
            # assign successor (left node) to parent
            if successor.value < remove_parent.value:
                remove_parent.left = successor
            else:
                remove_parent.right = successor
            return True
        # assign successor (right node) to parent
        if successor.value > remove_parent.value:
            remove_parent.right = successor
        else:
            remove_parent.left = successor
            successor.left = remove_node.left
        return True



    # Consider implementing methods that handle different removal scenarios; #
    # you may find that you're able to use some of them in the AVL.          #
    # Remove these comments.                                                 #
    # Remove these method stubs if you decide not to use them.               #
    # Change these methods in any way you'd like.                            #
    def _remove_no_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        TODO: Write your implementation
        """
        # remove node that has no subtrees (no left or right nodes)
        pass

    def _remove_one_subtree(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        TODO: Write your implementation
        """
        # remove node that has a left or right subtree (only)
        pass

    def _remove_two_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        TODO: Write your implementation
        """
        # remove node that has two subtrees
        # need to find inorder successor and its parent (make a method!)
        pass

    def contains(self, value: object) -> bool:
        """
        TODO: Write your implementation
        """
        pass

    def inorder_traversal(self) -> Queue:
        """
        TODO: Write your implementation
        """
        pass

    def find_min(self) -> object:
        """
        TODO: Write your implementation
        """
        pass

    def find_max(self) -> object:
        """
        TODO: Write your implementation
        """
        pass

    def is_empty(self) -> bool:
        """
        TODO: Write your implementation
        """
        pass

    def make_empty(self) -> None:
        """
        TODO: Write your implementation
        """
        pass


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
        ((32, 69, -26, 71, 72, 9, 81, 54, 59, 94), 32),
        ((32, 69, -26, 71, 72, 9, 81, 54, 59, 94), 71),
        ((1, 2, 3, 4), 2),
        ((1, 2, 3), 3),
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)
    # print("\nPDF - method remove() example 2")
    # print("-------------------------------")
    # test_cases = (
    #     ((50, 40, 60, 30, 70, 20, 80, 45), 20),
    #     ((50, 40, 60, 30, 70, 20, 80, 15), 40),
    #     ((50, 40, 60, 30, 70, 20, 80, 35), 20),
    #     ((50, 40, 60, 30, 70, 20, 80, 25), 40),
    # )
    # for case, del_value in test_cases:
    #     tree = BST(case)
    #     print('INPUT  :', tree, "DEL:", del_value)
    #     tree.remove(del_value)
    #     print('RESULT :', tree)
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
