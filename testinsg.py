from calculos import process_coordinates
import time
import ctypes
import win32api

my_dll = ctypes.CDLL('./MylibDLL.dll')
# Definir a estrutura Result no Python que corresponde à estrutura C++
class Result(ctypes.Structure):
    _fields_ = [("x1", ctypes.c_int),
                ("y1", ctypes.c_int),
                ("x2", ctypes.c_int),
                ("y2", ctypes.c_int)]

 
my_dll.process_coordinates.argtypes = [ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_int, ctypes.c_int]
my_dll.process_coordinates.restype = ctypes.POINTER(Result)  

 
# result_ptr = my_dll.process_coordinates(0.5, 0.5, 0.8, 0.8, 10, 10)


# result = result_ptr.contents

inicio = time.time()
size = {"left": 1920, "top": 1080}
# for i in range(20000):
    # Dicionário de tamanhos
result_ptr = my_dll.process_coordinates(0.5, 0.5, 0.8, 0.8, int(size['left']), int(size['top']))

#
result = result_ptr.contents
final = time.time()
print("\nResultado c++ (", result.x1, result.y1, result.x2, result.y2, f") tempo:  \n{(final - inicio):.14f}")
    
    
    
# print(f"x1: {result.x1}, y1: {result.y1}, x2: {result.x2}, y2: {result.y2}")


# input('')
# inicio = time.time()
# size = {"left": 1920.0, "top": 1080.0}








for i in range(20000):
    # Dicionário de tamanhos
    result = process_coordinates(0.5, 0.5, 0.8, 0.8, size)
final = time.time()
print("Resultado c++ com python", result, f"tempo:  \n{(final - inicio):.14f}")
    
    
    
    
input('')

def adjust_coordinates(x1: float, y1: float, x2: float, y2: float, size: dict) -> tuple[int, int, int, int]:
        x1_adjusted = int(x1 + size["left"])
        y1_adjusted = int(y1 + size["top"])
        x2_adjusted = int(x2 + size["left"])
        y2_adjusted = int(y2 + size["top"])

        return x1_adjusted, y1_adjusted, x2_adjusted, y2_adjusted
    
inicio = time.time()     
# for i in range(20000):
result = adjust_coordinates(0.5, 0.5, 0.8, 0.8, size)
final = time.time()
print("Resultado:", result, f"tempo:  \n{(final - inicio):.14f}")