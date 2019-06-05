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
import sys
from lxml import etree 

from ui import Ui_MainWindow  # importing our generated file
 

class mywindow(QtWidgets.QMainWindow):
 
    def __init__(self):
    
        global scene

        super(mywindow, self).__init__()
    
        self.ui = Ui_MainWindow()
        
        self.ui.setupUi(self)

        self.progress = QProgressBar(self)
        self.progress.setGeometry(50, 540, 700, 35)
        self.progress.setMaximum(100)

        filename = "resistor_220.svg"
        tree = etree.parse(open(filename, 'r'))

        for element in tree.iter():
                    if element.tag.split("}")[1] == "svg":
                        element.set("width", str(0.42917 * 0.7 * 3) + "in")
                        for i in range(4):
                            if i == 1:
                                x = re.split('(\d+)', element.get("width"))[i]
                            elif i > 1:
                                x = x + re.split('(\d+)', element.get("width"))[i]

                        element.set("height", str(0.0971 * 0.75 * 3) + "in")
                        for z in range(4):
                            if z == 1:
                                y = re.split('(\d+)', element.get("height"))[z]
                            elif z > 1:
                                y = y + re.split('(\d+)', element.get("height"))[z]
                        
                        element.set("viewBox", str(0 - 9 * 3) + " 0 " + str(42.917 + 18 * 3) + " " + str(7*3) )
                        size = [float(x), float(y)]
                        
                    if element.tag.split("}")[1] == "line":
                        if element.get("id") == "connector0leg":
                            element.set("x1", str(1.455 - 9 * 3))
                        if element.get("id") == "connector1leg":
                            element.set("x2", str(40.007 + 9 * 3))

        new_svg = etree.tostring(tree)
        print(size)
        svg_renderer = QtSvg.QSvgRenderer(new_svg)
        pixmap = QtGui.QImage(size[0] * 100, size[1] * 100, QtGui.QImage.Format_ARGB32)

        pixmap.fill(0x00000000)
        svg_renderer.render(QtGui.QPainter(pixmap))
        pixmap = QtGui.QPixmap.fromImage(pixmap)
        
        scene.addItem(QGraphicsPixmapItem(pixmap))

        size = self.getSvgSize('resistor_220.svg')
        svg_renderer = QtSvg.QSvgRenderer('resistor_220.svg')
        pixmap = QtGui.QImage(size[0] * 100, size[1] * 100, QtGui.QImage.Format_ARGB32)

        pixmap.fill(0x00000000)
        svg_renderer.render(QtGui.QPainter(pixmap))
        pixmap = QtGui.QPixmap.fromImage(pixmap)

        pixmapitem = QGraphicsPixmapItem(pixmap)
        
        scene.addItem(pixmapitem)

        pixmapitem.moveBy(167, 0) 

        view = self.ui.graphicsView

        view.setScene(scene)
        view.show()

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

app = QtWidgets.QApplication([])

scene = QGraphicsScene() 
application = mywindow()
  
application.show()
   
sys.exit(app.exec())