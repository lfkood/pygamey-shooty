import pygame
from pygame.math import Vector2
from src.entities.bullet import Bullet
import settings

class Player:
    def __init__(self, position, rotation):
        self.position = Vector2(position)
        self.rotation = float(rotation)
        self.speed = Vector2(0, 0)
        self.acceleration = Vector2(60, 60)
        self.max_speed = 300
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
        self.center = Vector2(0,0)
        self.upgrades = {
            "fire_rate": 0,  # Levels of fire rate upgrade
            "speed": 0,  # Levels of speed upgrade
            "health": 0  # Levels of health upgrade
        }
        self.upgrade_points = 0


    def handle_movement(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.speed.y -= self.acceleration.y 
            # self.position.y = max(self.radius, self.position.y - self.speed.y * dt)
        if keys[pygame.K_s]:
            self.speed.y += self.acceleration.x 
            # self.position.y = min(600 - self.radius, self.position.y + self.speed.y * dt)
        if keys[pygame.K_a]:
            self.speed.x -= self.acceleration.x 
            # self.position.x = max(self.radius, self.position.x - self.speed.x * dt)
        if keys[pygame.K_d]:
            self.speed.x += self.acceleration.x 
            # self.position.x = min(800 - self.radius, self.position.x + self.speed.x * dt)
        new_pos = self.position + self.speed * dt
        self.position.x = new_pos.x if self.radius <= new_pos.x <= 800 - self.radius else self.position.x
        self.position.y = new_pos.y if self.radius <= new_pos.y <= 600 - self.radius else self.position.y
        self.speed *= 0.75


    
    def handle_rotation(self, position):
        mouse_pos = Vector2(pygame.mouse.get_pos())
        direction = mouse_pos - position
        self.rotation = direction.angle_to(Vector2(1, 0))

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay:
            new_bullet = Bullet(self.position, self.rotation)
            self.bullets.add(new_bullet)
            self.last_shot = current_time

    def get_hit(self, current_time):
        if not self.invulnerable:
            self.lives -= 1
            self.invulnerable = True
            self.invulnerable_timer = current_time

    def update(self, current_time, screen, player_model):
        if self.invulnerable and current_time - self.invulnerable_timer >= self.invulnerable_duration:
            self.invulnerable = False
        if not self.invulnerable or pygame.time.get_ticks() % 200 < 100:
            self.center = player_model.get_rect(topleft = self.position).center
            self.handle_rotation(self.center)
            rotated_player = pygame.transform.rotate(player_model, self.rotation - 90)
            new_rect = rotated_player.get_rect(center = self.center)
            screen.blit(rotated_player, new_rect)

    def apply_upgrade(self, upgrade_type):
        if upgrade_type in self.upgrades and self.upgrades[upgrade_type] < settings.UPGRADES[upgrade_type]["levels"]:
            cost = settings.UPGRADES[upgrade_type]["cost"]
            if self.upgrade_points >= cost:
                self.upgrades[upgrade_type] += 1
                self.upgrade_points -= cost

                # Apply upgrade effects
                if upgrade_type == "fire_rate":
                    self.shoot_delay = max(100, self.shoot_delay - settings.UPGRADES[upgrade_type]["effect"])
                elif upgrade_type == "speed":
                    self.max_speed += settings.UPGRADES[upgrade_type]["effect"]
                elif upgrade_type == "health":
                    self.lives += settings.UPGRADES[upgrade_type]["effect"]

                return True
        return False