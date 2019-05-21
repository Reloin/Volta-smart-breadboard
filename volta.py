from range_key_dict import RangeKeyDict
import serial
import time

port = 'COM3'
rawdata = []
serialstring = ''
reading = [] #Array of resistance values converted to integers
data = [] #Array after obtaining mean of 2 resistance values
count = 0

try:
    arduino = serial.Serial(port, 9600, timeout=0)
except:
    print('Please check port ' + port)

while serial.readline():
    rawdata.append(str(serial.readline()))
    serialString = " ".join(rawdata)
    serialString = serialString.split('= ')[2]
    reading.append(int(serialString))
    if count & 1:
        mean = (reading[count] + reading[count + 1]) / 2
        data.append(mean)
        identify(mean, count)
    print(data)
    rawdata[:] = [] #Empties array
    serialString = ''
    time.sleep(500)
    count += 1
else:
    data[:] = []
    reading[:] = []
    serialString = ''
    count = 0

def identify(resistance, count):
    count -= 1
    switcher = RangeKeyDict({
        range(0, 100): '100 Ohm Resistor', #Add range of resistance values for different components
        range(100, 200): 'Button'
    })
    print(switcher.get(resistance))



