import pygame
import sys

class Morgen():

    def __init__(self, screen):
        """инициализация моргена"""

        self.screen =  screen
        self.image = pygame.image.load('image/Morgenshtern.png')
        self.rect = self.image.get_rect() # создание прямоугольника для картинки
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx # координата центра х нашего изображения
        self.rect.bottom = self.screen_rect.bottom

    def output(self):
        """рисование моргена"""
        self.screen.blit(self.image, self.rect) # метод blit отрисовывает изображение