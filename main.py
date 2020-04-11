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
        table = {}
        r = process.readArduino()
        data = r.read_data()
        for pin in data:
            # retrive and process data
            x, y, code = pin.split(",")
            x, y = int(x), int(y)
            # for pins
            if code in ("+", "-"): self.power(code, x,y)
            else: code = code[0] + code [2:]

            #for components with more than 1 pin
            if code in table:
                self.identify(code, (x, y), table[code])
                table.pop(code)
            else: table[code] = (x, y)
    


    #below here are functions for drawing all stuff

    # put code for component and draw on screen
    def identify(self, code, a, b):
        temp = code[0]
        if temp == 'r': self.draw_resistor(a,b)
        elif temp == 'w': self.wire(a, b)

    #function for showing breadboard
    def showBb(self):
        self.bbImg = ImageTk.PhotoImage(Image.open("svg/breadboard.png"))
        self.canvas.create_image(bbPos, image=self.bbImg)
    
    # draw resistor
    def draw_resistor(self, a, b):
        self.resistor = ImageTk.PhotoImage(Image.open("svg/resistor.png"))
        r_off = 25
        l_off = 29
        off_y = -3
        loc = idpy.component_pos(a, b)
        self.canvas.create_image(loc, image=self.resistor)
        self.pin_wire(a[0], a[1], loc[0] + r_off, loc[1] + off_y)
        self.pin_wire(b[0], b[1], loc[0] - l_off, loc[1] + off_y)

    # Function for drawing wire
    def pin_wire(self, ax, ay, bx, by):
        ax, ay = idpy.cor2pos(ax, ay)
        if ax == bx or ay == by:
            self.canvas.create_line(ax,ay,bx,by, fill="green", width=5)
        else:
            self.canvas.create_line(ax,ay,ax,by, fill="green", width=5)
            self.canvas.create_line(ax,by,bx,by, fill="green", width=5)

    def wire(self, a, b):
        ax, ay = idpy.cor2pos(a[0], a[1])
        bx, by = idpy.cor2pos(b[0], b[1])
        if ax == bx or ay == by:
            self.canvas.create_line(ax,ay,bx,by, fill="green", width=5)
        else:
            self.canvas.create_line(ax,ay,ax,by, fill="green", width=5)
            self.canvas.create_line(ax,by,bx,by, fill="green", width=5)

    # draw anode and cathode dot on board
    def power(self,code, x, y):
        size = 6
        offset = 20
        color = 'black' if code == '-' else 'red'
        text = 'Gnd' if code == '-' else 'Vcc'
        hor, ver = idpy.cor2pos(x,y)
        self.canvas.create_oval(hor-size,ver-size,hor+size,ver+size, fill=color, width = 0)
        self.canvas.create_text(hor-offset, ver, text=text)
    
    # Clearing Diagram
    def clear(self, Event):
        self.canvas.delete("all")
        self.showBb()

app()