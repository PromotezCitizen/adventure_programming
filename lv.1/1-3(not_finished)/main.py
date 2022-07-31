from beetle_processing import useProcessing
from utils import dataSplit, printResult

map_size = 100 # 가로, 세로 크기 조절해야하나?
num_process = 5
runners = 10
num_radroach = 1

if __name__ == "__main__":
    splited, can_run = dataSplit([x for x in range(runners)], num_process)
    if can_run:
        result_data, main_time = useProcessing(map_size, splited, num_radroach)
        printResult(runners, num_process, map_size, result_data, main_time, num_radroach)


# 제한요소 및 요구사항
    # ▪결과 보고서 작성 시, 실행 결과(방 크기 및 딱정벌레 수에 따른 수행 시간 등) 및 
    #   방 크기 증가에 따른 예측 결과를 쉽게 이해할 수 있도록
    #   표 또는 그래프 형태를 활용하여 표현한다. (엑셀 사용 권장)
    # ▪기본 메뉴를 제공한다.
    # ▪상세한 입력과 출력 메시지를 제공한다. 
    #   실행  결과에 대한 주요 정보만을 화면에 출력하고 자세한 내용은 파일에 저장한다.
    # ▪2개 이상의 소스파일과 1개 이상의 헤더파일을 사용한다.
    # ▪전역 변수를 사용할 수 없다.
# 확장 문제
    # 딱정벌레의 마리 수에 따른 통계 결과와 그래프를 추가적으로 제시하시오