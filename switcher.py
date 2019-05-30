import sys
from PyQt5 import QtGui, QtSvg, QtWidgets
from range_key_dict import RangeKeyDict

switcher = RangeKeyDict({
    (0, 100): ['220 Ohm Resistor', 'resistor_220.svg', 1.8, 5], #Add range of resistance values for different components in the form [Name of component, svg path, size to divide in x, size to divide in y]
    (100, 200): ['Button', '.svg', 1.8, 5]
})