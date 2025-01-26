# ==== IMPORTS ==== #
from utils import config, cuda_config, Mouse, Files, Config
from screencapture import frame
from mousemoviment import mov
from ultralytics import YOLO
from time import sleep
from render import *
from fov import Fov
import numpy as np
import win32api
import mss
from threading import Thread
import time
import random
import torch
from logic import mouse
from process import ProcessImg

class Target:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = (y - 0.33 * h)
        self.w = w
        self.h = h   
        

class App:
    def __init__(self, path):
        self.model_path = path
        self.device = None
        self.model = None
        self.is_onnx = False
        self.fov = Fov()
        self.draw_scren = True
        self.frame = None
        self.sct = mss.mss()
        self.best_lock = None
        self.distance = []
        self.config_monitor_default = config.monitor

    def load_model_path(self) -> str:
        # self.device = f"models\\{self.model_path}"
        self.device = Files.resource_path(
            relative_path=f"models\\{self.model_path}")
        
        if self.device.endswith(".pt"):
            self.is_onnx = False
        elif self.device.endswith(".onnx"):
            self.is_onnx = True
        else:
            self.is_onnx = False
        return self.device

    @property
    def is_cuda_enable(self) -> bool:
        return cuda_config.backend
        
    def set_device_model_and_cuda(self):
        self.model = YOLO(
            model=self.device,
            task="detect"
        )
        return self.model

    @staticmethod
    def adjust_coordinates(x1: float, y1: float, x2: float, y2: float, size: dict) -> tuple[int, int, int, int]:
        x1_adjusted = int(x1 + size["left"])
        y1_adjusted = int(y1 + size["top"])
        x2_adjusted = int(x2 + size["left"])
        y2_adjusted = int(y2 + size["top"])
        return x1_adjusted, y1_adjusted, x2_adjusted, y2_adjusted
    

    
    
    @staticmethod
    def stop_key() -> bool:
        key_state = win32api.GetAsyncKeyState(config.stopped_key)
        pressed = bool(key_state & 0x8000)
        if pressed == True:
            config.stopped = not config.stopped
            sleep(0.3)

    @property
    def is_rightmouse_down(self) -> bool:
        return bool(win32api.GetKeyState(Mouse.RIGHTC) < 0)
    
    @property
    def is_leftmouse_down(self) -> bool:
        return bool(win32api.GetKeyState(Mouse.LEFTC) < 0)
    
    
    def aim_loop(self, results):
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = self.adjust_coordinates(
                    *box.xyxy[0].tolist(),
                    size=config.monitor,
                )
     
                width = x2 - x1
                height = y2 - y1
                if width > height:
                    return
                center_x = int((x1 + x2) / 2)
                center_y = int((y1 + y2) / 2)
                center_y = math.floor(((y1 - y2) * config.offset_y) + center_y)
                    
                if self.draw_scren:
                    Draw.corner_box(
                        x1,
                        y1,
                        width,
                        height,
                        outline_color=Colors.vermelho,
                        color=Colors().vermelho,
                        rgb=True
                    )

                    if box.cls[0].tolist() != 7.0:
                        Draw.line(
                            config.crosshair_x, config.screen_height, center_x, y2, 
                            line_width=2, color=Colors.vermelho,
                            rgb=True
                        )

                if box.cls[0].tolist() != 7.0:
                    current_entity_distance = np.linalg.norm(np.array([(center_x - config.crosshair_x), (center_y - config.crosshair_y)]), axis=0)
                    config.distance.append({
                        "distance": current_entity_distance,  
                        "x": center_x,
                        "y": center_y,
                    })
        
        if self.is_leftmouse_down :
        # if self.is_leftmouse_down or self.is_rightmouse_down:
        #     win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,0, 2)
            mov.best_target(config.distance)

                 
    def nr(self):
        while True:
            if self.is_leftmouse_down and not config.stopped:
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,0, 1)
            sleep(0.004)
             
    def run(self) -> None:
        contador = 0
        fps = 0
        start_time = time.time() 
        # MAX_FPS=60
        # MIN_FRAME_TIME=1/MAX_FPS 
        Thread(target=lambda: self.nr()).start()
        with Render() as over:
            while over.loop:
                try:
                    start = time.time()
                    self.stop_key()
                    config.distance = []
                    Draw.draw_rectangle(
                        *config.fov.values(),
                        color=Colors.branco
                    )
         
                    if not config.stopped:
                        config.frame = frame.get_sc()
                        # if self.is_leftmouse_down :
                        results = ProcessImg().process(self.model, config.frame)
                        self.aim_loop(results)
                        contador += 1
                        # config.frame = None
                    elapsed_time = time.time() - start_time
                    if elapsed_time >= 1.0:
                        fps = contador   
                        contador = 0  # 
                        start_time = time.time()  
                    Draw.text(
                        200,
                        200,
                        Colors.branco,
                        f'FPS: {fps}'
                    )
                    over.update()   
                    
                    
                    # sleep(max(0, MIN_FRAME_TIME - (time.time() - start)))

                except KeyboardInterrupt:
                    sys.exit()
                except Exception as e:
                    # continue
                    print(repr(e))
    
    def start_and_run(self):
        self.load_model_path()
        self.set_device_model_and_cuda()
        # frame.start()
        # mov.start()
        self.run()
        
        
        
        
if __name__ == "__main__":
    app = App("model.engine")
    # app = App("w3.onnx")  
    app.start_and_run()
