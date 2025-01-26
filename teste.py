# ==== IMPORTS ==== #
from utils import config, cuda_config, Mouse, Files, Config
from screencapture import frame
from mousemoviment import mov
# from ultralytics import YOLO
from time import sleep
from render import *
from fov import Fov
import numpy as np
import win32api
import mss
import onnxruntime as ort
import time
from threading import Thread
import cv2
# from classtype import Vec3, Vec2
import torch
import cupy as cp
# from logic import mouse
# from process import ProcessImg

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
        self.mss = mss.mss()
        self.best_lock = None
        self.distance = []
        self.config_monitor_default = config.monitor
        self.input_name = None
        
    def load_model_path(self) -> str:
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
        
    def set_device_model_and_cuda(self, device="GPU"):
        # so = ort.SessionOptions()
        # so.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        # providers = ["CUDAExecutionProvider"] if device == "GPU" else ["CPUExecutionProvider"]
        cuda_options = {
            # "gpu_mem_limit": str(6 * 1024 * 1024 * 1024),  # Limite de 6 GB
            # "arena_extend_strategy": "kNextPowerOfTwo",  # Estratégia de alocação de memória
            # "cudnn_conv_algo_search": "EXHAUSTIVE",  # Busca exaustiva de algoritmos de convolução
            "do_copy_in_default_stream": "1",  # Usar o stream padrão para cópias de memória
            "use_tf32": "1",  # Ativar precisão TensorFloat-32 (TF32)
            "tunable_op_enable": "1",  # Habilitar operações ajustáveis
            "tunable_op_tuning_enable": "1",  # Permitir ajuste de operações ajustáveis
            # "enable_cuda_graph": "1",  # Habilitar gráficos CUDA
            "enable_skip_layer_norm_strict_mode": "1",  # Pular normalização de camadas, quando possível
        }
        self.session = ort.InferenceSession(self.device,providers=["TensorrtExecutionProvider"])
        
        # input(self.session.get_inputs()[0])
        # self.session = ort.InferenceSession(self.device, providers=["TensorrtExecutionProvider"])
        self.input_name = self.session.get_inputs()[0].name
        print("Providers disponíveis:", self.session.get_providers())
        print("Provider ativo:",self.session.get_provider_options())
        # input()
        return self.session

    
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
    
    def predict(self):
        start = time.time()
        outputs = self.session.run(None, {self.input_name: config.frame})
        # print(f"predict time: {time.time() - start:.4f}s")     
        return outputs[0].squeeze(0)
    
    def screenshot(self):
        while not config.stopped:
            # start = time.time()
            # frame = np.asarray(self.mss.grab(config.monitor), dtype=np.float32)[..., :3]
            with mss.mss() as sct:  
                screenshot = sct.grab(config.monitor)
            frame = cv2.resize(np.array(screenshot, dtype=np.uint8)[..., :3], (640, 640))
            # print(f"screenshot time: {time.time() - start:.4f}s")
            config.frame =  (frame.transpose(2, 0, 1) / 255.0)[np.newaxis, ...].astype(np.float32)
            # return config.frame    
    
    def aim_loop(self):
        
        x_centers, y_centers, widths, heights, confidences = self.predict()

        for i, confidence in enumerate(confidences):
            if confidence <= config.confidence:
                continue
            # x_center, y_center, width, height = x_centers[i], y_centers[i], widths[i], heights[i]
            # print(x_center, y_center, width, height)



            # x_center = x_centers[i] * 640
            # y_center = y_centers[i] * 640
            # width = widths[i] * 640
            # height = heights[i] * 640

            # # Escalonando as coordenadas para a região de captura
            # x_center_scaled = x_center * (config.monitor["width"] / 640)
            # y_center_scaled = y_center * (config.monitor["height"] / 640)
            # width_scaled = width * (config.monitor["width"] / 640)
            # height_scaled = height * (config.monitor["height"] / 640)

            # # Ajustando as coordenadas para a tela inteira
            # x_center_absolute = x_center_scaled + config.monitor["left"]
            # y_center_absolute = y_center_scaled + config.monitor["top"]
            # print(x_center_absolute, y_center_absolute)
            # Agora você pode usar x_center_absolute e y_center_absolute para mover o mouse ou desenhar na tela
            # if self.draw_scren:
            # Draw.corner_box(
            #     x_center_absolute,
            #     y_center_absolute,
            #     width_scaled,
            #     height_scaled,
            #     outline_color=Colors.vermelho,
            #     color=Colors().vermelho,
            #     rgb=True
            #     )

                # if box.cls[0].tolist() != 7.0:
                #     Draw.line(
                #         config.crosshair_x, config.screen_height, center_x, y2, 
                #         line_width=2, color=Colors.vermelho,
                #         rgb=True
                #     )

        #         if box.cls[0].tolist() != 7.0:
        #             current_entity_distance = np.linalg.norm(np.array([(center_x - config.crosshair_x), (center_y - config.crosshair_y)]), axis=0)
        #             config.distance.append({
        #                 "distance": current_entity_distance,  
        #                 "x": center_x,
        #                 "y": center_y,
        #             })
        
        # if self.is_leftmouse_down :
        # # if self.is_leftmouse_down or self.is_rightmouse_down:
        #     mov.best_target(config.distance)

                 
    def nr(self):
        while True:
            if self.is_leftmouse_down and not config.stopped:
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,0, 1)
            sleep(0.009)
             
    def run(self) -> None:
        MAX_FPS=60
        MIN_FRAME_TIME=1/MAX_FPS 
        
        Thread(target=lambda: self.screenshot()).start()
        with Render() as over:
            while over.loop:
                try:
                    # start = time.time()
                    self.stop_key()
                    # config.distance = []
                    Draw.draw_rectangle(
                        *config.fov.values(),
                        
                        color=Colors.branco
                    )
         
                    if not config.stopped:
                        self.aim_loop()

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
    # app = App("sunxds_0.5.6.engine")
    app = App("w3.onnx")
    app.start_and_run()


