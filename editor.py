import pygame
import time
import librosa
import soundfile as sf
import tempfile
import os
import json
import shutil
import tkinter as tk
from tkinter import colorchooser


def timer(elapsed_time, array, mode=0):
    output = []
    if mode == 0:
        missed = []
        array_copy = array.copy()
        for i in range(len(array)):
            if array[i]['Click_time'] - array[i]['Prep_start_time'] <= elapsed_time <= array[i]['Click_time'] + 0.2:
                if array[i]['Click_time'] - array[i]['Prep_start_time'] >= 0:
                    e = array[i].copy()
                    # print((e['Click_time'] - elapsed_time) / e['Prep_start_time'])
                    if e['Prep_start_time'] != 0:
                        e['Ring'] = (e['Click_time'] - elapsed_time) / e['Prep_start_time'] * 2.5
                    else:
                        e['Ring'] = 0
                    # e['Ring'] = (e['Click_time'] - elapsed_time) * 8
                    output.append(e)
                else:
                    e = array[i].copy()
                    e['Prep_start_time'] = e['Click_time']
                    if e['Prep_start_time'] != 0:
                        e['Ring'] = (e['Click_time'] - elapsed_time) / e['Prep_start_time'] * 2.5
                    else:
                        e['Ring'] = 0
                    # e['Ring'] = (e['Click_time'] - elapsed_time) * 8
                    output.append(e)
            elif array[i]['Click_time'] + 0.2 < elapsed_time:
                missed.append(array[i])
                for j in range(len(array_copy)):
                    if array_copy[j]['ID'] == array[i]['ID']:
                        del array_copy[j]
                        break
        return output, missed, array
    else:
        for e in array:
            if e['Click_time'] - e['Prep_start_time'] <= elapsed_time <= e['Click_time']:
                if e['Click_time'] - e['Prep_start_time'] >= 0:
                    if e['Prep_start_time'] != 0:
                        e['Ring'] = (e['Click_time'] - elapsed_time) / e['Prep_start_time'] * 2.5
                    else:
                        e['Ring'] = 0
                    # e['Ring'] = (e['Click_time'] - elapsed_time) * 8
                    output.append(e)
                else:
                    e['Prep_start_time'] = e['Click_time']
                    if e['Prep_start_time'] != 0:
                        e['Ring'] = (e['Click_time'] - elapsed_time) / e['Prep_start_time'] * 2.5
                    else:
                        e['Ring'] = 0
                    # e['Ring'] = (e['Click_time'] - elapsed_time) * 8
                    output.append(e)
            elif e['Click_time'] <= elapsed_time <= e['Click_time'] + 0.5 and e['Radius'] >= 0:
                b = {'Color': e['Color'], 'X_pos': e['X_pos'],
                     'Prep_start_time': e['Prep_start_time'], 'Click_time': e['Click_time'],
                     'Radius': e['Radius'] - round((elapsed_time - e['Click_time']) * 13 * e['Radius'], 2),
                     'ID': e['ID'], 'Ring': 0}
                output.append(b)
    return output


def edit(array, pos, click_time, radius, preptime, color):
    array.append({'Color': color, 'X_pos': pos,
                  'Prep_start_time': preptime, 'Click_time': click_time, 'Radius': radius, 'ID': len(array)})
    return array


def draw(array, screen):
    for circle in array:
        edge_color = list(circle['Color'])
        if edge_color[0] <= 40 and edge_color[1] <= 40 and edge_color[2] <= 40:
            for i in range(3):
                edge_color[i] += 40
        else:
            for i in range(3):
                if edge_color[i] >= 40:
                    edge_color[i] -= 40
                else:
                    edge_color[i] = 0
        pygame.draw.circle(screen, circle['Color'], circle['X_pos'],
                           circle['Radius'] + circle['Ring'] * circle['Radius'], width=int(circle['Radius'] / 5))
        pygame.draw.circle(screen, circle['Color'], circle['X_pos'], circle['Radius'])
        pygame.draw.circle(screen, edge_color, circle['X_pos'], circle['Radius'],
                           width=round(circle['Radius'] * 0.15))


def play_pause(is_playing, paused_time, start_time, playback_speed):
    if not is_playing:
        is_playing = True
        start_time = time.time() - paused_time
        pygame.mixer.music.play(start=(time.time() - start_time) * playback_speed)
    else:
        is_playing = False
        pygame.mixer.music.pause()
        paused_time = time.time() - start_time
    return is_playing, paused_time, start_time


def draw_timeline(selector_position, elapsed_time, total_duration, screen, current_size):
    font = pygame.font.SysFont(None, 24)
    img = font.render(f"{elapsed_time:.2f} / {total_duration}s", True, (255, 255, 255))
    screen.blit(img, (20, 20))

    timeline_width = current_size[0] * 3 // 4
    timeline_height = timeline_width // 20
    timeline_x = (current_size[0] - timeline_width) // 2
    timeline_y = current_size[1] - timeline_width // 20
    selector_width = timeline_width // 60
    selector_height = selector_width * 3
    border_radius = timeline_height // 10

    pygame.draw.rect(screen, (255, 255, 255), (timeline_x - border_radius, timeline_y - border_radius * 2,
                                               timeline_width + border_radius * 2, timeline_height + border_radius * 2))
    pygame.draw.rect(screen, (237, 107, 165), (timeline_x, timeline_y - border_radius, timeline_width,
                                               timeline_height))  # Таймлайн
    pygame.draw.rect(screen, (252, 144, 192), (selector_position, timeline_y - border_radius, selector_width,
                                               selector_height))  # Ползунок


def pause_menu(screen, current_size, bg):
    screen.blit(bg, (0, 0))
    pygame.draw.rect(screen, (45, 77, 133),
                     (current_size[0] / 10 * 2, current_size[1] / 10 * 2, current_size[0] / 10 * 6,
                      current_size[1] / 10 * 6),
                     border_radius=20)


def load_audio(inp):
    print('loading started')
    audio, sr = librosa.load(inp, sr=None)
    stretch_factor = 1 / 1.5
    print('applying effect')
    audio_fast = librosa.effects.time_stretch(audio, rate=stretch_factor)
    print('effect applied')
    temp_fd, temp_path = tempfile.mkstemp(suffix='.wav')
    sf.write(temp_path, audio_fast, sr)
    os.close(temp_fd)

    pygame.mixer.init()
    pygame.mixer.music.load(inp)
    print('loading ended')
    return round(librosa.get_duration(path=inp)), temp_path, round(librosa.get_duration(path=temp_path))


def alter_playback_speed(og, slowed, playback_speed):
    if playback_speed == 1:
        pygame.mixer.music.load(og)
    else:
        pygame.mixer.music.load(slowed)


def close_editor(inp, temp_path):
    pygame.mixer.music.load(inp)
    os.remove(temp_path)


def del_circle(args, cur_circles):
    x, y = args[0], args[1]
    for i in range(len(cur_circles)):
        centre = cur_circles[i]['X_pos']
        a, b = centre[0], centre[1]  # координаты центра круга
        r = cur_circles[i]['Radius']
        if abs(a - x) ** 2 + abs(b - y) ** 2 <= r ** 2:
            return cur_circles[i]['ID']


def save_level(circles, audio_path, image_path, directory):
    circles.sort(key=lambda x: x['Click_time'])
    os.mkdir(directory)
    with open(directory + '/level.json', 'w') as f:
        json.dump(circles, f)
    shutil.copyfile(audio_path, directory + '/audio.mp3')
    shutil.copyfile(image_path, directory + '/bg.png')


def get_color(cur_color):
    root = tk.Tk()
    root.withdraw()
    result = []
    a = colorchooser.askcolor(title="Выберите цвет")[0]
    if a is not None:
        for e in a:
            result.append(int(e))
        return tuple(result)
    return cur_color


def draw_swatch(color, screen, pos, size):
    pygame.draw.rect(screen, color, (int(pos[0] - size / 3), int(pos[1] - size / 3), int(size / 1.5),
                                     int(size / 1.5)), border_radius=20)
    pygame.draw.rect(screen, (240, 240, 240), (int(pos[0] - size / 3), int(pos[1] - size / 3), int(size / 1.5),
                                               int(size / 1.5)), border_radius=20, width=int(size / 18))
