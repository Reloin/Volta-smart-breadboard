"""
Code created by Reloin, for breadboard project
"""
from tkinter import Tk, Canvas
from PIL import ImageTk, Image


# You can read
window_width = 1080
window_heigth = 700
bbPos = 900, (window_heigth/2) #position of breadboard
title = 'Smart Breadboard'


class app(object):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        
        win = Tk()
        win.title(title)
        self.canvas = Canvas(win, width = window_width, height = window_heigth, background='white')
        self.canvas.grid(row=0, column=0)
        
        self.showBb() # show breadboard in canvas
        #self.resistor()

        # Use mouse as generate and clear btn
        self.canvas.bind('<Button-1>', self.generate)
        self.canvas.bind('<Button-3>', self.clear)

        win.mainloop()
    
    #function for showing breadboard
    def showBb(self):
        self.bbImg = ImageTk.PhotoImage(Image.open("svg/breadboard.png"))
        self.canvas.create_image(bbPos, image=self.bbImg)
        
    def showResistor(self, x, y):
        self.resistor = ImageTk.PhotoImage(Image.open("svg/resistor.png"))
        pos = x, y
        self.canvas.create_image(pos, image=self.resistor)

    # Function for drawing wire
    def wire(self, ax, ay, bx, by):
        self.canvas.create_line(ax,ay,bx,ay, fill="black", width=5)
        self.canvas.create_line(bx,ay,bx,by, fill="black", width=5)
        
    # Generating diagram
    def generate(self, Event):
        self.showBb()
        self.showResistor(100, 300)
        self.wire(136, 193, 160, 223)
    
    # Clearing Diagram
    def clear(self, Event):
        self.canvas.delete("all")
        self.showBb()

app()