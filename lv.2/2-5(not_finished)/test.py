from pynput import keyboard

def spin():
    print('start')
    while pause:
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
    print('end')

def on_press(key):
    try:
        if key.char == 'a':
            global pause
            print('pressed a', pause)
            pause = False
            return True
    except:
        None

    if key == keyboard.Key.up:
        print('pressed up')
        return False

if __name__ == "__main__":
    pause = True

    spin()