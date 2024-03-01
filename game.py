import pygame
import time


def over(simultaneous_circles, elapsed_time, duration_of_appearance):
    for i in simultaneous_circles:
        if i[0]['Click_time'] + duration_of_appearance < elapsed_time:
            i[0]['Color'] = (255, 0, 0)
            # добавить экран проигрыша, лучше отдельной функцией


def click_circle(args, simultaneous_circles):
    x, y = args[0], args[1]
    centre = simultaneous_circles[0][0]['X_pos']
    a, b = centre[0], centre[1]  #координаты центра круга
    r = simultaneous_circles[0][0]['Radius']
    if abs(a - x) ** 2 + abs(b - y) ** 2 <= r ** 2:
        del simultaneous_circles[0]
        return simultaneous_circles
    else:
        pass
    # опять же, проигрыш