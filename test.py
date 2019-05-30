import sys
from PyQt5 import QtGui, QtSvg, QtWidgets

app = QtWidgets.QApplication(sys.argv) 

svgWidget = QtSvg.QSvgWidget('halfBreadboard.svg')

svgWidget.show()


sys.exit(app.exec_())