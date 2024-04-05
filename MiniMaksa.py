import Tree

# Rekursīva funkcija, kurai nodot Tree objektu, un bool mainīgo, kurš norāda vai nākamais līmenis ir max vai min līmenis
def MiniMax(root, vaiLimenisIrMax):
    # Ja virsotne ir sturpceļa/ gala virsotne, tai piešķir hieristisko vērtību, balstoties uz cilvēka un datora punktu skaita
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
        # Ja virsotnes kādam pēctecim nav vēl hieristiskās vērtība, tas izsauc šo pašu funkciju MiniMax, lai to piešķirtu
        while(root.child1.heiristiskaVertiba == None or root.child2.heiristiskaVertiba == None or root.child3.heiristiskaVertiba == None):
            if(root.child1.heiristiskaVertiba == None):
                root.child1 = MiniMax(root.child1, not vaiLimenisIrMax)
            if(root.child2.heiristiskaVertiba == None):
                root.child2 = MiniMax(root.child2, not vaiLimenisIrMax)
            if(root.child3.heiristiskaVertiba == None):
                root.child3 = MiniMax(root.child3, not vaiLimenisIrMax)

        # Kad visiem pēctečiem ir hieristiskās vērtības, virsotnei piešķir savu hieristisko vērtību, balstoties uz esošās virsotnes līmeņa
        if(vaiLimenisIrMax):
            root.heiristiskaVertiba = max(root.child1.heiristiskaVertiba, root.child2.heiristiskaVertiba, root.child3.heiristiskaVertiba)
        else:
            root.heiristiskaVertiba = min(root.child1.heiristiskaVertiba, root.child2.heiristiskaVertiba, root.child3.heiristiskaVertiba)

    #Atgriež Tree objektu, kuram ir noteiktas visas hieristiskās vērtības
    return root

# Funkcija, no argumentie izveido koku un piešķir tās virsotnēm hieristiskās vērtības ar rekursīvo funkciju MiniMax
def MiniMaxIzvele(number, humanPoints, computerPoints, bankPoints, dzilums):
    root = Tree.TreeNode(number, humanPoints, computerPoints, bankPoints, 'c')
    root = Tree.tree_maker(root, dzilums)
    root = MiniMax(root, True)

    izvele = [root.child1.heiristiskaVertiba, root.child2.heiristiskaVertiba, root.child3.heiristiskaVertiba]
    return izvele.index(min(izvele)) + 2


# Testēšanai
#root = Tree.TreeNode(25, 0, 0, 0, 'c')
#root = Tree.tree_maker(root, 6)
#root = MiniMax(root, True)
#root.print_leaf_nodes()
#print(root.heiristiskaVertiba)
