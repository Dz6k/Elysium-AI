# ==== IMPORTS ==== #
from utils import Mouse, config
import threading
import win32api  
import time
from fast_ctypes_screenshots import ScreenshotOfRegion
import mss
import numpy as np
import cv2

class Frame(threading.Thread):
    def __init__(self):
        super().__init__()
       
    # @staticmethod 
    def get_sc(self):
        with mss.mss() as sct:  
            screenshot = sct.grab(config.monitor)
        frame = np.array(screenshot)
        return cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    # def get_sc(self) -> np.ndarray:
    #     with mss.mss() as sct:  
    #         screenshot = sct.grab(config.monitor)
    #     frame =  np.asarray(screenshot, dtype=np.float32)[..., :3]
    #     image_resized = cv2.resize(frame, (640, 640))  # Redimensionar (ajustar para o tamanho esperado pelo modelo)
    #     image_resized = image_resized.transpose(2, 0, 1)  # Converter HWC -> CHW
    #     image_resized = image_resized / 255.0  # Normalizar a imagem para a faixa [0, 1]
    #     return  np.expand_dims(image_resized, axis=0).astype(np.float32)  # Adicionar o batch size

    def get_screen(self):
        return self.__get_sc()
   
    @property
    def is_leftmouse_down(self) -> bool:
        return bool(win32api.GetKeyState(Mouse.LEFTC) < 0)
    
    def custom_fov(self) -> None:
        if self.is_leftmouse_down: pass
    
    def get_new_frame(self) -> None:
        while True:
            try:
                if not config.stopped:
                    if True:
                        config.frame = self.__get_sc()
                time.sleep(0.0001)
            except Exception as e:
                continue
        
    def run(self) -> None:
        self.get_new_frame()

frame = Frame()
# frame.start()