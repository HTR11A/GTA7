import tkinter as tk
from os import listdir
from tkinter import filedialog as fd
import json

import pygame


class Button:
    def __init__(self, text, image, x_pos, y_pos, screen):
        self.text_str = str(text)
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.screen = screen
        self.enabled = True
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.font = pygame.font.Font("fonts/Roboto-Black.ttf", 30)
        self.text_obj = self.font.render(self.text_str, True, (255, 235, 250))
        self.text_rect = self.text_obj.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.text_obj, self.text_rect)

    def checkforinput(self, position):
        if self.rect.left <= position[0] < self.rect.right and \
                self.rect.top <= position[1] < self.rect.bottom and self.enabled:
            return True
        return False

    def hover(self, position):
        if self.rect.left <= position[0] < self.rect.right and self.rect.top <= position[1] < self.rect.bottom:
            self.text_obj = self.font.render(self.text_str, True, (255, 255, 255))
        else:
            self.text_obj = self.font.render(self.text_str, True, (255, 235, 250))

    def changetext(self, text):
        self.text_str = str(text)
        self.text_obj = self.font.render(self.text_str, True, (255, 235, 250))
        self.text_rect = self.text_obj.get_rect(center=(self.x_pos, self.y_pos))

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False


def get_levels(levels, level_selector, screen, current_size):
    font = pygame.font.Font("fonts/Roboto-Black.ttf", 30)
    a = levels[level_selector]
    if len(a) >= 28:
        a = levels[level_selector][0:26] + '...'
    img = font.render(a, True, (255, 255, 255))
    text_rect = img.get_rect(center=(current_size[0] // 2, 8 / 10 * current_size[1]))
    screen.blit(img, text_rect)


def get_audio_path():
    root = tk.Tk()
    root.withdraw()
    return fd.askopenfilename(filetypes=[('Audio files', '.mp3')], title='Выберите аудифайл')


def get_image_path():
    root = tk.Tk()
    root.withdraw()
    return fd.askopenfilename(filetypes=[('PNG', '.png'), ('JPG', '.jpg')], title='Выберите фон')


def get_level_files(levels, level_selector):
    with open('levels/' + levels[level_selector] + '/level.json') as f:
        circles = json.load(f)
    if 'bg.png' in listdir('levels/' + levels[level_selector]):
        return circles, 'levels/' + levels[level_selector] + '/audio.mp3', \
               'levels/' + levels[level_selector] + '/bg.png'
    return circles, 'levels/' + levels[level_selector] + '/audio.mp3', 'levels/' + levels[level_selector] + '/bg.jpg'
