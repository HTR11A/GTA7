import pygame
import pygame_gui
import time
from editor import draw, timer, edit, draw_timeline, play_pause, pause_menu, load_audio, alter_playback_speed, \
    close_editor, del_circle, save_level, get_color, draw_swatch
from menu import Button, get_levels, get_audio_path, get_image_path, get_level_files
from game import click_circle, draw_x, draw_check, load_game_audio, display_result
from os import listdir


def menu(scr):
    global current_size
    screen_w, screen_h = current_size[0], current_size[1]

    BG = pygame.image.load('image/BG.jpg')
    gta7 = pygame.image.load('image/logo2.png')
    gta7 = pygame.transform.scale(gta7, (400, 400))

    long_button = pygame.image.load('image/long_button.png')
    long_button = pygame.transform.scale(long_button, (300, 75))
    short_button = pygame.image.load('image/short_button.png')
    short_button = pygame.transform.scale(short_button, (75, 75))
    menu_bg = pygame.image.load('image/menu_bg.png')
    menu_bg = pygame.transform.scale(menu_bg, (screen_w, screen_h))

    resume_btn = Button('Играть', long_button, screen_w // 2, 5 / 10 * screen_h, scr)
    editor_btn = Button('Редактор', long_button, screen_w // 2, 6 / 10 * screen_h, scr)
    quit_btn = Button('Выйти', long_button, screen_w // 2, 7 / 10 * screen_h, scr)
    next_btn = Button('>', short_button, screen_w // 2 + 350, 8 / 10 * screen_h, scr)
    prev_btn = Button('<', short_button, screen_w // 2 - 350, 8 / 10 * screen_h, scr)
    set_audio_btn = Button('Выбрать аудио', long_button, screen_w // 2, 5 / 10 * screen_h, scr)
    set_image_btn = Button('Выбрать фон', long_button, screen_w // 2, 6 / 10 * screen_h, scr)
    create_level_btn = Button('Создать', long_button, screen_w // 2, 7 / 10 * screen_h, scr)
    edit_existing_level_btn = Button('Править выбранный', long_button, screen_w // 2, 3 / 10 * screen_h, scr)
    editor_audio_path, editor_image_path = '', ''
    levels = listdir('levels')
    level_selector = 0
    ui_clock = pygame.time.Clock()
    manager = pygame_gui.UIManager((current_size[0], current_size[1]), theme_path='style.json')
    name_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(((screen_w / 2 - 260, 4 / 10 * screen_h - 38), (520, 76))), manager=manager,
        object_id='#name_input')
    edit_menu_on = False
    running = True
    while running:
        scr.blit(BG, (0, 0))
        scr.blit(gta7, (screen_w / 2 - 200, screen_h / 4.3 - 200))
        pygame.draw.rect(scr, (236, 102, 162), (screen_w / 2 - 260, 8 / 10 * screen_h - 38, 520, 76), border_radius=20)
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
                if edit_menu_on and edit_existing_level_btn.checkforinput(event.pos):
                    edit_existing_level_btn.changetext('Loading')
                    loaded_data = get_level_files(levels, level_selector)
                    editor(scr, loaded_data[1], loaded_data[2], 'levels/' + levels[level_selector], existing_level=loaded_data[0])
                if resume_btn.checkforinput(event.pos) and not edit_menu_on:
                    game(scr, *get_level_files(levels, level_selector))
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
                edit_existing_level_btn.hover(event.pos)
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
            pause_menu(scr, current_size, menu_bg)
            manager.draw_ui(scr)
            set_audio_btn.update()
            set_image_btn.update()
            create_level_btn.update()
            edit_existing_level_btn.update()
        pygame.display.flip()
        pygame.display.update()

    pygame.quit()


def game(scr, circles_game, audio_path, image_path):
    global current_size
    bg = pygame.image.load(image_path)
    bg = pygame.transform.scale(bg, (current_size[0], current_size[1]))
    clickable_circles = []
    missed_circles = []
    hit_circles = []
    hit_counter = 0
    total_circles = len(circles_game)
    total_duration = 0
    elapsed_time = 0
    is_playing = False
    game_start_time = 0
    game_is_paused = False
    running = True
    font = pygame.font.Font("fonts/Roboto-Black.ttf", 30)
    x_mark = pygame.image.load('image/x_mark.png')
    x_mark = pygame.transform.scale(x_mark, (50, 50))
    long_button = pygame.image.load('image/long_button.png')
    long_button = pygame.transform.scale(long_button, (300, 75))
    menu_bg = pygame.image.load('image/menu_bg.png')
    menu_bg = pygame.transform.scale(menu_bg, (screen_w, screen_h))
    menu_btn = Button('Quit to menu', long_button, screen_w // 2, screen_h // 2, scr)
    start_btn = Button('START', long_button, screen_w // 2, screen_h // 2, scr)

    while running:
        scr.fill((0, 0, 0))
        scr.blit(bg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_is_paused = not game_is_paused
                else:
                    if not game_is_paused and is_playing and len(clickable_circles) > 0:
                        a = click_circle(pygame.mouse.get_pos(), clickable_circles, circles_game, elapsed_time)
                        circles_game = a[0]
                        if a[1]:
                            a[2]['Click_time'] = elapsed_time
                            a[2]['Ring'] = 0
                            hit_circles.append(a[2])
                            hit_counter += 1
                        else:
                            a[2]['Click_time'] = elapsed_time
                            a[2]['Ring'] = 0
                            missed_circles.append(a[2])
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_is_paused and start_btn.checkforinput(event.pos) and not is_playing:
                    game_start_time = time.time() - game_start_time
                    is_playing = True
                    total_duration = load_game_audio(audio_path)
                elif not game_is_paused and is_playing and len(clickable_circles) > 0:
                    a = click_circle(event.pos, clickable_circles, circles_game, elapsed_time)
                    circles_game = a[0]
                    if a[1]:
                        a[2]['Click_time'] = elapsed_time
                        a[2]['Ring'] = 0
                        hit_circles.append(a[2])
                        hit_counter += 1
                    else:
                        a[2]['Click_time'] = elapsed_time
                        a[2]['Ring'] = 0
                        missed_circles.append(a[2])
                elif game_is_paused and menu_btn.checkforinput(event.pos):
                    pygame.mixer.music.stop()
                    menu(scr)
            elif event.type == pygame.MOUSEMOTION:
                menu_btn.hover(event.pos)
                start_btn.hover(event.pos)

        a = timer(elapsed_time, circles_game, mode=0)
        clickable_circles = a[0]
        for e in a[1]:
            missed_circles.append(e)
        circles_game = a[2]
        draw(clickable_circles, scr)
        missed_circles = draw_x(elapsed_time, missed_circles, x_mark, scr)
        hit_circles = draw_check(elapsed_time, hit_circles, scr)

        if is_playing:
            elapsed_time = time.time() - game_start_time
            if elapsed_time > total_duration:
                pygame.mixer.music.stop()
                elapsed_time = total_duration
                game_is_paused = True

        if not is_playing and not game_is_paused:
            pause_menu(scr, current_size, menu_bg)
            start_btn.update()

        if game_is_paused:
            pause_menu(scr, current_size, menu_bg)
            menu_btn.update()
            display_result(hit_counter, total_circles, font, scr, screen_w, screen_h)
        pygame.display.flip()
    pygame.quit()


def editor(scr, audio_file, bg_path, directory, existing_level=None):
    global current_size
    if existing_level is None:
        circles = []
    else:
        circles = existing_level
    bg = pygame.image.load(bg_path)
    bg = pygame.transform.scale(bg, (current_size[0], current_size[1]))
    total_duration, temp, dur_slow = load_audio(audio_file)
    is_playing = False
    is_dragging = False
    edit_timeline = False
    start_time = 0
    paused_time = 0
    elapsed_time = 0
    timeline_width = current_size[0] * 3 // 4
    timeline_height = timeline_width // 20
    border_radius = timeline_height // 10
    timeline_x = (current_size[0] - timeline_width) // 2
    timeline_y = current_size[1] - timeline_height
    selector_position = timeline_x
    selector_width = timeline_width // 60
    playback_speed = 1
    opt_playback_speed = dur_slow / total_duration
    cur_radius = 40
    cur_color = (255, 255, 255)
    cur_preptime = 0.5
    editor_is_paused = False
    running = True

    long_button = pygame.image.load('image/long_button.png')
    long_button = pygame.transform.scale(long_button, (300, 75))
    short_button = pygame.image.load('image/short_button.png')
    short_button = pygame.transform.scale(short_button, (timeline_height + border_radius * 2,
                                                         timeline_height + border_radius * 2))
    menu_bg = pygame.image.load('image/menu_bg.png')
    menu_bg = pygame.transform.scale(menu_bg, (screen_w, screen_h))

    save_btn = Button('Save', long_button, current_size[0] // 2, current_size[1] // 2 - current_size[1] // 10, scr)
    menu_btn = Button('Quit to menu', long_button, current_size[0] // 2, current_size[1] // 2 + current_size[1] // 10,
                      scr)
    button_indent = current_size[0] - (timeline_x + timeline_width + timeline_height * 1.5 + border_radius * 6)
    velocity_btn = Button(str(playback_speed) + 'x', short_button,
                          timeline_x + timeline_width + timeline_height // 2 + border_radius * 3,
                          timeline_y - border_radius + timeline_height // 2, scr)
    color_btn = Button('', short_button, button_indent + timeline_height + border_radius * 3,
                       timeline_y - border_radius + timeline_height // 2, scr)
    radius_btn = Button(str(cur_radius) + 'px', short_button,
                        timeline_x + timeline_width + timeline_height * 1.5 + border_radius * 6,
                        timeline_y - border_radius + timeline_height // 2, scr)
    preptime_btn = Button(str(cur_preptime) + 's', short_button, button_indent,
                          timeline_y - border_radius + timeline_height // 2, scr)
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
                else:
                    circles = edit(circles, pygame.mouse.get_pos(), elapsed_time, cur_radius, cur_preptime, cur_color)
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
                        velocity_btn.changetext(str(round(playback_speed, 1)) + 'x')
                    elif color_btn.checkforinput(event.pos):
                        cur_color = get_color(cur_color)
                    elif timeline_y - 2 * border_radius <= event.pos[1] <= timeline_y + timeline_height:
                        edit_timeline = True
                        is_dragging = True
                        is_playing = False
                        mouse_x = event.pos[0]
                        selector_position = max(timeline_x, min(mouse_x, timeline_x + timeline_width - selector_width))
                    else:
                        circles = edit(circles, event.pos, elapsed_time, cur_radius, cur_preptime, cur_color)
                elif event.button == 3:
                    try:
                        del_id = del_circle(event.pos, cur_circles)
                        for i in range(len(circles)):
                            if circles[i]['ID'] == del_id:
                                del circles[i]
                                break
                    except NameError:
                        pass
                elif event.button == 4:
                    if radius_btn.checkforinput(event.pos):
                        cur_radius += 1
                        radius_btn.changetext(str(cur_radius) + 'px')
                    elif preptime_btn.checkforinput(event.pos):
                        cur_preptime = round(cur_preptime + 0.1, 1)
                        preptime_btn.changetext(str(cur_preptime) + 's')
                elif event.button == 5:
                    if radius_btn.checkforinput(event.pos) and cur_radius > 1:
                        cur_radius -= 1
                        radius_btn.changetext(str(cur_radius) + 'px')
                    elif preptime_btn.checkforinput(event.pos) and cur_preptime > 0.1:
                        cur_preptime = round(cur_preptime - 0.1, 1)
                        preptime_btn.changetext(str(cur_preptime) + 's')
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
        scr.fill((0, 0, 0))
        scr.blit(bg, (0, 0))
        if is_playing:
            elapsed_time = paused_time + (time.time() - start_time - paused_time) / playback_speed
            if elapsed_time > total_duration:
                elapsed_time = total_duration
                is_playing = False
            selector_position = timeline_x + (elapsed_time / total_duration) * (timeline_width - selector_width)
        cur_circles = timer(elapsed_time, circles, mode=1)
        draw(cur_circles, screen)
        draw_timeline(selector_position, elapsed_time, total_duration, screen, current_size)

        radius_btn.hover(pygame.mouse.get_pos())
        preptime_btn.hover(pygame.mouse.get_pos())
        velocity_btn.update()
        color_btn.update()
        radius_btn.update()
        preptime_btn.update()
        draw_swatch(cur_color, scr, (button_indent + timeline_height + border_radius * 3,
                                     timeline_y - border_radius + timeline_height // 2),
                    timeline_height + border_radius * 2)

        if editor_is_paused:
            pause_menu(scr, current_size, menu_bg)
            save_btn.update()
            menu_btn.update()
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    pygame.init()

    info = pygame.display.Info()
    screen_w, screen_h = info.current_w, info.current_h
    screen = pygame.display.set_mode((screen_w, screen_h), pygame.RESIZABLE)
    current_size = screen.get_size()
    try:
        menu(screen)
    except pygame.error:
        pass
