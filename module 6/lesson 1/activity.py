import pygame

pygame.init()

window = pygame.display.set_mode((400, 300))
pygame.display.set_caption("My first pygame window")

clock = pygame.time.Clock()
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pygame.display.flip()
    clock.tick(60)

pygame.quit()