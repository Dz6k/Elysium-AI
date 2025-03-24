# ==== IMPORTS ==== #
from module.utils import config, Mouse, Files, update_config
from module.screencapture import frame
from module.mousemoviment import mov
from module.process import ProcessImg
from ultralytics import YOLO
from time import sleep
from ctypes import wintypes
import dearpygui.dearpygui as dpg
import math
import numpy as np
import win32api
from threading import Thread 
import time
import ctypes
import random
import win32con, win32gui
import supervision as sv
import time
import mousekey
import sys
import ctypes
import math

mousekey.MouseKey().enable_failsafekill()

class Colors:
    branco = (255, 255, 255, 255)           # White
    preto = (0, 0, 0, 255)                  # Black
    vermelho = (255, 0, 0, 255)             # Red
    verde = (0, 255, 0, 255)                # Green
    verde_kelly = (76, 187, 23, 255)        # Kelly green
    azul = (0, 0, 255, 255)                 # Blue
    amarelo = (255, 255, 0, 255)            # Yellow
    ciano = (0, 255, 255, 255)              # Cyan
    magenta = (255, 0, 255, 255)            # Magenta
    cinza_claro = (211, 211, 211, 255)      # Light Gray
    cinza_escuro = (169, 169, 169, 255)     # Dark Gray
    laranja = (255, 165, 0, 255)            # Orange
    roxo = (128, 0, 128, 255)               # Purple
    rosa = (255, 192, 203, 255)             # Light Rose
    marrom = (165, 42, 42, 255)             # Brown
    dourado = (255, 215, 0, 255)            # Gold

    @staticmethod
    def set_rgb(color: tuple):
        return color[:3] + (255,)

    @staticmethod
    def set_rgb1(color: tuple):
        return color[:3]

    @staticmethod
    def with_alpha(color: tuple, alpha: int):
        return color[:3] + (alpha,)

    @staticmethod
    def fade_rgb():
        t = (ctypes.windll.kernel32.GetTickCount() // 10) % 360
        rad = (t * 3.14159) / 180

        r = int((0.5 + 0.5 * math.cos(rad)) * 255)
        g = int((0.5 + 0.5 * math.cos(rad - 2.09439)) * 255)
        b = int((0.5 + 0.5 * math.cos(rad + 2.09439)) * 255)

        return (r, g, b, 255)

    @staticmethod
    def fade_rgb3f():
        t = (ctypes.windll.kernel32.GetTickCount() // 10) % 360
        rad = (t * 3.14159) / 180

        r = int((0.5 + 0.5 * math.cos(rad)) * 255)
        g = int((0.5 + 0.5 * math.cos(rad - 2.09439)) * 255)
        b = int((0.5 + 0.5 * math.cos(rad + 2.09439)) * 255)

        return (r, g, b)

    @staticmethod
    def fade_rgb_alpha(alpha: int):
        t = (ctypes.windll.kernel32.GetTickCount() // 10) % 360
        rad = (t * 3.14159) / 180

        r = int((0.5 + 0.5 * math.cos(rad)) * 255)
        g = int((0.5 + 0.5 * math.cos(rad - 2.09439)) * 255)
        b = int((0.5 + 0.5 * math.cos(rad + 2.09439)) * 255)

        return (r, g, b, alpha)

class MARGINS(ctypes.Structure):
    _fields_ = [("cxLeftWidth", ctypes.c_int),
                ("cxRightWidth", ctypes.c_int),
                ("cyTopHeight", ctypes.c_int),
                ("cyBottomHeight", ctypes.c_int)
                ]


class App:
    def __init__(self, path):
        self.model_path = path
        self.device = None
        self.model = None
        self.lines = []
        self.pi=None
        self.second = False
        self.nice_names = ["HUB", "Window", "Dz6k"]
        self.config_monitor_default = config.monitor
        self.window_name = random.choice(self.nice_names)
        dpg.create_context()
        dpg.create_viewport(vsync=True, title=self.window_name, resizable=False, always_on_top=True, decorated=False,
                            clear_color=[0.0, 0.0, 0.0, 0.0], width=config.screen_width, height=config.screen_height)
        dpg.setup_dearpygui()
        dpg.toggle_viewport_fullscreen()

        dpg.add_viewport_drawlist(front=True, tag="Viewport_back")
        dpg.show_viewport()
        self.setup()
        self.hide_window()
        self.stream_mode_on()
        self.dwm = ctypes.windll.dwmapi
        hwnd = win32gui.FindWindow(None, self.window_name)
        margins = MARGINS(-1, -1, -1, -1)
        self.dwm.DwmExtendFrameIntoClientArea(hwnd, margins)
        
    def setup(self):
        win32gui.SetWindowLong(win32gui.FindWindow(None, self.window_name),
                               win32con.GWL_EXSTYLE,
                               win32gui.GetWindowLong(win32gui.FindWindow(None, self.window_name),
                                                      win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
                               )

    def stream_mode_on(self):
        WDA_EXCLUDEFROMCAPTURE = 0x00000011  

        user32 = ctypes.WinDLL('user32', use_last_error=True)
        SetWindowDisplayAffinity = user32.SetWindowDisplayAffinity
        SetWindowDisplayAffinity.argtypes = (wintypes.HWND, wintypes.DWORD)
        SetWindowDisplayAffinity.restype = wintypes.BOOL

        result = SetWindowDisplayAffinity(win32gui.FindWindow(None, self.window_name), WDA_EXCLUDEFROMCAPTURE)
        if not result:
            raise ctypes.WinError(ctypes.get_last_error())
        
    def hide_window(self):
        hwnd = win32gui.FindWindow(None, self.window_name)

        if hwnd:
            style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                                   style | win32con.WS_EX_TOOLWINDOW & ~win32con.WS_EX_APPWINDOW)

            win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
            
    def load_model_path(self) -> str:
        self.device = Files.resource_path(
            relative_path=f"models\\{self.model_path}")
        return self.device

    def set_device_model_and_cuda(self):
        self.model = YOLO(
            model=self.device,
            task="detect"
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
    
    def draw_line(self, start_pos, end_pos, color23):
        idsdesenhos = dpg.draw_line(start_pos, end_pos, color=color23, thickness=0.5, parent="Viewport_back")
        self.lines.append(idsdesenhos)
        
    @staticmethod
    def convert_to_screen_coordinates(coords):
        mouse_x, mouse_y = config.crosshair_x, config.crosshair_y
 
        scale = config.fov_value / (640 / 2)
 
        x_center = coords[0] - (640 / 2)* scale
        y_center = coords[1] - (640 / 2)* scale
 
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
            if  bool(win32api.GetKeyState(Mouse.RIGHTC) < 0): 
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
                
                if config.benzier_distance_to_scale < 180:
                    config.benzier_distance_to_scale += 1
                """
                self.second = False
                start_time = None
            sleep(0.001)
            
    def aim_loop(self, results: sv.Detections):
        for r in results:
            bbox, _, _, _, _, _ = r

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
            
            self.draw_rect_line(
                x1,
                y1,
                width,
                height,
                Colors().fade_rgb()
            )

            self.draw_line(
                (config.crosshair_x, config.screen_height),
                (center_x, y2, ),
                Colors().fade_rgb()
            )

            current_entity_distance = np.linalg.norm(np.array([(center_x - config.crosshair_x), (center_y - config.crosshair_y)]), axis=0)
            
            config.distance.append({
                "distance": current_entity_distance,  
                "x": center_x,
                "y": center_y,
            })
                
        if self.is_leftmouse_down or self.is_rightmouse_down:
            Thread(target=lambda:mov.best_target()).start() 

    def draw_rect_line(self, x, y, width, height, color=(255, 255, 255, 255), thickness=1, fill=(255, 255, 255, 0),
                       rounding=0):
        p1 = (x, y)
        p2 = (x + width, y + height)
        retangulos_id = dpg.draw_rectangle(p1, p2, color=color, thickness=thickness, fill=fill, rounding=rounding,
                                           parent="Viewport_back")
        self.lines.append(retangulos_id)
        #
    
    def draw_text(self, pos, text, color=(255, 255, 255, 255), size=15):
        text_id = dpg.draw_text(pos, text, color=color, size=size, parent="Viewport_back")
        self.lines.append(text_id)
        #
         
    def nr(self):
        while True:
            if self.is_leftmouse_down and not config.stopped: 
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,int(random.randint(-2,2)), 2)
            sleep(0.008) 
        
    def delete_all_objects(self):
        for idsdesenhos in self.lines:
            dpg.delete_item(idsdesenhos)
        self.lines.clear()
                    
    def run(self) -> None:
        counter = 0
        fps = 0
        start_time = time.time() 
        MAX_FPS=80
        MIN_FRAME_TIME=1/MAX_FPS 
        Thread(target=self.time_click).start()
        Thread(target=self.nr).start()
        circle_id = None
        while dpg.is_dearpygui_running():
            try:
                start = time.time()
                self.stop_key()
                self.verify_config_update()
                config.distance = []
                dpg.render_dearpygui_frame()
                self.delete_all_objects()   
                try:
                    if circle_id is None:
                        circle_id = dpg.draw_circle(
                            center=(config.crosshair_x, config.crosshair_y),
                            radius=config.fov_value,
                            color=Colors().fade_rgb(),
                            thickness=0.5,
                            parent="Viewport_back"
                        )
                    else:
                        dpg.configure_item(circle_id, radius=config.fov_value, color=Colors().fade_rgb())
                
                except Exception as e:
                    continue
                
                if not config.stopped:
                    results = self.pi.process(self.model, config.frame)
                    self.aim_loop(results)
                    counter += 1
                    
                elapsed_time = time.time() - start_time
                if elapsed_time >= 1.0:
                    fps = counter   
                    counter = 0  
                    start_time = time.time()  

                
                self.draw_text(
                    (200,
                    200),
                    f'FPS: {fps}',
                    Colors().fade_rgb(),
                )
                
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
 