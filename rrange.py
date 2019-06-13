import sys
from PyQt5 import QtGui, QtSvg, QtWidgets
from range_key_dict import RangeKeyDict

rrange = RangeKeyDict({
    (110, 125): [range(100, 110), 'Button Positive'], #Add range of resistance values for different components in the form [Positive/Negative range, Component name + polarity]
    (100, 110): [range(110, 125), 'Button Negative'],
    (185, 210): [range(350, 400), '220 Ohm Resistor Positive'],
    (350, 400): [range(185, 210), '220 Ohm Resistor Positive'],
})