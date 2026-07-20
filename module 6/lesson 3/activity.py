import pygame
import random

pygame.init()

sprite_color_change_event = pygame.USEREVENT +1
background_color_change_event = pygame.USEREVENT +2

yellow = pygame.Color('yellow')
magenta = pygame.Color('magenta')
orange = pygame.Color('orange')
white = pygame.Color('white')

class Sprite(pygame.sprite)