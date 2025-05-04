"""
Settings module for Space Fighter game.

This module contains all global settings and constants used throughout the game,
including screen dimensions, colors, game states, difficulty settings, and upgrade parameters.
"""
import platform
import ctypes

if platform.system() == "Windows":
    ctypes.windll.user32.SetProcessDPIAware()

# Screen settings
SCREEN_SIZE = (800, 600)
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Game settings
PLAYER_SPEED = 300
BULLET_SPEED = 500
ENEMY_SPEED = 200
MENU = 0
DIFF_SELECT = 1
PLAYING = 2
GAME_OVER = 3

# Difficulty settings
EASY = 0
NORMAL = 1
HARD = 2


LEVEL_UP_SCORE = 20  # Changed from 500 to 300

DIFFICULTY_SETTINGS = {
    EASY: {
        "spawn_delay": 1500,
        "enemy_speed": 150,
        "enemy_health": 0.5,
        "score_multiplier": 2  # Increased from 1
    },
    NORMAL: {
        "spawn_delay": 1000,
        "enemy_speed": 200,
        "enemy_health": 2,
        "score_multiplier": 3  # Increased from 2
    },
    HARD: {
        "spawn_delay": 600,
        "enemy_speed": 250,
        "enemy_health": 3,
        "score_multiplier": 4  # Increased from 3
    }
}


# Upgrade costs
UPGRADES = {
    "fire_rate": {"cost": 100, "levels": 4, "effect": 1},
    "speed": {"cost": 150, "levels": 3, "effect": 50}, 
    "health": {"cost": 200, "levels": 2, "effect": 1},
    "damage": {"cost": 150, "levels": 4, "effect": 1}
}