import copy

PPM = 'P6'
PGM = 'P5'

class PNM:
    def __init__(self):
        self._i = lambda x: int(''.join([ chr(dat) for dat in x ]))
        self._c = lambda x: ''.join([ chr(dat) for dat in x ])

    def load(self):
        self._file = None

        self._header = None
        self._img_col = None
        self._img_row = None
        self._color_scale = None

        self._rgb_channel = None

        self._readFile()
        self._getHeader()
        self._getImgSize()
        self._getColorsacle()

    def _readFile(self):
        filename = input("파일 이름 입력 >> ")
        with open('files/' + filename, 'rb') as f:
            self._file = list(f.read())

    def _getHeader(self):
        self._header = []
        self._header.append(self._file.pop(0))
        self._header.append(self._file.pop(0))
        if self._file.pop(0) == 0x0D: # 구분자 제거
            self._file.pop(0)

    def _getImgSize(self):
        self._img_col = []
        self._img_col.append(self._file.pop(0))
        while self._img_col[-1] != 0x20 and self._img_col[-1] != 0x0D and self._img_col[-1] != 0x0A:
            self._img_col.append(self._file.pop(0))
        if self._img_col.pop(-1) == 0x0D:
            self._file.pop(0)

        self._img_row = []
        self._img_row.append(self._file.pop(0))
        while self._img_row[-1] != 0x20 and self._img_row[-1] != 0x0D and self._img_row[-1] != 0x0A:
            self._img_row.append(self._file.pop(0))
        if self._img_row.pop(-1) == 0x0D:
            self._file.pop(0)

    def _getColorsacle(self):
        self._color_scale = []
        self._color_scale.append(self._file.pop(0))
        while self._color_scale[-1] != 0x0D and self._color_scale[-1] != 0x0A:
            self._color_scale.append(self._file.pop(0))
        if self._color_scale.pop(-1) == 0x0D:
            self._file.pop(0)
            
        self._rgb_channel = 1 if self._c(self._header) == PGM else 3
    
    def reverse(self):
        for idx in range(len(self._file)):
            self._file[idx] = 0xFF - self._file[idx]

    def drawsquare(self):
        pos1_x = int(input('x1(1~{0}) >> '.format(self._i(self._img_row)))) - 1
        pos1_y = int(input('y1(1~{0}) >> '.format(self._i(self._img_col)))) - 1
        pos2_x = int(input('x2(1~{0}) >> '.format(self._i(self._img_row)))) - 1
        pos2_y = int(input('y2(1~{0}) >> '.format(self._i(self._img_col)))) - 1

        if pos1_x > pos2_x:
            temp = pos1_x
            pos1_x = pos2_x
            pos2_x = temp

            if pos2_x > self._i(self._img_col) - 1:
                pos2_x = self._i(self._img_col) - 1


        if pos1_y > pos2_y:
            temp = pos1_y
            pos1_y = pos2_y
            pos2_y = temp

            if pos2_y > self._i(self._img_col) - 1:
                pos2_y = self._i(self._img_col) - 1

        color = int(input('0~255 >> '))

        for row in range(pos1_y, pos2_y+1):
            for col in range(pos1_x, pos2_x+1):
                for rgb in range(self._rgb_channel):
                    self._file[(row*self._i(self._img_col) + col)*self._rgb_channel + rgb] = color

    def turn_right(self):

        temp = self._img_col
        self._img_col = self._img_row
        self._img_row = temp

        arr = [ [ 0 for _ in range(self._i(self._img_col)) ] for _ in range(self._i(self._img_row)) ]

        for row_idx, row in enumerate([ self._file[lst:lst+self._i(self._img_col)] for lst in range(0, len(self._file), self._i(self._img_row)) ]): # => row_cnt -> col_cnt, col_cnt -> row_cnt
            for col_idx, data in enumerate(row):
                for idx in range(self._rgb_channel):
                    arr[col_idx][self._i(self._img_row)- row_idx -1 + idx] = data

        self._file = []
        for data in arr:
            self._file += data

    def turn_left(self):
        None

    def mirror_lr(self):
        for col in range(self._i(self._img_col) // 2):
            for row in range(self._i(self._img_row)):
                for idx in range(self._rgb_channel):
                    temp = self._file[ (row*self._i(self._img_col) + col)*self._rgb_channel + idx ]
                    self._file[ (row*self._i(self._img_col) + col)*self._rgb_channel + idx ] = \
                        self._file[ ((row*self._i(self._img_col)) + (self._i(self._img_col) - col - 1))*self._rgb_channel + idx ]
                    self._file[ ((row*self._i(self._img_col)) + (self._i(self._img_col) - col - 1))*self._rgb_channel + idx ] = temp

    def mirror_td(self):
        for row in range(self._i(self._img_row) // 2):
            for col in range(self._i(self._img_col)):
                for idx in range(self._rgb_channel):
                    temp = self._file[ (row*self._i(self._img_col) + col)*self._rgb_channel + idx ]
                    self._file[ (row*self._i(self._img_col) + col - 1)*self._rgb_channel + idx ] = \
                        self._file[ ((self._i(self._img_col) - row - 1)*self._i(self._img_col) + col - 1)*self._rgb_channel + idx ]
                    self._file[ ((self._i(self._img_col) - row - 1)*self._i(self._img_col) + col - 1)*self._rgb_channel + idx ] = temp

    def save(self):
        with open('output.'+('pgm' if self._rgb_channel == 1 else 'ppm'), 'wb') as f:
            self._write(f, self._header)
            f.write(bytes([0x0A]))
            self._write(f, self._img_col)
            f.write(bytes([0x0A]))
            self._write(f, self._img_row)
            f.write(bytes([0x0A]))
            self._write(f, self._color_scale)
            f.write(bytes([0x0A]))
            self._write(f, self._file)

    def _write(self, f, list):
        for data in list:
            f.write(bytes([data]))



# # 기본 구분자는 0x0A
# # 확장자 / col / row / color_scale

# filename = 'house.ppm'
# with open('files/' + filename, 'rb') as f:
#     file = list(f.read())

# # ==============================
# header = []
# header.append(file.pop(0))
# header.append(file.pop(0))
# # ==============================
# if file.pop(0) == 0x0D: # 구분자 제거
#     file.pop(0)
# # ==============================
# img_col = []
# img_col.append(file.pop(0))
# while img_col[-1] != 0x20 and img_col[-1] != 0x0D and img_col[-1] != 0x0A:
#     img_col.append(file.pop(0))
# if img_col.pop(-1) == 0x0D:
#     file.pop(0)

# img_row = []
# img_row.append(file.pop(0))
# while img_row[-1] != 0x20 and img_row[-1] != 0x0D and img_row[-1] != 0x0A:
#     img_row.append(file.pop(0))
# if img_row.pop(-1) == 0x0D:
#     file.pop(0)
# # ==============================
# color_scale = []
# color_scale.append(file.pop(0))
# while color_scale[-1] != 0x0D and color_scale[-1] != 0x0A:
#     color_scale.append(file.pop(0))
# if color_scale.pop(-1) == 0x0D:
#     file.pop(0)
# # ==============================


# f = lambda x: ''.join([ chr(dat) for dat in x ])
# rgb_channel = 1 if f(header) == PGM else 3

# # print(list(img_data.values())[0] + list(img_data.values())[1])

# print("format:{0}\ncol:{1} row:{2}\ncolor scale:{3}".format(f(header), f(img_col), f(img_row), f(color_scale)))

# for idx in range(len(file)):
#     file[idx] = 0xFF - file[idx]


# pos1_x = int(input('x1 >> '))
# pos1_y = int(input('y1 >> '))
# pos2_x = int(input('x2 >> '))
# pos2_y = int(input('y2 >> '))

# color = int(input('0~255 >> '))

# for row in range(pos1_y, pos2_y+1):
#     for col in range(pos1_x, pos2_x+1):
#         for rgb in range(rgb_channel):
#             file[(row*int(f(img_col)) + col)*rgb_channel + rgb] = color

# # 저장하는 파일은 구분자로 0x0D 0x0A로 하지 않는다.
# # 오로지 0x0A
# def write(f, list):
#     for data in list:
#         f.write(bytes([data]))

# with open('output.'+('pgm' if rgb_channel == 1 else 'ppm'), 'wb') as f:
#     write(f, header)
#     f.write(bytes([0x0A]))
#     write(f, img_col)
#     f.write(bytes([0x0A]))
#     write(f, img_row)
#     f.write(bytes([0x0A]))
#     write(f, color_scale)
#     f.write(bytes([0x0A]))
#     write(f, file)
#     None

pnm = PNM()
pnm.load()
# pnm.reverse()
# pnm.drawsquare()
# pnm.mirror_td()
# pnm.mirror_lr()
pnm.turn_right()
pnm.save()