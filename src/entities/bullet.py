import pygame
from pygame.math import Vector2

class BaseBullet(pygame.sprite.Sprite):
    """
    Abstract base class for all bullet types.
    """
    def __init__(self, position, rotation, speed, damage, offset_distance):
        super().__init__()
        self.rotation = float(rotation)
        self.position = Vector2(position)
        self.speed = speed
        self.damage = damage
        self.offset_distance = offset_distance
        self.velocity = Vector2(0, -1).rotate(-self.rotation + 90) * self.speed

    def delete(self):
        """
        Remove the bullet from its sprite group.
        """
        self.kill()

    def update(self, dt):
        """
        Update the bullet's position and check if it's offscreen.
        Override this if needed.
        """
        direction = Vector2(-1, 0).rotate(-self.rotation)
        offset = direction * self.offset_distance
        shifted_position = self.position - offset
        self.position += self.velocity * dt
        self.rect.center = shifted_position
        screen_height = pygame.display.get_surface().get_height()
        if self.rect.bottom < 0 or self.rect.top > screen_height:
            self.kill()


class Bullet_default(BaseBullet):
    """
    Default bullet class for the player's standard weapon.
    """
    def __init__(self, position, rotation, damage_mult):
        image = pygame.image.load("assets/bul.png").convert_alpha()
        image = pygame.transform.rotate(image, rotation - 90)
        image = pygame.transform.scale(image, (20, 20))
        damage = 1 * (damage_mult / 2)
        speed = 500
        offset_distance = 20

        super().__init__(position, rotation, speed, damage, offset_distance)
        self.image = image
        self.rect = self.image.get_rect(center=position)


class Bullet_sniper(BaseBullet):
    """
    Sniper bullet class for high-damage, fast projectiles.
    """
    def __init__(self, position, rotation, damage_mult):
        image = pygame.image.load("assets/bul.png").convert_alpha()
        image = pygame.transform.rotate(image, rotation - 90)
        image = pygame.transform.scale(image, (30, 30))
        damage = 5 * (damage_mult / 2)
        speed = 1200
        offset_distance = 30

        super().__init__(position, rotation, speed, damage, offset_distance)
        self.image = image
        self.rect = self.image.get_rect(center=position)


class Laser(BaseBullet):
    """
    Laser class for a continuous beam weapon.
    """
    def __init__(self, position, rotation, damage_mult):
        damage = 0.03 * damage_mult
        speed = 5000
        offset_distance = 520
        super().__init__(position, rotation, speed, damage, offset_distance)

        self.lifetime = 100
        self.image = pygame.Surface((3, 1000), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (0, 255, 255), self.image.get_rect())
        self.image = pygame.transform.rotate(self.image, self.rotation - 90)
        self.rect = self.image.get_rect(center=position)

    def delete(self):
        """
        Handle laser deletion (can be extended for visual effects).
        """
        pass  # No deletion logic yet

    def update(self, dt):
        """
        Override to exclude screen bounds check.
        """
        direction = Vector2(-1, 0).rotate(-self.rotation)
        offset = direction * self.offset_distance
        shifted_position = self.position - offset
        self.position += self.velocity * dt
        self.rect.center = shifted_position
