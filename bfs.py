import Graphs

def BFS_u (G,node) :
    """
    applique BFS en partant d'un noeud
    """
    i = 0
    P,M = [None for u in G.V],[0 for u in G.V]
    F = [node]
    P[i] = node
    M[i] = 1
    while F != []:
        z = F.pop(0)
        for x in G.adj(z):
            if x.get_color() == "white" :
                i += 1
                x.set_color("grey")
                M[i] = 1
                P[i] = z
                F.append(x)
                
                
    return M,P


def BFS_X (G):
    """
    applique BFS sur la liste de tout les noeuds
    """
    i = -1
    BLOCK = [0 for v in G.V]
    F = []
    cs = 0
    for v in G.V:
        if v.get_color() == "white":
            i += 1
            v.set_color("grey")
            cs += 1
            BLOCK[i] = cs
            F.append(v)
        while F != []:
            z = F.pop(0)
            for x in G.adj(z):                
                if x.get_color() == "white" :
                    i = i + 1
                    x.set_color("grey")
                    if BLOCK[i] == 0 :
                        BLOCK[i] = cs
                        F.append(x)
    return BLOCK
