import pandas as pd
import random
import msvcrt
import time

class Spin():
    def __init__(self):
        self.__pause = False


    def spin(self):
        self.__isKeyHit()
        while self.__isPause():
            self.__isKeyHit()


    def __isKeyHit(self):
        if msvcrt.kbhit():
            _ = msvcrt.getch()
            self.__pause = not self.__pause

    def __isPause(self):
        return self.__pause

class Permutation():
    def __init__(self, arr_max):
        self._arr_max = arr_max
        self._permutate_arr = []
        self._permutate_result = []
        self._best_time = 999999
        self._best_course = None
        self._turn = 0
        self._countries_dict = {}
        self._max_time = 1800
        self._spin = Spin()
        try:
            self._df = pd.read_csv('tsp_data.txt', sep="\t", encoding="cp949", header=None)
        except:
            print("해당 파일 없음")

    def run(self):
        self._makePermutateArr()
        self._makeCountryDict()
        stop_start, stop_end = self._permutate(0, self._arr_max)
        print(stop_start, stop_end)
        self._printResult()

    def _makePermutateArr(self): # 랜덤으로 맵 생성
        if self._arr_max != 100:
            for _ in range(self._arr_max):
                a = random.randint(0,99)
                while a in self._permutate_arr:
                    a = random.randint(0,99)
                self._permutate_arr.append(a)
            self._permutate_arr.sort()
        else:
            self._permutete_arr = [ x for x in range(100) ]

    def _makeCountryDict(self):
        temp = []
        for i in self._permutate_arr:
            temp.append(self._df.iloc[i])

        for data in temp:
            self._countries_dict[data[0]] = {'x': int(data[1]), 'y': int(data[2])}

    def _permutate(self, start, end): # use stack
        self._spin.spin() # spin with kbhit. spin을 통해 대기 구현
        time.sleep(0.3)
            
        ret_start, ret_end = start, end
        if self._turn > self._max_time:
            return ret_start, ret_end
        self._turn += 1
        if (start == end):
            local_time = self._calcSpendTime()
            self._printSequence(local_time, self._permutate_arr)
            if local_time < self._best_time:
                self._best_time = local_time
                self._best_course = self._permutate_arr.copy()
            self._permutate_result.append(self._permutate_arr.copy())
        else:
            for i in range(start, end):
                self._swap(start, i)
                ret_start, ret_end = self._permutate(start+1, end)
                if self._turn >= self._max_time:
                    return ret_start, ret_end
                self._swap(start, i)
        return ret_start, ret_end

    def _swap(self, num1, num2):
        temp                        = self._permutate_arr[num1]
        self._permutate_arr[num1]   = self._permutate_arr[num2]
        self._permutate_arr[num2]   = temp
    
    def _calcSpendTime(self):
        calc_distance = 0
        for idx in range(self._arr_max-1):
            if idx == self._arr_max: break
            x_pos = (self._countries_dict[self._permutate_arr[idx]]['x'] - self._countries_dict[self._permutate_arr[idx+1]]['x'])**2
            y_pos = (self._countries_dict[self._permutate_arr[idx]]['y'] - self._countries_dict[self._permutate_arr[idx+1]]['y'])**2
            calc_distance += (x_pos + y_pos)**(1/2)
        return calc_distance

    def _printSequence(self, time, arr):
        print('turn: %3d, now time: %4.4f, path: ' % (self._turn, time), arr)
        if time < self._best_time:
            print('\tpath changed from ', self._best_course, 'to ', arr)

    def _printResult(self):
        print('순열 생성 결과')
        # for data in self._permutate_result: print('\t', data)
        print('best time: %4.4f, best path:' % (self._best_time), self._best_course)



# 기본 문제
    # ▪메뉴 방식으로 프로그램이 실행된다(도시 개수 선택 등) - 완료
    # ▪2개 이상의 소스파일과 1개 이상의 헤더파일을 사용한다. 
    # ▪첫 번째 경로와 거리를 출력하고 더 좋은 경로가 나오면 그때의 경로와 거리를 출력한다.
    #   최종적으로 가장 좋은 경로 및 거리를 출력한다. - 완료
    # ▪전역 변수 사용은 가급적 자제한다.
    # ▪실험 당 최대 수행 시간을 30분 이내로 제한하고, - 완료
    #   30분 이내에 몇 개의 도시까지 최적의 경로(모든 경로를 다 검사)를 찾을 수 있는지 확인한다.
    #   대략적으로 5개, 10개, 11개, 12개, 13개, ...와 같이 실험을 실행해 보면 된다.

# 확장 문제
    # ① 언덕 오르기 탐색 알고리즘을 적용하여 5개(0~4), 9개, 10개, 11개, 12개, 13개, 14개, 15개, 16개, 20개
    #   30개, 50개, 100개의 도시에 대해 적용해 보라. 각 실험 당 최대 수행 시간은 3분으로 제한한다.
    # 	실험 결과를 완전 탐색과 비교해 보라.
    # ② GUI 방식으로 구현한다. - GUI는 버린다
    # 	초기 경로(및 거리)를 보여주고 중간에 더 좋은 경로가 나타나면 업데이트한다.
    # 	따라서 최종적으로 가장 좋은 경로가 나타난다.
    # ③ 멈춤 기능 제공 - 완료
    # ④ 언덕 오르기 탐색 알고리즘에서 이웃해를 생성하는 방법을 다르게 적용해 보라.
    # 	예) 두 개의 위치를 선택하고 사이에 있는 도시 방문 순서를 역전(inversion)시킴