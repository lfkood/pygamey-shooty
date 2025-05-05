import random

"""
Weapons module for Space Fighter game.

This module defines different weapon types that can be used by the player,
each with unique firing characteristics and bullet types.
"""
from src.entities.bullet import *
import pygame
from abc import ABC, abstractmethod


class BaseWeapon(ABC):
    """
    Abstract base class for all weapons.
    """

    def __init__(self, shoot_delay: int) -> None:
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = shoot_delay

    @abstractmethod
    def shoot(self, position, rotation, fire_rate_mult, damage_mult):
        """
        Attempt to fire a bullet if enough time has passed.
        Must be implemented by subclasses.
        """
        pass


class Weapon_default(BaseWeapon):
    """
    Default weapon class with balanced fire rate and damage.
    """
    def __init__(self) -> None:
        super().__init__(shoot_delay=500)

    def shoot(self, position, rotation, fire_rate_mult, damage_mult):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay / fire_rate_mult:
            self.last_shot = current_time
            return Bullet_default(position, rotation, damage_mult)


class Weapon_laser(BaseWeapon):
    """
    Laser weapon class with high fire rate but low damage.
    """
    def __init__(self) -> None:
        super().__init__(shoot_delay=100)

    def shoot(self, position, rotation, fire_rate_mult, damage_mult):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay / fire_rate_mult:
            self.last_shot = current_time
            return Laser(position, rotation, damage_mult)


class Weapon_sniper(BaseWeapon):
    """
    Sniper weapon class with high damage but slow fire rate.
    """
    def __init__(self) -> None:
        super().__init__(shoot_delay=1500)

    def shoot(self, position, rotation, fire_rate_mult, damage_mult):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay / fire_rate_mult:
            self.last_shot = current_time
            return Bullet_sniper(position, rotation, damage_mult)


class Weapon_shotgun(BaseWeapon):
    """
    Sniper weapon class with high damage but slow fire rate.
    """
    def __init__(self) -> None:
        super().__init__(shoot_delay=800)

    def shoot(self, position, rotation, fire_rate_mult, damage_mult):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay / fire_rate_mult:
            self.last_shot = current_time
            return [Bullet_shotgun(position + Vector2((random.random()-0.5)*7, 0), rotation + (random.random()-0.5)*7, damage_mult) for _ in range(7)]
