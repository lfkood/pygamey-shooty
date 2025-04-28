import pygame
from pygame.math import Vector2
from src.entities.bullet import Bullet_default
import settings
import src.entities.weapons

class Player:
    def __init__(self, position, rotation):
        self.position = Vector2(position)
        self.rotation = float(rotation)
        self.speed = Vector2(0, 0)
        self.acceleration = Vector2(60, 60)
        self.max_speed = 300

        self.bullets = pygame.sprite.Group()
        self.weapon = src.entities.weapons.Weapon_default()
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
            "fire_rate": 1,  # Levels of fire rate upgrade
            "damage": 1,
            "speed": 0,  # Levels of speed upgrade
            "health": 0  # Levels of health upgrade
        }
        self.upgrade_points = 0


    def handle_movement(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.speed.y -= self.acceleration.y
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.speed.y += self.acceleration.y
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.speed.x -= self.acceleration.x
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.speed.x += self.acceleration.x

        new_pos = self.position + self.speed * dt
        self.position.x = new_pos.x if self.radius <= new_pos.x <= 800 - self.radius else self.position.x
        self.position.y = new_pos.y if self.radius <= new_pos.y <= 600 - self.radius else self.position.y
        self.speed *= 0.75


    
    def handle_rotation(self, position):
        mouse_pos = Vector2(pygame.mouse.get_pos())
        direction = mouse_pos - position
        self.rotation = direction.angle_to(Vector2(1, 0))

    def shoot(self):
        bullet = self.weapon.shoot(self.center, self.rotation, self.upgrades["fire_rate"], self.upgrades["damage"])
        if bullet:
            self.bullets.add(bullet)

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