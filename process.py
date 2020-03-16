import serial
import numpy as np
import time

com = 'COM3'
baudRate = 9600
row = 8
column = 6
data = np.zeros((row, column), dtype=int)

class readArduino:
    def __init__(self):
        try:
            self.ser = serial.Serial(com, baudRate)
            #time.sleep()
        except:
            print("Serial unavailable")
        
    def read(self):
        rawData = self.ser.readline()
        rawData = rawData.decode()
        while(rawData.strip() == "S"):
            for y in range(column):
                for x in range(row):
                    rawData = self.ser.readline()
                    rawData = rawData.decode()
                    data[x, y] = int(rawData.strip())
            return data
        
r = readArduino()
while(True):
    print(r.read())
    time.sleep(2)