from encoder import HuffmanEncoder
from decoder import HuffmanDecoder
import multiprocessing as mp

class FileNameErr(Exception):
    def __init__(self, str):
        self._str = str

    def __str__(self):
        return self._str

class HuffmanCodec():
    def __init__(self):
        self._encoder = HuffmanEncoder()
        self._decoder = HuffmanDecoder()
        self._codec = None
    
    def test(self):
        # print(mp.current_process().name)
        if mp.current_process().name == "MainProcess":
            # 이게 없으면 save는 프로세스 수 만큼 실행됨. run은 상관없음
            self.run()
            self.save()
    
    def isEncoded(self, filename):
        with open(filename, 'rb') as f:
            temp = f.read(2)
        return False if sum(temp) < 0xFF+0xFF else True

    def isEncoder(self):
        return self._codec is self._encoder

    def run(self, filename=None):
        if mp.current_process().name == "MainProcess":
            mp.freeze_support()
            if filename is None:
                while True:
                    filename = input("파일 이름 입력(확장자 없으면 huf파일) >> ")
                    filename = filename+".huf" if len(filename.split('.')) == 1 else filename
                    # middle -> middle.huf 변환. 확장자 없으면 huf 확장자 붙여서 진행
                    # middle.huf -> middle.huf, test.py -> test.py
                    try:
                        with open(filename, 'rb') as f:
                            temp = f.read(2)
                            break
                    # https://docs.python.org/ko/3/tutorial/errors.html
                    # OSError 참고
                    except OSError as e:
                        print('%s - 없는 파일입니다. 다시 입력해주세요.' % e.filename)
            else:
                with open(filename, 'rb') as f:
                    temp = f.read(2)

            self._codec = self._encoder if sum(temp) < 0xFF+0xFF else self._decoder
            
            msg = 'encoding' if self._codec is self._encoder else 'decoding'
            print('start {0}'.format(msg))
            self._codec.run(filename)
            print('end {0}'.format(msg))

    def save(self, filename=None):
        if filename is None:
            msg = "huf로 고정" if self._codec is self._encoder else "자동생성"
            filename = input("저장할 파일 이름 입력(확장자는 %s) >> " % msg)
        filename += '.huf' if self._codec is self._encoder else ""
        
        print('start saving')
        filename = self._codec.save(filename)
        print('end saving')
        return filename