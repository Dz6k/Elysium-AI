from ultralytics import YOLO
import threading
import numpy as np
import math
import win32api, win32con
from utils import (
    Files,
    cuda_config,
    Config,
    config
)

    


class MouseEvent:
    def __init__(self):
        # self.dpi = config.dpi
        self.mouse_sensitivity = config.sensibilidade
        self.fov_x = 100
        self.fov_y = 40
        self.disable_prediction = False
        self.prediction_interval = 1.0
        self.screen_width = config.monitor['width']
        self.screen_height = config.monitor['height']
        self.center_x = config.monitor['width'] // 2
        self.center_y = config.monitor['height'] // 2

        self.prev_x = 0
        self.prev_y = 0
        self.prev_time = None
        self.max_distance = math.sqrt(self.screen_width**2 + self.screen_height**2) / 2
        self.min_speed_multiplier = 4.0
        self.max_speed_multiplier = 1.0

        
    def process_data(self, data):
        target_x, target_y = data
        target_x, target_y = self.calc_movement(target_x, target_y)

        self.move_mouse(target_x, target_y)
    
    def calculate_speed_multiplier(self, distance):
        normalized_distance = min(distance / self.max_distance, 1)
        speed_multiplier = self.min_speed_multiplier + (self.max_speed_multiplier - self.min_speed_multiplier) * (1 - normalized_distance)
        
        return speed_multiplier
    
    def calc_movement(self, target_x, target_y):
        offset_x = target_x - self.center_x
        offset_y = target_y - self.center_y

        distance = math.sqrt(offset_x**2 + offset_y**2)
        if distance == 0:  
            return 0, 0

        speed_multiplier = self.calculate_speed_multiplier(distance)
        degrees_per_pixel_x = self.fov_x / self.screen_width
        degrees_per_pixel_y = self.fov_y / self.screen_height

        move_x = offset_x * degrees_per_pixel_x * speed_multiplier
        move_y = offset_y * degrees_per_pixel_y * speed_multiplier

        return move_x, move_y
    
    def move_mouse(self, x, y):
        if x is None:
            x = 0
        if y is None:
            y = 0
        
        if x != 0 and y != 0:
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(x), int(y), 0, 0)

                    
mouse = MouseEvent()