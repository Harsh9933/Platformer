import pygame
from sys import exit
from random import randint
from settings import *
del GROUND_LEVEL
from player import Player
from obstacle import Snail, Fly


class Main:

    def __init__(self):
        pygame.init()

        # Fixed resolution (720p)
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 1280, 720
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Runner")

        self.clock = pygame.time.Clock()

        # Background
        self.sky_surface = pygame.image.load('graphics/Sky.png').convert()
        self.ground_surface = pygame.image.load('graphics/ground.png').convert()

        self.sky_surface = pygame.transform.scale(self.sky_surface, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.ground_height = self.ground_surface.get_height()
        self.GROUND_LEVEL = self.screen.get_height() - self.ground_surface.get_height()

        # Groups
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player(self.SCREEN_WIDTH // 10, self.GROUND_LEVEL, self.GROUND_LEVEL))

        self.obstacles = pygame.sprite.Group()

        # Timer for spawning obstacles
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, randint(800, 2000))

        self.game_active = True
        self.start_time = pygame.time.get_ticks()

    def display_score(self):
        current_time = (pygame.time.get_ticks() - self.start_time) // 1000
        font = pygame.font.Font('font/Pixeltype.ttf', 50)
        score_surface = font.render(f"Score: {current_time}", False, "Black")
        score_rect = score_surface.get_rect(center=(self.SCREEN_WIDTH // 2, 50))
        self.screen.blit(score_surface, score_rect)
        return current_time

    def draw_ground(self):
        for x in range(0, self.SCREEN_WIDTH, self.ground_surface.get_width() ):
            self.screen.blit(self.ground_surface, (x, self.SCREEN_HEIGHT - self.ground_height))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if self.game_active and event.type == self.obstacle_timer:
                    if randint(0, 2):
                        self.obstacles.add(Snail(randint(1280, 1300)))
                        pygame.time.set_timer(self.obstacle_timer, randint(800, 2000))

                    else:
                        self.obstacles.add(Fly(randint(1280, 1300)))

            if self.game_active:
                self.screen.blit(self.sky_surface, (0, 0))
                self.draw_ground()
                score = self.display_score()

                # Player
                self.player.update()
                self.player.draw(self.screen)

                # Obstacles
                self.obstacles.update()
                self.obstacles.draw(self.screen)

                # Collisions
                if pygame.sprite.spritecollide(self.player.sprite, self.obstacles, False):
                    self.game_active = False
            else:
                self.screen.fill("Black")
                font = pygame.font.Font('font/Pixeltype.ttf', 50)
                end_surface = font.render("YOU LOSE - Press Enter", False, "Red")
                end_rect = end_surface.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
                self.screen.blit(end_surface, end_rect)

                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    self.obstacles.empty()
                    self.player.sprite.rect.midbottom = (80, self.GROUND_LEVEL)
                    self.game_active = True
                    self.start_time = pygame.time.get_ticks()

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Main()
    game.run()
