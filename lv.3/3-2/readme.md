임의의 텍스트 파일이 주어지면 허프만 코딩 방법을 이용하여 자료를 압축하며 압축된 파일을 해제하는 프로그램을 작성한다.
다수의 텍스트 파일에서 실험을 하여 각각의 압축률과 평균적인 압축률을 계산해 본다.


+ 제한요소 및 요구사항
  * 허프만 코드로 압축한 파일은 이진 파일로 저장한다. - 완료
  * 허프만 코드로 압축한 파일은 허프만 테이블과 허프만 부호화코드를 포함한다. - 완료
  * 50,000자, 100,000자, 500,000 자 이상의 텍스트 파일을 직접 준비한다.
  * 여러 가지 텍스트 파일에 대해 압축을 수행하여 파일별 및 평균적인 통계정보(압축률, 문자당 평균 비트 수, 압축 및 복원 시간 등)를 계산한다.

    압축률 : 파일 bit수 비교, 평균 비트 수 : encoder의 _huffman_len_histogram 활용
    압축 및 복원 시간 : time 함수 이용

+ 확장 기능
  * GUI 구현 - 완료
  * ASCII 문자 이외의 문자(한글, 유니코드 등)에 대해서도 동작하도록 한다.

        본 기능의 구현은 쉽지 않을 것으로 판단됨. 문제 분석 시 구현 가능성에 대해 검토
            - 동작은 함. binary로 읽어서 binary로 쓰기 때문.

+ 추가 기능
  * 자동 인코딩/디코딩 - 완료
  * 복호화 시 자동으로 확장자 명 추가 - 완료


- - -
# 참고사항
test.py - 개발하면서 테스트 했던 모든 함수 및 알고리즘 백업용

gui.py - pyinstaller로 exe 변환 가능. --hidden-import multipledispatch 옵션 줘야 함
cli.py - pyinstaller로 exe 변환 가능. --hidden-import multipledispatch 옵션 줘야 함

의존성
    pip install -r requiements

    | multipledispatch    # 함수 오버로딩 위한 모듈
    | pyinstaller         # *.py to *.exe

gui.py의 경우 exe로 만들 경우 아래와 같이 모든 프로세스 이름이 MainProcess, __name__값이 "\_\_main\_\_"으로 고정

환경변수 추가를 통해 해결

![image](https://user-images.githubusercontent.com/81803973/183275958-58e675e4-99f0-4dbb-8f54-d6c0108aee25.png)
