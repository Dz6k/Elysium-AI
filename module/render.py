from ctypes import wintypes
import glfw 
import ctypes
from win32gui import FindWindow, GetWindowLong, SetWindowLong, ShowWindow, SetWindowPos
from win32con import WS_EX_LAYERED, WS_EX_TRANSPARENT, GWL_EXSTYLE, SW_HIDE, SW_SHOW
from OpenGL.GL import *
from OpenGL.GLUT import *
import math

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
    def rgb3f(color: tuple):
        return color[:3] 
    
    @staticmethod
    def rgb4f(color: tuple, alpha: int):
        return color[:3] + (alpha,)
    
    @staticmethod
    def fade_rgb3():
        t = (ctypes.windll.kernel32.GetTickCount() // 10) % 360
        rad = (t * 3.14159) / 180

        r = int((0.5 + 0.5 * math.cos(rad)) * 255)
        g = int((0.5 + 0.5 * math.cos(rad - 2.09439)) * 255)   
        b = int((0.5 + 0.5 * math.cos(rad + 2.09439)) * 255)   
        
        return (r, g, b)
    
    @staticmethod
    def fade_rgb4f(alpha: int):
        t = (ctypes.windll.kernel32.GetTickCount() // 10) % 360
        rad = (t * 3.14159) / 180

        r = int((0.5 + 0.5 * math.cos(rad)) * 255)
        g = int((0.5 + 0.5 * math.cos(rad - 2.09439)) * 255)   
        b = int((0.5 + 0.5 * math.cos(rad + 2.09439)) * 255)   

        return (r, g, b, alpha)
    
        
class Render:
    def __init__(self):
        glfw.init()
        glutInit()
        self.video_mode, self.window = self.__create_window()
        self.hwnd = None
        self.width = self.video_mode.size.width
        self.height = self.video_mode.size.height

        self.mid = self.video_mode.size.width / 2, self.video_mode.size.height / 2
        self.corner = {
            "lower_left": (0, 0),
            "lower_right": (self.width, 0),
            "upper_left": (0, self.height),
            "upper_right": (self.width, self.height)
        }
                              
    
    def stream_mode_on(self, hwnd):
        WDA_NONE = 0x00000000   
        WDA_MONITOR = 0x00000001   
        WDA_EXCLUDEFROMCAPTURE = 0x00000011
        
        user32 = ctypes.WinDLL('user32', use_last_error=True)
        SetWindowDisplayAffinity = user32.SetWindowDisplayAffinity
        SetWindowDisplayAffinity.argtypes = (wintypes.HWND, wintypes.DWORD)
        SetWindowDisplayAffinity.restype = wintypes.BOOL
        
        result = SetWindowDisplayAffinity(hwnd, WDA_EXCLUDEFROMCAPTURE)
        if not result:
            raise ctypes.WinError(ctypes.get_last_error())
       
    def make_window_transparent(self, hwnd):
        ex_style = GetWindowLong(hwnd, GWL_EXSTYLE)
        SetWindowLong(hwnd, GWL_EXSTYLE, ex_style | WS_EX_LAYERED | WS_EX_TRANSPARENT)
        ShowWindow(hwnd, SW_SHOW)
        
    def __create_window(self):
        # glfw
        glfw.window_hint(glfw.SAMPLES, 16)
        glfw.window_hint(glfw.DECORATED, 0)
        glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, 1)
        glfw.window_hint(glfw.FLOATING, 1)
        
        window = glfw.create_window(1920, 1080, "Overlay", None, None)

        glfw.make_context_current(window)
        hwnd = FindWindow(None, "Overlay") 
        self.make_window_transparent(hwnd)
        # self.stream_mode_on(hwnd)

        glLoadIdentity() 
        glMatrixMode(GL_PROJECTION)
        glOrtho(0, 1920, 1080, 0, -1, 1)  
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_POLYGON_SMOOTH)
        glEnable(GL_MULTISAMPLE)
        
        return glfw.get_video_mode(glfw.get_primary_monitor()), window
        
    @property
    def loop(self):
        return not glfw.window_should_close(self.window)

    def update(self):
        glfw.swap_buffers(self.window)
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT)
        
    @property
    def clear(self):
        glClearColor(0.0, 0.0, 0.0, 0.0)  
        glClear(GL_COLOR_BUFFER_BIT)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        glfw.terminate()

class Draw:

    @staticmethod
    def line(x1, y1, x2, y2, line_width, color=None, rgb=False):
        glLineWidth(line_width)
        glBegin(GL_LINES)
        if rgb:
            rgb_color = Colors.fade_rgb3()
            glColor3f(rgb_color[0]/255, rgb_color[1]/255, rgb_color[2]/255)
        else:
            glColor3f(color[0]/255, color[1]/255, color[2]/255)
        glVertex2f(x1, y1)  
        glVertex2f(x2, y2)
        glEnd()
        
    @staticmethod
    def draw_triangle(x1, y1, x2, y2, x3, y3, color, filled=True, line_width=1, rgb=False):
        glLineWidth(line_width)
        if rgb:
            rgb_color = Colors.fade_rgb3()
            glColor3f(rgb_color[0]/255, rgb_color[1]/255, rgb_color[2]/255)
        else:
            glColor3f(color[0]/255, color[1]/255, color[2]/255) 
        
        if filled:
            glBegin(GL_TRIANGLES)
            glVertex2f(x1, y1)
            glVertex2f(x2, y2)
            glVertex2f(x3, y3)
            glEnd()
        else:
            glBegin(GL_LINE_LOOP)
            glVertex2f(x1, y1)
            glVertex2f(x2, y2)
            glVertex2f(x3, y3)
            glEnd()

    @staticmethod
    def corner_box(x, y, width, height, color, outline_color, line_width=1, rgb=False):
        line_w = width / 5
        line_h = height / 4
        
        def draw_corner():
            glBegin(GL_LINES)
            # Lower Left
            glVertex2f(x, y)
            glVertex2f(x + line_w, y)
            glVertex2f(x, y)
            glVertex2f(x, y + line_h)

            # Lower Right
            glVertex2f(x + width, y)
            glVertex2f(x + width, y + line_h)
            glVertex2f(x + width, y)
            glVertex2f(x + width - line_w, y)

            # Upper Left
            glVertex2f(x, y + height)
            glVertex2f(x, y + height - line_h)
            glVertex2f(x, y + height)
            glVertex2f(x + line_w, y + height)

            # Upper Right
            glVertex2f(x + width, y + height)
            glVertex2f(x + width, y + height - line_h)
            glVertex2f(x + width, y + height)
            glVertex2f(x + width - line_w, y + height)
            glEnd()

        glLineWidth(line_width + 0.5)
        if rgb:
            rgb_color = Colors.fade_rgb3()
            glColor3f(rgb_color[0]/255, rgb_color[1]/255, rgb_color[2]/255)
        else:
            glColor3f(outline_color[0] / 255, outline_color[1] / 255, outline_color[2]/ 255 ) 
        draw_corner()

        glLineWidth(line_width)
        if rgb:
            rgb_color = Colors.fade_rgb3()
            glColor3f(rgb_color[0]/255, rgb_color[1]/255, rgb_color[2]/255)
        else:
            glColor3f(color[0]/ 255 , color[1] / 255, color[2] / 255) 
        draw_corner()
        
    @staticmethod
    def draw_fade_rectangle(x, y, width, height, color_start, color_end, alpha=255, line_width=1, rgb=False):
        def draw_rectangle():
            glBegin(GL_QUADS)
            
            glColor4f(color_start[0]/255, color_start[1] / 255, color_start[2] / 255, alpha / 255)  
            glVertex2f(x, y)  
            glVertex2f(x + width, y) 
            if rgb:
                rgb_color = Colors.fade_rgb3()
                glColor4f(rgb_color[0]/255, rgb_color[1]/255, rgb_color[2]/255, alpha/255)
            else:
                glColor4f(color_end[0]/255, color_end[1] / 255, color_end[2] / 255, alpha / 255) 
            glVertex2f(x + width, y + height)
            glVertex2f(x, y + height)  
            glEnd()

        glLineWidth(line_width) 
        if rgb:
            rgb_color = Colors.fade_rgb3()
            glColor3f(rgb_color[0]/255, rgb_color[1]/255, rgb_color[2]/255)
        else:
            glColor3f(color_start[0] / 255, color_start[1] / 255, color_start[2] / 255) 
        
        draw_rectangle()
    
    @staticmethod
    def draw_rectangle(x1, y1, x2, y2, color, thickness=1.3, rgb=False):
        glLineWidth(thickness)  
        if rgb:
            rgb_color = Colors.fade_rgb3()
            glColor3f(rgb_color[0]/255, rgb_color[1]/255, rgb_color[2]/255)
        else:
            glColor3f(color[0]/255, color[1]/255, color[2]/255)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x1, y1)  
        glVertex2f(x2, y1)  
        glVertex2f(x2, y2)  
        glVertex2f(x1, y2)  
        glEnd()    
        
    @staticmethod
    def dashed_line(x1, y1, x2, y2, line_width, color, factor=1, pattern="11111110000"):
        glPushAttrib(GL_ENABLE_BIT)
        glLineStipple(factor, int(pattern, 2))
        glLineWidth(line_width)
        glEnable(GL_LINE_STIPPLE)

        glBegin(GL_LINES)
        glColor3f(color[0]/255, color[1]/255, color[2]/255)
        glVertex2f(x1, y1)
        glVertex2f(x2, y2)
        glEnd()
        glPopAttrib()

    @staticmethod
    def outline(x, y, width, height, line_width, color, filled=False):
        if filled:
            glBegin(GL_QUADS)
            glColor3f(color[0]/255, color[1]/255, color[2]/255)
            glVertex2f(x, y)
            glVertex2f(x + width, y)
            glVertex2f(x + width, y + height)
            glVertex2f(x, y + height)
            glEnd()
        else:
            glLineWidth(line_width)
            glBegin(GL_LINE_LOOP)
            glColor3f(color[0]/255, color[1]/255, color[2]/255)
            glVertex2f(x, y)
            glVertex2f(x + width, y)
            glVertex2f(x + width, y + height)
            glVertex2f(x, y + height)
            glEnd()
            
    @staticmethod
    def alpha_box(x, y, width, height, color, alpha=0.5):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBegin(GL_POLYGON)
        glColor4f(color[0]/255, color[1]/255, color[2]/255, alpha/255)
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + height)
        glVertex2f(x, y + height)
        glEnd()
        glDisable(GL_BLEND)

    @staticmethod
    def circle(x, y, radius, color,alpha=255, segments=100, filled=True, line_width=1, rgb=False):
        glEnable(GL_LINE_SMOOTH)
        glLineWidth(line_width) 
        if rgb:
            rgb_color = Colors.fade_rgb3()
            glColor4f(rgb_color[0]/255, rgb_color[1]/255, rgb_color[2]/255, alpha/255)
        else:
            glColor4f(color[0]/255,color[1]/255, color[2]/255, alpha/255) 

        if filled:
            glBegin(GL_TRIANGLE_FAN)
            glVertex2f(x, y)
            for i in range(segments + 1):
                angle = 2 * math.pi * i / segments
                glVertex2f(x + math.cos(angle) * radius, y + math.sin(angle) * radius)
            glEnd()
        else:
            glBegin(GL_LINE_LOOP)
            for i in range(segments):
                angle = 2 * math.pi * i / segments
                glVertex2f(x + math.cos(angle) * radius, y + math.sin(angle) * radius)
            glEnd()

        glDisable(GL_LINE_SMOOTH)

    @staticmethod
    def text(x, y, color, text, font=GLUT_BITMAP_9_BY_15): # type: ignore
        glColor3f(color[0]/255, color[1]/255, color[2]/255)
        glRasterPos2f(x, y)
        [glutBitmapCharacter(font, ord(ch)) for ch in text]


if __name__ == "__main__":
    with Render() as overlay:
        rect_width, rect_height = 200, 150
        monitor = glfw.get_primary_monitor()
        mode = glfw.get_video_mode(monitor)
        width, height = mode.size.width, mode.size.height
        while overlay.loop:
            Draw.outline(100, 500, 200, 100, 2.5, Colors.vermelho)
            Draw.dashed_line(*overlay.mid, *overlay.corner["lower_right"], 3, Colors.verde)
            Draw.circle(width // 2, height // 2,radius=100,color= Colors.branco, filled=False,segments=360, line_width=0.6)
            Draw.corner_box(500 ,500, 100, 200,color=(0.0, 0.0, 1.0, 1.0), outline_color=(0.0, 0.0, 1.0, 1.0))
            overlay.update()
            