import serial
import numpy as np
import time
import identifier as idpy

com = 'COM3'
baudRate = 9600
row = 6
column = 8
go = False

class readArduino():
    def __init__(self):
        try:
            self.ser = serial.Serial(port=com, baudrate=baudRate)
            go = True
            #time.sleep()
        except:
            print("Serial unavailable")

    # read and label data
    def read_data(self):
        #initiate data for storage
        data = np.zeros((row, column), dtype=object)
        # hash table for component identification
        table = {
            'r':{
                'pair': False,
                'count': 1
            },
            'l':{
                'pair': False,
                'count': 1
            }
        }

        # where to start read data, s for start
        d = self.element()
        while(d != "S"):
            d = self.element()
        d = self.element()

        # T for terminate, if not received then continue
        while(d != "T"):
            x, y, val = d.split(';')
            component = idpy.identify(int(val)) # return what typr of component it is
            data[int(x)][int(y)] = component + str(table[component]['count']) + ('b' if table[component]['pair'] else 'a')

            if table[component]['pair'] : 
                table[component]['pair'] = False
                table[component]['count'] += 1
            else:
                table[component]['pair'] = True
            d = self.element()
        return data


    # method to read and decode data
    def element(self):
        rawData = self.ser.readline()
        rawData = rawData.decode()
        rawData = rawData.strip()
        return rawData

r = readArduino()
print(r.read_data())
