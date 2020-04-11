"""
this python file does 2 things currently
1. convert raw data to word
2. convert pin location to pixel coordinate
"""
# value range for all component identifiable
res_a = (500, 550) #resistor
res_b = (551, 600)
vcc = (100,200) #Vcc
gnd = (201,300) #Gnd
led_an = (301, 350)
led_cat = (351, 400)

def identify(val):
    if res_a[0] <= val <= res_a[1]: return "ra"
    elif res_b[0] <= val <= res_b[1]: return "rc"
    elif vcc[0] <= val <= vcc[1]: return "+"
    elif gnd[0] <= val <= gnd[1]: return "-"
    elif led_an[0] <= val <= led_an[1]: return "la"
    elif led_cat[0] <= val <= led_cat[1]: return "lc"
    else:return "."

# to change breadboard position to pixel
def cor2pos(hor, ver):
    x = hor * 24 + 136.5 # for horizontal x = 24n + 136.5, 1 to infinity
    if ver < 4 : y = 477.5 - ver * 28.5 # for vertical y = 30n + 163
    else: y = 306 - (ver - 4) * 28.5 # for b to e

    return x, y

def component_pos(a, b):
    hor, ver = abs(b[0] - a[0])/2, abs(b[1]-a[1])/2
    x = hor * 24 + 141.5 # for horizontal x = 24n + 136.5, 1 to infinity
    if hor < 3 : y = 484.5 - ver * 28.5 # for vertical y = y = 477.5 - 28.5n
    else: y = 306 - (ver - 4) * 28.5 # for b to e

    return (x, y)