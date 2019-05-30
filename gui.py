from PyQt5 import QtWidgets, QtCore, QtSvg, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QIcon, QPixmap
from svgpathtools import svg2paths
from functools import partial
 
from ui import Ui_MainWindow  # importing our generated file
 
import sys


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
    
    def btnClicked(self):
        self.addComponents()
        
    def addComponents(self):
        global i
        global scene
        size = self.getSvgSize('resistor_220.svg')
        svg_renderer = QtSvg.QSvgRenderer('resistor_220.svg')

        pixmap = QtGui.QImage(size[0] / 2.2, size[1] /6, QtGui.QImage.Format_ARGB32)
        t = QtGui.QTransform()
        t.rotate(90)

        pixmap.fill(0x00000000)
        svg_renderer.render(QtGui.QPainter(pixmap))
        pixmap = QtGui.QPixmap.fromImage(pixmap)
        pixmap = pixmap.transformed(t)
    
        pixmapitem = QGraphicsPixmapItem(pixmap)
        
        scene.addItem(pixmapitem)
        pixmapitem.moveBy(67+19 * i + i * 1.1,92)
        
        view = self.ui.graphicsView
        
        view.setScene(scene)
        
        view.show()
        i += 1

    def getSvgSize(path, attributes):
        paths, attributes = svg2paths(attributes)

        # let's take the first path as an example
        mypath = paths[0]

        # Find height, width
        xmin, xmax, ymin, ymax = mypath.bbox()

        results = [mypath.length() * 1.5, (xmax-xmin)*1.5]
        return results
    
app = QtWidgets.QApplication([])

i = 0
scene = QGraphicsScene() 
application = mywindow()
  
application.show()
   
sys.exit(app.exec())