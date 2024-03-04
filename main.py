import pygame
import pygame_gui
import time
from editor import draw, timer, edit, draw_timeline, play_pause, pause_menu, load_audio, alter_playback_speed, \
    close_editor, del_circle, save_level
from menu import Button, get_levels, get_audio_path, get_image_path
from game import click_circle, draw_red_circles, color_change
from os import listdir
from morgen import Morgen


def menu(scr):
    global current_size
    screen_w, screen_h = current_size[0], current_size[1]

    BG = pygame.image.load('image/BG.jpg')
    gta7 = pygame.image.load('image/GTA7_IMG.png')
    gta7 = pygame.transform.scale(gta7, (600, 600))
    # gta7_rect = gta7.get_rect(bottomright=(123, 234))

    img = pygame.image.load('image/button.png')
    img = pygame.transform.scale(img, (300, 75))

    # img = pygame.image.load('image/Morgenshtern.png')
    # img = pygame.transform.scale(img, (200, 100))
    resume_btn = Button('Continue', img, screen_w // 2, 5 / 10 * screen_h, scr)
    editor_btn = Button('Create new level', img, screen_w // 2, 6 / 10 * screen_h, scr)
    quit_btn = Button('Quit', img, screen_w // 2, 7 / 10 * screen_h, scr)
    next_btn = Button('>', img, screen_w // 4 * 3, 8 / 10 * screen_h, scr)
    prev_btn = Button('<', img, screen_w // 4, 8 / 10 * screen_h, scr)
    set_audio_btn = Button('set audio', img, screen_w // 2, 5 / 10 * screen_h, scr)
    set_image_btn = Button('set image', img, screen_w // 2, 6 / 10 * screen_h, scr)
    create_level_btn = Button('continue', img, screen_w // 2, 7 / 10 * screen_h, scr)
    editor_audio_path, editor_image_path = '', ''
    levels = listdir('levels')
    level_selector = 0
    print(current_size)
    ui_clock = pygame.time.Clock()
    manager = pygame_gui.UIManager((current_size[0], current_size[1]), theme_path='style.json')
    name_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(((screen_w / 2 - 260, 4 / 10 * screen_h - 38), (520, 76))), manager=manager,
                                                     object_id='#name_input')
    # name_input.background_colour((255, 255, 255))
    edit_menu_on = False
    running = True
    while running:
        scr.blit(BG, (0, 0))
        scr.blit(gta7, (screen_w / 2.9, -10))
        pygame.draw.rect(scr, (0, 0, 0), (screen_w / 2 - 260, 8 / 10 * screen_h - 38, 520, 76), border_radius=20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if edit_menu_on and set_audio_btn.checkforinput(event.pos):
                    editor_audio_path = get_audio_path()
                if edit_menu_on and set_image_btn.checkforinput(event.pos):
                    editor_image_path = get_image_path()
                if edit_menu_on and create_level_btn.checkforinput(event.pos) and \
                        editor_audio_path != '' and editor_image_path != '' and name_input.get_text() != '':
                    create_level_btn.changetext('Loading')
                    editor(scr, editor_audio_path, editor_image_path, 'levels/' + name_input.get_text())
                if resume_btn.checkforinput(event.pos) and not edit_menu_on:
                    for e in listdir('levels/' + levels[level_selector]):
                        if e == 'bg.png':
                            game(scr, 'levels/' + levels[level_selector] + '/audio.mp3',
                                 'levels/' + levels[level_selector] + '/bg.png', 'levels/' + levels[level_selector])
                            print(scr, 'levels/' + levels[level_selector] + '/audio.mp3',
                                  'levels/' + levels[level_selector] + '/bg.png', 'levels/' + levels[level_selector])
                        elif e == 'bg.jpg':
                            game(scr, 'levels/' + levels[level_selector] + '/audio.mp3',
                                 'levels/' + levels[level_selector] + '/bg.jpg', 'levels/' + levels[level_selector])
                if editor_btn.checkforinput(event.pos) and not edit_menu_on:
                    edit_menu_on = True
                if quit_btn.checkforinput(event.pos) and not edit_menu_on:
                    pygame.quit()
                if next_btn.checkforinput(event.pos) and not edit_menu_on:
                    if level_selector < len(levels) - 1:
                        level_selector += 1
                    else:
                        level_selector = 0
                if prev_btn.checkforinput(event.pos) and not edit_menu_on:
                    if level_selector > 0:
                        level_selector -= 1
                    else:
                        level_selector = len(levels) - 1
            elif event.type == pygame.MOUSEMOTION:
                resume_btn.hover(event.pos)
                editor_btn.hover(event.pos)
                quit_btn.hover(event.pos)
                next_btn.hover(event.pos)
                prev_btn.hover(event.pos)
                set_audio_btn.hover(event.pos)
                set_image_btn.hover(event.pos)
                if editor_audio_path != '' and editor_image_path != '' and name_input.get_text() != '':
                    create_level_btn.hover(event.pos)
            elif event.type == pygame.VIDEORESIZE:
                current_size = event.size
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    edit_menu_on = False
            manager.process_events(event)
        manager.update(ui_clock.tick(60) / 1000)
        resume_btn.update()
        editor_btn.update()
        quit_btn.update()
        next_btn.update()
        prev_btn.update()
        get_levels(levels, level_selector, scr, current_size)
        if edit_menu_on:
            pause_menu(scr, current_size)
            manager.draw_ui(scr)
            set_audio_btn.update()
            set_image_btn.update()
            create_level_btn.update()
        pygame.display.flip()
        pygame.display.update()

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
                        simultaneous_circles, unpressed_circles = click_circle(event.pos, simultaneous_circles,
                                                                               unpressed_circles)
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
                if len(cur_circles) > 0 and \
                        elapsed_time < cur_circles[0]['Prep_start_time'] + cur_circles[0]['Click_time'] and \
                        cur_circles not in simultaneous_circles:
                    simultaneous_circles.append(cur_circles)
                for i in simultaneous_circles:
                    if elapsed_time < i[0]['Prep_start_time'] + i[0]['Click_time']:
                        draw(i, screen)
                    else:
                        n += 1
                if n > 0:
                    simultaneous_circles, unpressed_circles, n = color_change(simultaneous_circles, unpressed_circles,
                                                                              n)
                for i in unpressed_circles:
                    if elapsed_time < i[0]['Prep_start_time'] + i[0]['Click_time']:
                        draw_red_circles(i, screen)

            if editor_is_paused:
                pause_menu(scr, current_size)
                menu_btn.update()
            pygame.display.flip()
    pygame.quit()


def editor(scr, audio_file, bg_path, directory):
    circles = []
    bg = pygame.image.load(bg_path)
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
                if event.button == 1:
                    if editor_is_paused and save_btn.checkforinput(event.pos):
                        save_level(circles, audio_file, bg_path, directory)
                        close_editor(audio_file, temp)
                        menu(scr)
                    elif editor_is_paused and menu_btn.checkforinput(event.pos):
                        close_editor(audio_file, temp)
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
                        velocity_btn.changetext(str(round(playback_speed, 1)))
                    elif timeline_y <= event.pos[1] <= timeline_y + 30:
                        edit_timeline = True
                        is_dragging = True
                        is_playing = False
                        mouse_x, _ = event.pos
                        selector_position = max(timeline_x, min(mouse_x, timeline_x + timeline_width - selector_width))
                    else:
                        circles = edit(circles, event.pos, elapsed_time)
                elif event.button == 3:
                    try:
                        print('cur circles', cur_circles)
                        del_id = del_circle(event.pos, cur_circles)
                        for i in range(len(circles)):
                            if circles[i]['ID'] == del_id:
                                print('DELETING ID:', del_id)
                                print('circles before del:', circles)
                                del circles[i]
                                print('circles after del:', circles)
                                break
                    except NameError:
                        pass
                if editor_is_paused and save_btn.checkforinput(event.pos):
                    save_level(circles, audio_file, bg, directory)
                elif editor_is_paused and menu_btn.checkforinput(event.pos):
                    menu(scr)
                elif velocity_btn.checkforinput(event.pos):
                    if playback_speed == 1:
                        alter_playback_speed(audio_file, temp, opt_playback_speed)
                        playback_speed = opt_playback_speed
                        velocity_btn.changetext('1.5')
                    else:
                        alter_playback_speed(audio_file, temp, 1)
                        playback_speed = 1
                        velocity_btn.changetext('1')
                    if is_playing:
                        pp = play_pause(is_playing, paused_time, start_time, playback_speed)
                        is_playing, paused_time, start_time = pp[0], pp[1], pp[2]
                    # velocity_btn.changetext(str(round(playback_speed)))
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
        scr.blit(bg, (0, 0))
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
            pause_menu(scr, current_size)
            save_btn.update()
            menu_btn.update()
        velocity_btn.update()
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    pygame.init()

    info = pygame.display.Info()
    screen_w, screen_h = info.current_w, info.current_h
    # size = width, height = 800, 400
    screen = pygame.display.set_mode((screen_w, screen_h), pygame.RESIZABLE)
    current_size = screen.get_size()
    menu(screen)
