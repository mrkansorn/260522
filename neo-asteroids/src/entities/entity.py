"""
Entity system - base class and specific entity types.
All game objects inherit from Entity base class.
"""

import math
from typing import List, Tuple, Optional
from abc import ABC, abstractmethod


class Entity(ABC):
    """
    Base class for all game entities.
    Provides common properties and methods for position, rotation, and lifecycle.
    """

    def __init__(self, x: float, y: float, entity_type: str):
        self.x = x
        self.y = y
        self.entity_type = entity_type
        self.vx = 0.0  # Velocity X
        self.vy = 0.0  # Velocity Y
        self.angle = 0.0  # Rotation in degrees
        self.angular_velocity = 0.0  # Rotation speed
        self.alive = True
        self.size = 10  # Collision radius
        self.vertices: List[Tuple[float, float]] = []  # Shape vertices (local coords)
        self.color = (255, 255, 255)

    @abstractmethod
    def update(self, dt: float, screen_width: int, screen_height: int):
        """Update entity state."""
        pass

    @abstractmethod
    def get_vertices(self) -> List[Tuple[float, float]]:
        """Get world-space vertices for rendering."""
        pass

    def wrap_position(self, screen_width: int, screen_height: int):
        """Wrap position around screen edges (classic asteroids behavior)."""
        if self.x < -self.size:
            self.x = screen_width + self.size
        elif self.x > screen_width + self.size:
            self.x = -self.size
        
        if self.y < -self.size:
            self.y = screen_height + self.size
        elif self.y > screen_height + self.size:
            self.y = -self.size

    def apply_velocity(self, dt: float):
        """Apply velocity to position."""
        self.x += self.vx * dt
        self.y += self.vy * dt

    def apply_rotation(self, dt: float):
        """Apply angular velocity to rotation."""
        self.angle += self.angular_velocity * dt
        # Normalize angle to 0-360
        self.angle = self.angle % 360

    def destroy(self):
        """Mark entity for removal."""
        self.alive = False

    def get_collision_circle(self) -> Tuple[float, float, float]:
        """Get collision circle (x, y, radius)."""
        return self.x, self.y, self.size
