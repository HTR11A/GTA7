import pygame
import time
from xtest import draw, timer, edit, draw_timeline, play_pause


def menu(scr):
    pass


def game(scr):
    pass


def editor(scr):
    circles = []
    total_duration = 40
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
    running = True
    while running:
        scr.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pp = play_pause(is_playing, paused_time, start_time)
                    is_playing, paused_time, start_time = pp[0], pp[1], pp[2]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if timeline_y <= event.pos[1] <= timeline_y + 30:
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
                    paused_time = (selector_position - timeline_x) / (timeline_width - selector_width) * total_duration
                    elapsed_time = (selector_position - timeline_x) / (timeline_width - selector_width) * total_duration
            elif event.type == pygame.MOUSEMOTION and is_dragging:
                mouse_x, _ = event.pos
                selector_position = max(timeline_x, min(mouse_x, timeline_x + timeline_width - selector_width))
        if is_playing:
            elapsed_time = time.time() - start_time
            if elapsed_time > total_duration:
                elapsed_time = total_duration
                is_playing = False
            selector_position = timeline_x + (elapsed_time / total_duration) * (timeline_width - selector_width)
        else:
            if elapsed_time < total_duration:
                elapsed_time = paused_time
            else:
                elapsed_time = total_duration
        cur_circles = timer(elapsed_time, circles)
        draw(cur_circles, screen)
        draw_timeline(selector_position, elapsed_time, total_duration, screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 400
    print(width)
    screen = pygame.display.set_mode(size)

    editor(screen)
