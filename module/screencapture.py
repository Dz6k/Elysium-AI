# ==== IMPORTS ==== #
from module.utils import Mouse, config
import threading
import time
import mss
import numpy as np
import cv2

class Frame(threading.Thread):
    def __init__(self) -> None:
        super().__init__()
        self.lastframe = None

    def get_sc(self) -> cv2.typing.MatLike:
        with mss.mss() as sct:  
            mouse_x, mouse_y = config.crosshair_x, config.crosshair_y
            monitor = {
                "left": ( mouse_x - config.fov_value),
                "top": ( mouse_y - config.fov_value),
                "width": 2 * config.fov_value,
                "height": 2 * config.fov_value
            }

            screenshot = sct.grab(monitor)
        frame = np.array(screenshot)
        image = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        
        height, width = image.shape[:2]
        mask = np.zeros((height, width), dtype=np.uint8)
        
        cv2.circle(mask, (width // 2, height // 2), config.fov_value, 255, -1)
        self.lastframe = cv2.bitwise_and(image, image, mask=mask)

        return self.lastframe
        
    def get_screen(self) -> cv2.typing.MatLike:
        return self.lastframe
   
    def run_frame(self) -> None:
        while True:
            try:
                if not config.stopped:
                    config.frame = self.get_sc()
                time.sleep(0.0001)
            except Exception as e:
                continue
        
    def run(self) -> None:
        self.run_frame()

frame = Frame()
