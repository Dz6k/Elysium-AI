# ==== IMPORTS ==== #
from module.utils import config, Mouse, Files, update_config
from module.screencapture import frame
from module.mousemoviment import mov
from module.process import ProcessImg
from module.render import *
from ultralytics import YOLO
from time import sleep
import math
import numpy as np
import win32api
from threading import Thread 
import time
import random
import win32con
import supervision as sv
import time
import mousekey 
import sys
import math


mousekey.MouseKey().enable_failsafekill()


class Mouse:
    RIGHTC = 0x02  # right click
    LEFTC = 0x01  # left click
        

class App:
    def __init__(self, path):
        self.model_path = path
        self.device = None
        self.model = None
        self.lines = []
        self.pi=None
        self.second = False
        self.distance = []
        

    def load_model_path(self) -> str:
        self.device = Files.resource_path(
            relative_path=f"models\\{self.model_path}")
        return self.device

    def set_device_model_and_cuda(self):
        self.model = YOLO(
            model=self.device,
            task="detect",
            verbose=False
        )
        return self.model
    
    @staticmethod
    def stop_key() -> bool:
        key_state = win32api.GetAsyncKeyState(config.stopped_key)
        pressed = bool(key_state & 0x8000)
        if pressed == True:
            config.stopped = not config.stopped
            sleep(0.3)
            
    @staticmethod
    def verify_config_update() -> bool:
        key_state = win32api.GetAsyncKeyState(win32con.VK_HOME)
        pressed = bool(key_state & 0x8000)
        if pressed == True:
            update_config()
            sleep(0.3)
    
    @property
    def is_rightmouse_down(self) -> bool:
        return bool(win32api.GetKeyState(Mouse.RIGHTC) < 0)
    
    @property
    def is_leftmouse_down(self) -> bool:
        return bool(win32api.GetKeyState(Mouse.LEFTC) < 0)
    
        
    @staticmethod
    def convert_to_screen_coordinates(coords):
        mouse_x, mouse_y = config.crosshair_x, config.crosshair_y
 
        escala = config.fov_value / (640 / 2)
 
        x_center = coords[0] - (640 / 2)* escala
        y_center = coords[1] - (640 / 2)* escala
 
        screen_x = int(mouse_x + x_center )
        screen_y = int(mouse_y + y_center )
        
        return screen_x, screen_y

    @staticmethod
    def clamp_to_fov(x, y, fov_radius):
        mouse_x, mouse_y = config.crosshair_x, config.crosshair_y
        
        distance = math.sqrt((x - mouse_x)**2 + (y - mouse_y)**2)
        
        if distance > fov_radius:
            factor = fov_radius / distance
            x = mouse_x + (x - mouse_x) * factor
            y = mouse_y + (y - mouse_y) * factor
        return x, y
    
    def time_click(self):
        start_time = None
        while True:
            if bool(win32api.GetKeyState(Mouse.RIGHTC) < 0):  # 0x02 é o código do botão direito do mouse
                if start_time is None:
                    start_time = time.time()
                if time.time() - start_time >= 0.01:
                    if config.fov_value > config.fov_min:
                        config.fov_value -= 1
                        
                    """
                    DISABLE COMENT IF UR USING THE FUNCTION OF _BACKUP_M_EVENT_.py
                    
                    if config.benzier_distance_to_scale < 180:
                        config.benzier_distance_to_scale += 1
                    """
                    self.second = True
            else:
                if config.fov_value < config.fov_value_backup:
                    config.fov_value += 1
                    
                """
                DISABLE COMENT IF UR USING THE FUNCTION OF _BACKUP_M_EVENT_.py
                
                if config.benzier_distance_to_scale > 121:
                    config.benzier_distance_to_scale -= 1
                """
                self.second = False
                start_time = None
            sleep(0.001)
            
    def aim_loop(self, results: sv.Detections):
        for r in results:
            bbox, _, _, _, _, info = r

            x1, y1, x2, y2 = bbox

            x1, y1 = self.clamp_to_fov(
                *self.convert_to_screen_coordinates((x1, y1)),
                config.fov_value
            )
            x2, y2 = self.clamp_to_fov(
                *self.convert_to_screen_coordinates((x2, y2)),
                config.fov_value
            )
            
            width = x2 - x1 
            height = y2 - y1
            if width >= height:
                continue
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)
            center_y = math.floor(((y1 - y2) * config.offset_y) + center_y)
            
            Draw.corner_box(
                x1,
                y1,
                width,
                height,
                outline_color=Colors.vermelho,
                color=Colors().vermelho,
                rgb=True
            )

            Draw.line(
                config.crosshair_x, config.screen_height, center_x, y2, 
                line_width=2, color=Colors.vermelho,
                rgb=True
            )

            current_entity_distance = np.linalg.norm(
                np.array([(center_x - config.crosshair_x), (center_y - config.crosshair_y)]), axis=0)
            
            config.distance.append({
                "distance": current_entity_distance,  
                "x": center_x,
                "y": center_y,
            })
                
        if self.is_leftmouse_down or self.is_rightmouse_down:
            Thread(target=lambda:mov.best_target()).start() 
         
    def nr(self):
        while True:
            if self.is_leftmouse_down and not config.stopped: 
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,int(random.randint(-2,2)), 2)
            sleep(0.008) 
        
                    
    def run(self) -> None:
        contador = 0
        fps = 0
        start_time = time.time() 
        MAX_FPS=80
        MIN_FRAME_TIME=1/MAX_FPS 
        Thread(target=self.time_click).start()
        Thread(target=self.nr).start()
        with Render() as render:
            while render.loop:
                try:
                    start = time.time()
                    self.stop_key()
                    self.verify_config_update()
                    config.distance = []
            
                    Draw.circle(
                        config.crosshair_x,
                        config.crosshair_y,
                        radius=config.fov_value,
                        color=Colors.fade_rgb3(),
                        filled=False,
                        rgb=True
                    )
        
                    if not config.stopped:
                        results = self.pi.process(self.model, config.frame)
                        self.aim_loop(results)
                        contador += 1
    
                    elapsed_time = time.time() - start_time
    
                    if elapsed_time >= 1.0:
                        fps = contador   
                        contador = 0  
                        start_time = time.time()  

                    Draw.text(

                        200,
                        Colors().fade_rgb3(),
                        f'FPS: {fps}'
                    )
                    render.update()   
                    
                    sleep(max(0, MIN_FRAME_TIME - (time.time() - start)))

                except KeyboardInterrupt:
                    sys.exit()
                except Exception as e:
                    print(repr(e))
                
                
    def start_and_run(self):
        self.load_model_path()
        self.set_device_model_and_cuda()
        frame.start()
        self.pi = ProcessImg()
        self.run()
        
if __name__ == "__main__":
    app = App("w3.onnx")
    app.start_and_run()
 