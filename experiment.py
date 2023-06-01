import numpy as np
from scipy.integrate import ode
import math
import matplotlib.pyplot as plt

FlightTime, Distance, Height, v_yold = 0, 0, 0, 0
ts = []
ys = []
coef = 0.05

def asker():
    with open('db.txt', 'r') as file:
        latestParams = [float(i) for i in file.readline().split(' ')]
    flag = input(f'Хотите использовать предыдущие параметры запуска (g = {latestParams[0]} м/с^2, s = {latestParams[1]}м., k =  {latestParams[2]}, v0 = {latestParams[3]}м/с, h0 =  {latestParams[4]}м.)? [y/n] ')
    if flag == 'n':
        g = (input('Введите ускорение свободного падения (м/с^2): '))
        if g == '-' or g == '':
            g = latestParams[0]
        else:
            g = float(g)
        wantedRes = (input("Введите расстояние до точки на поверхности (м): "))
        if wantedRes == '-' or wantedRes == '':
            wantedRes = latestParams[1]
        else:
            wantedRes = float(wantedRes)
        k = (input("Введите коэффициент сопротивления воздуха: "))
        if k == '-' or k == '':
            k = latestParams[2]
        else:
            k = float(k)
        v0 = (input('Введите начальную скорость (м/с): '))
        if v0 == '-' or v0 == '':
            v0 = latestParams[3]
        else:
            v0 = float(v0)
        h = (input('Введите начальную высоту (м): '))
        if h == '-' or h == '':
            h = latestParams[4]
        else:
            h = float(h)
        with open('db.txt', 'w') as file:
            file.write(str(" ".join([str(g), str(wantedRes), str(k), str(v0), str(h)])) + '\n')
        return [g, wantedRes, k, v0, h]
    return latestParams
g, wantedRes, k, v0, h = asker()
def f(t, y, k):
    global g
    x, v_x, y_coordinate, v_y = y[0], y[1], y[2], y[3]
    return [v_x, -k * np.sqrt(v_x ** 2 + v_y ** 2) * v_x, v_y, -k * np.sqrt(v_x ** 2 + v_y ** 2) * v_y - g]

def checker(t, y):
    global FlightTime, Distance, Height, v_yold, g
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


def solver(alph, v0, h, k):
    global g
    y0, t0 = [0, v0 * np.cos(alph), h, v0 * np.sin(alph)], 0  # начальные условия
    ODE = ode(f)
    ODE.set_integrator('dopri5', max_step=0.01)
    ODE.set_solout(checker)
    ODE.set_initial_value(y0, t0)
    ODE.set_f_params(k)
    ODE.integrate(100)
    Y = np.array(ys)
    return Y[-1][0]




K = [0.0, 0.1, 0.3, 0.5]
if k not in K:
    K.append(k)

for ks in K:
    possibleAngles = []
    goodAngles = []
    k = ks
    print('\nПараметры текущего запуска:')
    print('==================')
    print(f'g = {g} м/с^2\ns = {wantedRes} м.\nk =  {k}\nv0 = {v0} м/с\nh0 =  {h} м.')
    print('==================')
    print('Начался рачёт угла для попадания в заданую точку поверхности ')
    start_angle = 0
    angle = start_angle
    for i in range(1, 10000):
        if (angle * 180/np.pi)<=90:
            angle = float(str(angle)[:5])
            ans = solver(angle, v0, h, k)
            #print(abs(ans - wantedRes), angle * 180 / np.pi)
            if abs(wantedRes - ans) <= 1 and (abs(wantedRes - ans) >= coef):
                #print("Возможный угол для попадания", str(angle * 180 / np.pi)[:5])
                possibleAngles.append(angle)
            if abs(wantedRes - ans) <= coef:
                goodAngles.append(angle)
                print("Угол для попадания", str(angle * 180 / np.pi)[:5], solver(angle, v0, h, k))
                new_angle = angle
                '''
                for j in range(1, 10000):
                    new_angle += (np.pi / 200)
                    candidate = solver(new_angle, v0, h, k)
                    if abs(wantedRes - candidate) <= 0.05505232035439867:
                        print("Более точный угол для попадания", str(new_angle * 180 / np.pi)[:5])
                        break
                        '''
                break
            angle += np.pi / 150
        else:
            if(len(goodAngles) == 0):
                if (len(possibleAngles) != 0):
                    print("Угол для попадания", str(max(possibleAngles) * 180 / np.pi)[:5])
                else:
                    print('Не удалось найти угол')
            print('Расчет окончен')
            break
'''
            
'''