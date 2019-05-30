import numpy as np
import re

row = 'abcdefgh'

a = np.array([ ['1a', 100], ['2a', 200], ['3a', 300] ])

r = re.compile("([a-zA-Z]+)([0-9]+)")

for i in range(len(a)):
    for x in range(2):
        print(a[i, x])
        pin = re.split('(\d+)', a[i, 0])[2]
        print(pin)

print(str(np.where(a == '4a')[0]))