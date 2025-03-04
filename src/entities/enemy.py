import pygame
from pygame.math import Vector2
import random
import settings

class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen_width, difficulty=settings.NORMAL):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, settings.RED, (15, 15), 15)

        # Position at top of screen at random x coordinate
        self.position = pygame.math.Vector2(
            random.randint(30, screen_width - 30),
            -30
        )

        # Set difficulty-based attributes
        difficulty_settings = settings.DIFFICULTY_SETTINGS[difficulty]
        self.speed = difficulty_settings["enemy_speed"]
        self.health = difficulty_settings["enemy_health"]
        self.score_value = difficulty_settings["score_multiplier"]

        self.rect = self.image.get_rect(center=self.position)

    def update(self, dt):
        # Move down
        self.position.y += self.speed * dt
        self.rect.center = self.position

        # Remove if offscreen
        if self.position.y > 650:
            self.kill()

    def take_damage(self, damage=1):
        self.health -= damage
        return self.health <= 0