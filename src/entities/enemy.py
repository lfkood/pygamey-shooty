import pygame
from pygame.math import Vector2
import random
import settings
from src.entities.enemy_ai import *



class Enemy_1(pygame.sprite.Sprite):
    def __init__(self, screen_width, player, difficulty=settings.NORMAL, health = 1):
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
        self.health = difficulty_settings["enemy_health"] + health
        self.score_value = difficulty_settings["score_multiplier"]

        self.rect = self.image.get_rect(center=self.position)

        self.player = player  

        self.ai = BasicAI(self, player)
    
    def update(self, dt):
        if self.player:
            self.ai.update(dt)

        if self.position.y > 650:
            self.kill()

    def take_damage(self, damage=1):
        self.health -= damage
        return self.health <= 0




class Enemy_2(pygame.sprite.Sprite):
    def __init__(self, screen_width, player, difficulty=settings.NORMAL, health = 1):
        super().__init__()
        self.image = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (0, 0, 255), (30, 30, 50, 20))

        # Position at top of screen at random x coordinate
        self.position = pygame.math.Vector2(
            random.randint(30, screen_width - 30),
            -30
        )

        # Set difficulty-based attributes
        difficulty_settings = settings.DIFFICULTY_SETTINGS[difficulty]
        self.speed = difficulty_settings["enemy_speed"]
        self.health = difficulty_settings["enemy_health"] + health*1.5
        self.score_value = difficulty_settings["score_multiplier"]

        self.rect = self.image.get_rect(center=self.position)

        self.player = player  

        self.ai = Down_AI(self, player)
    
    def update(self, dt):
        if self.player:
            self.ai.update(dt)

        if self.position.y > 650:
            self.kill()

    def take_damage(self, damage=1):
        self.health -= damage
        return self.health <= 0