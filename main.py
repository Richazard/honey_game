import pygame
import sys
import random
from pygame.locals import *
import time

# Initialization of the game
pygame.init()

# Choice of the FPS value
FPS = 60
FramePerSec = pygame.time.Clock()


# Setting up color for later use
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)


# Screen information
SCREEN_SIDE = 800
SCORE = 0
TIME = 20
NB_HONEY_POTS = 20
NB_WASPS = 3
SPEED = 5

# Setting up Fonts
font_end = pygame.font.SysFont("Arial", 60)
game_over = font_end.render("Game Over", True, YELLOW)
end_of_timer = font_end.render("Temps écoulé", True, YELLOW)
victory = font_end.render("Bien joué!", True, YELLOW)

font_honey_pot = pygame.font.SysFont("Arial", 30)
honey_pot = font_honey_pot.render("Vous avez collecté tous les pots de miel!", True, YELLOW)

font_score = pygame.font.SysFont("Arial", 20)

# Creating the window and its title
DISPLAYSURF = pygame.display.set_mode((SCREEN_SIDE, SCREEN_SIDE))
pygame.display.set_caption("Game")


class Wasp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Mean_wasp.png")
        self.rect = self.image.get_rect()
        self.up_down = random.randint(-SPEED, SPEED)
        self.right_left = random.randint(-SPEED, SPEED)
        self.rect.center = (random.randint(100, SCREEN_SIDE-100), random.randint(100, SCREEN_SIDE-100))

    def change_direction(self):
        self.up_down = random.randint(-SPEED, SPEED)
        self.right_left = random.randint(-SPEED, SPEED)

    def bounce(self):
        if self.rect.top < 0 or self.rect.bottom > SCREEN_SIDE:
            self.up_down *= -1

        if self.rect.left < 0 or self.rect.right > SCREEN_SIDE:
            self.right_left *= -1

    def move(self):
        self.rect.move_ip(self.right_left, self.up_down)


class Bee(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Cute_bee.png")
        self.rect = self.image.get_rect()
        self.rect.center = (400, 50)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        # Up and down movements
        if self.rect.top > 0:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, SPEED * -1)
        if self.rect.bottom < SCREEN_SIDE:
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, SPEED)

        # Side movements
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(SPEED * -1, 0)
        if self.rect.right < SCREEN_SIDE:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(SPEED, 0)


class Honey(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Honey_pot.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(50, SCREEN_SIDE), random.randint(100, SCREEN_SIDE))


# Adding Sprites
B1 = Bee()


# Putting sprites into Groups
enemies = pygame.sprite.Group()
for i in range(NB_WASPS):
    enemies.add(Wasp())

honeys = pygame.sprite.Group()
for i in range(NB_HONEY_POTS):
    honeys.add(Honey())

all_sprites = pygame.sprite.Group()
all_sprites.add(B1)

for elm in enemies:
    all_sprites.add(elm)

for elm in honeys:
    all_sprites.add(elm)


# Adding new custom events
END_OF_GAME = pygame.USEREVENT + 1
WASPS_MOVE = pygame.USEREVENT + 2

pygame.time.set_timer(END_OF_GAME, 1000)
pygame.time.set_timer(WASPS_MOVE, 500)



# Game Loop

while True:

    if TIME == 0:
        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(end_of_timer, (250, 360))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()
    for event in pygame.event.get():
        if event.type == END_OF_GAME:
            TIME -= 1

        if event.type == WASPS_MOVE:
            for entity in enemies:
                entity.change_direction()

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if pygame.sprite.spritecollideany(B1, honeys):
        SCORE += 1
        pygame.sprite.spritecollideany(B1, honeys).kill()

    # Moves and Re-draws all sprites
    DISPLAYSURF.fill(YELLOW)
    B1.move()
    for entity in enemies:
        entity.bounce()
        entity.move()
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)

    score = font_score.render(f"Score: {SCORE}", True, BLACK)
    time_left = font_score.render(f"Temps: {TIME}", True, BLACK)
    DISPLAYSURF.blit(score, (700, 30))
    DISPLAYSURF.blit(time_left, (10, 30))

    # To be run if collision occurs between Bee and Wasp
    if pygame.sprite.spritecollideany(B1, enemies):
        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(game_over, (250, 360))
        pygame.mixer.Sound('bzzzz.wav').play()
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    if honeys.__len__() == 0:
        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(victory, (250, 360))
        DISPLAYSURF.blit(honey_pot, (110, 460))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(3)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)


