from encoder import HuffmanEncoder
from decoder import HuffmanDecoder

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
    
    def run(self):
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

        print(filename)

        self._codec = self._encoder if sum(temp) < 0xFF+0xFF else self._decoder
        
        self._codec.run(filename)
        self._codec.save()


        print(__name__)
        