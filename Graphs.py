class Noeud:
    def __init__(self,label):
        self.label = label
    def getlabel(self):
        return self.label
    
class Arete:
    def __init__(self,n1,n2,w = None):
        self.bord1 = n1
        self.bord2 = n2
        self.poids = w
    
class Graph:
    def __init__(self,V,E,isOriented,isWeighted):
        self.V = V
        self.E = E
        self.isO = isOriented
        self.isW = isWeighted
    def getV(self):
        return self.V
    def affV(self):
        L = [x.label for x in self.getV()]
        return L
    def getE(self):
        L =[(x.bord1,x.bord2,x.poids) for x in self.E]
        return L
    def affE(self):
        L =[(x.bord1.label,x.bord2.label,x.poids) for x in self.E]
        return L
    def status(self):
        s = "Nodes: "+str(self.affV())+"\nEdges: " +str(self.affE())+"\nisOriented: "+str(self.isO)+"\nisWeighted: "+str(self.isW)
        return s
    def objectdetail(self):
        s = "Nodes: "+str(self.getV())+"\nEdges: " +str(self.getE())
        return s
    

def buildG(isO,isW):
    V = []
    E = []
    while True:
        s = input("Entrez les noeuds ('stop' pour passer à la suite): ")
        if s == "stop" :
            break
        else:            
            n = Noeud(s)
            V.append(n)
            
    while True:
        a = input("Entrez les aretes (avec noeuds existant ex: A,B,4 ou A,B)('stop' pour passer à la suite): ")
        if a == "stop" :
            break
        else:
            a = a.split(",")
            L = [(x,x.label) for x in V]
            LL1 = [i[1] for i in L]
            LL2 = [i[0] for i in L]
            if (a[0] in LL1) and (a[1] in LL1):                
                if isW :
                    e = Arete(LL2[LL1.index(a[0])],LL2[LL1.index(a[1])],a[2])
                else:                   
                    e = Arete(LL2[LL1.index(a[0])],LL2[LL1.index(a[1])])
            E.append(e)
    print (V,'\n', E)
    return Graph(V,E,isO,isW)
       
        
