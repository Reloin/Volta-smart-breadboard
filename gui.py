from PyQt5 import QtWidgets, QtCore, QtSvg, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QIcon, QPixmap
from svgpathtools import svg2paths
from functools import partial
import re
import numpy as np
from threading import Thread
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtWidgets import (QApplication, QDialog,
                             QProgressBar, QPushButton)
 
from ui import Ui_MainWindow  # importing our generated file
 
import sys
from range_key_dict import RangeKeyDict
import serial
import time
from switcher import switcher

port = '/dev/cu.usbmodem14101'
rawdata = []
serialstring = ''
data = [] #Array after obtaining mean of 2 resistance values

row = 'abcdefgh'
treading = np.array([1,2])

result = np.array([[1,2,3]]) #final result to be passed to addComponents function

arduino = serial.Serial(port, 9600, timeout=0)

class mywindow(QtWidgets.QMainWindow):
 
    def __init__(self):
    
        global scene

        super(mywindow, self).__init__()
    
        self.ui = Ui_MainWindow()
        
        self.ui.setupUi(self)

        self.progress = QProgressBar(self)
        self.progress.setGeometry(50, 540, 700, 35)
        self.progress.setMaximum(100)

        size = self.getSvgSize('halfBreadboard.svg')
        svg_renderer = QtSvg.QSvgRenderer('halfBreadboard.svg')
        pixmap = QtGui.QImage(size[0], size[1] * 1.2, QtGui.QImage.Format_ARGB32)

        pixmap.fill(0x00000000)
        svg_renderer.render(QtGui.QPainter(pixmap))
        pixmap = QtGui.QPixmap.fromImage(pixmap)
        
        scene.addItem(QGraphicsPixmapItem(pixmap))
        view = self.ui.graphicsView

        view.setScene(scene)
        view.show()

        self.ui.pushButton.clicked.connect(self.btnClicked)
    
    def btnClicked(self): #start identification on button click
        self.main()

    def main(self): #read serial to get resistance and pin
        global count
        global count2
        global treading

        treading = np.array([1,2])
        count = 0

        Worker().run()
        time.sleep(5)
        
        while arduino.readable():
            serialString = arduino.readline().decode()

            reading = np.array([['1', 1]]) #Array of resistance values converted to integers

            if serialString:
                row = serialString.split(' ')
                if serialString.split(' '):
                    if(len(row) > 1):
                        for i in range(len(row)):
                            if i == 0:
                                row[i] = str(row[i])
                            elif i == 1:
                                row[i] = int(row[i])

                        reading = np.vstack((reading, row))
                        
                        reading = np.delete(reading, 0, axis = 0) #delete first array, fak numpy

                        treading = np.vstack((treading, reading))

                    if count == 0:
                        treading = np.delete(treading, 0, axis = 0)
                        
                    rawdata[:] = [] #Empties array
                    serialString = ''
                    if ('1h' in treading): 
                        count2 = 1
                        self.identify()
                        break
                                
            rawdata[:] = [] #Empties array
            serialString = ''
            count += 1

            
            
        else:
            data[:] = []
            reading[:] = []
            serialString = ''
            

    def identify(self): #identify components, pass values to addComponents() to display corresponding components
        global treading
        global result

        result = np.array([[1,2,3]])

        #print(treading)

        r = re.compile("([a-zA-Z]+)([0-9]+)")
        for i in range(len(treading)): #for every row, pin
            for x in range(2): #for the 2 values in each array
                if x == 0:
                        num = re.split('(\d+)', treading[i, 0])[1]
                        pin = re.split('(\d+)', treading[i, 0])[2]
                        if row.index(pin) % 2 == 0: #only calculate average once for each component
                                r1 = int(treading[i, x+1]) #get resistance of current pin
                                if r1 > 0:
                                    if np.where(treading == num + row[row.index(pin)+1])[0].size > 0: #check if a corresponding pin exists\
                                        r2 = int(treading[(np.where(treading == num + row[row.index(pin)+1]))[0], int(np.where(treading == num + row[row.index(pin)+1])[1]) + 1]) #get next pin according to row number, and then get it's resistance value
                                        if r2 != 0:
                                            ravg = (r1 + r2) /2
                                            final = np.array([int(num) - 1, int(row.index(pin) / 2), switcher.get(ravg)]) #add all needed values to a single array
                                            result = np.vstack((result, final)) #add all needed values to result array
                                    if i == 0:
                                        result = np.delete(result, 0, axis = 0) #delete first array in result, can't create a np.array without it
                                    print(result) 
        
        self.addComponents()                            
                                   
        
    def addComponents(self):
        global scene
        global count2
        global result

        for i in range(len(result)): #for every component
            xfactor = result[i, 0]
            yfactor = result[i, 1]
            pin = result[i, 0]
            size = self.getSvgSize(result[i, 2][1])
            svg_renderer = QtSvg.QSvgRenderer(result[i, 2][1])

            pixmap = QtGui.QImage(size[0] / result[i, 2][2], size[1] / result[i, 2][3], QtGui.QImage.Format_ARGB32) #divide image width and height by ratio defined in switcher.py 
            t = QtGui.QTransform()
            t.rotate(90)

            pixmap.fill(0x00000000)
            svg_renderer.render(QtGui.QPainter(pixmap))
            pixmap = QtGui.QPixmap.fromImage(pixmap)
            pixmap = pixmap.transformed(t)
    
            pixmapitem = QGraphicsPixmapItem(pixmap)
            
            scene.addItem(pixmapitem)

            pixmapitem.moveBy(67+19 * xfactor + xfactor * 1.1, 92 + 37.5 * yfactor) 
            
            view = self.ui.graphicsView
            
            view.setScene(scene)
            
            view.show()       
            
            if i == len(result) - 1:
                time.sleep(3)
            
    def getSvgSize(path, attributes): #get dimensions of svg to keep proper aspect ratio
        paths, attributes = svg2paths(attributes)

        # let's take the first path as an example
        mypath = paths[0]

        # Find height, width
        xmin, xmax, ymin, ymax = mypath.bbox()

        results = [mypath.length() * 1.5, (xmax-xmin)*1.5]
        return results
    

class Worker(QThread): #read serial few times before real reading

    countChanged = pyqtSignal(int)

    def run(self):

        timeout = time.time() + 2.5

        while arduino.readable():
            
            arduino.readline().decode()
            
            if time.time() > timeout:
                break            

app = QtWidgets.QApplication([])

count = 0

count2 = 0

scene = QGraphicsScene() 
application = mywindow()
  
application.show()
   
sys.exit(app.exec())