# ==== IMPORTS ==== #
from utils import config, cuda_config, Mouse, Files, Config
from screencapture import frame
from mousemoviment import mov
from ultralytics import YOLO
from time import sleep
# from render import *
from fov import Fov
import numpy as np
import win32api
import mss
from threading import Thread
import time
import random
import torch
from logic import mouse
import cv2
import sys, math, win32con

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
        self.device = Files.resource_path(
            relative_path=f'models\\{self.model_path}'
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
    
    # @staticmethod
    # def adjust_coordinates(x: int, y: int, w: int, h: int, size: dict, circle_center: tuple[int, int], radius: int) -> tuple[int, int, int, int]:
    #     """
    #     Ajusta as coordenadas de uma caixa no formato `xywh` para que fiquem dentro de um círculo.
        
    #     Args:
    #         x (int): Coordenada X do canto superior esquerdo da caixa.
    #         y (int): Coordenada Y do canto superior esquerdo da caixa.
    #         w (int): Largura da caixa.
    #         h (int): Altura da caixa.
    #         size (dict): Dados sobre a posição da região monitorada (left, top, etc.).
    #         circle_center (tuple[int, int]): Centro do círculo (cx, cy).
    #         radius (int): Raio do círculo.

    #     Returns:
    #         tuple[int, int, int, int]: Coordenadas ajustadas `x`, `y`, `w`, `h`.
    #     """
    #     cx, cy = circle_center

    #     # Ajusta a posição inicial da caixa com base no monitor
    #     x += size['left']
    #     y += size['top']

    #     # Calcula o centro da caixa
    #     box_cx = x + w // 2
    #     box_cy = y + h // 2

    #     # Calcula a distância do centro da caixa ao centro do círculo
    #     distance = np.sqrt((box_cx - cx)**2 + (box_cy - cy)**2)

    #     # Verifica se o centro da caixa está fora do círculo
    #     if distance + max(w, h) / 2 > radius:
    #         # Ajusta a caixa para ficar dentro do círculo
    #         angle = np.arctan2(box_cy - cy, box_cx - cx)  # Ângulo em relação ao centro do círculo
    #         new_box_cx = cx + np.cos(angle) * (radius - max(w, h) / 2)
    #         new_box_cy = cy + np.sin(angle) * (radius - max(w, h) / 2)

    #         # Ajusta x e y com base no novo centro
    #         x = int(new_box_cx - w // 2)
    #         y = int(new_box_cy - h // 2)

    #     return x, y, w, h
    
    
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
            # classes=[7],
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
            # if r.boxes:
                # target = self.sort_targets(r)
            # frame_with_circle = r.plot()
            # track_ids = r.boxes.id.int().cpu().tolist()
            # print(track_ids)
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
                


                    
                # if self.draw_scren:
                #     Draw.corner_box(
                #         x1,
                #         y1,
                #         w,
                #         h,
                #         outline_color=Colors.vermelho,
                #         color=Colors().vermelho,
                #     )
                #     Draw.text(
                #         x1,
                #         y1,
                #         color=Colors().vermelho,
                #         text=f'{conf:.2f}%'
                #     )
                #     Draw.line(
                #         config.crosshair_x, config.screen_height, center_x, y2, 
                #         line_width=2, color=Colors.vermelho
                #     )
                
                current_entity_distance = np.linalg.norm(np.array([(center_x - config.crosshair_x), (center_y - config.crosshair_y)]), axis=0)
                # print(current_entity_distance)
                # if current_entity_distance <= 80:
                #     dist = current_entity_distance
                # if self.is_rightmouse_down:
                # mouse.process_data((target.x, target.y))
                if current_entity_distance >= 10:
                    config.distance.append({
                        'distance': current_entity_distance,  
                        'x': center_x + random.uniform(1,-4.5),
                        'y': center_y + random.uniform(4.5,-4.5),
                        'distance_y': center_y - config.crosshair_y   
                    })
                else:
                    config.distance.append({
                        'distance': current_entity_distance,  
                        'x': center_x,
                        'y': center_y,
                        'distance_y': center_y - config.crosshair_y   
                    })
        if self.is_leftmouse_down:
            mov.best_target(config.distance)
        # cv2.circle(frame_with_circle, (config.crosshair_x, config.crosshair_y), config.radio, (0, 255, 0), 2)
        # cv2.imshow("FOV Debug", frame_with_circle)
        # cv2.waitKey(1)
        
    def sort_targets(self, frame):
        boxes_array = frame.boxes.xywh.cpu()
        classes_tensor = frame.boxes.cls.cpu()
        
        if not classes_tensor.numel():
            return None
        center = torch.tensor([config.crosshair_x, config.crosshair_y], device='cpu')
        distances_sq = torch.sum((boxes_array[:, :2] - center) ** 2, dim=1)

        # non_head_mask = classes_tensor != 7
        # if non_head_mask.any():
        #     non_head_distances_sq = distances_sq[non_head_mask]
        #     nearest_idx = torch.argmin(non_head_distances_sq)
        #     nearest_idx = torch.nonzero(non_head_mask)[nearest_idx].item()
        # else:
        #     return None
        head_mask = classes_tensor == 7
        if head_mask.any():
            head_distances_sq = distances_sq[head_mask]
            nearest_head_idx = torch.argmin(head_distances_sq)
            nearest_idx = torch.nonzero(head_mask)[nearest_head_idx].item()
        else:
            nearest_idx = torch.argmin(distances_sq)
        target_data = boxes_array[nearest_idx, :4].cpu().numpy()
        
        return Target(*target_data)
                           
    def appy(self, distance_y, smoothing_factor=1.0):
        if distance_y > 0:  
            move_y = -distance_y * smoothing_factor
        else:   
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
                            # valor = random.randint(-2,2)
                            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,0, 1)
            except:pass
            finally:                
                sleep(0.009)
            
        sleep(0.0065)     
        
    def run(self) -> None:
        while True:
                try:
                    self.stop_key()
                    # config.distance = []
                    # Draw.draw_rectangle(
                        # config.monitor['left'],
                    #     config.monitor['top'],
                    #     config.monitor['left'] + config.monitor['width'],
                    #     config.monitor['top'] + config.monitor['height'],
                    #     color=Colors.branco
                    # )
                    # Draw.circle(
                    #     config.crosshair_x,
                    #     config.crosshair_y,
                    #     config.radio,
                    #     Colors.branco,
                    #     filled=False
                        
                    # )
                    if not config.stopped:
                        self.aim_loop()
                        # contador += 1
                    
                    # elapsed_time = time.time() - start_time
                    # if elapsed_time >= 1.0:
                    #     fps = contador   
                    #     contador = 0  # 
                    #     start_time = time.time()   
                        
                    # Draw.text(
                    #     200,
                    #     200,
                    #     Colors.branco,
                    #     f'FPS: {fps}'
                    # )
                    
                    # over.update()   
                    
                    
                    sleep(0.0001)
                except KeyboardInterrupt:
                    sys.exit()
                except Exception as e:
                    # continue
                    print(repr(e))
    
    def start_and_run(self):
        self.load_model_path()
        self.set_device_model_and_cuda()
        frame.start()
        # mov.start()
        self.run()
        
        
        
        
if __name__ == '__main__':
    # app = App('sunxds_0.5.6.engine')
    app = App('model.engine')
    app.start_and_run()
