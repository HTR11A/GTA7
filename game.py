import pygame
import librosa
from editor import draw


def click_circle(args, clickable_circles, circles, elapsed_time):
    clickable_circles.sort(key=lambda x: x['Click_time'])
    x, y = args[0], args[1]
    centre = clickable_circles[0]['X_pos']
    a, b = centre[0], centre[1]  #координаты центра круга
    r = clickable_circles[0]['Radius']
    if abs(a - x) ** 2 + abs(b - y) ** 2 <= r ** 2 and clickable_circles[0]['Click_time'] - 0.1 <= elapsed_time:
        for i in range(len(circles)):
            if circles[i]['ID'] == clickable_circles[0]['ID']:
                clickable_circles[0]['Color'] = (0, 255, 0)
                del circles[i]
                return circles, True, clickable_circles[0]
    else:
        for i in range(len(circles)):
            if circles[i]['ID'] == clickable_circles[0]['ID']:
                del circles[i]
                return circles, False, clickable_circles[0]
    # опять же, проигрыш


def draw_x(elapsed_time, array, x_mark, scr):
    array_copy = array.copy()
    for i in range(len(array)):
        if elapsed_time - array[i]['Click_time'] <= 1:
            scr.blit(x_mark, (array[i]['X_pos'][0] - 25, array[i]['X_pos'][1] - 25))
        else:
            for j in range(len(array_copy)):
                if array_copy[j]['ID'] == array[i]['ID']:
                    del array_copy[j]
                    break
    return array_copy


def draw_check(elapsed_time, array, scr):
    array_copy = array.copy()
    for i in range(len(array)):
        if elapsed_time - array[i]['Click_time'] <= 1 and array[i]['Radius'] > 10:
            array[i]['Radius'] -= round((elapsed_time - array[i]['Click_time']) * 0.5 * array[i]['Radius'])
            # array[i]['Ring'] += round((elapsed_time - array[i]['Click_time']) * 10)
        else:
            for j in range(len(array_copy)):
                if array_copy[j]['ID'] == array[i]['ID']:
                    del array_copy[j]
                    break
    draw(array, scr)
    return array_copy


def load_game_audio(inp):
    pygame.mixer.init()
    pygame.mixer.music.load(inp)
    pygame.mixer.music.play()
    return round(librosa.get_duration(path=inp))


def display_result(hit, total, font, scr, w, h):
    text = font.render(f'{round(hit / total * 100)}%\n{hit}/{total}', True, (255, 255, 255))
    rectangle = text.get_rect(center=(w // 2, h // 2 - 75))
    scr.blit(text, rectangle)
