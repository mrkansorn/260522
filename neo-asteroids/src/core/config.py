"""
Game configuration constants.
Centralized settings for easy balancing and tuning.
"""


class Config:
    """Game configuration and constants."""
    
    # Screen settings
    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 768
    FPS = 60
    
    # Player settings
    PLAYER_SIZE = 15
    PLAYER_SPEED = 300  # pixels per second
    PLAYER_ROTATION_SPEED = 180  # degrees per second
    PLAYER_ACCELERATION = 400
    PLAYER_FRICTION = 0.98
    PLAYER_MAX_SPEED = 500
    PLAYER_INVINCIBLE_TIME = 2.0  # seconds after respawn
    PLAYER_COOLDOWN = 0.25  # seconds between shots
    PLAYER_DASH_COOLDOWN = 2.0
    PLAYER_DASH_DURATION = 0.3
    PLAYER_DASH_SPEED = 800
    
    # Bullet settings
    BULLET_SPEED = 600
    BULLET_LIFETIME = 1.5  # seconds
    BULLET_SIZE = 3
    
    # Asteroid settings
    ASTEROID_SPAWN_MARGIN = 50  # distance from screen edge
    ASTEROID_MIN_SPAWN_DISTANCE = 150  # from player
    
    # Asteroid sizes and speeds (large, medium, small)
    ASTEROID_SIZES = [40, 25, 12]
    ASTEROID_SPEEDS = [50, 80, 120]
    ASTEROID_HEALTH = [3, 2, 1]
    ASTEROID_SCORES = [20, 50, 100]
    ASTEROID_VERTICES = [8, 7, 6]  # vertices for polygon shape
    
    # Level settings
    ASTEROIDS_PER_LEVEL = 4  # base number, increases with level
    LEVEL_INCREMENT = 1  # additional asteroids per level
    
    # Particle settings
    PARTICLE_LIFETIME = 0.8
    PARTICLE_COUNT_EXPLOSION = 20
    PARTICLE_COUNT_HIT = 8
    PARTICLE_DECAY = 0.95
    
    # Colors (RGB)
    COLOR_BLACK = (0, 0, 0)
    COLOR_WHITE = (255, 255, 255)
    COLOR_PLAYER = (0, 255, 255)  # Cyan
    COLOR_BULLET = (255, 255, 0)  # Yellow
    COLOR_ASTEROID_LARGE = (200, 200, 200)
    COLOR_ASTEROID_MEDIUM = (180, 180, 180)
    COLOR_ASTEROID_SMALL = (150, 150, 150)
    COLOR_PARTICLE = (255, 200, 100)
    COLOR_UI = (255, 255, 255)
    COLOR_DANGER = (255, 50, 50)
