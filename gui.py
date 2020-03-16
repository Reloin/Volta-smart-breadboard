# Python program that show components connected to breadboar

from tkinter import *

#import readData


# window properties
window_width = 720
window_heigth = 550
btn_width = 200
btn_height = 50
title = 'Smart Breadboard'

class ui_window(Frame):
    def __init__(self):
        super().__init__()
        
        self.initUI()
    
    def wire(self):
        self.canvas.create_line(0,0, 500, 500, fill='black', width=2)
    
    def initUI(self):
        self.win = Tk()
        self.canvas = Canvas(self.win, width = window_width, height = window_heigth, background='white')
        self.canvas.grid(row=0, column=0)
        
        gnrBtn = Button(self.win, text="Generate", command="wire", padx=50)
        gnrBtn.grid(row=1, column=0)
        
        self.win.mainloop()
        
    
def main():
    