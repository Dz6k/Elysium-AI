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


class Target:
    def __init__(self, x, y, w, h, cls):
        self.x = x
        self.y = y if cls == 7 else (y - 0.33 * h)
        self.w = w
        self.h = h
        self.cls = cls
        
        
        

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
        self.device = Files.resource_path(
            relative_path=f'models\{self.model_path}'
        )
        
        if self.device.endswith('.pt'):
            self.is_onnx = False
        elif self.device.endswith('.onnx'):
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
            task='detect'
        )
        return self.model

    @staticmethod
    def adjust_coordinates(x1: int, y1: int, x2: int, y2: int, size: dict) -> tuple[int, int, int, int]:
        x1_adjusted = int(x1 + size['left'])
        y1_adjusted = int(y1 + size['top'])
        x2_adjusted = int(x2 + size['left'])
        y2_adjusted = int(y2 + size['top'])
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
        
    def aim_loop(self):
        results = self.model(
            source=config.frame,
            conf=config.confidence,
            imgsz=640,
            iou=0.7,
            nms = False,
            classes=[0],
            stream=True,
            max_det=2,
            agnostic_nms=False,
            augment=False   ,
            vid_stride=False,
            visualize=False,
            verbose=False,
            show_boxes=False,
            show_labels=False, 
            show_conf=False,
            save=False,  
            show=False
        )
        
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = self.adjust_coordinates(*box.xyxy[0].cpu().tolist(), size=config.monitor)
                conf = float(box.conf[0]) * 100
                
                center_x = int((x1 + x2) / 2)
                center_y = int((y1 + y2) / 2)
                center_y = math.floor(((y1 - y2) / 3.5) + center_y)

                if self.draw_scren:
                    Draw.draw_rectangle(
                        x1,
                        y1,
                        x2,
                        y2,
                        color=Colors().vermelho,
                    )
                    Draw.text(
                        x1,
                        y1,
                        color=Colors().vermelho,
                        text=f'{conf:.2f}%'
                    )
                    Draw.line(
                        config.crosshair_x, config.screen_height, center_x, y2, 
                        line_width=2, color=Colors.vermelho
                    )
                
                current_entity_distance = np.linalg.norm(np.array([(center_x - config.crosshair_x), (center_y - config.crosshair_y)]), axis=0)
                
                config.distance.append({
                    'distance': current_entity_distance,  
                    'x': center_x,
                    'y': center_y,
                    'distance_y': center_y - config.crosshair_y   
                })
        if self.is_leftmouse_down:
            mov.best_target(config.distance)
                           
    def appy(self, distance_y, smoothing_factor=1.0):
        if distance_y > 0:  # Alvo está abaixo do centro
            move_y = -distance_y * smoothing_factor
        else:  # Alvo está acima do centro
            move_y = -distance_y * smoothing_factor
        return move_y      
    
    def get_distance_y(self):
        if config.distance:
            try:
                self.best_lock = min(config.distance, key=lambda item: item['distance'])
                return self.best_lock['y'] - config.crosshair_y
            except: 
                return 0
        return 0   
                 
    def nr(self):
        while True:
            try:
                if self.is_leftmouse_down and not config.stopped:
                    
                    # if config.distance:  # Verifica se há alvos detectados
                    #     # self.best_lock = min(config.distance, key=lambda item: item['distance'])
                        
                    #     # Verifica se a distância absoluta é menor que 20.0
                    #     if self.best_lock['distance_y'] <= 5.0:
                    #         # Obtém a distância do eixo Y
                    #         distance_y = self.best_lock['distance_y']
                            
                    #         move_y = self.appy(distance_y, smoothing_factor=0.2)
                            
                    #         # Move o mouse
                            valor = random.randint(-3,3)
                            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,valor, 1)
            except:pass
            finally:                
                sleep(0.005)
            
        sleep(0.0065)     
        
    def run(self) -> None:
        contador = 0
        fps = 0
        start_time = time.time()   
        # Thread(target=lambda: self.nr()).start()
        with Render() as over:
            while over.loop:
                try:
                    self.stop_key()
                    config.distance = []
                    Draw.draw_rectangle(
                        config.monitor['left'],
                        config.monitor['top'],
                        config.monitor['left'] + config.monitor['width'],
                        config.monitor['top'] + config.monitor['height'],
                        color=Colors.branco
                    )
                    
                    if not config.stopped:
                        self.aim_loop()
                        contador += 1
                    
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
                    
                    
                    sleep(0.0001)
                except KeyboardInterrupt:
                    sys.exit()
                except Exception as e:
                    print(repr(e))
    
    def start_and_run(self):
        self.load_model_path()
        self.set_device_model_and_cuda()
        frame.start()
        # mov.start()
        self.run()
        
        
        
        
if __name__ == '__main__':
    app = App('model.engine')
    app.start_and_run()
