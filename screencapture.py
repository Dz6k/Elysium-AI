import mss
from utils import Mouse, config
import numpy as np
import win32api
import time
 

class Screen:
    
    def __init__(self) -> None:
        self.sct = mss.mss()
        
    def get_sc(self) -> np.ndarray:
        screenshot = self.sct.grab(config.monitor)
        return np.array(screenshot)[:, :, :3]

    @property
    def is_leftmouse_down(self) -> bool:
        return bool(win32api.GetKeyState(Mouse.LEFTC) < 0)
    
    def custom_fov(self):
        if self.is_leftmouse_down:
            pass
    
    
    
screen = Screen()
print(screen.get_sc())
