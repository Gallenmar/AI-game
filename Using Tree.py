import Tree

number = 3 # picking a number (in the rules of the game it should be from 25 to 40)
counter = 4 # how deep the algorithm will build a tree
root = Tree.TreeNode(number, 0, 0, 0, 'c') # creating a root node
# def __init__(self, number, pp, cp, bank, turn):

root = Tree.tree_maker(root, counter) # calling a function to create a tree
root.print_leaf_nodes() # calling a function to display the tree leafs (strupceli)
# root.print_node_and_path # function to display the entire tree


# You can write any other code to use the tree here