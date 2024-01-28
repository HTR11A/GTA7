import pygame, sys
from circle import Circles
def events(screen, circles):
    """обработка событий"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN: # если клавиша нажата
            if event.key == pygame.K_SPACE:
                new_circle = Circles(screen)
                circles.add(new_circle)

def update(bg_color, screen, circles):
    """обновление экрана"""
    screen.fill(bg_color)
    for circle in circles.sprites():
        circle.draw_circle()
    circles.output()
    pygame.display.flip()