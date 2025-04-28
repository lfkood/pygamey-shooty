from src.entities.bullet import *
import pygame

class Weapon_default:
    def __init__(self) -> None:
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 500

    def shoot(self, position, rotation, fire_rate_mult, damage_mult):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay / fire_rate_mult:
            self.last_shot = current_time
            return Bullet_default(position, rotation, damage_mult)

class Weapon_laser:
    def __init__(self) -> None:
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 100

    def shoot(self, position, rotation, fire_rate_mult, damage_mult):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay / fire_rate_mult:
            self.last_shot = current_time
            return Laser(position, rotation, damage_mult)


class Weapon_sniper:
    def __init__(self) -> None:
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 1500 

    def shoot(self, position, rotation, fire_rate_mult, damage_mult):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay / fire_rate_mult:
            self.last_shot = current_time
            return Bullet_sniper(position, rotation, damage_mult)