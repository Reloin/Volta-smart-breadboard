from PyQt5 import QtWidgets
import ctypes
import sys

# window properties
window_width = 720
window_heigth = 480
title = 'Smart Breadboard'



#function to make interface to show breadboard

def clicked():
    print('Generate button clicked')

def gui():
    # make window centered
    user32 = ctypes.windll.user32
    xPos = (user32.GetSystemMetrics(0) - window_width)/2
    yPos = (user32.GetSystemMetrics(1) - window_heigth)/2
    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QMainWindow()
    win.setGeometry(xPos, yPos, window_width, window_heigth)
    win.setWindowTitle(title)

    # set the Generate button
    gnrBtn = QtWidgets.QPushButton(win)
    gnrBtn.setText('Generate')
    gnrBtn.clicked.connect()

    # make wiindow shows up
    win.show()
    sys.exit(app.exec_())