# ==== IMPORTS ==== #
from utils import config, lock, is_runing
from time import sleep
import math
import ctypes
 

PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
    

# CHANGE THIS OR CHANGE IN CONFIG.JSON (U NEED TO INCLUDE IN CONFIG.JSON AND IN UTILS.PY)
benzier_distance_to_scale  = 120 
pixel_increment = 1000 
aim_smooth = 130
benzier_sensi = 0.009
sensibilidade_BACKUP = benzier_sensi

class Moviment():
    
    @staticmethod
    def __moviment(move_x, move_y) -> None: 
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.mi = MouseInput(round(move_x), round(move_y), 0, 0x0001, 0, ctypes.pointer(extra))
        input_struct = Input(ctypes.c_ulong(0), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.byref(input_struct), ctypes.sizeof(input_struct))
    
    def bezier_interpolation(self,start, end, t):
        return (1 - t) * start + t * end
    def _nice_for_sniper_scope_(self) -> None:
        global is_runing
        if not is_runing.is_set():
            is_runing.set()
            try:
                with lock:
                    max_factor_near = 0.35
                    try:
                        best_lock = min(config.distance, key=lambda item: item["distance"])
                        delta_x = (best_lock['x'] - config.crosshair_x) 
                        delta_y = (best_lock['y'] - config.crosshair_y) 
                        if abs(delta_y) <= 0.2 or abs(delta_y) <= 0.2 :
                            sensibilidade = sensibilidade / 5
                        smoothing = round(0.5 + (aim_smooth - 10) / 10.0, 1)
                            
                        move_x = (delta_x / best_lock['distance']) * pixel_increment * smoothing
                        move_y = (delta_y / best_lock['distance']) * pixel_increment * smoothing

                        
                        move_x *= benzier_sensi
                        move_y *= benzier_sensi
            
                        t = min(1, (best_lock['distance'] / benzier_distance_to_scale))
                        move_x = self.bezier_interpolation(0, move_x, t)
                        move_y = self.bezier_interpolation(0, move_y, t)
                        factor = 1 + (max_factor_near - 1) * math.exp(-best_lock["distance"])
    
                        self.__moviment((move_x / factor), (move_y / factor))

                    except Exception as e: 
                            pass
            finally:
                sleep(0.001)
                is_runing.clear()    
            

    def _simple_(self) -> None:
        global is_runing
        if not is_runing.is_set():
            is_runing.set()
            try:
                
                with lock:
                    try:
                        max_factor = 0.35
                        best_lock = min(config.distance, key=lambda item: item["distance"])
                        
                        factor = 1 + (max_factor - 1) * math.exp(-best_lock["distance"])

                            
                        config.moviment = {
                            "x" : int(((best_lock["x"] - config.crosshair_x) / factor) * config.sensi),
                            "y" : int(((best_lock["y"] - config.crosshair_y) / factor) * config.sensi)
                        }
                    
        
                        self.__moviment(config.moviment['x'], config.moviment['y'])
                        config.moviment = {
                                "x" : None,
                                "y" : None
                            }

                    except Exception as e: 
                        pass
            finally:
                is_runing.clear()


        

