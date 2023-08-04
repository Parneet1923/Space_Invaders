import pygame
from random import randint
from math import *
from PIL import Image
from pygame import mixer

# Initialise the game
pygame.init()

# Creating a screen
screen = pygame.display.set_mode((1080, 720))

# Background Image
# img = Image.open('realistic-galaxy-background/background.jpg')
# img.thumbnail((1260, 720))
# img.save('bgk.jpg')
background = pygame.image.load('bgk.jpg')

# Title and Icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Adding a player
ship = pygame.image.load('spaceship.png')
shipX = 510
shipY = 600
ship_xchange = 0
ship_ychange = 0

# Background Music
mixer.music.load('background.wav')
mixer.music.play(-1)


def player(x, y):
    screen.blit(ship, (x, y))


enemy_img = []
enemyX = []
enemyY = []
enemy_changeX = []
enemy_changeY = []
enemy_state = []
num_of_enemy = 6
enemy_count = 6

for i in range(num_of_enemy):
    enemy_img.append(pygame.image.load('enemy.png'))
    enemyX.append(randint(0, 1015))
    enemyY.append(randint(50, 250))
    enemy_changeX.append(2)
    enemy_changeY.append(40)
    enemy_state.append('visible')


def enemy(x, y, i):
    e = (screen.blit(enemy_img[i], (x[i], y[i])))


# bullet
bullet_img = pygame.image.load('bullet.png')
bulletX = 526
bulletY = 565
bullet_state = "ready"


def fire(x, y):
    global bullet_state
    bullet_state = "Fire"
    screen.blit(bullet_img, (x + 16, y - 35))


def is_collision(ex, ey, bx, by):
    if bullet_state != 'ready':
        distance = sqrt(pow(ex - bx, 2) + pow(ey - by, 2))
        if distance < 28:
            return True
        else:
            return False


# Level define
level = 1
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)


def level_disp(level, x, y):
    level_text = font.render(f'Level : {str(level)}', True, (255, 255, 255))
    screen.blit(level_text, (x, y))


def score_disp(score, x, y):
    score_text = font.render(f'Score : {str(score)}', True, (255, 255, 255))
    screen.blit(score_text, (x, y))


def ship_collision(ex, ey, sx, sy):
    distance = sqrt(pow(ex - sx, 2) + pow(ey - sy, 2))
    if distance < 28:
        return True
    else:
        return False


def game_over():
    text = font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(text, (450, 300))


# Game loop
running = True
gameover = False
while running:
    # Screen Color
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    # Quit Enabled
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Ship Movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                ship_xchange = -2
            if event.key == pygame.K_RIGHT:
                ship_xchange = 2
            # Fire Bullet
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    fire_sound = mixer.Sound('laser.wav')
                    fire_sound.play()
                    fire(shipX, bulletY)
                    bulletX = shipX
        if event.type == pygame.KEYUP:
            ship_xchange = 0
            ship_ychange = 0

    # Ship boundaries
    if shipX <= 0:
        shipX = 0
    if shipX >= 1016:
        shipX = 1016
    if shipY <= 0:
        shipY = 0
    if shipY >= 656:
        shipY = 656

    # Enemy Movements
    if not gameover:
        shipX += ship_xchange
        shipY += ship_ychange
        for i in range(num_of_enemy):
            enemy(enemyX, enemyY, i)
            if enemyX[i] >= 1016:
                enemy_changeX[i] = -2
                enemyY[i] += enemy_changeY[i]
            if enemyX[i] <= 0:
                enemy_changeX[i] = 2
                enemyY[i] += enemy_changeY[i]
            enemyX[i] += enemy_changeX[i]

            collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosion = mixer.Sound('explosion.wav')
                explosion.play()
                bulletY = 565
                bullet_state = "ready"
                enemyX[i] = 2500
                enemy_count -= 1
                score = str(int(score) + 10)

            if enemy_count == 0:
                enemy_count = 6
                level = str(int(level) + 1)
                for i in range(num_of_enemy):
                    enemyX[i] = randint(0, 1015)
                    enemyY[i] = randint(50, 250)

            ship_coll = ship_collision(enemyX[i], enemyY[i], shipX, shipY)
            if ship_coll:
                gameover = True

    # Bullet Movements
    if bullet_state == "Fire":
        fire(bulletX, bulletY)
        bulletY -= 3
    if bulletY <= 45:
        bullet_state = "ready"
        bulletY = 565

    if gameover:
        game_over()
        mixer.music.stop()

    # Function Calling
    player(shipX, shipY)
    level_disp(level, 10, 10)
    score_disp(score, 900, 10)
    pygame.display.update()
