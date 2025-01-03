# ==== IMPORTS ==== #
from render import *
import torch
import mss
import win32api, win32con, win32process
from ultralytics import YOLO
from utils import config, cuda_config, Mouse, Files
import numpy as np
from time import sleep
from threading import Thread
from fov import Fov


class App:
    def __init__(self, path):
        self.model_path = path
        self.device = None
        self.model = None
        self.is_onnx = False
        self.fov = Fov()
        self.frame = None
        self.sct = mss.mss()
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
            self.is_onnx = True
        return self.device

    @property
    def is_cuda_enable(self) -> bool:
        return cuda_config.backend
        
    def set_device_model_and_cuda(self) -> None:
        if not self.is_onnx:
            if self.is_cuda_enable:
                try:
                    self.model.to(torch.device(cuda_config.backend))
                except AttributeError:
                    pass
            elif not self.is_cuda_enable:
                self.model.to('cpu')
        
        self.model = YOLO(
            model=self.device,
            task='detect',
            verbose=False
        )

        return

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
    
    def capture_screen(self) -> np.ndarray:
        screenshot = self.sct.grab(config.monitor)
        return np.array(screenshot)[:, :, :3]# Remove alpha
    
    @property
    def is_rightmouse_down(self) -> bool:
        return bool(win32api.GetKeyState(Mouse.RIGHTC) < 0)
    
    @property
    def is_leftmouse_down(self) -> bool:
        return bool(win32api.GetKeyState(Mouse.LEFTC) < 0)
        

    def aim_loop(self):
        self.frame = self.capture_screen()
        results = self.model(
            source=self.frame,
            conf=config.confidence,
            imgsz=640,
            iou=0.57,
            classes=[0],
            stream=True,
            max_det=2,
            agnostic_nms=False,
            augment=False,
            vid_stride=False,
            visualize=False,
            verbose=False,
            show_boxes=False,
            show_labels=False,
            show_conf=False,
            save=False,
            show=False
        )
        if not results:
            return
        for r in results:
            for box in r.boxes:
                if int(box.cls[0]) == 0:
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    x1, y1, x2, y2 = self.adjust_coordinates(x1, y1, x2, y2, size=config.monitor)

                    center_x = int((x1 + x2) / 2)
                    center_y = int((y1 + y2) / 2)
                    box_height = y2 - y1  
        
                    target_y = int(center_y - 0.27 * box_height)  
                    
                    Draw.draw_rectangle(
                        x1,
                        y1,
                        x2,
                        y2,
                        color=Colors().vermelho,
                    )
                    Draw.line(
                        config.crosshair_x, config.screen_height, center_x, y2, 
                        line_width=2, color=Colors.vermelho
                    )
                    
                    current_entity_distance = np.linalg.norm(np.array([(center_x - config.crosshair_x), (center_y - config.crosshair_y)]), axis=0)
                    if current_entity_distance <= 100.0:
                        self.distance.append(
                            {
                                'distance': current_entity_distance,
                                'x': center_x,
                                'y': target_y  
                            }
                        )

        self.best_target(self.distance)
                    
    def __smooth_move(self, target_x, target_y, smoothing_factor):
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(target_x/smoothing_factor), int(target_y/smoothing_factor), 0, 0)      
              
    def best_target(self, targets: list):
        if self.is_leftmouse_down:
            if not targets:
                return
            
            best_lock = min(targets, key=lambda item: item['distance'])
            distance = best_lock['distance']
            
            if distance <= 60:
                compensation_factor = 1.1
                dx = int((best_lock['x'] - config.crosshair_x) * compensation_factor)
                dy = int((best_lock['y'] - config.crosshair_y) * compensation_factor)
                self.__smooth_move(dx, dy, 1)
                return
            else:
                compensation_factor = max(1, 1.4 - ((distance - 60) / 30) * 0.4)

            dx = int((best_lock['x'] - config.crosshair_x) * compensation_factor)
            dy = int((best_lock['y'] - config.crosshair_y) * compensation_factor)
            # self.__smooth_move(dx, dy, 3)
            win32api.mouse_event(0x0001, dx, dy)
                
    def nr(self):
        while True:
            if self.is_leftmouse_down and not config.stopped:
                win32api.mouse_event(0x0001, 0, 1) 
            sleep(0.008)      
        
    def run(self) -> None:
        Thread(target=self.nr).start()
        with Render() as over:
            while over.loop:
                try:
                    self.distance = []
                    self.stop_key()
                    
                    Draw.draw_rectangle(
                        config.monitor['left'],
                        config.monitor['top'],
                        config.monitor['left'] + config.monitor['width'],
                        config.monitor['top'] + config.monitor['height'],
                        color=Colors.branco
                    )
                    
                    if not config.stopped:
                        self.aim_loop()
                        # cv2.imshow('imagem', self.frame)
                        self.fov.update()
                    over.update()  
                except KeyboardInterrupt:
                    sys.exit()
                except Exception as e:
                    # continue
                    print(repr(e))
    
    def start_and_run(self):
        self.load_model_path()
        self.set_device_model_and_cuda()
        return self.run()
        
        
        
        
if __name__ == '__main__':
    # app = App('new.engine')
    app = App('ofodao.pt')
    # app = App('w3.onnx')
    app.start_and_run()
