
import os
from controller.controller import Controller
from devices.device import Device
from display.display import Display
from menus.games.roms_menu_common import RomsMenuCommon
from themes.theme import Theme
from views.grid_or_list_entry import GridOrListEntry


class FavoritesMenu(RomsMenuCommon):
    def __init__(self, display: Display, controller: Controller, device: Device, theme: Theme):
        super().__init__(display,controller,device,theme)

    def _get_rom_list(self) -> list[GridOrListEntry]:
        return [
            GridOrListEntry(
                primary_text=f"{self._remove_extension(os.path.basename(recent.rom_path))} ({self._extract_game_system(recent.rom_path)})",
                image_path=(img_path := self._get_image_path(favorite.rom_path)),
                image_path_selected=img_path,
                description="Favorite", 
                icon=None,
                value=favorite.rom_path
            )
            for favorite in self.device.parse_favorites()
        ]

    def run_rom_selection(self) :
        self._run_rom_selection("Favorites")