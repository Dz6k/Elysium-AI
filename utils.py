# ==== IMPORTS ==== #
from dataclasses import dataclass, field
import win32api, win32con  
import numpy as np
import colorama
import torch
import sys
import os
import json
# COLORAMA CONFIG
colorama.init(True)

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
class CudaConfig:
    backend: str = field(init=False)
    
    def __post_init__(self):
        self.backend = "cuda" if torch.cuda.is_available() else "cpu"

 
@dataclass
class Config:
    screen_width: int 
    screen_height: int 
    crosshair_x: int
    crosshair_y: int
    box_size: int 
    sensibilidade: float
    offset_y: float 
    distance: list = field(default_factory=lambda: [{"distance": None, "x": None, "y": None}])
    moviment: dict = field(default_factory=lambda: {"x": None, "y": None})
    monitor: dict = field(init=False) 
    fov: dict = field(init=False) 
    alpha: int = field(init=False) 
    confidence: float = field(default=0.5) 
    stopped: bool = field(default=False) 
    frame: np.ndarray = field(default=None) 
    stopped_key: int = field(default=win32con.VK_F1)

    def __post_init__(self):
        self.alpha = round(self.screen_width * self.screen_height * self.box_size / (1920 * 1080))
        
        self.monitor = {
            "top"      :    self.crosshair_y - self.alpha,
            "left"     :    self.crosshair_x - self.alpha,
            "width"    :    2 * self.alpha,
            "height"   :    2 * self.alpha
        }
        
        self.fov = {
            "left"     :    self.monitor["left"],
            "top"      :    self.monitor["top"],
            "width"    :    self.monitor["left"] + self.monitor["width"],
            "height"   :    self.monitor["top"] + self.monitor["height"],
        } 
        
with open("config.json", "r") as file:
    config_data = json.load(file) 
# Acessando os dados
offset_y = config_data["offset_y"]
sensibilidade = config_data["sensibilidade"]
box_fov = config_data["box-fov"]
confidence = config_data["confidence"]

config = Config(
    screen_width   =   screen_metric()["x"],            # monitor metrics
    screen_height  =   screen_metric()["y"],            # monitor metrics
    crosshair_x    =   (screen_metric()["x"] // 2),     # monitor metrics // 2
    crosshair_y    =   (screen_metric()["y"] // 2),     # monitor metrics // 2
    box_size       =   int(box_fov),                             # ↑BOX_SIZE --> ↓SPEED ↑DETECTION_AREA
    confidence     =   float(confidence),                             # confidence (0.00, 1.00]
    stopped        =   False,                           # turn on/off
    stopped_key    =   win32con.VK_F1,                  # bind turn on/off event
    sensibilidade  =   float(sensibilidade),                             # radio of fov, -->> doesn"t work yet
    offset_y       =   float(offset_y),                           # radio of fov, -->> doesn"t work yet
)

cuda_config = CudaConfig()

# === DON"T CHANGE === #
MONITOR_CONFIG_BACKUP = config.monitor

if __name__ == "__main__":
    os.system("cls")
    
    print(f"{colorama.Fore.GREEN} Screen Wigth: {colorama.Fore.BLUE} {config.screen_width}")
    print(f"{colorama.Fore.GREEN} Screen Height: {colorama.Fore.BLUE} {config.screen_height}")
    print(f"{colorama.Fore.GREEN} Crosshair X: {colorama.Fore.BLUE} {config.crosshair_x}")
    print(f"{colorama.Fore.GREEN} Crosshair Y: {colorama.Fore.BLUE} {config.crosshair_y}")
    print(f"{colorama.Fore.GREEN} Box Size: {colorama.Fore.BLUE} {config.box_size}")
    print(f"{colorama.Fore.GREEN} Confidence Factor: {colorama.Fore.BLUE} {config.confidence}")
    print(f"{colorama.Fore.GREEN} Alpha: {colorama.Fore.BLUE} {config.alpha}")
    print(f"{colorama.Fore.GREEN} Stopped: {colorama.Fore.BLUE} {config.stopped}")
    print(f"{colorama.Fore.GREEN} Stopped Bind: {colorama.Fore.BLUE} {config.stopped_key}")
    print(f"{colorama.Fore.GREEN} Monitor Dict: {colorama.Fore.BLUE} {config.monitor}")
    print(f"{colorama.Fore.GREEN} Fov: {colorama.Fore.BLUE} {config.fov}")


    
    input(f"\nPress {colorama.Fore.RED}ENTER{colorama.Fore.RESET} to close and clear.")

    os.system("cls")