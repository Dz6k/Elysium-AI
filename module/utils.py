# ==== IMPORTS ==== #
from dataclasses import dataclass, field
import win32api, win32con  
import numpy as np
import colorama
import sys
import os
import json
from threading import Lock, Event
lock:Lock = Lock()
is_runing:Event = Event()
screen_metric = lambda: {"x":win32api.GetSystemMetrics(0), "y": win32api.GetSystemMetrics(1)} 

class Files:
    @staticmethod
    def resource_path(relative_path: str) -> str:
        """
        this function returns the file path based on your current folder
        
        Parameters:
            relative_path (str): Path of your yolo model.onnx | model.pt

        Returns:
            str: file path
        """
        base_path = getattr(
            sys,
            "_MEIPASS",
            os.path.dirname(os.path.abspath(__file__)))
        
        return os.path.join(base_path, relative_path)
    
    @staticmethod
    def resource_path_root(relative_path: str) -> str:
        """
        this function returns the file path based on your project"s root folder
        
        Parameters:
            relative_path (str): Path of your yolo model.onnx | model.pt

        Returns:
            str: file path
        """
        base_path = getattr(
            sys,
            "_MEIPASS", 
            os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  
        )
        return os.path.join(base_path, relative_path)
        

@dataclass(frozen=True)
class Mouse:
    RIGHTC: int = 0x02  
    LEFTC: int = 0x01  
    X1C: int =  0x05
    X2C: int =  0x06


@dataclass
class Config:
    screen_width: int 
    screen_height: int 
    crosshair_x: int
    crosshair_y: int
    result: list = field(default_factory=lambda: [])
    distance: list = field(default_factory=lambda: [{"distance": None, "x": None, "y": None}])
    moviment: dict = field(default_factory=lambda: {"x": None, "y": None})
    monitor: dict = field(init=False) 
    offset_y: float = field(init=False) 
    sensi: float = field(init=False)
    fov: dict = field(init=False) 
    fov_value: int = field(init=False)
    fov_value_backup: int = field(init=False) 
    fov_min: int = field(init=False) 
    smooth: bool = field(init=False)
    smooth_value: int = field(init=False)
    t_factor: float = field(init=False)
    fov_min_backup: int = field(init=False) 
    confidence: float = field(default=0.5) 
    stopped: bool = field(default=False) 
    frame: np.ndarray = field(default=None) 
    stopped_key: int = field(default=win32con.VK_F3)

    def __post_init__(self):
        with open("config.json", "r") as file:
            config_data = json.load(file) 

        self.offset_y = config_data["offset_y"]
        self.sensi = config_data["sensi"]
        self.fov_value = config_data["fov"]
        self.fov_value_backup = config_data["fov"]
        self.confidence = config_data["confidence"]
        self.smooth_value = config_data["smooth_value"]
        self.smooth = config_data["smooth_enable"]
        self.t_factor = config_data["t_factor"]
        self.fov_min = config_data["fov-min"]
        
        self.monitor = {
            "left"     :    self.crosshair_x - self.fov_value,
            "top"      :    self.crosshair_y - self.fov_value,
            "width"    :    2 * self.fov_value,
            "height"   :    2 * self.fov_value
        }
        
        self.fov = {
            "left"     :    self.monitor["left"],
            "top"      :    self.monitor["top"],
            "width"    :    self.monitor["left"] + self.monitor["width"],
            "height"   :    self.monitor["top"] + self.monitor["height"],
        } 
        
config = Config(
    screen_width   =   screen_metric()["x"],            # monitor metrics 
    screen_height  =   screen_metric()["y"],            # monitor metrics
    crosshair_x    =   (screen_metric()["x"] // 2),     # monitor metrics // 2
    crosshair_y    =   (screen_metric()["y"] // 2),     # monitor metrics // 2
    stopped        =   False,                           # turn on/off
)

def update_config():
    with open("config.json", "r") as file:
        config_data = json.load(file) 
    config.offset_y = config_data["offset_y"]
    config.sensi = config_data["sensi"]
    config.fov_value = config_data["fov"]
    config.fov_value_backup = config_data["fov"]
    config.confidence = config_data["confidence"]
    config.smooth = config_data["smooth_enable"]
    config.smooth_value = config_data["smooth_value"]
    config.fov_min = config_data["fov-min"]
    config.t_factor = config_data["t_factor"]
    os.system('cls')
    print('Config Update')

 
# === DON"T CHANGE === #
MONITOR_CONFIG_BACKUP = config.monitor

if __name__ == "__main__":
    os.system("cls")
    colorama.init(True)
    print(f"{colorama.Fore.GREEN} Screen Wigth: {colorama.Fore.BLUE} {config.screen_width}")
    print(f"{colorama.Fore.GREEN} Screen Height: {colorama.Fore.BLUE} {config.screen_height}")
    print(f"{colorama.Fore.GREEN} Crosshair X: {colorama.Fore.BLUE} {config.crosshair_x}")
    print(f"{colorama.Fore.GREEN} Crosshair Y: {colorama.Fore.BLUE} {config.crosshair_y}")
    print(f"{colorama.Fore.GREEN} Confidence Factor: {colorama.Fore.BLUE} {config.confidence}")
    print(f"{colorama.Fore.GREEN} Stopped: {colorama.Fore.BLUE} {config.stopped}")
    print(f"{colorama.Fore.GREEN} Stopped Bind: {colorama.Fore.BLUE} {config.stopped_key}")
    print(f"{colorama.Fore.GREEN} Monitor Dict: {colorama.Fore.BLUE} {config.monitor}")
    print(f"{colorama.Fore.GREEN} Fov: {colorama.Fore.BLUE} {config.benzier_sensibilidade}")
    print(f"{colorama.Fore.GREEN} Fov: {colorama.Fore.BLUE} {config.benzier_pixel_increment}")
    print(f"{colorama.Fore.GREEN} Fov: {colorama.Fore.BLUE} {config.benzier_aim_smooth}")
    print(f"{colorama.Fore.GREEN} Fov: {colorama.Fore.BLUE} {config.fov_min}")
    print(f"{colorama.Fore.GREEN} Fov: {colorama.Fore.BLUE} {config.benzier_distance_to_scale}")
    
    input(f"\nPress {colorama.Fore.RED}ENTER{colorama.Fore.RESET} to close and clear.")

    os.system("cls")