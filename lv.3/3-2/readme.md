test.py - 개발하면서 테스트 했던 모든 함수 및 알고리즘 백업용

gui.py - pyinstaller로 exe 변환 가능. --hidden-import multipledispatch 옵션 줘야 함
cli.py - pyinstaller로 exe 변환 가능. --hidden-import multipledispatch 옵션 줘야 함

의존성
    pip install -r requiements

    | multipledispatch    # 함수 오버로딩 위한 모듈
    | pyinstaller         # *.py to *.exe

gui.py의 경우 exe로 만들 경우 아래와 같이 모든 프로세스 이름이 MainProcess, __name__값이 "__main__"으로 고정
환경변수 추가를 통해 해결


![image](https://user-images.githubusercontent.com/81803973/183275958-58e675e4-99f0-4dbb-8f54-d6c0108aee25.png)
