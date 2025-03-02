import pygame
from pygame.math import Vector2

class Bullet(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=position)
        self.position = Vector2(position)
        self.speed = 500

    def update(self, dt):
        self.position.y -= self.speed * dt
        self.rect.center = self.position
        if self.rect.bottom < 0:
            self.kill()