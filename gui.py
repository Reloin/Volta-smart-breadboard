from PyQt5 import QtWidgets, QtCore, QtSvg, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QIcon, QPixmap
from svgpathtools import svg2paths
from functools import partial
import re
import numpy as np
 
from ui import Ui_MainWindow  # importing our generated file
 
import sys
from range_key_dict import RangeKeyDict
import serial
import time
from switcher import switcher

port = 'COM3'
rawdata = []
serialstring = ''
data = [] #Array after obtaining mean of 2 resistance values
count = 0
row = 'abcdefgh'

#arduino = serial.Serial(port, 9600, timeout=0)

class mywindow(QtWidgets.QMainWindow):
 
    def __init__(self):
    
        global scene

        super(mywindow, self).__init__()
    
        self.ui = Ui_MainWindow()
        
        self.ui.setupUi(self)

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
        while arduino.readline():
            rawdata.append(str(arduino.readline()))
            serialString = " ".join(rawdata)
            
            dataString = serialString.split(' ')[1]

            reading = np.array() #Array of resistance values converted to integers

            row = serialString().split(' ')
            if serialString().split(' ')[1]:
                for i in range(len(row)):
                    if i & 1:
                        row[i] = str(row[i])
                    else:
                        row[i] = int(row[i])
                reading.append(reading, row)
                reading = np.delete(reading, 0, axis = 0)

            

            r = re.compile("([a-zA-Z]+)([0-9]+)")
            pin = r.match(serialString.split(' ')[0])
            pin = int (pin.group(0))

            if count % 2 == 0: #only calculate mean on second pin
                mean = (reading[count] + reading[count + 1]) / 2
                data.append(mean)
                self.identify(partial(self, mean, pin))
            print(serialString.split(' ')[0] + data)
            rawdata[:] = [] #Empties array
            serialString = ''
            time.sleep(500)
            count += 1
        else:
            data[:] = []
            reading[:] = []
            serialString = ''
            count = 0

            if(len(reading) > 0):
                self.test(reading)

    def test(self, reading):
        global row
        for i in range(len(reading)/2):
            for x in range(2):
                row.index([i, 2])                

    def identify(self, resistance, pin): #identify components, pass values to addComponents() to display corresponding components
        global count
        count -= 1
        result = switcher.get(resistance)
        path = switcher.get(resistance)[1]
        self.addComponents(partial(self, path, result, pin))
        
    def addComponents(self, path, dictsize, pin):
        global xposition
        global scene
        global yposition
        size = self.getSvgSize(path)
        svg_renderer = QtSvg.QSvgRenderer(path)

        pixmap = QtGui.QImage(size[0] / dictsize[3], size[1] / dictsize[4], QtGui.QImage.Format_ARGB32) #divide image width and height by ratio defined in switcher.py 
        t = QtGui.QTransform()
        t.rotate(90)

        pixmap.fill(0x00000000)
        svg_renderer.render(QtGui.QPainter(pixmap))
        pixmap = QtGui.QPixmap.fromImage(pixmap)
        pixmap = pixmap.transformed(t)
    
        pixmapitem = QGraphicsPixmapItem(pixmap)
        
        scene.addItem(pixmapitem)

        if pin & 1 and pin > 1:
            yposition += 37

        pixmapitem.moveBy(67+19 * xposition + xposition * 1.1, 92 + yposition) 
        
        view = self.ui.graphicsView
        
        view.setScene(scene)
        
        view.show()
        xposition += 1

    def getSvgSize(path, attributes): #get dimensions of svg to keep proper aspect ratio
        paths, attributes = svg2paths(attributes)

        # let's take the first path as an example
        mypath = paths[0]

        # Find height, width
        xmin, xmax, ymin, ymax = mypath.bbox()

        results = [mypath.length() * 1.5, (xmax-xmin)*1.5]
        return results
    
app = QtWidgets.QApplication([])

xposition = 0 
yposition = 0
scene = QGraphicsScene() 
application = mywindow()
  
application.show()
   
sys.exit(app.exec())