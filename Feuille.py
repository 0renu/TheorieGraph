import Feuille
from tkinter import *
import tkinter
import bfs
import Graphs

def create_window() -> tkinter.Tk:
    """
    Create and return the main window
    """
    return Tk()


def create_upper_canvas(root, h, l,G) -> tkinter.Canvas:
    """
    Create and return the big canvas
    """
    canvas = Canvas(root, width=l, height=h, borderwidth=0, highlightthickness=0, bg="yellow")
    clear_button = Button(
        canvas,
        text="clear",
        height=1,
        width=5,
        command=lambda:clear(G),
        )
    clear_button.grid(row=0,column=1,sticky='nw')
    canvas.grid_propagate(False)
    
    return canvas

def clear(G):
     G.all_white_node()
     label_response.configure(text="")
    
def create_lower_canvas(root, h, l, G, upper_canvas, size) -> tkinter.Canvas:
    """
    Create and return the small canvas with the buttons
    """
    canvas = Canvas(root, width=l, height=h, bg="blue")
    global label_response
    label_response = Label(canvas , text = "", justify ='left')
    label_response.grid(row=0,column=3, sticky = 'nw')    


    # Add node
    add_node_field = Text(canvas, height=5, width=20)
    add_node_button = Button(
        canvas,
        text="Add Node (A)",
        height=5,
        width=20,
        command=lambda: onClick_add_node(add_node_field, G),
    )
    add_node_button.grid(row=0, column=0)
    add_node_field.grid(row=0, column=1)

    # Add edge

    add_edge_field = Text(canvas, height=5, width=20)
    add_edge_button = Button(
        canvas,
        text="Add Edge (A,B,2)",
        height=5,
        width=20,
        command=lambda: onClick_add_edge(add_edge_field, G),
    )
    add_edge_button.grid(row=1, column=0)
    add_edge_field.grid(row=1, column=1)
    
    BFS_X_button = Button(
        canvas,
        text="BFS_X",
        height=1,
        width=5,
        command=lambda: onClick_BFS_X (G)
    )
    BFS_X_button.grid(row=0, column=2 , sticky='nw')
    
    
    canvas.grid_propagate(False)

    return canvas


def onClick_add_node(text_field, G):
    """
    When Add Node button is pressed
    """
    text = text_field.get("1.0", "end-1c")
    # Vérifier texte ici

    G.add_node(text)
    # Erase text
    text_field.delete("1.0", END)


def onClick_add_edge(text_field, G):
    """
    When add Edge button is pressed
    """
    # Add Edge
    text = text_field.get("1.0", "end-1c")
    # Verifier texte ici
    # Avec si c'est orienté ou non
    # regex =
    # match = re.search(regex, text)
    L = text.split(",")
    G.add_edge(L)

    # Erase text
    text_field.delete("1.0", END)
    
def onClick_BFS_X(G):
    
    G.all_white_node()
    BLOCK = bfs.BFS_X(G)    
    label_response.configure(label_response ,text=str(BLOCK))
    
def onClick_BFS_u (G, node):
    G.all_white_node()
    M,P = bfs.BFS_u(G,node)
    P = [z.label for z in P if z != None]
    label_response.configure(text= str(P)+"\n"+str(M))
    
    

    
    
def __main__():
    
    # Instanciate graph
    G = Graphs.buildG()

    # Create the window
    l = 600
    upper_canvas_h = 400
    lower_canvas_h = 200
    size = 50
    root = create_window()
    upper_canvas = create_upper_canvas(root, upper_canvas_h, l,G)
    lower_canvas = create_lower_canvas(root, lower_canvas_h, l, G, upper_canvas, size)
    upper_canvas.pack()
    lower_canvas.pack()
    upper_canvas.pack_propagate(False)
    lower_canvas.pack_propagate(False)
    G.canvas = upper_canvas

    # Draw graph
    G.draw()
    
    root.mainloop()


__main__()
