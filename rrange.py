import sys
from PyQt5 import QtGui, QtSvg, QtWidgets
from range_key_dict import RangeKeyDict

rrange = RangeKeyDict({
    (110, 125): [range(100, 110), 'Button Positive'], #Add range of resistance values for different components in the form [Positive/Negative range, Component name + polarity]
    (100, 110): [range(110, 125), 'Button Negative'],
    (490, 500): [range(670, 680), '220 Ohm Resistor Positive'],
    (670, 680): [range(490, 500), '220 Ohm Resistor Positive'],
})