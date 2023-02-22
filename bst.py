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

        # # --------------------root case-----------------------------
        # # if value is root
        # if self._root.value == value:
        #
        #     # one child
        #     if self._root.left is None and self._root.right is not None:
        #         self._root = self._root.right
        #         return True
        #     if self._root.left is not None and self._root.right is None:
        #         self._root = self._root.left
        #         return True
        #
        #     # finds root successor
        #     node = self._root.right
        #     root_successor = None
        #     while node is not None:
        #         root_successor = node
        #         node = node.left
        #
        #     if root_successor is None:
        #         root_successor = self._root.left
        #
        #     # finds root successor parent
        #     node = self._root.right
        #     root_successor_parent = self._root
        #     while node is not None:
        #         # finds roots successor parent
        #         if node.right == root_successor:
        #             root_successor_parent = node
        #         if node.left == root_successor:
        #             root_successor_parent = node
        #         node = node.left
        #
        #     # if root successor is roots right node
        #     if self._root.right == root_successor:
        #         self._root.value = root_successor.value
        #         self._root.right = root_successor.right
        #         return True
        #     else:
        #         self._root.value = root_successor.value
        #         root_successor_parent.left = root_successor.right
        #         root_successor.right = None
        #         return True
        #     # --------------------end root case-----------------------------
        #
        #
        else:
            return False

    # Consider implementing methods that handle different removal scenarios; #
    # you may find that you're able to use some of them in the AVL.          #
    # Remove these comments.                                                 #
    # Remove these method stubs if you decide not to use them.               #
    # Change these methods in any way you'd like.                            #

    def find_remove_node(self, value):

        if self._root.value == value:
            return self._root, None
        node = self._root
        remove_node = None
        remove_parent = None
        while node is not None:
            # finds parent of node to be removed
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
        return remove_node, remove_parent


    def _remove_no_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        TODO: Write your implementation
        """
        # remove node that has no subtrees (no left or right nodes)

        if remove_parent is None:
            self._root = None
            return
        if remove_parent.left is remove_node:
            remove_parent.left = None
            remove_node.value = None

        if remove_parent.right is remove_node:
            remove_parent.right = None
            remove_node.value = None
        return

        # if remove_parent.value > remove_node.value:
        #     remove_parent.left = None
        #     return
        # else:
        #     remove_parent.right = None
        #     return

    def _remove_one_subtree(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        TODO: Write your implementation
        """
        # remove node that has a left or right subtree (only)
        if remove_parent is None:
            if self._root.left is None and self._root.right is not None:
                self._root = self._root.right
                return

            if self._root.left is not None and self._root.right is None:
                self._root = self._root.left
            return

        if remove_node.left is None:
            if remove_parent.value > remove_node.value:
                remove_parent.left = remove_node.right
            else:
                remove_parent.right = remove_node.right

        if remove_node.right is None:
            if remove_parent.value > remove_node.value:
                remove_parent.left = remove_node.left
            else:
                remove_parent.right = remove_node.left
        return

    def _remove_two_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        removes node that has two subtrees
        """

        # finds successor and parent
        successor, successor_parent = self.find_successor(remove_node)

        # if root successor is roots right node
        if self._root == remove_node:
            if self._root.right == successor:
                self._root.value = successor.value
                self._root.right = successor.right
                return
            if self._root.right != successor:
                self._root.value = successor.value
                successor_parent.left = successor.right
                successor.right = None
            return

        successor.left = remove_node.left
        if successor != remove_node.right:
            successor_parent.left = successor.right
            successor.right = remove_node.right
        if remove_parent.value < successor.value:
            remove_parent.right = successor
        else:
            remove_parent.left = successor
        return

    def find_successor(self, remove_node: BSTNode):
        """
        TODO
        """
        node = remove_node
        successor = None
        successor_parent = None
        node = node.right

        # iterates to successor
        while node is not None:
            successor = node
            # # finds successor parent
            # if previous_node.right == successor:
            #     successor_parent = node
            # if previous_node.left == successor:
            #     successor_parent = node
            node = node.left
        temp_node = remove_node.right
        while temp_node != successor:
            successor_parent = temp_node
            temp_node = temp_node.left

        return successor, successor_parent

    def contains(self, value: object) -> bool:
        """
        TODO: Write your implementation
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
        TODO: Write your implementation
        """
        pass
    #     ordered_queue = Queue()
    #     node = self._root
    #     previous_node = node
    #     self.rec_inorder_traversal(node, previous_node, ordered_queue)
    #
    # def rec_inorder_traversal(self, node, previous_node, queue):
    #     if node is None:
    #         ordered_queue.enqueue(previous_node)
    #     node = node.left

    def find_min(self) -> object:
        """
        TODO: Write your implementation
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
        TODO: Write your implementation
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
        TODO: Write your implementation
        """
        if self._root == None:
            return True
        return False

    def make_empty(self) -> None:
        """
        TODO: Write your implementation
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
    #((33, -58, -54, 77, 46, -17, 49, -47, -43, 25), 33),
        # ((46, -58, -54, -17, -47, -43, 25, 77, 49 ), -54),
        # ((46, -58, -17, -47, -43, 25, 77, 49 ), 46),
    print("-------------------------------")
    test_cases = (
        (( 49, -58, -17, -47, -43, 25, 77 ), 49),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),
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


    # print("\nPDF - method remove() example 1")
    # list_1 = [68, -21, 44, 19, -45, 53, 55, -98, -97]
    #
    # tree = BST(list_1)
    # print(tree)
    # tree.remove(55)
    # print(tree, "two", 55)
    # tree.remove(-98)
    # print(tree, "one", -98)
    # tree.remove(-97)
    # print(tree, "zero", -97)
    #
    # list_2 = [20, 19, 18, 17, 16]
    # tree = BST(list_2)
    # print(tree)
    # tree.remove(20)
    # print(tree, "root, left heavy", 20)
    #
    # list_4 = [1, 2, 3, 4, 5, 6, 7]
    # tree = BST(list_4)
    # print(tree)
    # tree.remove(1)
    # print(tree, "root, right heavy", 1)
    #
    # list_3 = [32, 69, -26, 71, 72, 9, 81, 54, 59, 94]
    # tree = BST(list_3)
    # print(tree)
    # tree.remove(32)
    # print(tree, "root, both sides", 32)
    #
    # print("-------------------------------")
    # # ((98, -29, -55, -87, -18, 48, -44, -12, -4, 31), 98),
    # # ((-29, -55, -87, -44, -18, 48, -12, -4, 31), -55),
    # # ((68, -21, 44, 19, -45, 53, 55, -98, -97), 68),
    # # ((68, -21, 44, 19, -45, 53, 55, -98, -97), 68),
    # # ((98, -90, 92, 52, 87, 57, -39, -67, -2, 31), 98),
    # # ((32, 69, -26, 71, 72, 9, 81, 54, 59, 94), 32),
    # # ((32, 69, -26, 71, 72, 9, 81, 54, 59, 94), 71),
    # # ((1, 2, 3, 4), 2),
    # # ((1, 2, 3), 3),
    # # ((26, 58, 42, 12, -45, -12, 22, -70, -36), - 70),
    # # ((3, 37, 6, 40, -83, -66, 85, 25, -4, 30), 3),
    # # ((6, -83, -66, -4, 37, 25, 30, 40, 85), 6),
    # # ((25, -83, -66, -21, 37, 30, 40, 85), -83),
    # # ((64, 100, -59, -22, -17, 54, 24, 26, -5, -33), 64),
    # # ((50, 40, 60, 30, 70, 20, 80, 45), 0),
    # # ((50, 40, 60, 30, 70, 20, 80, 45), 45),
    # # ((50, 40, 60, 30, 70, 20, 80, 45), 40),
    # # ((50, 40, 60, 30, 70, 20, 80, 45), 20),
    # # ((50, 40, 60, 30, 70, 20, 80, 45), 0),
    # # ((50, 40, 60, 30, 70, 20, 80, 45), 45),
