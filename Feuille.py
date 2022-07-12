#from tkinter import ttk
from tkinter import *
#from tkinter.ttk import *
import Graphs

def pgcd(a,b):
    while b!=0:
        r=a%b
        a,b=b,r
    return a
def is_prime(n):
    if n > 1:
        for i in range(2, int(n/2)+1):
            if (n % i) == 0:
                break
            else:
                return True
    else:
       return False

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle

def create_node(node,posx,posy):
    canvas.create_circle(posx,posy,(h//c),width = 2)
    canvas.create_text(posx,posy,text=node.label)

def rearrange_draw_node(L):
    n = len(L)   
    nL=[]
    boul = 0
    a = 0
    b = pgcd(n//2,n)
    if is_prime(n) :
        b = pgcd((n-1)//2,(n-1))
        nL.append([L[0]])
        boul = 1
        
    for i in range (0+boul,n,b):
        nL.append(L[i:i+b])           
    return nL


G = Graphs.buildG(False,False)
root = Tk()
l = 800
h = 650
c = 30
canvas = Canvas(root,width=l,height=h,borderwidth=0,highlightthickness=0)
canvas.grid()

label = Label(anchor='nw',justify ='left', text=G.status())
label.grid()



i=0
j=1
for sL in rearrange_draw_node(G.getV()):
    for x in sL:
        i +=1        
        create_node(x,(h//c)+(c*5*i),(h//c)+(c * 5*j))
    i = 0
    j+= 1

    
root.mainloop()

