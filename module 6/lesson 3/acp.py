import pygame
import sys


pygame.init()


WIDTH = 800
HEIGHT = 600


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Add Sprites")


WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)


player = pygame.Rect(100, 100, 60, 60)


block = pygame.Rect(500, 250, 80, 80)


speed = 5

clock = pygame.time.Clock()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.x -= speed
    if keys[pygame.K_RIGHT]:
        player.x += speed
    if keys[pygame.K_UP]:
        player.y -= speed
    if keys[pygame.K_DOWN]:
        player.y += speed

    
    screen.fill(WHITE)

    
    pygame.draw.rect(screen, BLUE, player)
    pygame.draw.rect(screen, RED, block)

    
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()