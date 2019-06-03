from range_key_dict import RangeKeyDict
import serial
import time
import numpy as np
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)
port = '/dev/cu.usbmodem14101'
rawdata = []
serialstring = ''
reading = [] #Array of resistance values converted to integers
data = [] #Array after obtaining mean of 2 resistance values
count = 0
i = 0

arduino = serial.Serial(port, 9600)
treading = np.array([[1,1]])

while arduino.readable():
    serialString = arduino.readline().decode()
    reading = np.array([['1', 1]]) #Array of resistance values converted to integers

    row = serialString.split(' ')
    if serialString.split(' ')[1]:
        for i in range(len(row)):
            if i == 0:
                row[i] = str(row[i])
            elif i == 1:
                row[i] = int(row[i])
               
        reading = np.vstack((reading, row))
             
        reading = np.delete(reading, 0, axis = 0) #delete first array, fak numpy
                
        treading = np.vstack((treading, reading))
        if count == 0:
            treading = np.delete(treading, 0, axis = 0)
            
        rawdata[:] = [] #Empties array
        serialString = ''

        count += 1

        if ('1h' in treading):
            print("Reading: " + str(i))
            print(treading)    
            treading = np.array([[1,1]])
            count = 0
    i += 1
        

