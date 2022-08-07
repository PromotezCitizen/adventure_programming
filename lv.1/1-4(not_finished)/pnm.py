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

PPM = 'P6'
PGM = 'P5'

# 기본 구분자는 0x0A

# 확장자 / col / row / color_scale

filename = 'airplane.pgm'
with open('files/' + filename, 'rb') as f:
    file = list(f.read())

print(len(file))
# ==============================
header = []
header.append(file.pop(0))
header.append(file.pop(0))
# ==============================
if file.pop(0) == 0x0D: # 구분자 제거
    file.pop(0)
# ==============================
img_col = []
img_col.append(file.pop(0))
while img_col[-1] != 0x20 and img_col[-1] != 0x0D and img_col[-1] != 0x0A:
    img_col.append(file.pop(0))
if img_col.pop(-1) == 0x0D:
    file.pop(0)

img_row = []
img_row.append(file.pop(0))
while img_row[-1] != 0x20 and img_row[-1] != 0x0D and img_row[-1] != 0x0A:
    img_row.append(file.pop(0))
if img_row.pop(-1) == 0x0D:
    file.pop(0)
# ==============================
color_scale = []
color_scale.append(file.pop(0))
while color_scale[-1] != 0x0D and color_scale[-1] != 0x0A:
    color_scale.append(file.pop(0))
if color_scale.pop(-1) == 0x0D:
    file.pop(0)
# ==============================
f = lambda x: ''.join([ chr(dat) for dat in x ])

rgb_channel = 1 if f(header) == PGM else 3
print(int(f(img_col)) * int(f(img_row)) == len(file)/rgb_channel)

print(file[0:10])

for idx in range(len(file)):
    file[idx] = 0xFF - file[idx]

print(file[0:10])

output = 'output.' + ('pgm' if rgb_channel == 1 else 'ppm')


def write(f, list):
    for data in list:
        f.write(bytes([data]))

print("format:{0}\ncol:{1} row:{2}\ncolor scale:{3}".format(f(header), f(img_col), f(img_row), f(color_scale)))

with open(output, 'wb') as f:
    write(f, header)
    f.write(bytes([0x0A]))
    write(f, img_col)
    f.write(bytes([0x0A]))
    write(f, img_row)
    f.write(bytes([0x0A]))
    write(f, color_scale)
    f.write(bytes([0x0A]))
    write(f, file)
    None

