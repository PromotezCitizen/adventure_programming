from pynput import keyboard

from puzzle_runner import NPuzzleRunner

def on_press(key):
    end = False
    try:
        if key.char == 'h':
            print(test.hint())
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
        size = int(input('퍼즐 가로 크기 입력 >> '))
        test = NPuzzleRunner(size)
        test.mv_start()
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
        if input("exit?(Y/n) >> ").lower() == 'y':
            break