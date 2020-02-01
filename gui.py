# Python program that show components connected to breadboar

from PyQt5 import QtWidgets, QtSvg
import ctypes
import sys
#import readData


# window properties
window_width = 720
window_heigth = 550
btn_width = 200
btn_height = 50
title = 'Smart Breadboard'

class ui_window(object):
    def __init__(self):
        # make window centered
        user32 = ctypes.windll.user32
        xPos = (user32.GetSystemMetrics(0) - window_width)/2
        yPos = (user32.GetSystemMetrics(1) - window_heigth)/2
        # make ui
        self.app = QtWidgets.QApplication(sys.argv)
        self.win = QtWidgets.QMainWindow()
        self.win.setGeometry(xPos, yPos, window_width, window_heigth)
        self.win.setWindowTitle(title)

        # display breadboard
        self.bbsvg = QtSvg.QSvgWidget('svg/breadboard.svg', self.win)
        self.bbsvg.setGeometry(20, 20, 1300, 400)
        self.bbsvg.show()
        
        # set the Generate button
        self.gnrBtn = QtWidgets.QPushButton(self.win)
        self.gnrBtn.setText('Generate')
        xBtn = (window_width - btn_width ) / 2
        self.gnrBtn.setGeometry(xBtn, 475, btn_width, btn_height)
        self.gnrBtn.clicked.connect(self.clicked)

        # make wiindow shows up
        self.win.show()
        sys.exit(self.app.exec_())
    
    def clicked(self):
        #readData.read()
        print('reading')
