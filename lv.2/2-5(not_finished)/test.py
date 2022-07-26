from pynput import keyboard

def spin():
    print('start')
    while pause:
        None
    print('end')

def on_press(key):
    try:
        if key.char == 'a':
            pause = False
            return True
    except:
        None

    if key == keyboard.Key.up:
        return False

if __name__ == "__main__":
    pause = True
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
    spin()