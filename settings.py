import ctypes
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
PLAYING = 1
GAME_OVER = 2