import numpy as np
from scipy.integrate import ode
import matplotlib.pyplot as plt

FlightTime, Distance, Height, v_yold = 0, 0, 0, 0
ts = []
ys = []

def f(t, y, k):
    print(y[0])
    g = 9.81
    x, v_x, y_coordinate, v_y = y[0], y[1], y[2], y[3]
    return [v_x, -k * np.sqrt(v_x ** 2 + v_y ** 2) * v_x, v_y, -k * np.sqrt(v_x ** 2 + v_y ** 2) * v_y - g]

def checker(t, y):
    global FlightTime, Distance, Height, v_yold
    ts.append(t)
    ys.append(list(y.copy()))
    x, v_x, y_coordinate, v_y = y[0], y[1], y[2], y[3]
    if v_y * v_yold <= 0:  # достигнута точка максимума
        Height = y_coordinate
    if v_y < 0 and y_coordinate <= 0.0:  # тело достигло поверхности
        FlightTime = t
        Distance = x
        return -1
    v_yold = v_y

alph = np.pi / 4  # угол бросания тела
v0 = float(input("Введите начальную скорость: "))
h = float(input("Введите высоту: "))
K = [0.5, 0.3, 0.1]  # анализируемые коэффициенты сопротивления
y0, t0 = [0, v0 * np.cos(alph), h, v0 * np.sin(alph)], 0  # начальные условия
ODE = ode(f)
ODE.set_integrator('dopri5', max_step=0.01)
ODE.set_solout(checker)
fig, ax = plt.subplots()
fig.set_facecolor('white')
for k in K:
    ts, ys = [], []
    ODE.set_initial_value(y0, t0)
    ODE.set_f_params(k)
    ODE.integrate(100)
    Y = np.array(ys)
    plt.plot(Y[:, 0], Y[:, 2], linewidth=3, label='k=%.1f' % k)
plt.title("Результаты численного решения")
plt.grid(True)
plt.xlim(0, Distance*1.5)
plt.ylim(-0.1, Height*1.5)
plt.legend(loc='best')
plt.show()
