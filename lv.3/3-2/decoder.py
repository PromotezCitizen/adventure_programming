from huffman_node import *
from huffman import *

# 디코딩에서는 멀티프로세싱을 사용할 수 없음

class HuffmanDecoder(Huffman):
    def __init__(self):
        super().__init__()

        self._result = []           # 디코딩된 결과를 저장

    def run(self, filename):
        self.__init__()

        start = self._getRunStartTime()
        self._getBinLines(filename) # 모든 문자열 가져오기
        self._printRunTime(start, 'readfile')

        start = self._getRunStartTime()
        self._removeExtensionsInfo()
        self._getDecodeInfo() # 헤더 정보 가져오기
        self._printRunTime(start, 'get_header_data')

        start = self._getRunStartTime()
        self._makeHuffmanTree() # 헤더 정보를 통해 허프만 트리 구축
        self._printRunTime(start, 'make_huffmantree')

        start = self._getRunStartTime()
        self._getEncodedStr()   # 인코딩된 문자열 가져오기.
        self._printRunTime(start, 'get_encoded_str')
        
        start = self._getRunStartTime()
        self._decodingStr() # 인코딩된 문자열 디코딩
        self._printRunTime(start, 'decoding')

        # print(type(ord(data)), ord(data))
    def _removeExtensionsInfo(self):
        self._lines.pop(0)
        self._lines.pop(0)

        origin_ext_len = self._lines.pop(0) # 확장자 길이
        if origin_ext_len > 0:
            for _ in range(origin_ext_len):
                self._origin_ext.append(chr(self._lines.pop(0))) # 확장자 복구
            self._origin_ext.insert(0, '.')
        

    def _getDecodeInfo(self):
        # [ data(8), code_len(8), code(n) ] 헤더는 왼쪽과 같은 방식으로 저장됨. 괄호 안의 숫자는 byte
        # with open('middle.bin', 'rb') as f:
        #     for data in self._lines:
        #         f.write(bytes([data]))

        huffman_bin_len = self._lines.pop(0)
        huffman_bin_len = huffman_bin_len if huffman_bin_len != 0 else (256 if len(self._lines) > 0 else huffman_bin_len)

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
            
            self._header_data[data] = code

    def _makeHuffmanTree(self): # 인코딩과 디코딩의 트리 만드는 구조가 다름
        self._head_tree = HuffmanNode()

        for data, code in self._header_data.items():
            temp = self._head_tree
            for idx in code:
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
            temp.setData(data, len(code), code)

    def _getEncodedStr(self):
        str_len = self._getEncodedStrLen()
        for _ in range(str_len//8):
            data = bin(self._lines.pop(0))
            self._encoded_str += data[2:].zfill(8)
        if str_len % 8 != 0:
            self._encoded_str += bin(self._lines.pop(0))[2:].zfill(str_len % 8)

        # zfill(n) - 반환될 문장의 길이가 n이 될때까지 좌측에 0을 추가
        # 인코딩된 문장은 byte로 저장되어있어 0b00110110으로 저장된 경우 110110만 가져온다. 이를 해결

    def _getEncodedStrLen(self):
        # ========메인 문자열 길이 설정==========
        str_len_arr = []
        str_arr_len = self._lines.pop(0)
        for _ in range(str_arr_len):
            str_len_arr.append(self._lines.pop(0))

        str_len = 0
        for i, data in enumerate(str_len_arr):
            str_len += 256**(str_arr_len-1 - i) * data

        return str_len
        # =====================================

    def _decodingStr(self):
        # 인코딩된 파일 구조로 인한 프로세스 분리 불가
        # 가능했으면 이미 빠른 속도로 복호화가 가능했을 것
        temp = self._head_tree
        max_len = len(self._encoded_str)
        for idx, data in enumerate(self._encoded_str):
            if data == '0':
                if temp.getLeft() is None:
                    self._result.append(temp.getData()['data'])
                    if idx != max_len: temp = self._head_tree.getLeft()
                else:
                    temp = temp.getLeft()
            else:
                if temp.getRight() is None:
                    self._result.append(temp.getData()['data'])
                    if idx != max_len: temp = self._head_tree.getRight()
                else:
                    temp = temp.getRight()
        self._result.append(temp.getData()['data'])

    def save(self, filename):
        start = self._getRunStartTime()
        with open(filename + "".join(self._origin_ext), 'wb') as f:
            for data in self._result:
                f.write(bytes([data]))
                
        self._printRunTime(start, 'save')

        return filename + "".join(self._origin_ext)