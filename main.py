import pygame, controls
from morgen import Morgen
from pygame.sprite import Group
def run():

    pygame.init()
    screen = pygame.display.set_mode((1200, 600))
    pygame.display.set_caption('SOSU GAME')
    bg_color = (0, 0, 0)
    morgen = Morgen(screen)
    circles = Group()

    while True:
        controls.events(screen, circles)
        screen.fill(bg_color)
        circles.update()
        morgen.output() # вызов функции отрисовки картинки
        pygame.display.flip()
run()