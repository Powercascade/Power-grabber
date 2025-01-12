import random
import os
import subprocess
import sys
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
try:
    import requests
except ImportError:
    install('requests')
    import requests
try:
    from discord import Embed
except ImportError:
    install('discord.py')
    from discord import Embed
port_file = "port.txt"
port_range_start = 1000
port_range_end = 5051
def is_port_in_use(port):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return False
        except OSError:
            return True
if os.path.exists(port_file):
    with open(port_file, 'r') as f:
        port = int(f.read().strip())
else:
    port = random.randint(port_range_start, port_range_end)
    while True:
        if not is_port_in_use(port):
            break
        port = random.randint(port_range_start, port_range_end)
    with open(port_file, 'w') as f:
        f.write(str(port))
embed = Embed(title='New Port Available', color=0x8B0000)
embed.add_field(name='Port Number', value=str(port))
payload = {'embeds': [embed.to_dict()]}
response = requests.post(webhook_url, json=payload)
if response.status_code == 204:
    pass
else:
    pass
