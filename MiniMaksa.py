import Tree

def MiniMax(root, vaiLimenisIrMax):
    if(root.child1 == None and root.child2 == None and root.child3 == None):
        
        if(root.number >= 5000):
            if(root.turn == 'c'):
                root.pp += root.bank
            else:
                root.cp += root.bank

        if(root.pp < root.cp):
            root.heiristiskaVertiba = -1
        elif(root.pp > root.cp):
            root.heiristiskaVertiba = 1
        else:
            root.heiristiskaVertiba = 0

    else:
        while(root.child1.heiristiskaVertiba == None or root.child2.heiristiskaVertiba == None or root.child3.heiristiskaVertiba == None):
            if(root.child1.heiristiskaVertiba == None):
                root.child1 = MiniMax(root.child1, not vaiLimenisIrMax)
            if(root.child2.heiristiskaVertiba == None):
                root.child2 = MiniMax(root.child2, not vaiLimenisIrMax)
            if(root.child3.heiristiskaVertiba == None):
               root.child3 = MiniMax(root.child3, not vaiLimenisIrMax)

    
        if(vaiLimenisIrMax):
            root.heiristiskaVertiba = max(root.child1.heiristiskaVertiba, root.child2.heiristiskaVertiba, root.child3.heiristiskaVertiba)
        else:
            root.heiristiskaVertiba = min(root.child1.heiristiskaVertiba, root.child2.heiristiskaVertiba, root.child3.heiristiskaVertiba)

    
    return root


def MiniMaxIzvele(number, humanPoints, computerPoints, bankPoints, dzilums):
    root = Tree.TreeNode(number, humanPoints, computerPoints, bankPoints, 'c')
    root = Tree.tree_maker(root, dzilums)
    root = MiniMax(root, True)
    #root.print_leaf_nodes()
    #print(root.child1.heiristiskaVertiba)
    #print(root.child2.heiristiskaVertiba)
    #print(root.child3.heiristiskaVertiba)

    izvele = [root.child1.heiristiskaVertiba, root.child2.heiristiskaVertiba, root.child3.heiristiskaVertiba]
    return izvele.index(min(izvele)) + 2
    
#root = Tree.TreeNode(25, 0, 0, 0, 'c')
#root = Tree.tree_maker(root, 6)
#root = MiniMax(root, True)
#root.print_leaf_nodes()
#print(root.heiristiskaVertiba)