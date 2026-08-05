import math
import random
import pygame

screen_width = 800
screen_height = 500
player_start_x = 370
player_start_y = 380
enemy_start_y_min = 50
enemy_start_y_max = 150
enemy_speed_x = 4
enemy_speed_y = 40
bullet_speed_y = 10
collision_distance = 27

pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
bg = pygame.image.load("spaceship_bg.jpeg")
pygame.display.set_caption("Space Invader")

playerImg = pygame.image.load("rocket=removebg-preview (1).png")
playerX = player_start_x
playerY = player_start_y
playerX_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('ufo.png'))
    enemyX.append(random.randint(0, screen_width - 64))
    enemyY.append(random.randint(enemy_start_y_min, enemy_start_y_max))
    enemyX_change.append(enemy_speed_x)
    enemyY_change.append(enemy_speed_y)

bulletimg = pygame.Image.load('bullet.png')
bulletX = 0
bulletY = player_start_y
bulletx_change = 0
bullet_change = bullet_speed_y
bullet_state = "ready"

score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10
over_font = pygame.font.Font('freesansbold.ttf',64)