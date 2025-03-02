import pygame
from pygame.math import Vector2
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, width):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))
        self.position = Vector2(random.randint(0, width), -30)
        self.rect = self.image.get_rect(center=self.position)
        self.speed = 200

    def update(self, dt):
        self.position.y += self.speed * dt
        self.rect.center = self.position
        if self.rect.top > 600:
            self.kill()