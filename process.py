import serial
import numpy as np
import time
import identifier as idpy

com = 'COM4'
baudRate = 9600
row = 2
column = 8

class readArduino():
    def __init__(self):
        try:
            self.ser = serial.Serial(port=com, baudrate=baudRate)
            #time.sleep()
        except:
            print("Serial unavailable")

    # pass breadboard size
    def get_size(self):
        return row, column

    # read and label data
    def read_data(self):
        #initiate data for storage
        data = []
        # hash table for component identification
        table = {}

        # where to start read data, s for start
        d = self.element()
        while(d != "S"):
            d = self.element()
        d = self.element()

        # T for terminate, if not received then continue
        while(d != "T"):
            x, y, val = d.split(';')
            component = idpy.identify(int(val)) # return what typr of component it is
            if component in ("+", "-"): data.append(x+ ','+ y + ','+ component)
            else:
                if component not in table :  table[component] = 1
                data.append(x+ ','+ y + ','+ component + str(table[component]))
                table[component] += 1
            d = self.element()


        return data


    # method to read and decode data
    def element(self):
        rawData = self.ser.readline()
        rawData = rawData.decode('unicode_escape')
        rawData = rawData.strip()
        print(rawData)
        return rawData