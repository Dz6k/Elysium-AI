# ==== IMPORTS ==== #
from utils import Mouse, config
from time import sleep
import threading
import win32api
import win32con
import mouse


class Moviment(threading.Thread):
    def __init__(self) -> None:
        super().__init__()
    
    @staticmethod         
    def __moviment() -> None: 
        win32api.mouse_event(
            win32con.MOUSEEVENTF_MOVE, 
            int(config.moviment['x']),
            int(config.moviment['y'])
        )

    @staticmethod 
    def __smooth_move(smooth_factor) -> None:
        win32api.mouse_event(
            win32con.MOUSEEVENTF_MOVE,
            int( config.moviment['x'] / smooth_factor), 
            int( config.moviment['y'] / smooth_factor),
        )
    
    @property
    def is_leftmouse_down(self) -> bool:
        return bool(win32api.GetKeyState(Mouse.RIGHTC) < 0)
    
    def __best_target(self, targets) -> None:
        if not targets:
            return
        
        if self.is_leftmouse_down:
            try:
                if config.distance is not None:
                    best_lock = min(targets, key=lambda item: item['distance'])
                    
                    config.moviment = {
                        'x' : int((best_lock['x'] - config.crosshair_x)),
                        'y' : int((best_lock['y'] - config.crosshair_y))
                    }

                    # TODO: update mouse event function
                    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(config.moviment['x']),int(config.moviment['y']))
                    # self.__moviment()
                    
                    # I really need this?
                    # mouse.click()
                    
                    # I'm still analyzing the real need this yet....
                    config.moviment = {
                        'x': None,
                        'y': None
                    }
                    
                    config.distance = [{
                        'distance': None,
                        'x': None,
                        'y': None
                    }]
                    
                    
            except Exception as e: 
                pass

    def run_api(self) -> None:
        while True:
            try:
                if config.stopped:
                    continue
                
                if config.distance[0]['distance'] == None:
                    continue

                if config.moviment['x'] == None:
                    self.__best_target(config.distance)

                sleep(0.0005)            
            except Exception as e: 
                pass

    def run(self) -> None:
        self.run_api()
        
        
mov = Moviment()
# mov.start()