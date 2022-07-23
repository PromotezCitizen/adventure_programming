from pynput import keyboard
from puzzle_runner import NPuzzleRunner

def on_press(key):
    end = False
    try:
        if key.char == 'h':
            print(test.hint())
        elif key.char == '1':
            test.save()
        elif key.char == '2':
            test.load()
            None
    except:
        None
    
    if key == keyboard.Key.up:
        end = test.mv_up()
    elif key == keyboard.Key.down:
        end = test.mv_down()
    elif key == keyboard.Key.left:
        end = test.mv_left()
    elif key == keyboard.Key.right:
        end = test.mv_right()
    if end == True:
        return False
    if key == keyboard.Key.esc:
        return False

if __name__ == "__main__":
    while True:
        while True:
            sl = input("시작 : s, 로드 : l")
            if sl.lower() == 's':
                size = int(input('퍼즐 가로 크기 입력 >> '))
                test = NPuzzleRunner(size)
                test.mv_start()
                break
            elif sl.lower() == 'l':
                test = NPuzzleRunner(2)
                if test.load():
                    break


        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
        if input("exit?(Y/n) >> ").lower() == 'y':
            break