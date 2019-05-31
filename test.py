import numpy as np
import re

row = 'abcdefgh'

a = np.array([ ['1a', 100], ['1c', 200], ['1f', 300], ['1h', 300], ['3e', 400], ['3f', 500]])

b = ['220 Ohm Resistor', 'resistor_220.svg', 1.8, 5]

result = np.array([[1,2,3]]) #final result to be passed to identify function

r = re.compile("([a-zA-Z]+)([0-9]+)")

for i in range(len(a)): #for every row, pin
    for x in range(2): #for the 2 values in each array
        if x == 0:
                num = re.split('(\d+)', a[i, 0])[1]
                pin = re.split('(\d+)', a[i, 0])[2]
                if row.index(pin) % 2 == 0: #only calculate average once for each component
                        r1 = int(a[i, x+1]) #get resistance of current pin
                        if np.where(a == num + row[row.index(pin)+1])[0].size > 0:
                                r2 = int(a[(np.where(a == num + row[row.index(pin)+1]))[0], int(np.where(a == num + row[row.index(pin)+1])[1]) + 1]) #get next pin according to row number, and then get it's resistance value
                                ravg = (r1 + r2) /2
                                final = np.array([int(num) - 1, int(row.index(pin) / 2), b]) #add all needed values to a single array
                                result = np.vstack((result, final)) #add all needed values to result array
                        if i == 0:
                                result = np.delete(result, 0, axis = 0) #delete first array in result, can't create a np.array without it
                                
print(result)