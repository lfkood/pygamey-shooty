"""
Player module for Space Fighter game.

This module defines the Player class that represents the player-controlled character in the game.
"""
import pygame
from pygame.math import Vector2
import settings
import src.entities.weapons

class Player:
    """
    Player class representing the player-controlled character.
    
    Handles player movement, shooting, health, upgrades, and collision detection.
    """
    def __init__(self, position, rotation):
        """
        Initialize the player object.
        
        Args:
            position (tuple): Initial position (x, y) of the player.
            rotation (float): Initial rotation angle in degrees.
        """
        self.position = Vector2(position)
        self.rotation = float(rotation)
        self.speed = Vector2(0, 0)
        self.base_acceleration = 60
        self.acceleration = Vector2(self.base_acceleration, self.base_acceleration)

        self.bullets = pygame.sprite.Group()
        self.weapon = src.entities.weapons.Weapon_laser()
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
            "damage": 0,
            "speed": 0,  # Levels of speed upgrade
            "health": 0  # Levels of health upgrade
        }

    def handle_movement(self, dt):
        """
        Handle player movement based on keyboard input.
        
        Args:
            dt (float): Delta time in seconds since the last frame.
        """
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
        """
        Handle player rotation based on mouse position.
        
        Args:
            position (Vector2): Current player position.
        """
        mouse_pos = Vector2(pygame.mouse.get_pos())
        direction = mouse_pos - position
        self.rotation = direction.angle_to(Vector2(1, 0))

    def shoot(self):
        """
        Create a new bullet when the player shoots.
        
        Returns:
            bool: True if a bullet was fired, False otherwise.
        """
        bullet = self.weapon.shoot(self.center, self.rotation, self.upgrades["fire_rate"]+1, self.upgrades["damage"]+1)
        if bullet:
            self.bullets.add(bullet)

    def get_hit(self, current_time):
        """
        Handle player being hit by an enemy.
        
        Args:
            current_time (int): Current game time in milliseconds.
        """
        if not self.invulnerable:
            self.lives -= 1
            self.invulnerable = True
            self.invulnerable_timer = current_time

    def update(self, current_time, screen, player_model):
        """
        Update player's state and render the player on the screen.
        
        Args:
            current_time (int): Current game time in milliseconds.
            screen (pygame.Surface): Game screen to render the player on.
            player_model (pygame.Surface): Player sprite image.
        """
        if self.invulnerable and current_time - self.invulnerable_timer >= self.invulnerable_duration:
            self.invulnerable = False
        if not self.invulnerable or pygame.time.get_ticks() % 200 < 100:
            self.center = player_model.get_rect(topleft = self.position).center
            self.handle_rotation(self.center)
            rotated_player = pygame.transform.rotate(player_model, self.rotation - 90)
            new_rect = rotated_player.get_rect(center = self.center)
            screen.blit(rotated_player, new_rect)
        
        self.acceleration = Vector2(self.base_acceleration, self.base_acceleration)


def apply_upgrade(self, upgrade_type):
    """
    Apply an upgrade to the player based on the specified type.
    
    Args:
        upgrade_type (str): The type of upgrade to apply.
        
    Returns:
        bool: True if the upgrade was applied successfully, False otherwise.
    """
    # Handle weapon upgrades (they don't have levels)
    if upgrade_type.startswith("weapon_"):
        weapon_type = upgrade_type.split("_")[1]
        if weapon_type == "default":
            self.weapon = src.entities.weapons.Weapon_default()
        elif weapon_type == "laser":
            self.weapon = src.entities.weapons.Weapon_laser()
        elif weapon_type == "sniper":
            self.weapon = src.entities.weapons.Weapon_sniper()
        return True
    
    # Handle regular upgrades (check levels)
    if upgrade_type in self.upgrades and self.upgrades[upgrade_type] < settings.UPGRADES[upgrade_type]["levels"]:
        self.upgrades[upgrade_type] += 1

        # Apply upgrade effects
        if upgrade_type == "fire_rate":
            self.shoot_delay = max(100, self.shoot_delay - 50)
        elif upgrade_type == "speed":
            self.base_acceleration += 10
            self.acceleration = Vector2(self.base_acceleration, self.base_acceleration)
        elif upgrade_type == "health":
            self.lives += 1
        elif upgrade_type == "damage":
            pass 

        return True
    return False
