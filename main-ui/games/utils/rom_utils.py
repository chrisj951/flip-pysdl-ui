import os

class RomUtils:
    def __init__(self, roms_path):
        self.roms_path = roms_path

    def get_roms_path(self):
        return self.roms_path
    
    def get_roms(self, system):
        return [
            filename for filename in os.listdir(os.path.join(self.roms_path, system))
            if not (
                os.path.isdir(os.path.join(directory, filename))
                or any(filename.endswith(ext) for ext in (".xml", ".txt", ".db"))
                or filename.startswith(".")
            )
        ]