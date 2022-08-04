from encoding import HuffmanEncoding
from huffman import Huffman




# C:\\Users\\Han\\Documents\\now.png
# test.txt
encoding = HuffmanEncoding('test.txt') # encoding에서 허프만 트리는 필요없다. 
encoding.run()
#encoding.printHuffmanBin()
#encoding.printEncoded()
encoding.save()

class HuffmanDecoding():
    def __init__(self, filename):
        self._filename = filename
        self._head_data = []
        self._encoded_data = []
        self._head = None

    def run(self):
        self._getDecodedData()
        self._getDecodeInfoFromBin()
        self._makeHuffmanTree()

    def _getDecodedData(self):
        with open('test.bin', 'rb') as f:
            self._encoded_data = list(f.read())

    def _getDecodeInfoFromBin(self):
        huffman_bin_len = self._encoded_data.pop(0)
        for _ in range(huffman_bin_len):
            data = self._encoded_data.pop(0)
            code_len = self._encoded_data.pop(0)
            code = ""
            max_range = (code_len+7) // 8
            for idx in range(max_range):
                temp = bin(self._encoded_data.pop(0))[2:]
                filler = 8 if idx < max_range - 1 else code_len
                # https://www.delftstack.com/ko/howto/python/pad-string-with-zeros-in-python/
                code += temp.zfill(filler) # 원하는 길이가 될때까지 좌측에 추가

                # print("bin:%8s, bin_len:%2d, code_len:%2d, start_idx:%2d, now_idx:%d, fill_pos:%2d" % 
                #    (temp, len(temp), code_len, 8*idx, idx, filler))
                code_len -= 8
            # print(data, code_len, code)
            # print('')
            self._head_data.append({'data': data, 'code': code})

    def _makeHuffmanTree(self):
        self._head = Huffman()

        for data in self._head_data: # header_data : { data, code }
            temp = self._head
            for idx in data['code']:
                if idx == '0': # left
                    if temp.getLeft() is None:
                        temp.setLeft()
                    temp = temp.getLeft()
                else: # right
                    if temp.getRight() is None:
                        temp.setRight()
                    temp = temp.getRight()
            temp.setData(data['data'], None, data['code'])

    def printHuffmanTree(self):
        self._printHuffmanTree(self._head)

    def _printHuffmanTree(self, huffman):
        node = huffman.getLeft()
        if node is not None:
            self._printHuffmanTree(node)

        node = huffman.getRight()
        if node is not None:
            self._printHuffmanTree(node)

        data = huffman.getData()

        if data['code'] is not None:
            print(data)

# decoding = HuffmanDecoding('test.bin')
# decoding.run()
# decoding.printHuffmanTree()

trid = (lambda x, y, z, n=8: n if x < y else z)

def getDecodeInfoFromBin(line, huffman_bin_len):
    ret = []
    for _ in range(huffman_bin_len):
        data = line.pop(0)
        code_len = line.pop(0)
        code = ""
        max_range = (code_len+7) // 8
        for idx in range(max_range):
            temp = bin(line.pop(0))[2:]
            filler = 8 if idx < max_range - 1 else code_len

            # print("bin:%8s, bin_len:%2d, code_len:%2d, start_idx:%2d, now_idx:%d, fill_pos:%2d" % 
            #    (temp, len(temp), code_len, 8*idx, idx, filler))
            # https://www.delftstack.com/ko/howto/python/pad-string-with-zeros-in-python/
            code += temp.zfill(filler) # 원하는 길이가 될때까지 좌측에 추가
            code_len -= 8
        # print(data, code_len, code)
        # print('')
        ret.append({'data': data, 'code': code})
    return ret

def printHuffmanTree(huffman):
    node = huffman.getLeft()
    if node is not None:
        printHuffmanTree(node)

    node = huffman.getRight()
    if node is not None:
        printHuffmanTree(node)

    data = huffman.getData()

    if data['code'] is not None:
        print(data)

def makeHuffmanTree(header_data):
    head = Huffman()

    for data in header_data: # header_data : { data, code }
        temp = head
        for idx in data['code']:
            if idx == '0': # left
                if temp.getLeft() is None:
                    temp.setLeft()
                temp = temp.getLeft()
            else: # right
                if temp.getRight() is None:
                    temp.setRight()
                temp = temp.getRight()
        temp.setData(data['data'], None, data['code'])

    return head

def getEncodedStr(line):
    power = line.pop(0)
    share = line.pop(0)
    remainder = line.pop(0)

    print(power, share, remainder)

    str_len = 0 if power == 0 else 256**power + 256*share + remainder
    encoded_str = ""
    for _ in range(str_len//8):
        encoded_str += bin(line.pop(0))[2:].zfill(8)
    if str_len % 8 != 0:
        encoded_str += bin(line.pop(0))[2:].zfill(str_len % 8)

    return encoded_str

with open('test.bin', 'rb') as f:
    line = list(f.read())

huffman_bin_len = line.pop(0)

header_data = getDecodeInfoFromBin(line, huffman_bin_len)

head = makeHuffmanTree(header_data)

printHuffmanTree(head)

encoded_str = getEncodedStr(line)
print(encoded_str)