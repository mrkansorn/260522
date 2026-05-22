"""
Bullet entity - player projectiles.
Simple high-speed projectiles with limited lifetime.
"""

import math
from typing import List, Tuple

from entities.entity import Entity
from core.config import Config


class Bullet(Entity):
    """
    Player-fired projectile.
    Travels in a straight line and expires after short duration.
    """

    def __init__(self, x: float, y: float, angle: float):
        """
        Initialize bullet at player position, fired in player's facing direction.
        
        Args:
            x, y: Starting position (player position)
            angle: Firing angle in degrees
        """
        super().__init__(x, y, "bullet")
        self.size = Config.BULLET_SIZE
        self.color = Config.COLOR_BULLET
        self.lifetime = Config.BULLET_LIFETIME
        
        # Calculate velocity based on firing angle
        rad = math.radians(angle)
        self.vx = math.sin(rad) * Config.BULLET_SPEED
        self.vy = -math.cos(rad) * Config.BULLET_SPEED
        
        # Simple circular shape
        self.vertices = [
            (self.size, 0),
            (-self.size, 0),
        ]

    def update(self, dt: float, screen_width: int, screen_height: int):
        """Update bullet position and lifetime."""
        self.apply_velocity(dt)
        self.wrap_position(screen_width, screen_height)
        
        # Decrease lifetime
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.destroy()

    def get_vertices(self) -> List[Tuple[float, float]]:
        """Get transformed vertices for rendering."""
        # Bullets don't rotate, just translate
        return [(self.x + vx, self.y + vy) for vx, vy in self.vertices]

    def render_as_circle(self) -> bool:
        """Bullets render as small circles."""
        return True
