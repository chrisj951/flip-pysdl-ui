

import os

class GameSystemUtils:
    def __init__(self):
        self.roms_path = "/mnt/sdcard/Roms/"
        self.emu_path = "/mnt/sdcard/Emu/"

    def is_system_active(self, folder):
        config_path = os.path.join(self.emu_path,folder, "config.json")
        if not os.path.isfile(config_path):
            return False

        try: # maybe replace this with an attempt at running json.load? we purposely break the json to hide systems anyway
            with open(config_path, "r", encoding="utf-8") as f:
                first_chars = f.read(2)
                return first_chars != "{{"
        except:
            return False
        
    def get_active_systems(self):        
        # Step 1: Get list of folders in self.emu_path
        try:
            folders = [folder for folder in os.listdir(self.emu_path) if os.path.isdir(os.path.join(self.emu_path, folder))]
        except FileNotFoundError:
            return []  # or handle the error as needed

        # sorted list of active systems
        return sorted(folder for folder in folders if self.is_system_active(folder))