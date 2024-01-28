import pygame
import random

class Circles(pygame.sprite.Sprite):

    def __init__(self, screen):
        """создаем кружок"""
        super(Circles,self).__init__()
        self.screen = screen
        self.rect = pygame.Rect(0, 0, 100, 10)
        self.color = (pygame.Color('white'))

    def update(self):
        """появление кружка в рандомном месте"""
        self.rect.centerx = random.randint(100, 100)
    def draw_circle(self):
        """рисуем кружок на экране"""
        pygame.draw.rect(self.screen, self.color, self.rect)
