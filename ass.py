from pynput import keyboard
import threading
import time

typed_chars = []
lock = threading.Lock() #the python built-in threading.Lock() (mutex) object
delay = 1  # s

def get_active_window():
    # Placeholder function for platform-specific active window retrieval
    return "Active Window"

def print_typed_chars():
    while True:
        time.sleep(delay)
        with lock:
            if typed_chars:
                active_window = get_active_window()
                print(f'Typed in {active_window}: {"".join(typed_chars)}')
                typed_chars.clear()

def on_press(key):
    with lock:
        try:
            typed_chars.append(key.char)
        except AttributeError:
            typed_chars.append(f'[{key}]')

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Start thread
threading.Thread(target=print_typed_chars, daemon=True).start()

# Collect events until> released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
