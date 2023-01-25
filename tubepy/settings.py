# all settings for the application
import tkinter as tk
from tkinter import filedialog
import json
from lang import read_config_file, download_location, empty

# using new_location for testing purposes
# new_location:str = "~/Music"
def change_download_location(new_location):
    try:
        # default_location = read_config_file
        default_location = read_config_file()
        default_location["download_location"] = new_location

        with open('utilities/config.json', 'w') as file_location:
            json.dump(default_location, file_location, indent=4 )
        
    except Exception:
        print(empty.get("empty_location"))
    else:
        default_location["download_location"] = download_location
        
# change_download_location(new_location)

def download_path_settings():
    root = tk.Tk()
    root.withdraw()

    filepath = filedialog.askdirectory()
    change_download_location(filepath)
