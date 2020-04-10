
# value range for all component identifiable
err = 50 # false positive
res = (500, 600) #resistor
vcc = (100,200) #Vcc
gnd = (201,300) #Gnd
led = (301, 400)

def identify(val):
    if val < err : return "."
    elif res[0] <= val <= res[1]: return "r"
    elif vcc[0] <= val <= vcc[1]: return "+"
    elif gnd[0] <= val <= gnd[1]: return "-"
    elif led[0] <= val <= led[1]: return "l"
    else:return "."

# to change breadboard position to pixel
def code2pos(hor, ver):
    cor = [0, 0]
    cor[0] = hor * 24 + 112 # for horizontal x = 24n + 112
    cor[1] = ver * 30 + 163 # for vertical y = 30n + 163
    
    return cor
