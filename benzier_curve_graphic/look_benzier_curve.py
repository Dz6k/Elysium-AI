import matplotlib.pyplot as plt
import numpy as np
import random

def cubic_bezier(start, end, control1, control2, t):
    u = 1 - t
    tt = t * t
    uu = u * u
    uuu = uu * u
    ttt = tt * t

    x = uuu * start[0] + 3 * uu * t * control1[0] + 3 * u * tt * control2[0] + ttt * end[0]
    y = uuu * start[1] + 3 * uu * t * control1[1] + 3 * u * tt * control2[1] + ttt * end[1]

    return x, y


detected_x, detected_y = 566, 511
crosshair_x, crosshair_y = 0, 0  #
sensibilidade = 1 

start = (0, 0)
end = (detected_x - crosshair_x, detected_y - crosshair_y)
offset = random.randint(100,700) 
control1 = (start[0] + (end[0] - start[0]) // 3, start[1] + (end[1] - start[1]) // 3 + offset)
control2 = (start[0] + 2 * (end[0] - start[0]) // 3, start[1] + 2 * (end[1] - start[1]) // 3 - offset)

t_values = np.linspace(0, 1, 100)
curve_points = [cubic_bezier(start, end, control1, control2, t) for t in t_values]


x_vals, y_vals = zip(*curve_points)


plt.figure(figsize=(8, 6))
plt.plot(x_vals, y_vals, label="Curva Bézier", color="blue")
plt.scatter(*zip(start, control1, control2, end), color="red", label="Pontos de Controle")
plt.text(*start, "Start", fontsize=12, verticalalignment='bottom', horizontalalignment='right')
plt.text(*control1, "C1", fontsize=12, verticalalignment='bottom', horizontalalignment='right')
plt.text(*control2, "C2", fontsize=12, verticalalignment='bottom', horizontalalignment='right')
plt.text(*end, "End", fontsize=12, verticalalignment='bottom', horizontalalignment='right')

plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.title("Movimento da Mira com Curva Bézier")
plt.grid()
plt.show()
