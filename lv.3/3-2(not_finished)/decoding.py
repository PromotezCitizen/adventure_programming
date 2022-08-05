from huffman_node import *
from huffman import *

class HuffmanDecoding(Huffman):
    def __init__(self, filename):
        super().__init__(filename)
        self._header_data = []
        self._result = []

    def decode(self):
        self._getBinLines() # 모든 문자열 가져오기

        self._getDecodeInfo() # 헤더 정보 가져오기
        self._makeHuffmanTree() # 헤더 정보를 통해 허프만 트리 구축

        self._getEncodedStr()   # 인코딩된 문자열 가져오기.
                                
        self._decodingStr() # 인코딩된 문자열 디코딩


    def _getDecodeInfo(self):
        # [ data(8), code_len(8), code(n) ] 헤더는 왼쪽과 같은 방식으로 저장됨. 괄호 안의 숫자는 byte
        huffman_bin_len = self._lines.pop(0)
        for _ in range(huffman_bin_len):
            data = self._lines.pop(0)
            code_len = self._lines.pop(0)
            code = ""
            max_range = (code_len+7) // 8
            for idx in range(max_range):
                temp = bin(self._lines.pop(0))[2:]
                filler = 8 if idx < max_range - 1 else code_len
                # https://www.delftstack.com/ko/howto/python/pad-string-with-zeros-in-python/
                code += temp.zfill(filler) # 원하는 길이가 될때까지 좌측에 추가

                # print("bin:%8s, bin_len:%2d, code_len:%2d, start_idx:%2d, now_idx:%d, fill_pos:%2d" % 
                #    (temp, len(temp), code_len, 8*idx, idx, filler))
                code_len -= 8

            self._head_data.append({'data': data, 'code_len': len(code), 'code': code})

    def _makeHuffmanTree(self): # 인코딩과 디코딩의 트리 만드는 구조가 다름
        self._head = HuffmanNode()

        for data in self._header_data: # header_data : { data, code }
            temp = self._head
            for idx in data['code']:
                if idx == '0': # left
                    if temp.getLeft() is None:
                        temp.setLeft()
                        temp.setData('-', -1, '')
                    temp = temp.getLeft()
                else: # right
                    if temp.getRight() is None:
                        temp.setRight()
                        temp.setData('-', -1, '')
                    temp = temp.getRight()
            temp.setData(data['data'], data['code_len'], data['code'])

    def _getEncodedStr(self):
        # ========메인 문자열 길이 설정==========
        power = self._lines.pop(0)
        share = self._lines.pop(0)
        remainder = self._lines.pop(0)
        # =====================================
        str_len = (0 if power == 0 else 256**power + 256*share + remainder)
        self._encoded_str = ""
        for _ in range(str_len//8):
            self._encoded_str += bin(self._lines.pop(0))[2:].zfill(8)
        if str_len % 8 != 0:
            self._encoded_str += bin(self._lines.pop(0))[2:].zfill(str_len % 8)

        # zfill(n) - 반환될 문장의 길이가 n이 될때까지 좌측에 0을 추가
        # 인코딩된 문장은 byte로 저장되어있어 0b00110110으로 저장된 경우 110110만 가져온다. 이를 해결

    def _decodingStr(self):
        temp = self._head
        result_str = ""
        max_len = len(self._encoded_str)
        for idx, data in enumerate(self._encoded_str):
            if data == '0':
                if temp.getLeft() is None:
                    self._result.append(temp.getData()['data'])
                    if idx != max_len: temp = self._head.getLeft()
                    result_str = ""
                else:
                    temp = temp.getLeft()

            else:
                if temp.getRight() is None:
                    self._result.append(temp.getData()['data'])
                    if idx != max_len: temp = self._head.getRight()
                    result_str = ""
                else:
                    temp = temp.getRight()
            result_str += data
        self._result.append(temp.getData()['data'])

    def save(self, filename):
        with open(filename, 'wb') as f:
            for data in self._result:
                f.write(bytes([data]))