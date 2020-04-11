"""
Code created by Reloin, for breadboard project
"""
from tkinter import Tk, Canvas
from PIL import ImageTk, Image
import process
import identifier as idpy


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
        # initiate ui stuff
        win = Tk()
        win.title(title)
        self.canvas = Canvas(win, width = window_width, height = window_heigth, background='white')
        self.canvas.grid(row=0, column=0)
        
        self.showBb() # show breadboard in canvas


        # Use mouse as generate and clear btn
        self.canvas.bind('<Button-1>', self.generate_diagram)
        self.canvas.bind('<Button-3>', self.clear)

        win.mainloop()

    # Generating diagram
    def generate_diagram(self, Event):
        pass
        # self.showBb()
        # data = process.readArduino.read_data()
        # row, column = process.readArduino.get_size()
        # for i in range(row):
        #     for j in range(column):
        #         pass
    
    #below here are functions for drawing all stuff

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

    # draw positive power in
    def vcc(self, x, y):
        size = 6
        offset = 20
        hor, ver = idpy.cor2pos(x,y)
        self.canvas.create_oval(hor-size,ver-size,hor+size,ver+size, fill="red", width = 0)
        self.canvas.create_text(hor-offset, ver, text="Vcc")

    # draw dot for ground
    def gnd(self, x, y):
        size = 6
        offset = 20
        hor, ver = idpy.cor2pos(x,y)
        self.canvas.create_oval(hor-size,ver-size,hor+size,ver+size, fill="red", width = 0)
        self.canvas.create_text(hor-offset, ver, text="GND")
    
    # Clearing Diagram
    def clear(self, Event):
        self.canvas.delete("all")
        self.showBb()

app()