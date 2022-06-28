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

# Setting up Fonts
font_game_over = pygame.font.SysFont("Arial", 60)
game_over = font_game_over.render("Game Over", True, YELLOW)

font_score = pygame.font.SysFont("Arial", 10)
score = font_score.render(f"Score: {SCORE}", True, BLACK)

font_victory = pygame.font.SysFont("Arial", 60)
victory = font_victory.render("Bien joué!", True, YELLOW)

font_honey_pot = pygame.font.SysFont("Arial", 30)
honey_pot = font_honey_pot.render("Vous avez collecté tous les pots de miel!", True, YELLOW)


DISPLAYSURF = pygame.display.set_mode((SCREEN_SIDE, SCREEN_SIDE))
pygame.display.set_caption("Game")


class Wasp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Mean_wasp.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(100, SCREEN_SIDE-100), random.randint(100, SCREEN_SIDE-100))


class Bee(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Cute_bee.png")
        self.rect = self.image.get_rect()
        self.rect.center = (400, 200)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        # Up and down movements
        if self.rect.top > 0:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -5)
        if self.rect.bottom < SCREEN_SIDE:
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, 5)

        # Side movements
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_SIDE:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)


class Honey(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Honey_pot.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, SCREEN_SIDE), random.randint(0, SCREEN_SIDE))


# Adding Sprites
B1 = Bee()
W1 = Wasp()
W2 = Wasp()
W3 = Wasp()
H1 = Honey()
H2 = Honey()
H3 = Honey()
H4 = Honey()
H5 = Honey()
H6 = Honey()
H7 = Honey()

# Putting sprites into Groups
enemies = pygame.sprite.Group()
enemies.add(W1)
enemies.add(W2)
enemies.add(W3)
honeys = pygame.sprite.Group()
honeys.add(H1)
honeys.add(H2)
honeys.add(H3)
honeys.add(H4)
honeys.add(H5)
honeys.add(H6)
honeys.add(H7)
all_sprites = pygame.sprite.Group()
all_sprites.add(B1)
all_sprites.add(W1)
all_sprites.add(W2)
all_sprites.add(W3)
all_sprites.add(H1)
all_sprites.add(H2)
all_sprites.add(H3)
all_sprites.add(H4)
all_sprites.add(H5)
all_sprites.add(H6)
all_sprites.add(H7)

# Adding new custom events
END_OF_GAME = pygame.USEREVENT + 1
pygame.time.set_timer(END_OF_GAME, 25000)

# Game Loop
while True:

    for event in pygame.event.get():
        if event.type == END_OF_GAME:
            pygame.quit()
            sys.exit()

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if pygame.sprite.spritecollideany(B1, honeys):
        pygame.sprite.spritecollideany(B1, honeys).kill()
        SCORE += 1


    # Moves and Re-draws all sprites
    DISPLAYSURF.fill(YELLOW)
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
    B1.move()

    # To be run if collision occurs between Bee and Wasp
    if pygame.sprite.spritecollideany(B1, enemies):
        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(game_over, (250, 360))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    if SCORE == 7:
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


