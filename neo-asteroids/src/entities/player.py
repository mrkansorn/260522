"""
Player entity - the user-controlled spaceship.
Handles movement, shooting, and player state.
"""

import math
from typing import List, Tuple

from entities.entity import Entity
from core.config import Config


class Player(Entity):
    """
    Player-controlled spaceship.
    Implements classic asteroids movement with inertia.
    """

    def __init__(self, x: float, y: float):
        super().__init__(x, y, "player")
        self.size = Config.PLAYER_SIZE
        self.color = Config.COLOR_PLAYER
        
        # Movement properties
        self.acceleration = Config.PLAYER_ACCELERATION
        self.max_speed = Config.PLAYER_MAX_SPEED
        self.friction = Config.PLAYER_FRICTION
        self.rotation_speed = Config.PLAYER_ROTATION_SPEED
        
        # Shooting
        self.shoot_cooldown = 0.0
        self.shoot_cooldown_max = Config.PLAYER_COOLDOWN
        
        # Dash ability
        self.dash_cooldown = 0.0
        self.dash_cooldown_max = Config.PLAYER_DASH_COOLDOWN
        self.is_dashing = False
        self.dash_timer = 0.0
        
        # Invincibility after respawn
        self.invincible_timer = Config.PLAYER_INVINCIBLE_TIME
        self.invincible = True
        
        # Generate ship shape (triangle)
        self._generate_vertices()

    def _generate_vertices(self):
        """Generate player ship vertices (pointing up by default)."""
        size = self.size
        # Triangle pointing up
        self.vertices = [
            (0, -size),      # Nose
            (-size * 0.7, size * 0.8),  # Back left
            (0, size * 0.5),  # Back center (indent)
            (size * 0.7, size * 0.8),   # Back right
        ]

    def update(self, dt: float, screen_width: int, screen_height: int, input_handler):
        """Update player based on input."""
        # Handle rotation
        rotation_dir = input_handler.get_rotation_direction()
        self.angular_velocity = rotation_dir * self.rotation_speed
        self.apply_rotation(dt)
        
        # Handle thrust
        thrust = input_handler.get_thrust()
        if thrust > 0:
            # Calculate acceleration in facing direction
            rad = math.radians(self.angle)
            ax = math.sin(rad) * self.acceleration * thrust
            ay = -math.cos(rad) * self.acceleration * thrust
            
            self.vx += ax * dt
            self.vy += ay * dt
            
            # Apply speed limit
            speed = math.sqrt(self.vx**2 + self.vy**2)
            if speed > self.max_speed:
                scale = self.max_speed / speed
                self.vx *= scale
                self.vy *= scale
        
        # Handle dash
        if input_handler.dash and self.dash_cooldown <= 0:
            self.start_dash()
        
        # Update dash state
        if self.is_dashing:
            self.dash_timer -= dt
            if self.dash_timer <= 0:
                self.is_dashing = False
        else:
            # Apply friction when not dashing
            self.vx *= self.friction
            self.vy *= self.friction
        
        # Update cooldowns
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt
        if self.dash_cooldown > 0:
            self.dash_cooldown -= dt
        
        # Update invincibility
        if self.invincible:
            self.invincible_timer -= dt
            if self.invincible_timer <= 0:
                self.invincible = False
        
        # Apply velocity
        self.apply_velocity(dt)
        
        # Wrap around screen
        self.wrap_position(screen_width, screen_height)

    def start_dash(self):
        """Initiate dash maneuver."""
        self.is_dashing = True
        self.dash_timer = Config.PLAYER_DASH_DURATION
        self.dash_cooldown = self.dash_cooldown_max
        
        # Boost in current direction
        dash_speed = Config.PLAYER_DASH_SPEED
        rad = math.radians(self.angle)
        self.vx = math.sin(rad) * dash_speed
        self.vy = -math.cos(rad) * dash_speed

    def can_shoot(self) -> bool:
        """Check if player can shoot."""
        return self.shoot_cooldown <= 0 and not self.is_dashing

    def shoot(self) -> bool:
        """Attempt to shoot. Returns True if shot was fired."""
        if self.can_shoot():
            self.shoot_cooldown = self.shoot_cooldown_max
            return True
        return False

    def take_damage(self, amount: int = 1):
        """Handle damage - only works when not invincible."""
        if not self.invincible:
            self.invincible = True
            self.invincible_timer = Config.PLAYER_INVINCIBLE_TIME
            # Knockback
            self.vx *= 0.5
            self.vy *= 0.5

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

    def render_flash(self) -> bool:
        """Check if player should flash (when invincible)."""
        return self.invincible and self.invincible_timer > 0.5
