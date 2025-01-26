# ==== IMPORTS ==== #
from utils import config, cuda_config, Mouse, Files
from screencapture import frame
from mousemoviment import mov
from ultralytics import YOLO
from time import sleep
from render import *
from fov import Fov
import numpy as np
import win32api
import torch
import mss




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

    @property
    def is_rightmouse_down(self) -> bool:
        return bool(win32api.GetKeyState(Mouse.RIGHTC) < 0)
    
    @property
    def is_leftmouse_down(self) -> bool:
        return bool(win32api.GetKeyState(Mouse.LEFTC) < 0)
        
    def aim_loop(self):
        if config.frame is not None:
            results = self.model(
                source=config.frame,
                conf=config.confidence,
                imgsz=640,
                iou=0.57,
                classes=[0],
                stream=False,
                max_det=1,
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
            
            for r in results:
                for box in r.boxes:
                    if int(box.cls[0]) == 0:
                        x1, y1, x2, y2 = box.xyxy[0].tolist()
                        x1, y1, x2, y2 = self.adjust_coordinates(x1, y1, x2, y2, size=config.monitor)
                        conf = float(box.conf[0]) * 100
                        
                        center_x = int((x1 + x2) / 2)
                        center_y = int((y1 + y2) / 2)

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
                       
                        # if current_entity_distance <= 100.0:
                        config.distance = [{
                                'distance': current_entity_distance,
                                'x': center_x,
                                'y': center_y  
                            }] 
                           
    def nr(self):
        while True:
            if self.is_leftmouse_down and not config.stopped:
                win32api.mouse_event(0x0001, 0, 1) 
            sleep(0.008)      
        
    def run(self) -> None:
        # Thread(target=self.nr).start()
        with Render() as over:
            while over.loop:
                try:
                    self.stop_key()
                    
                    Draw.draw_rectangle(
                        config.monitor['left'],
                        config.monitor['top'],
                        config.monitor['left'] + config.monitor['width'],
                        config.monitor['top'] + config.monitor['height'],
                        color=Colors.branco
                    )
                    
                    # Draw.circle(config.screen_width // 2, config.screen_height // 2,radius=100,color= Colors.branco, filled=False,segments=360, line_width=0.6)
                    if not config.stopped:
                        self.aim_loop()
                        # self.fov.update(True)
                        
                    over.update()   
                    sleep(0.008)
                except KeyboardInterrupt:
                    sys.exit()
                    
                except Exception as e:
                    continue
                    # print(repr(e))
    
    def start_and_run(self):
        self.load_model_path()
        self.set_device_model_and_cuda()
        frame.start()
        mov.start()
        self.run()
        
        
        
        
if __name__ == '__main__':
    # app = App('new.engine')
    # app = App('ofodao.pt')
    app = App('w3.onnx')
    app.start_and_run()