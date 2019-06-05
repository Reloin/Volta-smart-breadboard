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
from rrange import rrange
from lxml import etree

port = 'COM4'
rawdata = []
serialstring = ''
data = [] #Array after obtaining mean of 2 resistance values

row = 'ABCDEFGH'
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
        pixmap = QtGui.QImage(size[0] * 2.5, size[1] * 2.3 , QtGui.QImage.Format_ARGB32)

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
                    if ('2H' in treading): 
                        #print(treading)
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

        result = np.array([[1,2,3,4,5,6]]) #[xfactor, yfactor, xlength, ylength, orientation, switcher result]

        pair = np.array(['1', '1']) #[pin1, pin2]

        #print(treading)

        r = re.compile("([a-zA-Z]+)([0-9]+)")
        for i in range(len(treading)): #for every row, pin
               
                for x in range(2): #for the 2 values in each array
                    if x == 0:

                        r1 = int(treading[i, x+1]) #get resistance of current pin
                            
                        num = re.split('(\d+)', treading[i, 0])[1]
                        pin = re.split('(\d+)', treading[i, 0])[2]

                        if r1 > 0:

                            if(np.where(pair == str(treading[(np.where(treading == str(r1)))[0], 0][0]))[0].size == 0): #check if pin 1 paired to another pin before
                                #if np.where(treading == num + row[row.index(pin)+1])[0].size > 0: #check if a corresponding pin exists

                                    r2range = rrange.get(r1)[0]
                                    #print(r2range)

                                    r2 = 0
                                    r3 = 0

                                    for z in range(2):
                                        for y in range(8):
                                            if row.index(pin) + y < 8: #only start reading from E
                                                r2 = int(treading[(np.where(treading == str(int(num) + z) + row[row.index(pin)+ y]))[0], 1])
                                                if r2 in r2range:   
                                                    if(np.where(pair == str(treading[(np.where(treading == str(r2)))[0], 0][0]))[0].size == 0): #check if pin 2 paired to another pin before
                                                        r3 = r2
                                                        #print(r2)
                                                        break  
                                        if r3 > 0:
                                            ravg = (r1 + r3) /2
                                            currentpin = str(treading[(np.where(treading == str(r3)))[0], 0][0])
                                            temppair = np.array([str(treading[i, 0]), currentpin])
                                            p1 = re.split('(\d+)', treading[i, 0]) #find orientation
                                            p2 = re.split('(\d+)', currentpin)
                                            if p1[1] == p2[1]:
                                                orientation = 0 #horizontal
                                            elif p1[2] == p2[2]:
                                                orientation = 1 #vertical
                                            else:
                                                orientation = 2 #diagonal

                                            if int(p2[1]) - int(p1[1]) > 0 or row.index(p2[2]) - row.index(p1[2]) > 1:
                                                xlength = int(p2[1]) - int(p1[1])
                                                ylength = row.index(p2[2]) - row.index(p1[2])
                                                yfactor = float(row.index(pin) / 2)
                                                if row.index(pin) > 4:
                                                    yfactor += 1.05
                                                final = np.array([int(num) - 1, yfactor, xlength, ylength, orientation, switcher.get(ravg)]) #add all needed values to a single array
                                                result = np.vstack((result, final)) #add all needed values to result array
                                            else: 
                                                print("Error")
                                            pair = np.vstack((pair, temppair))
                                            break
                                                     
                                
                if i == 0:
                    
                    result = np.delete(result, 0, axis = 0) #delete first array in result, can't create a np.array without it
                        
        print(result)
        print(pair)
        self.addComponents()                            
                                   
        
    def addComponents(self):
        global scene
        global count2
        global result

        for i in range(len(result)): #for every component
            xfactor = result[i, 0]
            yfactor = result[i, 1]
            pin = result[i, 0]

            if result[i, 3] <= 1:
                size = self.getSvgSize(result[i, 5][1])
                svg_renderer = QtSvg.QSvgRenderer(result[i, 5][1])

                pixmap = QtGui.QImage(size[0] * 91, size[1] * 90, QtGui.QImage.Format_ARGB32) #divide image width and height by ratio defined in switcher.py 
                t = QtGui.QTransform()
                if result[i, 4] == 0:
                    t.rotate(90)

                pixmap.fill(0x00000000)
                svg_renderer.render(QtGui.QPainter(pixmap))
                pixmap = QtGui.QPixmap.fromImage(pixmap)
                pixmap = pixmap.transformed(t)
        
                pixmapitem = QGraphicsPixmapItem(pixmap)
                
                scene.addItem(pixmapitem)

                pixmapitem.moveBy(60 + 17.7 * xfactor + xfactor * 1.1, 79 + 35 * yfactor) 
            
            else:
                filename = result[i, 5][1]
                tree = etree.parse(open(filename, 'r'))

                for element in tree.iter():
                    if element.tag.split("}")[1] == "svg":
                        element.set("width", str(0.42917 + 0.18 * result[i, 3]) + "in")
                        for g in range(4):
                            if g == 1:
                                x = re.split('(\d+)', element.get("width"))[g]
                            elif g > 1:
                                x = x + re.split('(\d+)', element.get("width"))[g]

                        for z in range(4):
                            if z == 1:
                                y = re.split('(\d+)', element.get("height"))[z]
                            elif z > 1:
                                y = y + re.split('(\d+)', element.get("height"))[z]

                        element.set("viewBox", str(0 - 9 * result[i, 3]) + " 0 " + str(42.917 + 18 * result[i, 3]) + " " +  str(7*3))
                        
                    if element.tag.split("}")[1] == "line":
                        if element.get("id") == "connector0leg":
                            element.set("x1", str(1.455 - 9 * result[i, 3]))
                        if element.get("id") == "connector1leg":
                            element.set("x2", str(40.007 + 9 * result[i, 3]))

                new_svg = etree.tostring(tree)

                svg_renderer = QtSvg.QSvgRenderer(new_svg)

                size = [float(x) * 91, float(y) * 90]
                print(size)

                pixmap = QtGui.QImage(size[0], size[1] * 2, QtGui.QImage.Format_ARGB32) #divide image width and height by ratio defined in switcher.py 
                t = QtGui.QTransform()
                if result[i, 4] == 0:
                    t.rotate(90)

                pixmap.fill(0x00000000)
                svg_renderer.render(QtGui.QPainter(pixmap))
                pixmap = QtGui.QPixmap.fromImage(pixmap)
                pixmap = pixmap.transformed(t)
        
                pixmapitem = QGraphicsPixmapItem(pixmap)
                
                scene.addItem(pixmapitem)

                pixmapitem.moveBy(50 + 17 * xfactor + xfactor * 1.1, 79.5 + 35 * yfactor) 
                
            view = self.ui.graphicsView
                
            view.setScene(scene)
                
            view.show()       
            
            if i == len(result) - 1:
                time.sleep(3)
            
    def getSvgSize(path, attributes): #get dimensions of svg to keep proper aspect ratio

        filename = attributes
        tree = etree.parse(open(filename, 'r'))

        for elem in tree.iter():
            if elem.tag.split("}")[1] == "svg":
                for i in range(4):
                    if i == 1:
                        x = re.split('(\d+)', elem.get("width"))[i]
                    elif i > 1:
                        x = x + re.split('(\d+)', elem.get("width"))[i]

                for z in range(4):
                    if z == 1:
                        y = re.split('(\d+)', elem.get("height"))[z]
                    elif z > 1:
                        y = y + re.split('(\d+)', elem.get("height"))[z]

        results = [float(x), float(y)]
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