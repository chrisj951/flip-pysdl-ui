
import os
from controller.controller import Controller
from controller.controller_inputs import ControllerInput
from devices.device import Device
from display.display import Display
from display.on_screen_keyboard import OnScreenKeyboard
from menus.settings.bluetooth_menu import BluetoothMenu
from menus.settings.wifi_menu import WifiMenu
from themes.theme import Theme
from utils.py_ui_config import PyUiConfig
from views.descriptive_list_view import DescriptiveListView
from views.grid_or_list_entry import GridOrListEntry
from views.selection import Selection
from views.view_creator import ViewCreator
from views.view_type import ViewType


class SettingsMenu:
    def __init__(self, display: Display, controller: Controller, device: Device, theme: Theme, config: PyUiConfig):
        self.display = display
        self.controller = controller
        self.device = device
        self.theme = theme
        self.config : PyUiConfig = config 
        self.on_screen_keyboard = OnScreenKeyboard(display,controller,device,theme)
        self.wifi_menu = WifiMenu(display,controller,device,theme)
        self.bt_menu = BluetoothMenu(display,controller,device,theme)
        self.view_creator = ViewCreator(display,controller,device,theme)

    def shutdown(self, input: ControllerInput):
        if(ControllerInput.A == input):
           self.device.run_app(self.device.power_off_cmd)
    
    def reboot(self, input: ControllerInput):
        if(ControllerInput.A == input):
            self.device.run_app(self.device.reboot_cmd)
    
    def lumination_adjust(self, input: ControllerInput):
        if(ControllerInput.DPAD_LEFT == input or ControllerInput.L1 == input):
            self.device.lower_lumination()
        elif(ControllerInput.DPAD_RIGHT == input or ControllerInput.R1 == input):
            self.device.raise_lumination()
    
    def brightness_adjust(self, input: ControllerInput):
        if(ControllerInput.DPAD_LEFT == input or ControllerInput.L1 == input):
            self.device.lower_brightness()
        elif(ControllerInput.DPAD_RIGHT == input or ControllerInput.R1 == input):
            self.device.raise_brightness()

    def contrast_adjust(self, input: ControllerInput):
        if(ControllerInput.DPAD_LEFT == input or ControllerInput.L1 == input):
            self.device.lower_contrast()
        elif(ControllerInput.DPAD_RIGHT == input or ControllerInput.R1 == input):
            self.device.raise_contrast()

    def saturation_adjust(self, input: ControllerInput):
        if(ControllerInput.DPAD_LEFT == input or ControllerInput.L1 == input):
            self.device.lower_saturation()
        elif(ControllerInput.DPAD_RIGHT == input or ControllerInput.R1 == input):
            self.device.raise_saturation()
    
    def volume_adjust(self, input: ControllerInput):
        if(ControllerInput.DPAD_LEFT == input):
            self.device.change_volume(-10)
        elif(ControllerInput.L1 == input):
            self.device.change_volume(-1)
        elif(ControllerInput.DPAD_RIGHT == input):
            self.device.change_volume(+10)
        elif(ControllerInput.R1 == input):
            self.device.change_volume(+1)

    def show_on_screen_keyboard(self, input):
        print(self.on_screen_keyboard.get_input())

    def show_wifi_menu(self, input):
        if(ControllerInput.DPAD_LEFT == input or ControllerInput.DPAD_RIGHT == input):
            if(self.device.is_wifi_enabled()):
                self.device.disable_wifi()
            else:
                self.device.enable_wifi()
        else:
            self.wifi_menu.show_wifi_menu()

    def show_bt_menu(self, input):
        if(ControllerInput.DPAD_LEFT == input or ControllerInput.DPAD_RIGHT == input):
            if(self.device.is_bluetooth_enabled()):
                self.device.disable_bluetooth()
            else:
                self.device.enable_bluetooth()
        else:
            self.bt_menu.show_bluetooth_menu()



    def get_theme_folders(self):
        theme_dir = self.config["theme_dir"]
        return sorted(
            [
                name for name in os.listdir(theme_dir)
                if os.path.isdir(os.path.join(theme_dir, name)) and
                os.path.isfile(os.path.join(theme_dir, name, "config.json"))
            ]
        )    
    
    def change_theme(self, input):
        theme_folders = self.get_theme_folders()
        selected_index = theme_folders.index(self.config["theme"])

        if(ControllerInput.DPAD_LEFT == input):
            selected_index-=1
            if(selected_index < 0):
                selected_index = len(theme_folders) -1
        elif(ControllerInput.DPAD_RIGHT == input):
            selected_index+=1
            if(selected_index == len(theme_folders)):
                selected_index = 0

        self.theme.set_theme_path(os.path.join(self.config["theme_dir"], theme_folders[selected_index]))
        self.display.init_fonts()   
        self.config["theme"] = theme_folders[selected_index]
        self.config.save()

    def build_options_list(self):
        option_list = []
        option_list.append(
                GridOrListEntry(
                        primary_text="Power Off",
                        image_path=None,
                        image_path_selected=None,
                        description=None,
                        icon=None,
                        value=self.shutdown
                    )
            )
        option_list.append(
                GridOrListEntry(
                        primary_text="Lumination",
                        value_text="<    " + str(self.device.lumination) + "    >",
                        image_path=None,
                        image_path_selected=None,
                        description=None,
                        icon=None,
                        value=self.lumination_adjust
                    )
            )

        option_list.append(
                GridOrListEntry(
                        primary_text="Volume",
                        value_text="<    " + str(self.device.get_volume()) + "    >",
                        image_path=None,
                        image_path_selected=None,
                        description=None,
                        icon=None,
                        value=self.volume_adjust
                    )
            )
        option_list.append(
                GridOrListEntry(
                        primary_text="WiFi",
                        value_text="<    " + ("On" if self.device.is_wifi_enabled() else "Off") + "    >",
                        image_path=None,
                        image_path_selected=None,
                        description=None,
                        icon=None,
                        value=self.show_wifi_menu
                    )
            )
        option_list.append(
                GridOrListEntry(
                        primary_text="Bluetooth",
                        value_text="<    " + ("On" if self.device.is_bluetooth_enabled() else "Off") + "    >",
                        image_path=None,
                        image_path_selected=None,
                        description=None,
                        icon=None,
                        value=self.show_bt_menu
                    )
            )
            
        option_list.append(
                GridOrListEntry(
                        primary_text="Theme",
                        value_text="<    " + self.config["theme"] + "    >",
                        image_path=None,
                        image_path_selected=None,
                        description=None,
                        icon=None,
                        value=self.change_theme
                    )
            )
        option_list.append(
                GridOrListEntry(
                        primary_text="Brightness",
                        value_text="<    " + str(self.device.brightness) + "    >",
                        image_path=None,
                        image_path_selected=None,
                        description=None,
                        icon=None,
                        value=self.brightness_adjust
                    )
            )
        option_list.append(
                GridOrListEntry(
                        primary_text="Contrast",
                        value_text="<    " + str(self.device.contrast) + "    >",
                        image_path=None,
                        image_path_selected=None,
                        description=None,
                        icon=None,
                        value=self.contrast_adjust
                    )
            )
        option_list.append(
                GridOrListEntry(
                        primary_text="Saturation",
                        value_text="<    " + str(self.device.saturation) + "    >",
                        image_path=None,
                        image_path_selected=None,
                        description=None,
                        icon=None,
                        value=self.saturation_adjust
                    )
            )
        option_list.append(
                GridOrListEntry(
                        primary_text="On Screen Keyboard",
                        value_text=None,
                        image_path=None,
                        image_path_selected=None,
                        description=None,
                        icon=None,
                        value=self.show_on_screen_keyboard
                    )
            )
        option_list.append(
                GridOrListEntry(
                        primary_text="Reboot",
                        image_path=None,
                        image_path_selected=None,
                        description=None,
                        icon=None,
                        value=self.reboot
                )
        )
        
        return option_list


    def show_menu(self) :
        selected = Selection(None, None, 0)
        list_view = None
        while(selected is not None):
            option_list = self.build_options_list()
            

            if(list_view is None):
                list_view = self.view_creator.create_view(
                    view_type=ViewType.DESCRIPTIVE_LIST_VIEW,
                    top_bar_text="Settings", 
                    options=option_list,
                    selected_index=selected.get_index())
            else:
                list_view.set_options(option_list)

            control_options = [ControllerInput.A, ControllerInput.DPAD_LEFT, ControllerInput.DPAD_RIGHT,
                                                  ControllerInput.L1, ControllerInput.R1]
            selected = list_view.get_selection(control_options)

            if(selected.get_input() in control_options):
                selected.get_selection().get_value()(selected.get_input())
            elif(ControllerInput.B == selected.get_input()):
                selected = None

