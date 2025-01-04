# ==== IMPORTS ==== #
from utils import *
from render import *


class Fov:
    '''
    Set dinamic fov metrics 
    '''
    @staticmethod
    def __is_rightmouse_down() -> bool:
        return bool(win32api.GetKeyState(Mouse.LEFTC) < 0)
    
    def update(self, relative_confidence: bool=False) -> None:
        '''
        update the new fov metrics based on time and key state
        
        Parameters:
            relative_confidence (bool): if confidence change with fov

        Returns:
            None
        '''
        if self.__is_rightmouse_down(): 
            if any(config.monitor[key] <= MONITOR_CONFIG_BACKUP[key] * 0.8 for key in ['top', 'left', 'width', 'height']):
                pass
            else:
                config.monitor = {
                    key: value + 8 if key in ['top', 'left'] else value - 16
                    for key, value in config.monitor.items()
                }
                if relative_confidence:
                    config.confidence -= 0.01

        elif not self.__is_rightmouse_down():             
            if config.monitor == MONITOR_CONFIG_BACKUP: pass
            else:
                config.monitor = {
                    key: value - 8 if key in ['top', 'left'] else value + 16
                    for key, value in config.monitor.items()
                }
                if relative_confidence:
                    config.confidence += 0.01
                
                