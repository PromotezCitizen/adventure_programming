import random
from collections import Counter

class NumRngErr(Exception): # 사용자 정의 에러
    pass

class SelectedCardErr(Exception):
    pass


class NumberGameDeckMaker():
    def __init__(self):
        self._player_num = self._inputPlayerNum()
        self._dup_flag = self._setDufFlag()
        self._multiplier = 1
        self._scores = self._makeCardDeck()

    def _inputPlayerNum(self):
        while True:
            num_player = input("풀레이어의 수 입력 >> ")
            if num_player.isdigit():
                return num_player

    def _makeCardDeck(self):
        return [ [] for _ in range(int(self._player_num)) ]

    def createdeck(pls, flag=1):
        arr = []
        for val in range(pls*4):
            arr.append(val)
            if flag == 2:
                arr.append(val)
        random.shuffle(arr)
        return arr, [0]*(pls*4*flag)

    def _setDufFlag():
        flag = None
        while True:
            try:
                flag = int(input("숫자 중복을 허용하시겠습니까? (1: 중복 비허용, 2: 중복 허용)"))
                if not (flag == 1 or flag == 2):
                    raise NumRngErr
                break
            except NumRngErr:
                print("옳지 않은 값입니다.", end=" ")
        return flag

    def _setMultiplier(self):
        while True:
            try:
                mltp = input("중복 배수값을 입력해주세요(1 이상) : ")
                if mltp == '':
                    raise NumRngErr
                
                mltp = int(mltp)
                if mltp < 1:
                    raise NumRngErr
                
                break
            except NumRngErr:
                print("옳지 않은 값입니다.")
        if mltp > 1:
            self._multiplier = mltp

def inputplayer():
    while True:
        num_player = input("풀레이어의 수 입력 >> ")
        if num_player.isdigit():
            break
    return int(num_player), [ [] for _ in range(int(num_player)) ]

def setdufflag():
    flag = None
    while True:
        try:
            flag = int(input("숫자 중복을 허용하시겠습니까? (1: 중복 비허용, 2: 중복 허용)"))
            if not (flag == 1 or flag == 2):
                raise NumRngErr
            break
        except NumRngErr:
            print("옳지 않은 값입니다.", end=" ")
    return flag

def createdeck(pls, flag=1):
    arr = []
    for val in range(pls*4):
        arr.append(val)
        if flag == 2:
            arr.append(val)
    random.shuffle(arr)
    return arr, [0]*(pls*4*flag)

def printsequence(deck, is_selected):
    for idx, val in enumerate(deck):
        if (is_selected[idx] == 0):
            val = "■"
        print(val, end=" ")
    print("")

def comselect(is_selected, pls, flag):
    while True:
        rnd = random.randrange(0, pls*4)
        if is_selected[rnd] == 0:
            is_selected[rnd] = 1
            break
    print("computer selected %d card" % (rnd+1))
    return rnd

def playerselect(is_selected, pls, idx, flag=1):
    while True:
        try:
            npt = input("카드를 선택해주세요(1~%d)" % (pls*4*flag))

            if npt == '':
                raise NumRngErr

            npt = int(npt) - 1
            if npt < 0:
                raise NumRngErr
            if npt > pls*4*flag - 1:
                raise NumRngErr
            if is_selected[npt]== 1:
                raise SelectedCardErr

            is_selected[npt]= 1
            break
        except NumRngErr:
            print("해당 카드는 범위를 벗어났습니다.", end=" ")
        except SelectedCardErr:
            print("해당 카드는 이미 선택되었습니다.", end=" ")
    print("player %d selected %d card" % (idx, npt+1))
    return npt

def sortselections(score):
    for score in scores:
        score.sort()

def setmultiplier():
    while True:
        try:
            mltp = input("중복 배수값을 입력해주세요(1 이상) : ")
            if mltp == '':
                raise NumRngErr
            
            mltp = int(mltp)
            if mltp < 1:
                raise NumRngErr
            
            break
        except NumRngErr:
            print("옳지 않은 값입니다.")
    return mltp


def play(scores, pls):
    flag = setdufflag()
    mltp = 1
    if flag == 2:
        mltp = setmultiplier()

    deck, is_selected = createdeck(players, flag)

    for _ in range(4):
        for idx, _ in enumerate(range(pls)):
            if idx == 0:
                func = comselect(is_selected, pls, flag)
            else:
                func = playerselect(is_selected, pls, idx, flag)
            scores[idx].append(deck[func])
            printsequence(deck, is_selected)

    sortselections(scores)

    return mltp

def makeresult(scores, mltp):
    result, result_idx = {}, 0
    for score in scores:
        dct = dict(Counter(score))
        result[result_idx] = 0
        for slct, cnt in dct.items():
            if cnt == 1:
                result[result_idx] += slct
            else:
                result[result_idx] += slct * mltp
        result_idx += 1
    return result

players, scores = inputplayer()
mltp = play(scores, players)
print(scores)
print(makeresult(scores, mltp))