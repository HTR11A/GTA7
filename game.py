import pygame
import time


def draw_red_circles(unpressed_circles, screen):
    for circle in unpressed_circles:
        pygame.draw.circle(screen, (255, 0, 0), circle['X_pos'], circle['Radius'])

def click_circle(args, simultaneous_circles, unpressed_circles):
    n = 0
    x, y = args[0], args[1]
    centre = simultaneous_circles[0][0]['X_pos']
    a, b = centre[0], centre[1]  #координаты центра круга
    r = simultaneous_circles[0][0]['Radius']
    if abs(a - x) ** 2 + abs(b - y) ** 2 <= r ** 2:
        del simultaneous_circles[0]
        return simultaneous_circles, unpressed_circles
    else:
        n += 1
        simultaneous_circles, unpressed_circles, n = color_change(simultaneous_circles, unpressed_circles, n)
        return simultaneous_circles, unpressed_circles
    # опять же, проигрыш


def color_change(simultaneous_circles, unpressed_circles, n):
    for i in range(n):
        circle = [{'Color': (255, 0, 0), 'X_pos': simultaneous_circles[0][0]['X_pos'], 'Prep_start_time': 0.3,
                   'Click_time': simultaneous_circles[0][0]['Click_time'] + simultaneous_circles[0][0]['Prep_start_time'],
                   'Radius': simultaneous_circles[0][0]['Radius']}]
        unpressed_circles.append(circle)
        del simultaneous_circles[0]
    n = 0
    return simultaneous_circles, unpressed_circles, n