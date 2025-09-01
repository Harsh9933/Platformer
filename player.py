import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, GROUND_LEVEL):
        super().__init__()
        player_surface_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_surface_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.walk_frames = [player_surface_1, player_surface_2]
        self.jump_frame = pygame.image.load('graphics/Player/jump.png').convert_alpha()

        self.index = 0
        self.image = self.walk_frames[self.index]
        self.rect = self.image.get_rect(midbottom=(pos_x, pos_y))
        self.gravity = 0
        self.GROUND_LEVEL = GROUND_LEVEL

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= self.GROUND_LEVEL:
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= self.GROUND_LEVEL:
            self.rect.bottom = self.GROUND_LEVEL

    def animate(self):
        if self.rect.bottom < self.GROUND_LEVEL:
            self.image = self.jump_frame
        else:
            self.index += 0.1
            if self.index >= len(self.walk_frames):
                self.index = 0
            self.image = self.walk_frames[int(self.index)]

    def update(self):
        self.handle_input()
        self.apply_gravity()
        self.animate()
