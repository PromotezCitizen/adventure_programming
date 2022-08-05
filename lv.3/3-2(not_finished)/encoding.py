from huffman_node import *
from huffman import *



# 파일 구조
#   len of huffman_code num
#   huffman code key-value
#    eg)[
#           data
#           len(8byte씩 나눔)
#           encoded_data
#       ]
#   power share remainder <- 인코딩된 문자열 길이 저장
#   encoded string

class HuffmanEncoding(Huffman):
    def __init__(self, filename):
        super().__init__(filename)
        self._huffman_dict = {}             # { key:data, value:HuffmanNode }
                                            # 허프만 트리 만들때만 사용
        self._huffman_len_histogram = {}    # histogram에 저장용.
                                            # 허프만 부호화된 문자의 길이에 관한 histogram

    def encode(self):
        self._getBinLines() # 모든 문자열 가져오기

        self._makeHuffmanDict() # 허프만 트리를 만들 기본 딕셔너리 생성. { key:data, value:HuffmanNode }
        self._makeHuffmanTree() # 허프만 트리 정보가 담긴 딕셔너리를 이용해 허프만 트리 생성.

        self._setHuffmanCodeBin(self._head) # 허프만 히스토그램 생성 및 [ key:data, value:code ] 쌍 생성

        self._encodingStr()

    def _makeHuffmanDict(self):
        data_dict = self._getBinDict(self._lines)
        self._getHuffmanDict(data_dict)

    def _getBinDict(self, lines):
        data_dict = {}
        for data in lines:
            try:
                data_dict[data] += 1
            except:
                data_dict[data] = 1
        return data_dict

    def _getHuffmanDict(self, data_dict):
        for key, val in data_dict.items():
            self._huffman_dict[key] = HuffmanNode(key, val)

    def _makeHuffmanTree(self): # 인코딩과 디코딩의 트리 만드는 구조가 다름
        temp_data = ''

        while len(self._huffman_dict) > 1:
            # https://blockdmask.tistory.com/566 - dict sort
            self._huffman_dict = dict(sorted(self._huffman_dict.items(), key=lambda x: x[1].getData()['cnt'], reverse=True))
    
            temp_data += '-' # 테스트 시 트리 구성을 보기 편하게

            huffman_right = self._huffman_dict.popitem()[1]
            data = huffman_right.getData()
            temp_cnt = data['cnt']

            huffman_left = self._huffman_dict.popitem()[1]
            data = huffman_left.getData()
            temp_cnt += data['cnt']
            
            huffman = HuffmanNode(temp_data, temp_cnt)
            huffman.setRight(huffman_right)
            huffman.setLeft(huffman_left)

            self._huffman_dict[temp_data] = huffman

        self._head = self._huffman_dict.popitem()[1]

    def _setHuffmanCodeBin(self, huffman, code=""): 
        node = huffman.getLeft()
        if node is not None:
            self._setHuffmanCodeBin(node, code+'0')

        node = huffman.getRight()
        if node is not None:
            self._setHuffmanCodeBin(node, code+'1')

        data = huffman.getData()

        if self._isInt(data['data']):
            try:
                self._huffman_len_histogram[len(code)] += 1
            except:
                self._huffman_len_histogram[len(code)] = 1
            finally:
                self._header_data[data['data']] = code
            # print(huffman.getData()) # only test

    def _encodingStr(self):
        for data in self._lines:
            print(data, type(data))
            self._encoded_str += self._header_data[data]

    def save(self, filename):
        self._saveEncodedTree(filename)
        self._saveEncodedStr(filename)

    def _saveEncodedTree(self, filename):
        with open(filename, 'wb') as f:
            f.write(bytes([len(self._header_data)]))
            for key, val in self._header_data.items():
                codes = spliter(val)
                f.write(bytes([key]))
                f.write(bytes([len(val)]))
                for code in codes:
                    f.write(bytes([int(code, 2)]))

    def _saveEncodedStr(self, filename):
        str_head = self._getEncodedStrLen(len(self._encoded_str))
        with open(filename, 'ab') as f:
            for data in str_head:
                f.write(data)

        with open(filename, 'ab') as f:
            for bin in spliter(self._encoded_str):
                f.write(bytes([int(bin, 2)]))

    def _getEncodedStrLen(self, str_len):
        power = 0
        while 256**power < str_len:
            power += 1
        power -= 1
        str_len -= 256**power
        share = str_len // 256
        remainder = str_len % 256

        return [bytes([power]), bytes([share]), bytes([remainder])]



    def printHuffmanBin(self):
        for key, val in self._header_data.items():
            print(key, val)

    def printEncoded(self):
        print(self._encoded_str)
        for binary in spliter(self._encoded_str):
            print(binary)