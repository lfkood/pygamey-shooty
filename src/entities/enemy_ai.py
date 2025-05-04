"""
Enemy AI module for Space Fighter game.

This module defines different AI behaviors for enemy entities,
controlling how they move and interact with the player.
"""
import pygame
from pygame.math import Vector2

class BasicAI():
    """
    Simple AI that follows the player.
    
    Moves the enemy directly toward the player's current position.
    """
    def __init__(self, enemy, player):
        """
        Initialize the basic AI controller.
        
        Args:
            enemy (Enemy): The enemy entity controlled by this AI.
            player (Player): Reference to the player object to track.
        """
        self.enemy = enemy
        self.player = player
        
    def update(self, dt):
        """
        Update enemy movement toward the player.
        
        Args:
            dt (float): Delta time in seconds since the last frame.
        """
        if self.player:
            direction = self.player.position - self.enemy.position
            if direction.length() > 0:
                direction = direction.normalize()

            self.enemy.position += direction * self.enemy.speed * dt
            self.enemy.rect.center = self.enemy.position


class Down_AI():
    """
    AI that moves the enemy straight down.
    
    Ignores the player's position and simply moves downward at a constant speed.
    """
    def __init__(self, enemy, player):
        """
        Initialize the downward movement AI controller.
        
        Args:
            enemy (Enemy): The enemy entity controlled by this AI.
            player (Player): Reference to the player object (not used for movement).
        """
        self.enemy = enemy
        self.player = player
        
    def update(self, dt):
        """
        Update enemy movement downward.
        
        Args:
            dt (float): Delta time in seconds since the last frame.
        """
        if self.player:
            self.enemy.position += Vector2(0, 1) * self.enemy.speed * dt
            self.enemy.rect.center = self.enemy.position



class PredictiveAI():
    """
    AI that predicts where the player is going and moves to that spot.
    
    Uses the player's current speed and position to predict future location.
    """
    def __init__(self, enemy, player):
        """
        Initialize the predictive AI controller.
        
        Args:
            enemy (Enemy): The enemy entity controlled by this AI.
            player (Player): Reference to the player object to track.
        """
        self.enemy = enemy
        self.player = player
        
    def update(self, dt):
        """
        Update enemy movement toward predicted player position.
        
        Args:
            dt (float): Delta time in seconds since the last frame.
        """
        if self.player:
            prediction_time = 0.5
            predicted_position = self.player.position + self.player.acceleration * prediction_time
            
            direction = predicted_position - self.enemy.position
            if direction.length() > 0:
                direction = direction.normalize()

            self.enemy.position += direction * self.enemy.speed * dt
            self.enemy.rect.center = self.enemy.position