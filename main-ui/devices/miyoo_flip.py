import subprocess
from apps.miyoo.miyoo_app_finder import MiyooAppFinder
from controller.controller_inputs import ControllerInput
from devices.charge.charge_status import ChargeStatus
from devices.device import Device
import os
from devices.miyoo.system_config import SystemConfig
from devices.wifi.wifi_status import WifiStatus
import sdl2
from utils import throttle

os.environ["SDL_VIDEODRIVER"] = "KMSDRM"
os.environ["SDL_RENDER_DRIVER"] = "kmsdrm"

class MiyooFlip(Device):
    
    def __init__(self):
        self.path = self
        self.sdl_button_to_input = {
            sdl2.SDL_CONTROLLER_BUTTON_A: ControllerInput.B,
            sdl2.SDL_CONTROLLER_BUTTON_B: ControllerInput.A,
            sdl2.SDL_CONTROLLER_BUTTON_X: ControllerInput.Y,
            sdl2.SDL_CONTROLLER_BUTTON_Y: ControllerInput.X,
            sdl2.SDL_CONTROLLER_BUTTON_DPAD_UP: ControllerInput.DPAD_UP,
            sdl2.SDL_CONTROLLER_BUTTON_DPAD_DOWN: ControllerInput.DPAD_DOWN,
            sdl2.SDL_CONTROLLER_BUTTON_DPAD_LEFT: ControllerInput.DPAD_LEFT,
            sdl2.SDL_CONTROLLER_BUTTON_DPAD_RIGHT: ControllerInput.DPAD_RIGHT,
            sdl2.SDL_CONTROLLER_BUTTON_LEFTSHOULDER: ControllerInput.L1,
            sdl2.SDL_CONTROLLER_BUTTON_RIGHTSHOULDER: ControllerInput.R1,
            sdl2.SDL_CONTROLLER_BUTTON_START: ControllerInput.START,
            sdl2.SDL_CONTROLLER_BUTTON_BACK: ControllerInput.SELECT,
        }

        #Idea is if something were to change from he we can reload it
        #so it always has the more accurate data
        self.SystemConfig = SystemConfig("/userdata/system.json")

    @property
    def screen_width(self):
        return 640

    @property
    def screen_height(self):
        return 480

    @property
    def font_size_small(self):
        return 12
    
    @property
    def font_size_medium(self):
        return 18
    
    @property
    def font_size_large(self):
        return 26

    @property
    def max_rows_for_list(self):
        return 10

    @property
    def max_rows_for_descriptive_list(self):
        return 4
    
    #Can we dynamically calculate these?
    @property
    def max_icons_for_large_grid_view(self):
        return 4
    
    @property
    def large_grid_x_offset(self):
        return 34

    @property
    def large_grid_y_offset(self):
        return 160
    
    @property
    def large_grid_spacing_multiplier(self):
        icon_size = 140
        return icon_size + self.large_grid_x_offset // 2
    
    def run_game(self, file_path):
        print(f"About to launch /mnt/sdcard/Emu/.emu_setup/standard_launch.sh {file_path}")
        subprocess.run(["/mnt/sdcard/Emu/.emu_setup/standard_launch.sh",file_path])

    def run_app(self, file_path):
        print(f"About to launch app {file_path}")
        subprocess.run([file_path])

    #TODO untested
    def map_analog_axis(self,sdl_input, value, threshold=16000):
        if sdl_input == sdl2.SDL_CONTROLLER_AXIS_LEFTX:
            if value < -threshold:
                return ControllerInput.LEFT_STICK_LEFT
            elif value > threshold:
                return ControllerInput.LEFT_STICK_RIGHT
        elif sdl_input == sdl2.SDL_CONTROLLER_AXIS_LEFTY:
            if value < -threshold:
                return ControllerInput.LEFT_STICK_UP
            elif value > threshold:
                return ControllerInput.LEFT_STICK_DOWN
        elif sdl_input == sdl2.SDL_CONTROLLER_AXIS_RIGHTX:
            if value < -threshold:
                return ControllerInput.RIGHT_STICK_LEFT
            elif value > threshold:
                return ControllerInput.RIGHT_STICK_RIGHT
        elif sdl_input == sdl2.SDL_CONTROLLER_AXIS_RIGHTY:
            if value < -threshold:
                return ControllerInput.RIGHT_STICK_UP
            elif value > threshold:
                return ControllerInput.RIGHT_STICK_DOWN
        return None
    
    def map_input(self, sdl_input):
        return self.sdl_button_to_input[sdl_input]
    
    def get_wifi_link_quality_level(self):
        try:
            with open("/proc/net/wireless", "r") as wireless_info:
                output = [*map(str.strip, wireless_info.readlines())]
            
            if len(output) >= 3:
                # The 3rd line contains the actual wireless stats
                data_line = output[2]
                parts = data_line.split()
                
                # parts[2] is the link quality, parts[3] is the level
                link_level = float(parts[3].strip('.'))  # Remove trailing dot
                return int(link_level)
        except Exception as e:
            return 0
    
    @throttle.limit_refresh(15)
    def get_wifi_status(self):
        link_quality_level = self.get_wifi_link_quality_level()
        if(link_quality_level >= 70):
            return WifiStatus.GREAT
        elif(link_quality_level >= 50):
            return WifiStatus.GOOD
        elif(link_quality_level >= 30):
            return WifiStatus.OKAY
        else:
            return WifiStatus.BAD
        
    @throttle.limit_refresh(15)
    def get_charge_status(self):
        with open("/sys/class/power_supply/usb/online", "r") as usb:
            return ChargeStatus.CHARGING if int(usb.read().strip()) == 1 else ChargeStatus.DISCONNECTED

    @throttle.limit_refresh(15)
    def get_battery_percent(self):
        with open("/sys/class/power_supply/battery/capacity", "r") as capacity:
            return int(capacity.read().strip())
    
    def get_app_finder(self):
        return MiyooAppFinder()