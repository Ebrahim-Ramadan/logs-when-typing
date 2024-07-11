from pynput import keyboard
import threading
import time

typed_chars = []
lock = threading.Lock()
delay = 1  # seconds

def get_active_window():
    # Placeholder function for platform-specific active window retrieval
    return "Active Window"

def print_typed_word():
    while True:
        time.sleep(delay)
        with lock:
            if typed_chars:
                active_window = get_active_window()
                print(f'Typed in {active_window}: {"".join(typed_chars)}')
                typed_chars.clear()

def on_press(key):
    global typed_chars
    with lock:
        try:
            if key.char == " ":
                active_window = get_active_window()
                print(f'Typed in {active_window}: {"".join(typed_chars)}')
                typed_chars = []
            else:
                typed_chars.append(key.char)
        except AttributeError:
            if key == keyboard.Key.enter:
                active_window = get_active_window()
                print(f'Typed in {active_window}: {"".join(typed_chars)}')
                typed_chars = []

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Start a thread to print typed words with a delay
threading.Thread(target=print_typed_word, daemon=True).start()

# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
