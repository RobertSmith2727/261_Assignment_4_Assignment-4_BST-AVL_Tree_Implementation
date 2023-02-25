# Name: Robert Smith
# OSU Email: Smithro8@oregonstate.edu
# Course:       CS261 - Data Structures
# Assignment: 4
# Due Date: 02/27/2023
# Description:

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
                    print("height")
                    return False
                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        print("p/c pointers")
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self._root:
                        print("null parent")
                        return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #
    def add(self, value: object) -> None:
        """
        TODO: Write your implementation
        """

        # if empty
        if self._root is None:
            self._root = AVLNode(value)
            return
        # if repeat value
        if value == self._root.value:
            return
        # iterates to end node
        node = self._root
        while node is not None:
            parent_node = node
            if value == node.value:
                return
            if value < node.value:
                node = node.left
            else:
                node = node.right
        # assigns proper node and parent
        if value < parent_node.value:
            parent_node.left = AVLNode(value)
            parent_node.left.parent = parent_node
        if value > parent_node.value:
            parent_node.right = AVLNode(value)
            parent_node.right.parent = parent_node
        while parent_node is not None:
            self._rebalance(parent_node)
            parent_node = parent_node.parent


    def remove(self, value: object) -> bool:
        """
        TODO: Write your implementation
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
            self._remove_rebalance(remove_node)
            print(self.is_valid_avl())
            return True
        # one subtree
        if remove_node.left is not None and remove_node.right is None or \
                remove_node.left is None and remove_node.right is not None:
            self._remove_one_subtree(remove_parent, remove_node)
            if remove_node.right is not None:
                remove_node.right.parent = remove_parent
            else:
                remove_node.left.parent = remove_parent
            self._remove_rebalance(remove_parent)
            print(self.is_valid_avl())
            return True
        # two subtrees
        if remove_node.left is not None and remove_node.right is not None:
            successor_parent = self._remove_two_subtrees(remove_parent, remove_node)
            self._remove_rebalance(successor_parent)
            print(self.is_valid_avl())
            return True
        else:
            return False

    # Experiment and see if you can use the optional                         #
    # subtree removal methods defined in the BST here in the AVL.            #
    # Call normally using self -> self._remove_no_subtrees(parent, node)     #
    # You need to override the _remove_two_subtrees() method in any case.    #
    # Remove these comments.                                                 #
    # Remove these method stubs if you decide not to use them.               #
    # Change this method in any way you'd like.                              #
    def _remove_two_subtrees(self, remove_parent: AVLNode, remove_node: AVLNode) -> AVLNode:
        """
        TODO: Write your implementation
        """
        # calls finds successor and parent
        successor, successor_parent = self.find_successor(remove_node)
        if successor_parent is None:
            successor_parent = successor
        # if root
        if self._root == remove_node:
            # if root successor is roots right node
            if self._root.right == successor:
                self._root.value = successor.value
                self._root.right = successor.right
                return successor_parent
            if self._root.right != successor:
                self._root.value = successor.value
                successor_parent.left = successor.right
                if successor.right is not None:
                    successor.right.parent = successor_parent
                successor.right = None
            return successor_parent
        # assigns remove left to successor left
        successor.left = remove_node.left
        successor.left.parent = successor
        if successor != remove_node.right:
            # replaces successor with its right
            successor_parent.left = successor.right
            if successor.right is not None:
                successor.right.parent = successor_parent
            successor.right = remove_node.right
            remove_node.right.parent = successor
            if successor_parent.parent == remove_node:
                successor_parent.parent = successor
            successor.parent = remove_parent.parent
        # assigns successor to proper parent node
        if remove_parent.value < successor.value:
            remove_parent.right = successor
            successor.parent = remove_parent
        else:
            remove_parent.left = successor
            successor.parent = remove_parent
        return successor_parent


    def _remove_rebalance(self, parent_node: AVLNode):
        while parent_node is not None:
            self._rebalance(parent_node)
            parent_node = parent_node.parent

    # It's highly recommended to implement                          #
    # the following methods for balancing the AVL Tree.             #
    # Remove these comments.                                        #
    # Remove these method stubs if you decide not to use them.      #
    # Change these methods in any way you'd like.                   #
    def _balance_factor(self, node: AVLNode) -> int:
        """
        TODO: Write your implementation
        """
        return self._get_height(node.right) - self._get_height(node.left)

    def _get_height(self, node: AVLNode) -> int:
        """
        TODO: Write your implementation
        """
        if node is None:
            return -1
        left_height = self._get_height(node.left)
        right_height = self._get_height(node.right)
        return max(left_height, right_height) + 1

    def _rotate_left(self, node: AVLNode) -> AVLNode:
        """
        TODO: Write your implementation
        """
        child = node.right
        node.right = child.left
        if node.right is not None:
            node.right.parent = node
        child.left = node
        node.parent = child
        self._update_height(node)
        self._update_height(child)
        return child

    def _rotate_right(self, node: AVLNode) -> AVLNode:
        """
        TODO: Write your implementation
        """
        child = node.left
        node.left = child.right
        if node.left is not None:
            node.left.parent = node
        child.right = node
        node.parent = child
        self._update_height(node)
        self._update_height(child)
        return child

    def _update_height(self, node: AVLNode) -> None:
        """
        TODO: Write your implementation
        """

        # sets height up to root
        node.height = max(self._get_height(node.left), self._get_height(node.right)) + 1

    def _rebalance(self, node: AVLNode) -> None:
        """
        TODO: Write your implementation
        """
        balance_f = self._balance_factor(node)
        if self._balance_factor(node) < -1:
            if self._balance_factor(node.left) > 0:
                node.left = self._rotate_left(node.left)
                node.left.parent = node
            previous_node_parent = node.parent
            new_subtree_root = self._rotate_right(node)
            new_subtree_root.parent = previous_node_parent
            if previous_node_parent is None:
                self._root = new_subtree_root
                return
            if previous_node_parent.value > new_subtree_root.value:
                previous_node_parent.left = new_subtree_root
            else:
                previous_node_parent.right = new_subtree_root
        elif self._balance_factor(node) > 1:
            if self._balance_factor(node.right) < 0:
                node.right = self._rotate_right(node.right)
                node.right.parent = node
            previous_node_parent = node.parent
            new_subtree_root = self._rotate_left(node)
            new_subtree_root.parent = previous_node_parent
            if previous_node_parent is None:
                self._root = new_subtree_root
                return
            if previous_node_parent.value > new_subtree_root.value:
                previous_node_parent.left = new_subtree_root
            else:
                previous_node_parent.right = new_subtree_root
        else:
            self._update_height(node)

# ------------------- BASIC TESTING -----------------------------------------
if __name__ == '__main__':
    # print("\nPDF - method add() example 1")
    # # -27, -77, -97, -54, 26, 23, 15, 75, 60, 88  right answer
    # print("----------------------------")
    # test_cases = (
    #     (1,2,3),  # RR
    #     (3, 2, 1),  # LL
    #     (1, 3, 2),  # RL
    #     (3, 1, 2),  # LR
    # )
    # for case in test_cases:
    #     tree = AVL(case)
    #     print(tree)
    # print("\nPDF - method add() example 2")
    # print("----------------------------")
    # test_cases = (
    #     (10, 20, 30, 40, 50),  # RR, RR
    #     (10, 20, 30, 50, 40),  # RR, RL
    #     (30, 20, 10, 5, 1),  # LL, LL
    #     (30, 20, 10, 1, 5),  # LL, LR
    #     (5, 4, 6, 3, 7, 2, 8),  # LL, RR
    #     (range(0, 30, 3)),
    #     (range(0, 31, 3)),
    #     (range(0, 34, 3)),
    #     (range(10, -10, -2)),
    #     ('A', 'B', 'C', 'D', 'E'),
    #     (1, 1, 1, 1),
    # )
    # for case in test_cases:
    #     tree = AVL(case)
    #     print('INPUT  :', case)
    #     print('RESULT :', tree)
    # print("\nPDF - method add() example 3")
    # print("----------------------------")
    # for _ in range(100):
    #     case = list(set(random.randrange(1, 20000) for _ in range(900)))
    #     tree = AVL()
    #     for value in case:
    #         tree.add(value)
    #     if not tree.is_valid_avl():
    #         raise Exception("PROBLEM WITH ADD OPERATION")
    # print('add() stress test finished')
    print("\nPDF - method remove() example 1")
    # print("-------------------------------")
    # test_cases = (
    #     ((1, 2, 3), 2),  # no AVL rotation
    #     ((1, 2, 3), 1),  # no AVL rotation
    #     ((1, 2, 3), 3),  # no AVL rotation
    #     ((50, 40, 60, 30, 70, 20, 80, 45), 0),
    #     ((50, 40, 60, 30, 70, 20, 80, 45), 45),  # no AVL rotation
    #     ((50, 40, 60, 30, 70, 20, 80, 45), 40),  # no AVL rotation
    #     ((50, 40, 60, 30, 70, 20, 80, 45), 30),  # no AVL rotation
    # )
    # for case, del_value in test_cases:
    #     tree = AVL(case)
    #     print('INPUT  :', tree, "DEL:", del_value)
    #     tree.remove(del_value)
    #     print('RESULT :', tree)
    # print("\nPDF - method remove() example 2")
    print("-------------------------------")
    # test_cases = (
    #     ((-94, 5, 27, -23, 28, 17, -14, 21, -37, 60), -94),  # RR
    #     (( 5, -23, -37, -14, 27, 17, 21, 28, 60), 27),  # LL
    #     ((5, -23, -37, -14, 21, 17, 28, 60), 28),  # RL
    #
    # )
    # for case, del_value in test_cases:
    #     tree = AVL(case)
    #     print('INPUT  :', tree, "DEL:", del_value)
    #     tree.remove(del_value)
    #     print('RESULT :', tree)
    # print("\nPDF - method remove() example 3")
    # print("-------------------------------")
    # case = range(-9, 16, 2)
    # tree = AVL(case)
    # for del_value in case:
    #     print('INPUT  :', tree, del_value)
    #     tree.remove(del_value)
    #     print('RESULT :', tree)
    print("\nPDF - method remove() example 4")
    # -29310, 97347, 64451, 79621, -82395, -96057, 93000, 83017, 96810, 843, 50149, 37383, -28815, 12081, -10383, -5423, -1291, 90198, 57170, -62661
    # -29310, 64451
    print("-------------------------------")
    case = [-24, 73, -84, 49, 51, 19, 58, -37, -68, 95]
    remove = [-24]
    tree = AVL(case)
    for x in remove:

        print('INPUT  :', tree, x)
        tree.remove(x)
        print('RESULT :', tree)
    # print("\nPDF - method remove() example 5")
    # print("-------------------------------")
    # for _ in range(100):
    #     case = list(set(random.randrange(1, 20000) for _ in range(900)))
    #     tree = AVL(case)
    #     for value in case[::2]:
    #         tree.remove(value)
    #     if not tree.is_valid_avl():
    #         raise Exception("PROBLEM WITH REMOVE OPERATION")
    # print('remove() stress test finished')
    # print("\nPDF - method contains() example 1")
    # print("---------------------------------")
    # tree = AVL([10, 5, 15])
    # print(tree.contains(15))
    # print(tree.contains(-10))
    # print(tree.contains(15))
    # print("\nPDF - method contains() example 2")
    # print("---------------------------------")
    # tree = AVL()
    # print(tree.contains(0))
    # print("\nPDF - method inorder_traversal() example 1")
    # print("---------------------------------")
    # tree = AVL([10, 20, 5, 15, 17, 7, 12])
    # print(tree.inorder_traversal())
    # print("\nPDF - method inorder_traversal() example 2")
    # print("---------------------------------")
    # tree = AVL([8, 10, -4, 5, -1])
    # print(tree.inorder_traversal())
    # print("\nPDF - method find_min() example 1")
    # print("---------------------------------")
    # tree = AVL([10, 20, 5, 15, 17, 7, 12])
    # print(tree)
    # print("Minimum value is:", tree.find_min())
    # print("\nPDF - method find_min() example 2")
    # print("---------------------------------")
    # tree = AVL([8, 10, -4, 5, -1])
    # print(tree)
    # print("Minimum value is:", tree.find_min())
    # print("\nPDF - method find_max() example 1")
    # print("---------------------------------")
    # tree = AVL([10, 20, 5, 15, 17, 7, 12])
    # print(tree)
    # print("Maximum value is:", tree.find_max())
    # print("\nPDF - method find_max() example 2")
    # print("---------------------------------")
    # tree = AVL([8, 10, -4, 5, -1])
    # print(tree)
    # print("Maximum value is:", tree.find_max())
    # print("\nPDF - method is_empty() example 1")
    # print("---------------------------------")
    # tree = AVL([10, 20, 5, 15, 17, 7, 12])
    # print("Tree is empty:", tree.is_empty())
    # print("\nPDF - method is_empty() example 2")
    # print("---------------------------------")
    # tree = AVL()
    # print("Tree is empty:", tree.is_empty())
    # print("\nPDF - method make_empty() example 1")
    # print("---------------------------------")
    # tree = AVL([10, 20, 5, 15, 17, 7, 12])
    # print("Tree before make_empty():", tree)
    # tree.make_empty()
    # print("Tree after make_empty(): ", tree)
    # print("\nPDF - method make_empty() example 2")
    # print("---------------------------------")
    # tree = AVL()
    # print("Tree before make_empty():", tree)
    # tree.make_empty()
    # print("Tree after make_empty(): ", tree)