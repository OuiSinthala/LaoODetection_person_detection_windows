from pynput import keyboard

def default_function():
    print("Default function running")

def function_1():
    print("Function 1 running")

def function_2():
    print("Function 2 running")

# Global variable to store the latest key press
latest_key = None

def on_press(key):
    global latest_key

    try:
        latest_key = key.char
    except AttributeError:
        pass

    if latest_key == '1':
        default_function()
    elif latest_key == '2':
        function_1()
    elif latest_key == '3':
        function_2()

def on_release(key):
    pass

def listen_for_key_press():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Run the function in the background
if __name__ == '__main__':
    listen_for_key_press()
