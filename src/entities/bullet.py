"""
Bullet module for Space Fighter game.

This module defines different types of bullets/projectiles that can be fired by the player.
"""
import pygame
from pygame.math import Vector2

class Bullet_default(pygame.sprite.Sprite):
    """
    Default bullet class for the player's standard weapon.
    
    A simple projectile with moderate damage and speed.
    """
    def __init__(self, position, rotation, damage_mult):
        """
        Initialize a default bullet object.
        
        Args:
            position (tuple): Initial position (x, y) of the bullet.
            rotation (float): Rotation angle in degrees for the bullet's trajectory.
            damage_mult (float): Multiplier for the bullet's base damage.
        """
        super().__init__()

        self.damage = 1 * (damage_mult/2)
        self.rotation = float(rotation)
        self.image = pygame.image.load("assets/bul.png").convert_alpha()
        self.position = Vector2(position)
        self.speed = 500
        
        self.image = pygame.transform.rotate(self.image, self.rotation-90)
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.velocity = Vector2(0, -1).rotate(-self.rotation+90) * self.speed

        self.rect = self.image.get_rect(center=position)
        self.offset_distance = 20

    def delete(self):
        """
        Remove the bullet from its sprite group.
        """
        self.kill()

    def update(self, dt):
        """
        Update the bullet's position and check if it's offscreen.
        
        Args:
            dt (float): Delta time in seconds since the last frame.
        """
        direction = Vector2(-1, 0).rotate(-self.rotation)
        offset = direction * self.offset_distance
        shifted_position = self.position - offset
        self.position += self.velocity * dt
        self.rect.center = shifted_position
        if self.rect.bottom < 0 or self.rect.top > pygame.display.get_surface().get_height():
            self.kill()


class Laser(pygame.sprite.Sprite):
    """
    Laser class for a continuous beam weapon.
    
    A fast, beam-like projectile with constant low damage.
    """
    def __init__(self, position, rotation, damage_mult):
        """
        Initialize a laser beam object.
        
        Args:
            position (tuple): Initial position (x, y) of the laser.
            rotation (float): Rotation angle in degrees for the laser's trajectory.
            damage_mult (float): Multiplier for the laser's base damage.
        """
        super().__init__()
        self.damage = 0.1 * damage_mult

        self.rotation = float(rotation)
        self.lifetime = 100
        self.image = pygame.Surface((3, 1000), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (0, 255, 255), self.image.get_rect())

        self.image = pygame.transform.rotate(self.image, self.rotation - 90)

        self.rect = self.image.get_rect(center = position)
        self.position = Vector2(position)
        self.speed = 5000
        self.offset_distance = 520


        self.velocity = Vector2(0, -1).rotate(-self.rotation + 90) * self.speed
    
    def delete(self):
        """
        Handle laser deletion (placeholder method).
        """
        pass

    def update(self, dt):
        """
        Update the laser's position.
        
        Args:
            dt (float): Delta time in seconds since the last frame.
        """
        direction = Vector2(-1, 0).rotate(-self.rotation)
        offset = direction * self.offset_distance
        shifted_position = self.position - offset
        self.position += self.velocity * dt
        self.rect.center = shifted_position
        #if self.rect.bottom < 0 or self.rect.top > pygame.display.get_surface().get_height():
        #    self.kill()



class Bullet_sniper(pygame.sprite.Sprite):
    """
    Sniper bullet class for high-damage, fast projectiles.
    
    A powerful bullet with high damage and speed but slower fire rate.
    """
    def __init__(self, position, rotation, damage_mult):
        """
        Initialize a sniper bullet object.
        
        Args:
            position (tuple): Initial position (x, y) of the bullet.
            rotation (float): Rotation angle in degrees for the bullet's trajectory.
            damage_mult (float): Multiplier for the bullet's base damage.
        """
        super().__init__()

        self.damage = 5 * (damage_mult / 2)
        self.rotation = float(rotation)
        self.image = pygame.image.load("assets/bul.png").convert_alpha()
        self.position = Vector2(position)
        self.speed = 1200

        self.image = pygame.transform.rotate(self.image, self.rotation - 90)
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.velocity = Vector2(0, -1).rotate(-self.rotation + 90) * self.speed

        self.rect = self.image.get_rect(center=position)
        self.offset_distance = 30

    def delete(self):
        """
        Remove the bullet from its sprite group.
        """
        self.kill()

    def update(self, dt):
        """
        Update the bullet's position and check if it's offscreen.
        
        Args:
            dt (float): Delta time in seconds since the last frame.
        """
        direction = Vector2(-1, 0).rotate(-self.rotation)
        offset = direction * self.offset_distance
        shifted_position = self.position - offset
        self.position += self.velocity * dt
        self.rect.center = shifted_position
        if self.rect.bottom < 0 or self.rect.top > pygame.display.get_surface().get_height():
            self.kill()