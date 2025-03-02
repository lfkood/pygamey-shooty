# libraries
import pygame
import sys
import settings

# Initialize the window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(settings.SCREEN_SIZE)
pygame.display.set_caption("Hello, World!")
clock = pygame.time.Clock()
dt = 0

background = pygame.image.load("assets/bg.jpg").convert()
background = pygame.transform.scale(background, settings.SCREEN_SIZE)

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# Main loop
while True:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # RENDER YOUR GAME HERE
    screen.blit(background, (0, 0))

    pygame.draw.circle(screen, "red", player_pos, 40)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    pygame.display.update()

    # limits FPS to 60 dt
    dt = clock.tick(60) / 1000
