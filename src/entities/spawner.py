"""
Enemy spawner module for Space Fighter game.

This module is responsible for spawning enemies based on the current difficulty level.
"""

class Spawner:
    """
    Enemy spawner class that manages enemy creation.
    
    Handles the spawning of different enemy types based on game difficulty and level.
    """
    enemies: map = {}  # Dictionary to store enemy types
