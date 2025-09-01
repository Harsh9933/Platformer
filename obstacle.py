import pygame
from random import randint
from settings import GROUND_LEVEL

class Snail(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        super().__init__()
        snail1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
        snail2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
        self.frames = [snail1, snail2]
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(midbottom=(pos_x, GROUND_LEVEL))

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()
        self.index += 0.1
        if self.index >= len(self.frames):
            self.index = 0
        self.image = self.frames[int(self.index)]


class Fly(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        super().__init__()
        fly1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
        fly2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
        self.frames = [fly1, fly2]
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(midbottom=(pos_x, 400))

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()
        self.index += 0.1
        if self.index >= len(self.frames):
            self.index = 0
        self.image = self.frames[int(self.index)]
