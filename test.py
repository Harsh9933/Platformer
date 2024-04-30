import pygame
from sys import exit
from random import randint

def diplay_score():
    global simple_score
    current_time = pygame.time.get_ticks() - start_time
    simple_score = current_time//1000
    score_surface = test_font.render(f'Score:{simple_score}',False, "Black")
    score_rect = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface,score_rect)
    return simple_score


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen.blit(fly_surface, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []


def collisions(player, obstacles):
    if obstacles:
        for obstacles_rect in obstacles:
            if player.colliderect(obstacles_rect):
                return False
    return True


def player_animation():
    global player_move, player_index

    if player_rect.bottom < 300:
        player_move = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):player_index = 0
        player_move = player_walk[int(player_index)]


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_surface = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_surface_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_surface, player_surface_2]
        self.player_index = 1
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()


        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(200, 300))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20

    def appy_gravity(self):
        self.gravity += 1
        self.rect.bottom += self.gravity
        if self.rect.bottom >=300:
            self.rect.bottom = 300

    def animation(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.appy_gravity()
        self.animation()
pygame.init()
SCREEN_HEIGHT = 800
SCREEN_WIDTH = 400
screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
pygame.display.set_caption('Runner')

jump_sound = pygame.mixer.Sound('audio/jump.mp3')
back_sound = pygame.mixer.Sound('audio/music.wav')
back_sound.set_volume(0.1)
back_sound.play(loops=-1)

clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf',50)
re_font = pygame.font.Font('font/Pixeltype.ttf', 20)


sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# text_surface = test_font.render("PyGame",False , 'Black').convert_alpha()
# text_rect = text_surface.get_rect(center=(400,50))

snail_x_pos = 600
player_x_pos = 80

player_surface = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_surface_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_surface, player_surface_2]
player_index = 0
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

player_move = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom=(player_x_pos, 300))

# Obstacle
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png')
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png')
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]


fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png')
fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png')
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]
# snail_rect = snail_surface.get_rect(midbottom=(snail_x_pos, 300))

obstacle_rect_list = []

player_gravity = 0

# player = pygame.sprite.GroupSingle()
# player.add(Player())

game_active = True
start_time = 0
score = 0

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1400)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:

            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(snail_surface.get_rect(midbottom=(randint(900, 1100), 300)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(midbottom=(randint(900, 1100), 210)))

            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surface = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surface = fly_frames[fly_frame_index]

    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))

        # pygame.draw.rect(screen,'Pink',text_rect,border_radius=20)

        # pygame.draw.lines(screen, 'Gold', True, [(0, 0), pygame.mouse.get_pos()], 10)

        # screen.blit(text_surface,text_rect)
        # screen.blit(snail_surface, snail_rect)



        score = diplay_score()
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom > 300:
            player_rect.bottom = 300

        player_animation()
        screen.blit(player_move, player_rect)
        # player.draw(screen)
        # player.update()

        # snail_rect.left -= 6
        # if snail_rect.left < -100:
        #     snail_rect.left = 800

        # Obstacle movement

        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            if player_rect.bottom == 300:
                player_gravity = -20
                jump_sound.play()

        if pygame.mouse.get_pressed()[0] and player_rect.collidepoint(pygame.mouse.get_pos()):
            player_gravity = -20

        # collisions

        game_active = collisions(player_rect, obstacle_rect_list)

        # if player_rect.colliderect(obstacle_rect_list):
        #     game_active = False

        # player_rect.right += 3
        # if player_rect.left > 800:
        #     player_rect.left = -100
        # if player_rect.colliderect(snail_rect):
        #     print("Collision")
        #
        # mouse_pos = pygame.mouse.get_pos()
        # if player_rect.collidepoint(mouse_pos):
        #     print("Collision")
    else:
        screen.fill('Black')
        # red font
        end_surface = test_font.render("YOU LOOSE", False, 'Red')
        end_rect = end_surface.get_rect(center=(400, 200))
        screen.blit(end_surface,end_rect)

        # final score display

        score_surf = test_font.render(f'Score: {score}', False, 'Blue')
        score_rect = score_surf.get_rect(center=(400, 250))
        screen.blit(score_surf, score_rect)

        # timer
        start_time = pygame.time.get_ticks()

        # Play Again text
        re_surface = re_font.render("Play Again", False, 'White')
        re_rect = end_surface.get_rect(center=(450, 300))
        screen.blit(re_surface,re_rect)

        if pygame.mouse.get_pressed()[0] and re_rect.collidepoint(pygame.mouse.get_pos()):
            game_active = True
            obstacle_rect_list = []
            player_rect.midbottom = (80, 300)
            player_gravity = 0


    pygame.display.update()
    clock.tick(60)