import pygame
import time
from editor import draw, timer, edit, draw_timeline, play_pause, pause_menu
from menu import Button
from xtest import load_audio, alter_playback_speed
from game import click_circle, draw_red_circles, color_change


def menu(scr):
    img = pygame.image.load('image/Morgenshtern.png')
    img = pygame.transform.scale(img, (200, 100))
    resume_btn = Button('Continue', img, 200, 10, scr)
    load_level_btn = Button('Load level', img, 200, 110, scr)
    editor_btn = Button('Create new level', img, 200, 210, scr)
    quit_btn = Button('Quit', img, 200, 310, scr)
    running = True
    while running:
        scr.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if resume_btn.checkforinput(event.pos):
                    game(scr)
                if load_level_btn.checkforinput(event.pos):
                    pass
                if editor_btn.checkforinput(event.pos):
                    editor(scr)
                if quit_btn.checkforinput(event.pos):
                    pygame.quit()
            elif event.type == pygame.MOUSEMOTION:
                resume_btn.hover(event.pos)
                load_level_btn.hover(event.pos)
                editor_btn.hover(event.pos)
                quit_btn.hover(event.pos)
        resume_btn.update()
        load_level_btn.update()
        editor_btn.update()
        quit_btn.update()
        pygame.display.flip()

    pygame.quit()


def game(scr):
    global circles
    circles_game = circles.copy()
    simultaneous_circles = []
    unpressed_circles = []
    total_duration = 40
    is_playing = False
    game_start_time = 0
    editor_is_paused = False
    running = True
    img = pygame.image.load('image/Morgenshtern.png')
    img = pygame.transform.scale(img, (200, 100))
    menu_btn = Button('Quit to menu', img, 400, 250, scr)
    start_btn = Button('START', img, 400, 250, scr)
    n = 0

    while running:
        while running:
            scr.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        editor_is_paused = not editor_is_paused
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_btn.checkforinput(event.pos) and not editor_is_paused and not is_playing:
                        game_start_time = time.time() - game_start_time
                        is_playing = True
                        print(1)
                    if len(simultaneous_circles) > 0 and not editor_is_paused and is_playing:
                        simultaneous_circles, unpressed_circles = click_circle(event.pos, simultaneous_circles, unpressed_circles)
                    if menu_btn.checkforinput(event.pos) and editor_is_paused:
                        menu(scr)
                        print(2)
                elif event.type == pygame.MOUSEMOTION:

                    menu_btn.hover(event.pos)
                    start_btn.hover(event.pos)
            if not is_playing:
                start_btn.update()
            if is_playing:
                elapsed_time = time.time() - game_start_time
                if elapsed_time > total_duration:
                    elapsed_time = total_duration
                    # нужно добавить экран окончания уровня
                cur_circles = timer(elapsed_time, circles_game, mode=0)
                if len(cur_circles) > 0 and elapsed_time < cur_circles[0]['Prep_start_time'] + cur_circles[0]['Click_time'] and cur_circles not in simultaneous_circles:
                    simultaneous_circles.append(cur_circles)
                for i in simultaneous_circles:
                    if elapsed_time < i[0]['Prep_start_time'] + i[0]['Click_time']:
                        draw(i, screen)
                    else:
                        n += 1
                if n > 0:
                    simultaneous_circles, unpressed_circles, n = color_change(simultaneous_circles, unpressed_circles, n)
                for i in unpressed_circles:
                    if elapsed_time < i[0]['Prep_start_time'] + i[0]['Click_time']:
                        draw_red_circles(i, screen)

            if editor_is_paused:
                pause_menu(scr)
                menu_btn.update()
            pygame.display.flip()
    pygame.quit()


def editor(scr):
    circles = []
    audio_file = "MACAN-ASPHALT-8.mp3"
    total_duration, temp, dur_slow = load_audio(audio_file)
    print(total_duration, temp)
    is_playing = False
    is_dragging = False
    edit_timeline = False
    start_time = 0
    paused_time = 0
    elapsed_time = 0
    timeline_width = 600
    timeline_x = (800 - timeline_width) // 2
    timeline_y = 400 // 1.5
    selector_position = timeline_x
    selector_width = 10
    playback_speed = 1
    opt_playback_speed = dur_slow / total_duration
    editor_is_paused = False
    running = True
    img = pygame.image.load('image/Morgenshtern.png')
    img = pygame.transform.scale(img, (200, 100))
    save_btn = Button('Save', img, 400, 110, scr)
    menu_btn = Button('Quit to menu', img, 400, 250, scr)
    img = pygame.transform.scale(img, (50, 50))
    velocity_btn = Button(str(playback_speed), img, timeline_x + timeline_width + 35, timeline_y, scr)
    while running:
        scr.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pp = play_pause(is_playing, paused_time, start_time, playback_speed)
                    is_playing, paused_time, start_time = pp[0], pp[1], pp[2]
                elif event.key == pygame.K_ESCAPE:
                    editor_is_paused = not editor_is_paused
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if editor_is_paused and save_btn.checkforinput(event.pos):
                    pass
                elif editor_is_paused and menu_btn.checkforinput(event.pos):
                    menu(scr)
                elif velocity_btn.checkforinput(event.pos):
                    if playback_speed == 1:
                        alter_playback_speed(audio_file, temp, opt_playback_speed)
                        playback_speed = opt_playback_speed
                    else:
                        alter_playback_speed(audio_file, temp, 1)
                        playback_speed = 1
                    if is_playing:
                        pp = play_pause(is_playing, paused_time, start_time, playback_speed)
                        is_playing, paused_time, start_time = pp[0], pp[1], pp[2]
                    velocity_btn.changetext(str(round(playback_speed)))
                elif timeline_y <= event.pos[1] <= timeline_y + 30:
                    edit_timeline = True
                    is_dragging = True
                    is_playing = False
                    mouse_x, _ = event.pos
                    selector_position = max(timeline_x, min(mouse_x, timeline_x + timeline_width - selector_width))
                else:
                    circles = edit(circles, event.pos, elapsed_time)
            elif event.type == pygame.MOUSEBUTTONUP:
                if edit_timeline is True:
                    edit_timeline = False
                    is_dragging = False
                    pygame.mixer.music.pause()
                    paused_time = (selector_position - timeline_x) / (timeline_width - selector_width) * total_duration
                    elapsed_time = (selector_position - timeline_x) / (timeline_width - selector_width) * total_duration
            elif event.type == pygame.MOUSEMOTION:
                if is_dragging:
                    mouse_x, _ = event.pos
                    selector_position = max(timeline_x, min(mouse_x, timeline_x + timeline_width - selector_width))
                save_btn.hover(event.pos)
                menu_btn.hover(event.pos)
                velocity_btn.hover(event.pos)
        if is_playing:
            elapsed_time = paused_time + (time.time() - start_time - paused_time) / playback_speed
            if elapsed_time > total_duration:
                elapsed_time = total_duration
                is_playing = False
            selector_position = timeline_x + (elapsed_time / total_duration) * (timeline_width - selector_width)
        cur_circles = timer(elapsed_time, circles, mode=1)
        draw(cur_circles, screen)
        draw_timeline(selector_position, elapsed_time, total_duration, screen)
        if editor_is_paused:
            pause_menu(scr)
            save_btn.update()
            menu_btn.update()
        velocity_btn.update()
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)

    menu(screen)
