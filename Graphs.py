from tkinter import *
from math import sqrt, ceil
from typing import List
from math import cos, sin, atan2, sin
from tkinter.colorchooser import askcolor
import Feuille


class Node:
    def __init__(self, label) -> None:
        self.label = label  # node label
        self.posx = 0  # x position of the small canvas
        self.posy = 0  # y position of the small canvas

        self.G = None # Graph
        self.canvas = None  # small canvas

    def get_infos(self) -> str:
        return f"Label -> {self.label}\nposX -> {self.posx}\nposY -> {self.posy}"

    def drag_start(self, event) -> None:
        """
        When a node is clicked
        """
        widget = self.canvas
        widget.startX = event.x
        widget.startY = event.y

    def drag_motion(self, event) -> None:
        """
        When a node is dragged
        Move the node and the edges
        """
        widget = self.canvas

        # New coords
        x = widget.winfo_x() - widget.startX + event.x
        y = widget.winfo_y() - widget.startY + event.y

        # Update node that is in the canvas
        self.posx = x
        self.posy = y

        # Move associated edges
        for edge in self.G.get_edges_of_node(self):
            edge.delete()
            edge.draw(self.G)

        # Move node
        widget.place(x=x, y=y)

    def right_click(self, event):
        '''
        When right clicking on a node
        '''
        m = Menu(self.canvas, tearoff = 0)
        m.add_command(label = "BFS_u", command = lambda: Feuille.onClick_BFS_u(self.G,self))
        m.add_command(label ="Supprimer le noeud", command = self.delete)
        m.tk_popup(event.x_root, event.y_root)

    def set_color (self, color):
        self.color = color
        self.canvas.itemconfigure(self.cercle ,fill= self.color)
    def get_color (self) :
        return self.canvas.itemcget(self.cercle ,"fill")

    def draw(self, G, x, y) -> None:
        """
        Draw node on the canvas
        Saves x,y coordinates
        """
        self.posx = x
        self.posy = y
        self.G = G
        # Création du petit canvas et ajout du petit canvas dans le grand
        self.canvas = Canvas(self.G.canvas, width=self.G.size, height=self.G.size, background="#000000")
        self.G.canvas.create_window(x, y, anchor=NW, window=self.canvas)

        # Création du cercle et du texte
        self.cercle = self.canvas.create_oval(
            0, 0, self.G.size, self.G.size, width=2, fill="white", tag=("clickable", "node")
        )
        self.canvas.create_text(self.G.size / 2, self.G.size / 2, text=self.label, tag=("clickable"))

        self.canvas.tag_bind("clickable", "<Button-1>", self.drag_start)
        self.canvas.tag_bind(
            "clickable",
            "<B1-Motion>",self.drag_motion )
        self.canvas.tag_bind("clickable", "<Button-3>", self.right_click)

    def delete(self):
        '''
        Delete all the edges connected to the node
        Delete the node
        '''
        # Update the edge list
        L = list()
        for edge in self.G.E:
            if edge.bord1 != self and edge.bord2 != self:
                L.append(edge)
            else:
                edge.delete(True)
        self.G.E = L
        # Remove from node list
        self.G.V.remove(self)
        # Destroy on the graph
        self.canvas.destroy()

class Edge:
    def __init__(self, n1: Node, n2: Node, w=None, is_oriented=False) -> None:
        self.bord1 = n1
        self.bord2 = n2
        self.poids = w  # real weight
        self.is_oriented = is_oriented  # If edge is oriented

        self.G = None # The graph
        self.poids_var = None   # Weight displayed
        self.line = None  # line object
        self.text = None  # text object
        self.color = "black"

    def draw(self, G) -> None:
        """
        Draw the edge based on the positions of the 2 nodes
        """
        # Create the text variable and add the canvas
        self.poids_var = StringVar(value = self.poids)
        self.G = G
        size = self.G.size

        # Nodes pos
        x1 = self.bord1.posx + size / 2
        y1 = self.bord1.posy + size / 2
        x2 = self.bord2.posx + size / 2
        y2 = self.bord2.posy + size / 2

        # Middle point pos
        t = atan2(y2 - y1, x2 - x1)
        d = 30
        xC = (x1 + x2) / 2 + d * sin(t)
        yC = (y1 + y2) / 2 - d * cos(t)

        # Creation de la ligne et du poids
        angle = atan2(yC - y2, xC - x2)
        final_x = x2 + size / 2 * cos(angle)
        final_y = y2 + size / 2 * sin(angle)

        self.line = self.G.canvas.create_line(
            (x1, y1), (xC, yC), (final_x, final_y), smooth=True, fill = self.color
        )

        # Text label
        self.text = Label(self.G.canvas, textvariable=self.poids_var, bg = "red")
        self.text.place(x=xC, y=yC, anchor="sw")
        self.text.bind('<Button-3>', self.onClick)
       
           

        if self.is_oriented :  # Ajoute une flèche
            self.G.canvas.itemconfig(self.line, arrow="last", arrowshape=(20, 20, 5))

    def onClick(self, event):
        '''
        When click on label
        '''
        # Open menu
        m = Menu(self.G.canvas, tearoff = 0)
        m.add_command(label ="Supprimer l'arete", command = lambda: self.delete(remove = True))
        m.add_command(label ="Changer le poids", command = self.update_weight_window)
        m.add_command(label ="Changer la couleur", command = self.change_color)
        m.tk_popup(event.x_root, event.y_root)

    def update_weight_window(self) -> None:
            '''
            Update the weight of the edge
            '''
            win = Toplevel()
            win.wm_title("Changer le poids de l'arete")
            win.grid_propagate(False)

            text_frame = Frame(win, width=5, height=5)
            text_frame.pack()

            l = Text(text_frame)
            l.pack()

            text_frame.grid_propagate(False)


            b = Button(win, text="Okay", command= lambda : self.update_weight(win, l))
            b.pack()
    
    def update_weight(self, win, text_box) -> None:
        '''
        Update weight
        '''
        new_weight = text_box.get("1.0", "end-1c")
        self.poids = int(new_weight)
        self.poids_var.set(new_weight)
        win.destroy()

    def delete(self, remove = False) -> None:
        """
        Erase the line and weight text from the canvas
        Remove the edge from the edge list
        """
        self.G.canvas.delete(self.line)
        self.text.destroy()
        

        # Remove from edge list (not called when only moving nodes)
        if remove:
            self.G.E.remove(self)
            self.G.update_adj()
    def change_color(self) -> None:
        """
        Change the color
        """
        self.color = askcolor(title="Change edge color")[1]
        self.G.canvas.itemconfig(self.line, fill=self.color)
        

class Graph:
    def __init__(self, V, E, isOriented, isWeighted) -> None:
        self.V = V  # Noeuds
        self.E = E  # Arretes
        self.isO = isOriented
        self.isW = isWeighted

        self.canvas = None  # The canvas in which the graph is drawn
        self.size = 50  # Default nodes size
        
        self.update_adj()
   
    def update_adj(self) -> None:
        self.dict_node_adjs = dict()
        for v in self.V:     
            # A -> B
            L = [edge.bord2 for edge in self.E if edge.bord1 == v]
            # Si c'est pas orienté, on ajoute les B -> A
            if not self.isO:    
                L.extend([edge.bord1 for edge in self.E if edge.bord2 == v])  
            self.dict_node_adjs[v] = L
            
    def adj(self, node) -> List[Node]:
        return self.dict_node_adjs[node]
    
    def all_white_node (self):
        for v in self.V:
            v.set_color ("white")

    def add_node(self, label) -> Node:
        """
        add a Node to the graph
        """
        # Check if it doesnt already exist
        if label not in [existing_node.label for existing_node in self.V]:
            node = Node(label)
            self.V.append(node)
            node.draw(self, 300, 300)
            self.update_adj()
            return node
        else:
            print("Node already exists")
            return None

    def add_edge(self, edge_list) -> Edge:
        """
        add a Node to the graph
        """
        # Check if it doesnt already exist
        bord1 = self.get_node_from_label(edge_list[0])
        bord2 = self.get_node_from_label(edge_list[1])
        if not bord1 or not bord2:
            print("Un des noeuds n'existe pas")
            return None

        for existing_edge in self.E:
            if existing_edge.bord1 == bord1 and existing_edge.bord2 == bord2:
                print("Edge already exist")
                return None
        if self.isW == True:
            edge = Edge(bord1, bord2, w=edge_list[2], is_oriented=self.isO)
        else:
            edge = Edge(bord1, bord2, w=None, is_oriented=self.isO)
        edge.draw(self)
        self.E.append(edge)
        self.update_adj()
        return edge

    def affV(self)-> str:
        c = ""
        for x in self.V:
            c = c+ x.label +", "
        return c

    def getE(self):
        return [(x.bord1, x.bord2, x.poids) for x in self.E]

    def affE(self):
        return [(x.bord1.label, x.bord2.label, x.poids) for x in self.E]

    def status(self) -> str:
        return f"Nodes: {self.affV()}\nEdges: {self.affE()}\nisOriented: {self.isO}\nisWeighted: {self.isW}"

    def objectdetail(self) -> str:
        return f"Nodes: {self.V()}\nEdges: {self.getE()}"

    def draw(self, size=50, espacement=50, x=20, y=100) -> None:
        """
        Draw nodes and edges
        """
        self.size = size

        self._draw_nodes(espacement, x, y)
        self._draw_edges()

    def _draw_nodes(self, espacement=50, x=20, y=100) -> None:
        """
        Draw every node at different places
        """
        matrix_size = ceil(sqrt(len(self.V)))
        default_y = y

        for i, node in enumerate(self.V):

            node.draw(self, x, y)  # Draw

            # If we start a new line of nodes
            if (i + 1) % matrix_size == 0:
                x += espacement + self.size
                y = default_y
            # Same line of nodes
            else:
                y += self.size + espacement

    def _draw_edges(self) -> None:
        """
        Draw every edge
        """
        for edge in self.E:
            edge.draw(self)

    def get_node_from_label(self, label) -> Node:
        """
        Return the node object that has the given label
        """
        for node in self.V:
            if node.label == label:
                return node
        return None

    def get_node_from_canvas(self, canvas) -> Node:
        """
        Return the nodes that has the given canvas
        """
        for node in self.V:
            if node.canvas == canvas:
                return node
        return None

    def get_edges_of_node(self, node) -> List[Edge]:
        """
        Return the edges connected to a given node
        """
        return [edge for edge in self.E if node == edge.bord1 or node == edge.bord2]


def buildG() -> Graph:
    """
    Main function
    Gets the input and builds the Nodes/Edges/Graph
    Returns the final Graph
    """
    isO = None
    isW = None
    V = []
    E = []
    a = " "
    while a not in  ["oui", "non"]:
        a = input("Le graph est-il orrienté ?(oui/non): ")
        if a == "oui":
            print ("ici")
            isO = True
        else:
            isO = False
    a = " "
    while a not in  ["oui", "non"]:
        a = input("Les arêtes ont elles un poids ?(oui/non): ")
        if a == "oui" :
            isW = True
        else:
            isW = False
    a = " "
    while a != "":
        a = input("Entrez les noeuds: ")
        if a != "":
            n = Node(a)
            V.append(n)

    # GET THE EDGES
    a = " "
    edge_list = list()  # List of edges
    while a != "":
        a = input("Entrez les aretes (avec noeuds existant ex: A,B,4 ou A,B): ")
        if a != "":
            a = a.split(",")
            if isW :
                weight = a[2]
            else:
                weight = None

            # Get the nodes
            bord_1 = None
            bord_2 = None
            

            for node in V:
                if node.label == a[0]:
                    bord_1 = node
                if node.label == a[1]:
                    bord_2 = node

                if bord_1 and bord_2:  # Si les nodes existent
                    edge_list.append([a[0], a[1]])
                    E.append(Edge(bord_1, bord_2, w=weight, is_oriented=isO))
    G = Graph(V, E, isO, isW)
    return G
