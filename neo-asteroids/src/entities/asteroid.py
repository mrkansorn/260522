"""
Asteroid entity - destructible space rocks.
Supports multiple sizes and splitting behavior.
"""

import math
import random
from typing import List, Tuple

from entities.entity import Entity
from core.config import Config


class Asteroid(Entity):
    """
    Destructible asteroid with multiple size variants.
    Splits into smaller asteroids when hit.
    """

    def __init__(self, x: float, y: float, size_index: int = 0):
        """
        Initialize asteroid.
        
        Args:
            x, y: Starting position
            size_index: 0=large, 1=medium, 2=small
        """
        super().__init__(x, y, "asteroid")
        
        # Size properties based on index
        self.size_index = size_index
        self.size = Config.ASTEROID_SIZES[size_index]
        self.speed = Config.ASTEROID_SPEEDS[size_index]
        self.health = Config.ASTEROID_HEALTH[size_index]
        self.max_health = self.health
        self.score_value = Config.ASTEROID_SCORES[size_index]
        self.num_vertices = Config.ASTEROID_VERTICES[size_index]
        
        # Set color based on size
        if size_index == 0:
            self.color = Config.COLOR_ASTEROID_LARGE
        elif size_index == 1:
            self.color = Config.COLOR_ASTEROID_MEDIUM
        else:
            self.color = Config.ASTEROID_SMALL if hasattr(Config, 'ASTEROID_SMALL') else Config.COLOR_ASTEROID_SMALL
        
        # Random rotation speed
        self.angular_velocity = random.uniform(-30, 30)
        
        # Random movement direction
        angle = random.uniform(0, 360)
        rad = math.radians(angle)
        self.vx = math.cos(rad) * self.speed
        self.vy = math.sin(rad) * self.speed
        
        # Generate irregular polygon shape
        self._generate_vertices()

    def _generate_vertices(self):
        """Generate irregular polygon vertices for natural look."""
        self.vertices = []
        for i in range(self.num_vertices):
            angle = (2 * math.pi * i) / self.num_vertices
            # Add some randomness to radius for irregular shape
            radius = self.size * random.uniform(0.8, 1.2)
            vx = math.cos(angle) * radius
            vy = math.sin(angle) * radius
            self.vertices.append((vx, vy))

    def update(self, dt: float, screen_width: int, screen_height: int):
        """Update asteroid position and rotation."""
        self.apply_rotation(dt)
        self.apply_velocity(dt)
        self.wrap_position(screen_width, screen_height)

    def hit(self):
        """Handle being hit by a bullet."""
        self.health -= 1
        if self.health <= 0:
            self.destroy()

    def should_split(self) -> bool:
        """Check if asteroid should split into smaller pieces."""
        return self.health <= 0 and self.size_index < 2

    def can_split(self) -> bool:
        """Check if asteroid is large enough to split."""
        return self.size_index < 2

    def get_score(self) -> int:
        """Get score value for destroying this asteroid."""
        return self.score_value

    def get_vertices(self) -> List[Tuple[float, float]]:
        """Get transformed vertices for rendering."""
        return self._transform_vertices()

    def _transform_vertices(self) -> List[Tuple[float, float]]:
        """Transform local vertices to world space."""
        rad = math.radians(self.angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        
        transformed = []
        for vx, vy in self.vertices:
            rx = vx * cos_a - vy * sin_a
            ry = vx * sin_a + vy * cos_a
            transformed.append((self.x + rx, self.y + ry))
        
        return transformed

    def get_split_data(self) -> dict:
        """Get data needed to spawn split asteroids."""
        return {
            'x': self.x,
            'y': self.y,
            'size_index': self.size_index + 1,
            'vx': self.vx,
            'vy': self.vy,
        }
