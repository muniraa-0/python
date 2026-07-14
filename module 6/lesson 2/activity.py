import pygame

pygame.init()
window = pygame.display.set_mode((500, 500))
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pygame.draw.rect(window, (255, 0, 0), pygame.Rect(100, 100, 50, 50))
    pygame.display.flip()