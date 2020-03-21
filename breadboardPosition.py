# to change breadboard position to pixel

def code2pos(hor, ver):
    cor = [0, 0]
    cor[0] = hor * 24 + 112 # for horizontal x = 24n + 112
    cor[1] = ver * 30 + 163 # for vertical y = 30n + 163
    
    
    return cor