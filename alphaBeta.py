import Tree

def AlphaBeta(root, alpha, beta, vaiLimenisIrMax):
    if root.child1 is None and root.child2 is None and root.child3 is None:
        if root.number >= 5000:
            if root.turn == 'c':
                root.pp += root.bank
            else:
                root.cp += root.bank

        if root.pp < root.cp:
            root.heiristiskaVertiba = -1
        elif root.pp > root.cp:
            root.heiristiskaVertiba = 1
        else:
            root.heiristiskaVertiba = 0

    else:
        if vaiLimenisIrMax:
            v = float('-inf')
            children = [root.child1, root.child2, root.child3]
            for child in children:
                v = max(v, AlphaBeta(child, alpha, beta, not vaiLimenisIrMax))
                alpha = max(alpha, v)
                if beta <= alpha:
                    break
            root.heiristiskaVertiba = v
        else:
            v = float('inf')
            children = [root.child1, root.child2, root.child3]
            for child in children:
                v = min(v, AlphaBeta(child, alpha, beta, not vaiLimenisIrMax))
                beta = min(beta, v)
                if beta <= alpha:
                    break
            root.heiristiskaVertiba = v

    return root.heiristiskaVertiba


def AlphaBetaIzvele(number, humanPoints, computerPoints, bankPoints, dzilums):
    root = Tree.TreeNode(number, humanPoints, computerPoints, bankPoints, 'c')
    root = Tree.tree_maker(root, dzilums)
    val = AlphaBeta(root, float('-inf'), float('inf'), True)
    izvele = [root.child1.heiristiskaVertiba, root.child2.heiristiskaVertiba, root.child3.heiristiskaVertiba]
    return izvele.index(val) + 2

# Piemērs, kā izmantot AlphaBetaIzvele funkciju:
# number = 25
# humanPoints = 0
# computerPoints = 0
# bankPoints = 0
# dzilums = 6
# izvele = AlphaBetaIzvele(number, humanPoints, computerPoints, bankPoints, dzilums)
# print("Optimālais gājiens:", izvele)

