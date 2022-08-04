from encoding import HuffmanEncoding
# C:\\Users\\Han\\Documents\\now.png
# test.txt
encoding = HuffmanEncoding('test.txt') # encoding에서 허프만 트리는 필요없다. 
encoding.run()
#encoding.printHuffmanBin()
#encoding.printEncoded()

encoding.saveEncodedTree()
encoding.saveEncodedStr()

class HuffmanDecoding():
    def __init__(self, filename):
        self._filename = filename
        self._head_data = []
        self._encoded_data = []

    def run(self):
        self._getDecodedData()
        self._getDecodeInfoFromBin()


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



# HuffmanDecoding('test.bin').run()
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

with open('test.bin', 'rb') as f:
    line = list(f.read())

huffman_bin_len = line.pop(0)

print(huffman_bin_len)

print(line)

header_data = getDecodeInfoFromBin(line, huffman_bin_len)

print(line)

from huffman import Huffman

for data in header_data: # header_data : { data, code }
    for idx in data['code']:
        print(idx)

for data in header_data:
    print(data)

