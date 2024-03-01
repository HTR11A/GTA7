import pygame
import time


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
                     'Radius': e['Radius'] - round((elapsed_time - e['Click_time']) * 13 * e['Radius'], 2)}
                output.append(b)
    return output


def edit(array, pos, click_time):
    array.append({'Color': (255, 255, 255), 'X_pos': pos,
                  'Prep_start_time': 0.5, 'Click_time': click_time, 'Radius': 20})
    return array


def draw(array, screen):
    for circle in array:
        pygame.draw.circle(screen, circle['Color'], circle['X_pos'], circle['Radius'])


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


def pause_menu(screen):
    pygame.draw.rect(screen, (255, 255, 255), (50, 50, 700, 300))  # Таймлайн