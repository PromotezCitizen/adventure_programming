from encoder import HuffmanEncoder
from decoder import HuffmanDecoder

class HuffmanCodec():
    def __init__(self):
        self._encoder = HuffmanEncoder()
        self._decoder = HuffmanDecoder()
        self._codec = None
        # encoder : 0
        # decoder : 1
    
    def run(self):
        filename = input("파일 이름 입력 >> ")
        with open(filename, 'rb') as f:
            temp = f.read(2)

        if sum(temp) < 0xFF+0xFF:
            self._codec = self._encoder
        else:
            self._codec = self._decoder
        
        self._codec.run(filename)
        self._codec.save()
        