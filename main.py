# Python program that show components connected to breadboar

from PyQt5 import QtWidgets, QtSvg
import drawDiagram
import ctypes
import sys
import serial


port = 'com3'
baudRate = 9600
arduino = serial.Serial(port, baudrate = baudRate, timeout = 1)

# window properties
window_width = 720
window_heigth = 480
btn_width = 200
btn_height = 50
title = 'Smart Breadboard'



def clicked():
    data = arduino.readline().decode('ascii')
    print(data)

#function to make interface to show breadboard
def gui():
    # make window centered
    user32 = ctypes.windll.user32
    xPos = (user32.GetSystemMetrics(0) - window_width)/2
    yPos = (user32.GetSystemMetrics(1) - window_heigth)/2
    # make ui
    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QMainWindow()
    win.setGeometry(xPos, yPos, window_width, window_heigth)
    win.setWindowTitle(title)

    # display breadboard
    bbsvg = QtSvg.QSvgWidget('svg/breadboard.svg', win)
    bbsvg.setGeometry(150, -150, 880, 600)
    bbsvg.show()
    # set the Generate button
    gnrBtn = QtWidgets.QPushButton(win)
    gnrBtn.setText('Generate')
    xBtn = (window_width - btn_width ) / 2
    gnrBtn.setGeometry(xBtn, 350, btn_width, btn_height)
    gnrBtn.clicked.connect(clicked)

    # make wiindow shows up
    win.show()
    sys.exit(app.exec_())
    
gui()
