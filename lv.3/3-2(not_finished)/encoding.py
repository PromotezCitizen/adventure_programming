from huffman import *

class HuffmanEncoding():
    def __init__(self, filename):
        self._huffman_dict = {}
        self._huffman_len_histogram = {}
        self._huffman_code_bin = {}
        self._lines = None
        self._head = None
        self._encoded_str = ""
        self._filename = filename

    def run(self):
        self._makeHuffmanDict(self._filename)
        self._makeHuffmanTree()
        self._setHuffmanCode(self._head)
        self._encodingStr()

    def _makeHuffmanDict(self, filename):
        self._lines = self._getBinLines(filename)
        data_dict = self._getBinDict(self._lines)
        self._getHuffmanDict(data_dict)

    def _getBinLines(self, filename):
        with open(filename, 'rb') as f:
            lines = f.readlines()
            lines = [ list(x) for x in lines ]
        return lines

    def _getBinDict(self, lines):
        data_dict = {}
        for line in lines:
            for data in line:
                try:
                    data_dict[data] += 1
                except:
                    data_dict[data] = 1

        return data_dict

    def _getHuffmanDict(self, data_dict):
        for key, val in data_dict.items():
            self._huffman_dict[key] = Huffman(key, val)

    def _isInt(self, val):
        try:
            int(val)
        except:
            return False
        return True

    def _setHuffmanCode(self, huffman, code=""):
        node = huffman.getLeft()
        if node is not None:
            self._setHuffmanCode(node, code+'0')

        node = huffman.getRight()
        if node is not None:
            self._setHuffmanCode(node, code+'1')

        data = huffman.getData()

        if self._isInt(data['data']):
            try:
                self._huffman_len_histogram[len(code)] += 1
            except:
                self._huffman_len_histogram[len(code)] = 1
            finally:
                self._huffman_code_bin[data['data']] = code
                huffman.setData(data['data'], data['cnt'], code)
            # print(huffman.getData()) # only test

    def _makeHuffmanTree(self):
        temp_data = ''

        while len(self._huffman_dict) > 1:
            # https://blockdmask.tistory.com/566 - dict sort
            self._huffman_dict = dict(sorted(self._huffman_dict.items(), key=lambda x: x[1].getData()['cnt'], reverse=True))

            temp_data += '-'

            huffman_right = self._huffman_dict.popitem()[1]
            data = huffman_right.getData()
            temp_cnt = data['cnt']

            huffman_left = self._huffman_dict.popitem()[1]
            data = huffman_left.getData()
            temp_cnt += data['cnt']

            huffman = Huffman(temp_data, temp_cnt)
            huffman.setRight(huffman_right)
            huffman.setLeft(huffman_left)

            self._huffman_dict[temp_data] = huffman

        self._head = self._huffman_dict.popitem()[1]

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

        if self._isInt(data['data']):
            print(data)

    def printHuffmanBin(self):
        for key, val in self._huffman_code_bin.items():
            print(key, val)

    def printEncoded(self):
        print(self._encoded_str)
        for binary in spliter(self._encoded_str):
            print(binary)

    def _encodingStr(self):
        self._encoded_str = ""
        for list in self._lines:
            for data in list:
                self._encoded_str += self._huffman_code_bin[data]

# 파일 구조
#   len of huffman_code num
#   huffman code key-value
#       [
#           data
#           len(8byte씩 나눔)
#           encoded_data
#       ]
#   encoded string

    def saveEncodedTree(self):
        print(len(self._huffman_code_bin))
        with open('test.bin', 'wb') as f:
            f.write(bytes([len(self._huffman_code_bin)]))
            for key, val in self._huffman_code_bin.items():
                codes = spliter(val)
                print(key, bytes([key]), codes, [ int(code, 2) for code in codes ])
                f.write(bytes([key]))
                f.write(bytes([len(val)]))
                for code in codes:
                    f.write(bytes([int(code, 2)]))

    def saveEncodedStr(self):
        with open('test.bin', 'ab') as f:
            print(len(self._encoded_str) / 8)
            for bin in spliter(self._encoded_str):
                f.write(bytes([int(bin, 2)]))