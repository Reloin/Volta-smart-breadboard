import sys
from PyQt5 import QtGui, QtSvg, QtWidgets
from range_key_dict import RangeKeyDict

rrange = RangeKeyDict({
    (110, 125): [range(100, 110), 'Button Positive'], #Add range of resistance values for different components in the form [Positive/Negative range, Component name + polarity]
    (100, 110): [range(110, 121), 'Button Negative'],
    (190, 200): [range(50, 60), '220 Ohm Resistor Positive'],
    (50, 60): [range(190, 200), '220 Ohm Resistor Positive'],
})