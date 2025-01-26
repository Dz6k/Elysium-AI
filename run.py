# # ==== IMPORTS ==== #
# import main
# from utils import *
# from render import *
# from screencapture import frame
# from mousemoviment import mov
# from ultralytics import YOLO
# from time import sleep
# from render import *
# from fov import Fov
# import numpy as np
# import win32api
# from threading import Thread
# import random
# import torch
# from logic import mouse
# from process import ProcessImg
# import socket, struct, time
# import os
# from utils import Mouse, config
# import threading
# import win32api  
# import time
# from fast_ctypes_screenshots import ScreenshotOfRegion
# from math import cos, sin, pi
# from ctypes import wintypes
# import glfw 
# import win32gui # type: ignore
# import win32con # type: ignore
# from win32gui import FindWindow, GetWindowLong, SetWindowLong, ShowWindow, SetWindowPos # type: ignore
# from win32con import WS_EX_LAYERED, WS_EX_TRANSPARENT, GWL_EXSTYLE, SW_HIDE, SW_SHOW # type: ignore
# from OpenGL.GL import *
# from OpenGL.GLUT import *
# import math

# if __name__ == "__main__":
#     app = main.App("model.engine") # nao me descompile >.< vou ficar muito triste e parar de dar previas para voce!
#     app.start_and_run()

import onnxruntime as ort

# Criar uma sessão com opções padrão
session = ort.InferenceSession(
    "models\w3.onnx",
    providers=["CUDAExecutionProvider"]
)

print("Providers disponíveis:", session.get_providers())
print("Provider ativo:", session.get_provider_options())
