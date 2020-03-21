
# value range for all component identifiable
err = 50 # false positive
res = (500, 600) #resistor
vcc = (100,200) #Vcc
gnd = (201,300) #Gnd

def identify(val):
    if val < err : return None
    elif res[0] <= val <= res[1]: return "res"
    elif vcc[0] <= val <= vcc[1]: return "vcc"
    elif gnd[0] <= val <= gnd[1]: return "gnd"


