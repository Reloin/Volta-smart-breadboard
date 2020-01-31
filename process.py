import serial


row, column = 3, 8
reading = [[0 for x in range(column)] for y in range(row)]

port = 'com3'
baudRate = 9600
#arduino = serial.Serial(port, baudrate = baudRate, timeout = 1)

#def read():
#    for y in range(row):
#        for x in range(column):
#            reading[x][y] = arduino.read()
            
def read():
    data = [[0, 0, 100, 0, 0, 0, 100, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
    return data