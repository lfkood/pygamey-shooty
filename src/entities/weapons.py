"""
Weapons module for Space Fighter game.

This module defines different weapon types that can be used by the player,
each with unique firing characteristics and bullet types.
"""
from src.entities.bullet import *
import pygame

class Weapon_default:
    """
    Default weapon class with balanced fire rate and damage.
    
    The standard weapon available to the player that fires basic bullets.
    """
    def __init__(self) -> None:
        """
        Initialize default weapon with standard firing parameters.
        """
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 500

    def shoot(self, position, rotation, fire_rate_mult, damage_mult):
        """
        Create a new bullet if cooldown period has passed.
        
        Args:
            position (Vector2): Position to spawn the bullet.
            rotation (float): Rotation angle in degrees for the bullet.
            fire_rate_mult (float): Fire rate multiplier from player upgrades.
            damage_mult (float): Damage multiplier from player upgrades.
            
        Returns:
            Bullet_default: A new bullet object if cooldown passed, None otherwise.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay / fire_rate_mult:
            self.last_shot = current_time
            return Bullet_default(position, rotation, damage_mult)

class Weapon_laser:
    """
    Laser weapon class with high fire rate but low damage.
    
    A rapid-fire weapon that shoots continuous laser beams.
    """
    def __init__(self) -> None:
        """
        Initialize laser weapon with high-frequency firing parameters.
        """
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 100

    def shoot(self, position, rotation, fire_rate_mult, damage_mult):
        """
        Create a new laser beam if cooldown period has passed.
        
        Args:
            position (Vector2): Position to spawn the laser.
            rotation (float): Rotation angle in degrees for the laser.
            fire_rate_mult (float): Fire rate multiplier from player upgrades.
            damage_mult (float): Damage multiplier from player upgrades.
            
        Returns:
            Laser: A new laser object if cooldown passed, None otherwise.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay / fire_rate_mult:
            self.last_shot = current_time
            return Laser(position, rotation, damage_mult)


class Weapon_sniper:
    """
    Sniper weapon class with high damage but slow fire rate.
    
    A precision weapon that fires powerful but slow bullets.
    """
    def __init__(self) -> None:
        """
        Initialize sniper weapon with high-damage, slow-firing parameters.
        """
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 1500 

    def shoot(self, position, rotation, fire_rate_mult, damage_mult):
        """
        Create a new sniper bullet if cooldown period has passed.
        
        Args:
            position (Vector2): Position to spawn the bullet.
            rotation (float): Rotation angle in degrees for the bullet.
            fire_rate_mult (float): Fire rate multiplier from player upgrades.
            damage_mult (float): Damage multiplier from player upgrades.
            
        Returns:
            Bullet_sniper: A new sniper bullet if cooldown passed, None otherwise.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay / fire_rate_mult:
            self.last_shot = current_time
            return Bullet_sniper(position, rotation, damage_mult)