class TreeNode:
    def __init__(self, number, pp, cp, bank, turn):
        # number itself (used as int)
        self.number = number
        # Player and computer points (also int type)
        self.pp = pp
        self.cp = cp
        # Bank points
        self.bank = bank
        # variable that indicates who's turn it is
        # it is either 'c' or 'p' char value
        # for a computer or player turn respectively
        self.turn = turn
        # children nodes that contain either Treenode class objects
        # or nothing indicating tree end
        self.child1 = None
        self.child2 = None
        self.child3 = None

        self.heiristiskaVertiba = None

    # def print_node_and_path(self, path=""):
    #     """Prints the node's attributes and path leading to it."""
    #     print("Path:", path, " -> ", str(self.number))
    #     print("PP:", self.pp, "CP:", self.cp, "Bank:", self.bank, "Turn:", self.turn, "HV:", self.heiristiskaVertiba)
    #     print("------------------------")
    #     if self.child1:
    #         self.child1.print_node_and_path(path + " -> " + str(self.number))
    #     if self.child2:
    #         self.child2.print_node_and_path(path + " -> " + str(self.number))
    #     if self.child3:
    #         self.child3.print_node_and_path(path + " -> " + str(self.number))

    # def print_leaf_nodes(self, path=""):
    #     """Prints the leaf nodes of the tree."""
    #     if not self.child1 and not self.child2 and not self.child3:
    #         print("Path:", path, " -> ", str(self.number))
    #         print("PP:", self.pp, "CP:", self.cp, "Bank:", self.bank, "Turn:", self.turn, "HV:", self.heiristiskaVertiba)
    #         print("------------------------")
    #     if self.child1:
    #         self.child1.print_leaf_nodes(path + " -> " + str(self.number))
    #     if self.child2:
    #         self.child2.print_leaf_nodes(path + " -> " + str(self.number))
    #     if self.child3:
    #         self.child3.print_leaf_nodes(path + " -> " + str(self.number))

def tree_maker(root, counter):
    """
    Recursively generates a tree of TreeNode objects based on a root node and a specified depth.

    Parameters:
        root (TreeNode): The starting node of the tree.
        counter (int): Counter to control the depth of the tree.

    Returns:
        TreeNode: The root node of the generated tree.

    The function generates a tree structure by creating child nodes based on the root node's number.
    Each iteration counter is reduced by one.
    If the counter reaches 0, the function stops generating further nodes.
    """
    # Base case: If counter is 0, return None and end the loop
    if counter == 0:
        return None
    
    # Check if the root's number is greater than or equal to 5000 to set the counter
    # because if the number is 5000 I want to display only this node but not any further
    if root.number >= 5000:
        counter = 1

    # Calculate numbers for children nodes
    children_num = [root.number * 2, root.number * 3, root.number * 4]

    # Create an empty array of node objects
    children = []

    # Iterate over children numbers to create child nodes
    for child_num in children_num:
        # Check if the child number is divisible by 5
        # Depending on the number properties, create child nodes with appropriate attributes
        # Create an object node depending on who's turn it is, then add it to the array
        if child_num % 5 == 0:
            if root.turn == 'c':
                node = TreeNode(child_num, root.pp, root.cp, root.bank + 1, 'p')
                children.append(node)
            else:
                node = TreeNode(child_num, root.pp, root.cp, root.bank + 1, 'c')
                children.append(node)
        else:
            if child_num % 2 == 0:
                if root.turn == 'c':
                    node = TreeNode(child_num, root.pp, root.cp - 1, root.bank, 'p')
                    children.append(node)
                else:
                    node = TreeNode(child_num, root.pp - 1, root.cp, root.bank, 'c')
                    children.append(node)
            else:
                if root.turn == 'c':
                    node = TreeNode(child_num, root.pp, root.cp + 1, root.bank, 'p')
                    children.append(node)
                else:
                    node = TreeNode(child_num, root.pp + 1, root.cp, root.bank, 'c')
                    children.append(node)

    # Recursively call tree_maker to create further child nodes
    root.child1 = tree_maker(children[0], counter - 1)
    root.child2 = tree_maker(children[1], counter - 1)
    root.child3 = tree_maker(children[2], counter - 1)
    
    return root

