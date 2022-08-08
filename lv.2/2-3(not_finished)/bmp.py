# https://dojang.io/mod/page/view.php?id=702
# bmp 구조

# file header
bfType = None           # 2byte, 매직 넘버
bfSize = None           # 4byte, 파일 크기
bfReserved1 = None      # 2byte, 예약된 공간, 사용X
bfReserved2 = None      # 2byte, 예약된 공간, 사용X
bfOffBits = None        # 4byte, 비트맵 데이터의 시작 위치

# info header
biSize = None           # 4byte, 정보 헤더 크기
biWidth = None          # 4byte, 가로 크기
biHeight = None         # 4byte, 세로 크기
biPlanes = None         # 2byte, 색상판 수, 항상 1
biBitCount = None       # 2byte, 픽셀 하나를 표현하는 비트 수
biCompression = None    # 4byte, 압축 유형 (BI_RGB: 1, BI_RLE4: 4, BI_RLE8: 8), 일반적으로 0
biSizeImage = None      # 4byte, 비트맵 이미지 픽셀 데이터 크기
biXPelsPerMeter = None  # 4byte, 가로 해상도
biYPelsPerMeter	= None  # 4byte, 세로 해상도
biClrUsed = None        # 4byte, 색상 테이블에서 실제 사용되는 색상 수
biClrImportant = None   # 4byte, 비트맵을 표현하기 위해 필요한 색상 인덱스 수

# pixel 구조
pixels = []
rgbtBlue = None         # 1byte
rgbtGreen = None        # 1byte
rgbtRed = None          # 1byte
rgbReserved = None      # 1byte

# imgData
image = None

def read(f, size):
    return [ int(x) for x in f.read(size) ]

l = lambda arr: list(arr)
e = lambda arr: enumerate(list(arr))
s = lambda arr: sum([ x*256**(i) for i, x in enumerate(list(arr)) ])
pad = lambda arr: (4 - s(arr)%4) % 4

def reverseColor(arr):
    for p_idx, pixel in enumerate(arr):
        for c_idx, _ in enumerate(pixel):
            if c_idx != 3:
                arr[p_idx][c_idx] = 0xFF - arr[p_idx][c_idx]

def write(f, arr):
    for data in arr:
        try:
            f.write(bytes([data]))
        except:
            f.write(data)

with open('files/BLACK_RLE_2.BMP', 'rb') as f:
    bfType = read(f, 2)
    bfSize = read(f, 4)
    bfReserved1 = read(f, 2)
    bfReserved2 = read(f, 2)
    bfOffBits = read(f, 4)

    biSize = read(f, 4)
    biWidth = read(f, 4)
    biHeight = read(f, 4)
    biPlanes = read(f, 2)
    biBitCount = read(f, 2)
    biCompression = read(f, 4)
    biSizeImage = read(f, 4)
    biXPelsPerMeter = read(f, 4)
    biYPelsPerMeter = read(f, 4)
    biClrImportant = read(f, 4)
    biClrImportant = read(f, 4)

    biPadding = pad(biWidth)

    while f.tell() < s(bfOffBits):
        pixels.append(l(f.read(4)))

    print(s(bfOffBits))
    print(f.tell())

    image = l(f.read())

reverseColor(pixels)

with open('test.bmp', 'wb') as f:
    write(f, bfType)
    write(f, bfSize)
    write(f, bfReserved1)
    write(f, bfReserved2)
    write(f, bfOffBits)

    write(f, biSize)
    write(f, biWidth)
    write(f, biHeight)
    write(f, biPlanes)
    write(f, biBitCount)
    write(f, biCompression)
    write(f, biSizeImage)
    write(f, biXPelsPerMeter)
    write(f, biYPelsPerMeter)
    write(f, biClrImportant)
    write(f, biClrImportant)


    for data in pixels:
        write(f, data)
    
    write(f, image)


