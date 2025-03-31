import pygame
from pygame.math import Vector2

class BasicAI():
    """Simple AI that follows the player."""
    def __init__(self, enemy, player):
        self.enemy = enemy
        self.player = player
    def update(self, dt):
        if self.player:
            direction = self.player.position - self.enemy.position
            if direction.length() > 0:
                direction = direction.normalize()

            self.enemy.position += direction * self.enemy.speed * dt
            self.enemy.rect.center = self.enemy.position


class PredictiveAI():
    """AI that predicts where the player is going and moves to that spot."""
    def __init__(self, enemy, player):
        self.enemy = enemy
        self.player = player
    def update(self, dt):
        if self.player:
            prediction_time = 0.5
            predicted_position = self.player.position + self.player.acceleration * prediction_time
            
            direction = predicted_position - self.enemy.position
            if direction.length() > 0:
                direction = direction.normalize()

            self.enemy.position += direction * self.enemy.speed * dt
            self.enemy.rect.center = self.enemy.position