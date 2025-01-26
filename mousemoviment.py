# ==== IMPORTS ==== #
from utils import Mouse, config
from time import sleep
import threading
import win32api
import win32con
import math

class Moviment(threading.Thread):
    def __init__(self) -> None:
        super().__init__()
    
    @staticmethod         
    def __moviment() -> None: 
        win32api.mouse_event(
            win32con.MOUSEEVENTF_MOVE, 
            int(config.moviment["x"]),
            int(config.moviment["y"])
        )

    @staticmethod 
    def __smooth_move(self, smooth_factor) -> None:
        win32api.mouse_event(
            win32con.MOUSEEVENTF_MOVE,
            int( config.moviment["x"] / smooth_factor), 
            int( config.moviment["y"] / smooth_factor),
        )
    
    @property
    def is_leftmouse_down(self) -> bool:
        return bool(win32api.GetKeyState(Mouse.LEFTC) < 0)
    
    def best_target(self, targets) -> None:
        if not targets:
            return

        max_factor = 2.0

        if config.moviment["x"] is None:
            try:
                if config.distance is not None:
                    best_lock = min(targets, key=lambda item: item["distance"])
                    
                    factor = 1 + (max_factor - 1) * math.exp(-best_lock["distance"] / 10)

                        
                    config.moviment = {
                        "x" : int(((best_lock["x"] - config.crosshair_x) / factor) * config.sensibilidade),
                        "y" : int(((best_lock["y"] - config.crosshair_y) / factor) * 1.5)
                    }
                   
                    # TODO: update mouse event function
                    self.__moviment()
                    # win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,0, 2)
                    config.moviment = {
                            "x" : None,
                            "y" : None
                        }

            except Exception as e: 
                pass

    def run_api(self) -> None:
        while True:
            try:
                if config.stopped:
                    continue
                
                # if config.distance[0]["distance"] == None:
                #     continue

                # if config.moviment["x"] == None:
                    # self.best_target(config.distance)

                sleep(0.0005)            
            except Exception as e: 
                pass

    def run(self) -> None:
        self.run_api()
        
        
mov = Moviment()
# mov.start()