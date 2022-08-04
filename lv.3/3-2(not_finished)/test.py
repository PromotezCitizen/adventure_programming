class T():
    def __init__(self):
        self._a = "asdf"

    def print(self):
        return self._a


def test(cls):
    print(cls.print(), type(cls))

# t = T()
# print(type(t))
# test(t)

# data = 200
# with open('test.bin', 'wb') as f:
#     f.write(bytes([data]))

# def spliter(arr, size):
#     ret = []
#     for idx in range(0, len(arr), size):
#         ret.append(arr[idx:idx+size])
#     return ret

# encoded = "1110100110000101001011100111000001010110100000001100101001000000001000001000110100000"

# for arr in spliter(encoded, 8):
#     print(int(arr, 2))


# with open('asdf.txt', 'rb') as f:
#     lines = f.readlines()
#     lines = [ list(x) for x in lines ]

#     print(lines)

# for line in lines:
#     for data in line:
#         print(data)


temp = 100000

power = 0
while 256**power < temp:
    power += 1
power -= 1
temp -= 256**power
share = temp // 256
remainder = temp % 256

with open('asdf.bin', 'wb') as f:
    print(power, share, remainder)
    f.write(bytes([power]))
    f.write(bytes([share]))
    f.write(bytes([remainder]))