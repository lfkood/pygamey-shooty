import pygame
from pygame.math import Vector2

class Bullet_default(pygame.sprite.Sprite):
    def __init__(self, position, rotation, damage_mult):
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
        self.kill()

    def update(self, dt):
        direction = Vector2(-1, 0).rotate(-self.rotation)
        offset = direction * self.offset_distance
        shifted_position = self.position - offset
        self.position += self.velocity * dt
        self.rect.center = shifted_position
        if self.rect.bottom < 0 or self.rect.top > pygame.display.get_surface().get_height():
            self.kill()


class Laser(pygame.sprite.Sprite):
    def __init__(self, position, rotation, damage_mult):
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
        pass

    def update(self, dt):
        direction = Vector2(-1, 0).rotate(-self.rotation)
        offset = direction * self.offset_distance
        shifted_position = self.position - offset
        self.position += self.velocity * dt
        self.rect.center = shifted_position
        #if self.rect.bottom < 0 or self.rect.top > pygame.display.get_surface().get_height():
        #    self.kill()



class Bullet_sniper(pygame.sprite.Sprite):
    def __init__(self, position, rotation, damage_mult):
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
        self.kill()

    def update(self, dt):
        direction = Vector2(-1, 0).rotate(-self.rotation)
        offset = direction * self.offset_distance
        shifted_position = self.position - offset
        self.position += self.velocity * dt
        self.rect.center = shifted_position
        if self.rect.bottom < 0 or self.rect.top > pygame.display.get_surface().get_height():
            self.kill()