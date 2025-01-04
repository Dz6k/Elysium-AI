# ==== IMPORTS ==== #
from utils import Mouse, config
import numpy as np
import threading
import win32api
import time
import mss
import cv2


class Frame(threading.Thread):
    def __init__(self):
        super().__init__()
       
    @staticmethod 
    def __get_sc(self) -> np.ndarray:
        with mss.mss() as sct:  
            screenshot = sct.grab(config.monitor)
            frame = np.array(screenshot)
            return cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        
    @property
    def is_leftmouse_down(self) -> bool:
        return bool(win32api.GetKeyState(Mouse.LEFTC) < 0)
    
    def custom_fov(self) -> None:
        if self.is_leftmouse_down: pass
    
    def get_new_frame(self) -> None:
        while True:
            if not config.stopped:
                config.frame = self.__get_sc()
            time.sleep(0.0001)
    
    def run(self) -> None:
        self.get_new_frame()

frame = Frame()
# frame.start()
