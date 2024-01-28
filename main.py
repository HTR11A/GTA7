import pygame
import sys
from morgen import Morgen

def run():

    pygame.init()
    screen = pygame.display.set_mode((1200, 600))
    pygame.display.set_caption('SOSU GAME')
    bg_color = (0, 0, 0)
    morgen = Morgen(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(bg_color)
        morgen.output() # вызов функции отрисовки картинки
        pygame.display.flip()
run()