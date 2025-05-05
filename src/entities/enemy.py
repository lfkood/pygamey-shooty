"""
Enemy module for Space Fighter game.

This module defines different enemy types that appear in the game with
different behaviors, health values, and scoring characteristics.
"""
import pygame
from pygame.math import Vector2
import random
import sys
import os

# Add the project root to the Python path to find the settings module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import settings
from src.entities.enemy_ai import *

# Initialize pygame font for damage indicators
pygame.font.init()
DAMAGE_FONT = pygame.font.SysFont('Arial', 14, bold=True)


class DamageIndicator(pygame.sprite.Sprite):
    """
    A floating text indicator showing damage dealt to enemies.
    
    This class creates a visual representation of damage that floats upward
    and fades out over time.
    """
    def __init__(self, position, damage, color=(255, 255, 150)):
        """
        Initialize a damage indicator.
        
        Args:
            position (Vector2): The position where the indicator should appear.
            damage (float): The amount of damage to display.
            color (tuple): RGB color for the damage text.
        """
        super().__init__()
        self.position = Vector2(position)
        self.damage = damage
        self.color = color
        self.alpha = 255  # Full opacity to start
        self.lifespan = 1.0  # Seconds to live
        self.lifetime = 0
        self.speed = Vector2(0, -50)  # Moving upward
        
        # Render the damage text
        self.update_image()
        self.rect = self.image.get_rect(center=self.position)
        
    def update_image(self):
        """Update the indicator's image with current alpha value."""
        text = DAMAGE_FONT.render(f"-{self.damage:.1f}", True, self.color)
        self.image = pygame.Surface(text.get_size(), pygame.SRCALPHA)
        self.image.blit(text, (0, 0))
        self.image.set_alpha(self.alpha)
        
    def update(self, dt):
        """
        Update the indicator's position and transparency.
        
        Args:
            dt (float): Delta time in seconds since the last frame.
        """
        self.lifetime += dt
        if self.lifetime >= self.lifespan:
            self.kill()
            return
            
        # Move upward
        self.position += self.speed * dt
        
        # Fade out
        self.alpha = max(0, 255 * (1 - self.lifetime / self.lifespan))
        self.update_image()
        
        # Update rect position
        self.rect.center = self.position


class Enemy_1(pygame.sprite.Sprite):
    """
    Basic enemy class with simple movement pattern.
    
    A small circular enemy that follows the player using basic AI.
    """
    # Class-level damage indicators group
    damage_indicators = pygame.sprite.Group()
    
    def __init__(self, screen_width, player, difficulty=settings.NORMAL, health = 1):
        """
        Initialize a basic enemy.
        
        Args:
            screen_width (int): Width of the game screen.
            player (Player): Reference to the player object.
            difficulty (int): Difficulty setting (EASY, NORMAL, HARD) affecting enemy stats.
            health (float): Base health modifier for the enemy.
        """
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, settings.RED, (15, 15), 15)

        # Position at top of screen at random x coordinate
        self.position = pygame.math.Vector2(
            random.randint(30, screen_width - 30),
            -30
        )

        # Set difficulty-based attributes
        difficulty_settings = settings.DIFFICULTY_SETTINGS[difficulty]
        self.speed = difficulty_settings["enemy_speed"]
        self.health = difficulty_settings["enemy_health"] + health
        self.max_health = self.health  # Store max health for health bar
        self.score_value = difficulty_settings["score_multiplier"]

        self.rect = self.image.get_rect(center=self.position)

        self.player = player  

        self.ai = BasicAI(self, player)
    
    def update(self, dt):
        """
        Update enemy position and behavior.
        
        Args:
            dt (float): Delta time in seconds since the last frame.
        """
        if self.player:
            self.ai.update(dt)

        if self.position.y > 650:
            self.kill()
    
    def draw_health_bar(self, screen):
        """
        Draw a health bar above the enemy.
        
        Args:
            screen: The pygame surface to draw on.
        """
        # Health bar size and position
        bar_width = self.rect.width + 10
        bar_height = 5
        bar_position = (self.rect.centerx - bar_width // 2, self.rect.top - 10)
        
        # Health percentage
        health_ratio = max(0, self.health / self.max_health)
        
        # Draw background/border
        pygame.draw.rect(screen, settings.BLACK, 
                        (bar_position[0], bar_position[1], bar_width, bar_height))
        
        # Draw actual health (only if enemy has been damaged)
        if health_ratio < 1.0:
            current_width = int(bar_width * health_ratio)
            pygame.draw.rect(screen, settings.HEALTH_BAR_RED,
                            (bar_position[0], bar_position[1], current_width, bar_height))

    def take_damage(self, damage=1):
        """
        Reduce enemy health when hit by player projectiles.
        
        Args:
            damage (float): Amount of damage to apply to the enemy.
            
        Returns:
            bool: True if the enemy's health reaches zero or below, False otherwise.
        """
        # Create damage indicator
        indicator = DamageIndicator(self.position, damage)
        Enemy_1.damage_indicators.add(indicator)
        
        self.health -= damage
        return self.health <= 0


class Enemy_2(pygame.sprite.Sprite):
    """
    Advanced enemy class with more health and different movement behavior.
    
    A larger rectangular enemy that moves straight down, has more health,
    and provides more score points.
    """
    # Use the same damage indicators group as Enemy_1
    damage_indicators = Enemy_1.damage_indicators
    
    def __init__(self, screen_width, player, difficulty=settings.NORMAL, health = 1):
        """
        Initialize an advanced enemy.
        
        Args:
            screen_width (int): Width of the game screen.
            player (Player): Reference to the player object.
            difficulty (int): Difficulty setting (EASY, NORMAL, HARD) affecting enemy stats.
            health (float): Base health modifier for the enemy.
        """
        super().__init__()
        self.image = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (0, 0, 255), (30, 30, 50, 20))

        # Position at top of screen at random x coordinate
        self.position = pygame.math.Vector2(
            random.randint(30, screen_width - 30),
            -30
        )

        # Set difficulty-based attributes
        difficulty_settings = settings.DIFFICULTY_SETTINGS[difficulty]
        self.speed = difficulty_settings["enemy_speed"]
        self.health = difficulty_settings["enemy_health"] + health*1.5
        self.max_health = self.health  # Store max health for health bar
        self.score_value = difficulty_settings["score_multiplier"]

        self.rect = self.image.get_rect(center=self.position)

        self.player = player  

        self.ai = Down_AI(self, player)
    
    def update(self, dt):
        """
        Update enemy position and behavior.
        
        Args:
            dt (float): Delta time in seconds since the last frame.
        """
        if self.player:
            self.ai.update(dt)

        if self.position.y > 650:
            self.kill()
            
    def draw_health_bar(self, screen):
        """
        Draw a health bar above the enemy.
        
        Args:
            screen: The pygame surface to draw on.
        """
        # Health bar size and position - wider for larger enemy
        bar_width = self.rect.width + 10
        bar_height = 6
        bar_position = (self.rect.centerx - bar_width // 2, self.rect.top - 12)
        
        # Health percentage
        health_ratio = max(0, self.health / self.max_health)
        
        # Draw background/border
        pygame.draw.rect(screen, settings.BLACK, 
                        (bar_position[0], bar_position[1], bar_width, bar_height))
        
        # Draw actual health
        if health_ratio < 1.0:
            current_width = int(bar_width * health_ratio)
            color = settings.HEALTH_BAR_RED
            # Add color gradient based on health (blue for Enemy_2)
            if health_ratio > 0.6:
                color = (60, 60, 220)  # Blue for high health
            pygame.draw.rect(screen, color,
                            (bar_position[0], bar_position[1], current_width, bar_height))

    def take_damage(self, damage=1):
        """
        Reduce enemy health when hit by player projectiles.
        
        Args:
            damage (float): Amount of damage to apply to the enemy.
            
        Returns:
            bool: True if the enemy's health reaches zero or below, False otherwise.
        """
        # Create damage indicator with a different color for Enemy_2
        indicator = DamageIndicator(self.position, damage, color=(100, 200, 255))
        Enemy_2.damage_indicators.add(indicator)
        
        self.health -= damage
        return self.health <= 0