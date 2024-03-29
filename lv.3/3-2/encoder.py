from huffman_node import *
from huffman import *
import multiprocessing as mp
# from multipledispatch import dispatch

# process 수는 4로 고정
class HuffmanEncoder(Huffman):
    def __init__(self):
        super().__init__()
        self._huffman_dict = None           # { key:data, value:HuffmanNode }
                                            # 허프만 트리 만들때만 사용
        self._huffman_char_len_histogram = {}   # 허프만 부호화된 문자의 길이에 관한 histogram

        self._huffman_len_histogram = {}    # 전체 파일에 대한 histogram

        # self._char_histogram = {}           # 개별 문자에 대한 histogram
                                            

    def run(self, filename):
        self.__init__()

        start = self._getRunStartTime()
        self._getBinLines(filename) # 모든 문자열 가져오기
        self._printRunTime(start, 'readfile')

        temp = filename.split('.')
        if len(temp) > 1:
            self._origin_ext = temp[-1]

        start = self._getRunStartTime()
        self._makeHuffmanDict() # 허프만 트리를 만들 기본 딕셔너리 생성. { key:data, value:HuffmanNode }
        self._printRunTime(start, 'make_huffman_dict')

        start = self._getRunStartTime()
        self._makeHuffmanTree() # 허프만 트리 정보가 담긴 딕셔너리를 이용해 허프만 트리 생성.
        self._printRunTime(start, 'make_huffman_tree')

        start = self._getRunStartTime()
        self._setHuffmanCodeBin(self._head) # 허프만 히스토그램 생성 및 [ key:data, value:code ] 쌍 생성
        self._printRunTime(start, 'make_huffman_code')

        start = self._getRunStartTime()
        self._encodingStr()
        self._printRunTime(start, 'encoding')

    def _makeHuffmanDict(self):
        self._huffman_dict = {}
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
                self._huffman_char_len_histogram[len(code)] += 1
            except:
                self._huffman_char_len_histogram[len(code)] = 1
            finally:
                self._header_data[data['data']] = code

    # @dispatch(list)
    # def _encodingStr(self, arg):
    def _encodingStr(self):
        # codec 클래스에서 자신이 호출한 프로세스인지 확인하므로
        #   인코딩 클래스에서는 자신이 호출한 프로세스인지 확인할 필요가 없다
        process_num = 4
        mp.freeze_support()
        manager = mp.Manager()          # 멀티프로세싱의 global 변수
        return_dict = manager.dict()    # 딕셔너리를 global 변수로 쓰겠다
        histogram_dict = manager.dict()
        jobs = []                       # process pool
        data = self._spliterByArrLen(self._lines, process_num)
            # 기본은 프로세스 4개
            # arg: 테스트 후 self._lines로 변경 예정
        for i in range(process_num):
            jobs.append(mp.Process(
                target=self._encodeProcessWorker,
                args=(i, return_dict, histogram_dict, data[i])
            ))
            jobs[-1].start()

        for proc in jobs:
            proc.join()
        
        self._encoded_str = ''.join(return_dict.values())

        temp = [ x for x in histogram_dict.values() ]
        for data in temp:
            for key, cnt in data.items():
                try:
                    self._huffman_len_histogram[key] += cnt
                except:
                    self._huffman_len_histogram[key] = cnt

    def _encodeProcessWorker(self, procnum, return_dict, histogram_dict, calc_range):
        temp = ""
        histogram = {}
        for data in calc_range:
            temp += self._header_data[data]
            try:
                histogram[len(self._header_data[data])] += 1
            except:
                histogram[len(self._header_data[data])] = 1
        return_dict[procnum] = temp
        histogram_dict[procnum] = histogram


    # @dispatch()
    # def _encodingStr(self):
    #     for data in self._lines:
    #         self._encoded_str += self._header_data[data]

    def save(self, filename):
        start = self._getRunStartTime()
        self._saveFileHeader(filename)
        self._saveEncodeTree(filename)
        self._saveEncodedStrLen(filename)
        self._saveEncodedStr(filename)
        self._saveHuffmanCharHistogram(filename)
        self._printRunTime(start, 'save')
        
        return filename

    def _saveFileHeader(self, filename):
        with open(filename, 'wb') as f:
            f.write(bytes([0xFF]))
            f.write(bytes([0xFF])) # file header. 0xFF FF로 저장

            f.write(bytes([len(self._origin_ext)])) # 원래 파일의 확장자 길이
            for ext in self._origin_ext: # 원래 파일의 확장자 이름
                f.write(bytes([ord(ext)]))

    def _saveEncodeTree(self, filename):
        with open(filename, 'ab') as f:
            f.write(bytes([len(self._header_data) % 256])) # 0~255까지만 저장 가능하므로 256은 0으로 저장
            for key, val in self._header_data.items():
                codes = self._spliterByStrLen(val)
                f.write(bytes([key]))
                f.write(bytes([len(val)]))
                for code in codes:
                    f.write(bytes([int(code, 2)]))

    def _saveEncodedStrLen(self, filename):
        # str_len_arr = []
        str_len_calc = 0
        str_len = len(self._encoded_str)

        max_power = 0
        while 256**max_power < str_len:
            max_power += 1
        max_power -= 1

        with open(filename, 'ab') as f:
            f.write(bytes([max_power+1])) # mod 256이 있기 때문에 range는 실제 길이보다 1 짧다.
            for i in range(max_power):
                # str_len_arr.append(str_len // 256**(max_power - i))
                # f.write(bytes([str_len // 256**(max_power - i)]))
                # str_len -= 256**(max_power-i) * str_len_arr[-1]
                str_len_calc = str_len // 256**(max_power - i)
                f.write(bytes([str_len_calc]))
                str_len -= 256**(max_power-i) * str_len_calc
            # str_len_arr.append(str_len % 256)
            f.write(bytes([str_len % 256]))
        # print(str_len_arr) # 실제 코드에서는 테스트 용도로만 사용

    def _saveEncodedStr(self, filename):
        with open(filename, 'ab') as f:
            for bin in self._spliterByStrLen(self._encoded_str):
                f.write(bytes([int(bin, 2)]))

    def _spliterByArrLen(self, arr, arr_len=4):
        ret = []
        each_str_len = len(arr) // arr_len
        remainder_str_len = len(arr) % arr_len
        last = -1
        for _ in range(arr_len): 
            # 0              ~ each_str_len -1      =>  last=-1
            # 1*each_str_len ~ 2*each_str_len - 1       for
            # 2*each_str_len ~ 3*each_str_len - 1           start=last+1
            # 3*each_str_len ~                              last=(start-1) + each_str_len + idx_adder(0 or 1)
            idx_adder = 1 if remainder_str_len > 0 else 0
            remainder_str_len -= 1
            start = last+1
            last = (start-1) + each_str_len + idx_adder
            ret.append(arr[start:last+1]) # split range: [start:last)
            # print(start, last, last-start+1)

        return ret

    def _spliterByStrLen(self, arr, size=8):
        ret = []
        for idx in range(0, len(arr), size):
            ret.append(arr[idx:idx+size])
        return ret

    def _saveHuffmanCharHistogram(self, filename):
        filename = filename.split('.')[0] + '_histogram.csv'
        with open(filename, 'w') as f:
            f.write("len_code, count, per each char\n")
            for code, cnt in self._huffman_char_len_histogram.items():
                f.write("{0}, {1}\n".format(code, cnt))

            f.write("\nlen_code, count, all file\n")
            for code, cnt in self._huffman_len_histogram.items():
                f.write("{0}, {1}\n".format(code, cnt))
            f.write("avg len : {0}\n".format(sum([ len*cnt for len, cnt in self._huffman_len_histogram.items() ]) / sum([ x for x in self._huffman_len_histogram.values() ])))