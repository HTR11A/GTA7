import pygame


class Button:
    def __init__(self, text, image, x_pos, y_pos, screen):
        self.text_str = text
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.screen = screen
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.font = pygame.font.Font("fonts/font.ttf", 25)
        self.text_obj = self.font.render(self.text_str, True, (255, 255, 255))
        self.text_rect = self.text_obj.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.text_obj, self.text_rect)

    def checkforinput(self, position):
        if self.rect.left <= position[0] < self.rect.right and self.rect.top <= position[1] < self.rect.bottom:
            return True
        return False

    def hover(self, position):
        if self.rect.left <= position[0] < self.rect.right and self.rect.top <= position[1] < self.rect.bottom:
            self.text_obj = self.font.render(self.text_str, True, "blue")
        else:
            self.text_obj = self.font.render(self.text_str, True, "white")

    def changetext(self, text):
        self.text_str = text
        self.text_obj = self.font.render(self.text_str, True, (255, 255, 255))
