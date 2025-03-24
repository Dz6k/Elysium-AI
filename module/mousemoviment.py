# ==== IMPORTS ==== #
from utils import Mouse, config, lock, is_runing
from time import sleep
from typing import Tuple
import ctypes
from datetime import datetime
import random
from wise import WiseManager, Wise

k32 = ctypes.windll.kernel32
k32.GetModuleHandleW.argtypes = [ctypes.c_wchar_p]
k32.GetModuleHandleW.restype = ctypes.c_void_p
k32.GetProcAddress.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
k32.GetProcAddress.restype = ctypes.c_void_p
PUL = ctypes.POINTER(ctypes.c_ulong)
                     
class MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]
 
class KEYBDINPUT(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                            ("wScan", ctypes.c_ushort),
                            ("dwFlags", ctypes.c_ulong),
                            ("time", ctypes.c_ulong),
                            ("dwExtraInfo", PUL)]
 
class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]
 
class INPUT_I(ctypes.Union):
                _fields_ = [("ki", KEYBDINPUT),
                            ("mi", MOUSEINPUT),
                            ("hi", HARDWAREINPUT)]
 
class INPUT(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", INPUT_I)]
 

class Moviment:
    def __init__(self):
        LPINPUT = ctypes.POINTER(INPUT)
        NtUserSendInput_POINTER = k32.GetProcAddress(k32.GetModuleHandleW(r"win32u.dll"), b"NtUserSendInput")
        self.NtUserSendInput = ctypes.WINFUNCTYPE(ctypes.c_uint, ctypes.c_uint, LPINPUT, ctypes.c_int)(NtUserSendInput_POINTER)
                            
    def __moviment(self, move_x: int, move_y: int) -> None: 
        extra = ctypes.c_ulong(0)
        ii_ = INPUT_I()
        ii_.mi = MOUSEINPUT(round(move_x), round(move_y), 0,0x0001 , 0, ctypes.pointer(extra))
        cmd = INPUT(ctypes.c_ulong(0), ii_)

        self.NtUserSendInput(1, ctypes.pointer(cmd), ctypes.sizeof(cmd))
    
    def __cubic_bezier(self, start: tuple, end: tuple, control1: tuple, control2: tuple, t: float) -> Tuple[int, int]:
        u = 1 - t
        tt = t * t
        uu = u * u
        uuu = uu * u
        ttt = tt * t

        x = uuu * start[0] + 3 * uu * t * control1[0] + 3 * u * tt * control2[0] + ttt * end[0]
        y = uuu * start[1] + 3 * uu * t * control1[1] + 3 * u * tt * control2[1] + ttt * end[1]

        if config.smooth:
            x = self.__ema_smoothing(0, x, config.smooth_value)                   
            y = self.__ema_smoothing(0, y, config.smooth_value)
                    

        return int(x), int(y)
    
    def __ema_smoothing(self, previous_value: int, current_value: int, smoothing_factor: float) -> int:
        return current_value * smoothing_factor + previous_value * (1 - smoothing_factor)

    def __move_crosshair(self, detected_x: int, detected_y: int) -> None:
        try:
            target_x = detected_x - config.crosshair_x
            target_y = detected_y - config.crosshair_y
            
            offset = random.randint(100,700) 
            control1 = (0 + (target_x - 0) // 3, 1 + (target_y - 1) // 3 + offset)
            control2 = (0 + 2 * (target_x - 0) // 3, 1 + 2 * (target_y - 1) // 3 - offset)
            new_position = self.__cubic_bezier((0, 0), (target_x, target_y), control1, control2, (1 - config.t_factor))

            x, y = (max(-150, min(150, new_position[0])), 
                            max(-150, min(150, new_position[1])))
                    
            self.__moviment(x,y)

        except Exception as e:
            pass
        
    def best_target(self) -> None:
        if config.distance is None:
            return
        global is_runing
        if not is_runing.is_set():
            is_runing.set()
            try:
                with lock:
                    try:
                        best_lock = min(config.distance, key=lambda item: item["distance"])
                        WiseManager.update_detection(
                            Wise.WiseDetect(
                                x = best_lock["x"],
                                y = best_lock["y"],
                            )
                        )
                        
                        wtfpredictedPosition = WiseManager.get_estimated_position()
                        
                        self.__move_crosshair((wtfpredictedPosition.x),(wtfpredictedPosition.y))
                    except Exception as e: 
                            pass
            finally:
                sleep(random.uniform(0.005, 0.001))
                is_runing.clear()    
                
                        
mov = Moviment()
