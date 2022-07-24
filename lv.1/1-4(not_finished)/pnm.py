class IsInteger(Exception):
    pass

class IsNotSingleLen(Exception):
    pass

def cnv(i): # convert char -> byte or int -> byte
    try:
        if i.isdigit(): None
        return bytes([ord(i)])
    except:
        return bytes([int(i)])

    
TAB = 9
ENT = 10
SPC = 32

header = []
size = []
color = ['2', '5', '5']
rows = []

arr = ['P', '6', ENT, '3', '2', SPC, '2', ENT, '2', '5', '5', ENT, 255, 0, 0, 0, 255, 0, 0, 0, 255, 125, 125, 125, 255, 255, 255, 0, 0, 0]
f = open("test.ppm", 'wb')
for data in arr:
    f.write(cnv(data))
f.close()
