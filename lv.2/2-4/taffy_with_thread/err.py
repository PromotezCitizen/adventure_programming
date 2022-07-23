class NumRngErr(Exception): # 사용자 정의 에러
    def __init__(self, msg):
        self.msg = msg
    
    def __str__(self):
        return "[RNG error] input value : " + str(self.msg)

class NotNumErr(Exception):
    def __init__(self, msg):
        self.msg = msg
    
    def __str__(self):
        return "[NUM error] input value : " + str(self.msg)