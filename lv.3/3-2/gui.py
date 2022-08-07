import multiprocessing as mp
import os

from main_dialog import GUI

if __name__ == "__main__":
    mp.freeze_support()
    # https://github.com/pyinstaller/pyinstaller/issues/3957#issuecomment-674579877
    # Pyinstaller multiprocessing name of process is always "MainProcess" 해결
    if 'main_started' not in os.environ:
        os.environ['main_started'] = ''
        GUI().run() # 인스턴스 생성 없이 바로 실행
        os.system('pause')

# pyinstaller --onefile gui.py
