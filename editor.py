import pygame
import time
import librosa
import soundfile as sf
import tempfile
import os
import json
import shutil


def timer(elapsed_time, array, mode=0):
    output = []
    if mode == 0:
        for e in array:
            if e['Click_time'] - e['Prep_start_time'] <= elapsed_time <= e['Click_time']:
                if e['Click_time'] - e['Prep_start_time'] >= 0:
                    output.append(e)
                else:
                    e['Prep_start_time'] = e['Click_time']
                    output.append(e)
    else:
        for e in array:
            if e['Click_time'] <= elapsed_time <= e['Click_time']:
                if e['Click_time'] - e['Prep_start_time'] >= 0:
                    output.append(e)
                else:
                    e['Prep_start_time'] = e['Click_time']
                    output.append(e)
            elif e['Click_time'] <= elapsed_time <= e['Click_time'] + 0.5 and e['Radius'] >= 0:
                b = {'Color': (255, 255, 255), 'X_pos': e['X_pos'],
                     'Prep_start_time': e['Prep_start_time'], 'Click_time': e['Click_time'],
                     'Radius': e['Radius'] - round((elapsed_time - e['Click_time']) * 13 * e['Radius'], 2), 'ID': e['ID']}
                output.append(b)
    return output


def edit(array, pos, click_time):
    array.append({'Color': (255, 255, 255), 'X_pos': pos,
                  'Prep_start_time': 0.5, 'Click_time': click_time, 'Radius': 20, 'ID': len(array)})
    return array


def draw(array, screen):
    for circle in array:
        pygame.draw.circle(screen, circle['Color'], circle['X_pos'], circle['Radius'])


def play_pause(is_playing, paused_time, start_time, playback_speed):
    if not is_playing:
        is_playing = True
        start_time = time.time() - paused_time
        print((time.time() - start_time) * playback_speed)
        pygame.mixer.music.play(start=(time.time() - start_time) * playback_speed)
    else:
        is_playing = False
        pygame.mixer.music.pause()
        paused_time = time.time() - start_time
    return is_playing, paused_time, start_time


def draw_timeline(selector_position, elapsed_time, total_duration, screen):
    font = pygame.font.SysFont(None, 24)
    img = font.render(f"{elapsed_time:.2f} / {total_duration}s", True, (255, 255, 255))
    screen.blit(img, (20, 20))

    timeline_width = 600
    timeline_height = 30
    timeline_x = (800 - timeline_width) // 2
    timeline_y = 400 // 1.5
    selector_width = 10
    selector_height = 30

    pygame.draw.rect(screen, (255, 255, 255), (timeline_x, timeline_y, timeline_width, timeline_height))  # Таймлайн
    pygame.draw.rect(screen, (255, 0, 0), (selector_position, timeline_y, selector_width, selector_height))  # Ползунок


def pause_menu(screen, current_size):
    pygame.draw.rect(screen, (62, 62, 72), (current_size[0] / 10, current_size[1] / 10, current_size[0] / 10 * 8, current_size[1] / 10 * 8), border_radius=20)


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
            print(cur_circles[i])
            print('ID RETURNED:', cur_circles[i]['ID'])
            return cur_circles[i]['ID']


def save_level(circles, audio_path, image_path, directory):
    os.mkdir(directory)
    with open(directory + '/level.json', 'w') as f:
        json.dump(circles, f)
    shutil.copyfile(audio_path, directory + '/audio.mp3')
    shutil.copyfile(image_path, directory + '/bg.png')
