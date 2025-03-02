import pygame
from pygame.math import Vector2

class Player:
    def __init__(self, position):
        self.position = Vector2(position)
        self.speed = 300
        self.bullets = pygame.sprite.Group()
        self.last_shot = 0
        self.shoot_delay = 250
        self.lives = 3
        self.radius = 20
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.invulnerable_duration = 2000  # 2 seconds
        self.shoot_delay = 500  # Increased delay for auto-shooting
        self.score = 0  # Add score tracking

    def handle_movement(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.position.y = max(self.radius, self.position.y - self.speed * dt)
        if keys[pygame.K_s]:
            self.position.y = min(600 - self.radius, self.position.y + self.speed * dt)
        if keys[pygame.K_a]:
            self.position.x = max(self.radius, self.position.x - self.speed * dt)
        if keys[pygame.K_d]:
            self.position.x = min(800 - self.radius, self.position.x + self.speed * dt)

    def shoot(self, current_time):
        if current_time - self.last_shot >= self.shoot_delay:
            self.last_shot = current_time
            return True
        return False

    def get_hit(self, current_time):
        if not self.invulnerable:
            self.lives -= 1
            self.invulnerable = True
            self.invulnerable_timer = current_time

    def update(self, current_time):
        if self.invulnerable and current_time - self.invulnerable_timer >= self.invulnerable_duration:
            self.invulnerable = False