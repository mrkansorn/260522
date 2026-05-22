"""
Entity Manager - manages all game entities.
Handles spawning, updating, and cleanup of entities.
"""

import math
import random
from typing import List, Optional

from entities.entity import Entity
from entities.player import Player
from entities.asteroid import Asteroid
from entities.bullet import Bullet
from core.config import Config


class EntityManager:
    """
    Centralized entity management system.
    Handles lifecycle of all game entities.
    """

    def __init__(self):
        self.entities: List[Entity] = []
        self.player: Optional[Player] = None

    def clear(self):
        """Remove all entities."""
        self.entities.clear()
        self.player = None

    def add_entity(self, entity: Entity):
        """Add entity to manager."""
        self.entities.append(entity)

    def remove_dead_entities(self):
        """Remove all entities marked as dead."""
        self.entities = [e for e in self.entities if e.alive]

    @property
    def asteroids(self) -> List[Asteroid]:
        """Get all asteroid entities."""
        return [e for e in self.entities if e.entity_type == "asteroid"]

    @property
    def bullets(self) -> List[Bullet]:
        """Get all bullet entities."""
        return [e for e in self.entities if e.entity_type == "bullet"]

    def spawn_player(self, x: float, y: float):
        """Spawn player at specified position."""
        self.player = Player(x, y)

    def respawn_player(self):
        """Respawn player at center of screen."""
        if self.player:
            self.player.x = Config.SCREEN_WIDTH // 2
            self.player.y = Config.SCREEN_HEIGHT // 2
            self.player.vx = 0
            self.player.vy = 0
            self.player.angle = 0
            self.player.invincible = True
            self.player.invincible_timer = Config.PLAYER_INVINCIBLE_TIME

    def has_player(self) -> bool:
        """Check if player exists and is alive."""
        return self.player is not None and self.player.alive

    def player_shoot(self):
        """Fire bullet from player position."""
        if self.player and self.player.shoot():
            # Spawn bullet at player nose position
            angle_rad = math.radians(self.player.angle)
            offset_x = math.sin(angle_rad) * (self.player.size + 5)
            offset_y = -math.cos(angle_rad) * (self.player.size + 5)
            
            bullet = Bullet(
                self.player.x + offset_x,
                self.player.y + offset_y,
                self.player.angle
            )
            self.add_entity(bullet)

    def spawn_asteroids(self, level: int):
        """
        Spawn asteroids for current level.
        Ensures asteroids don't spawn too close to player.
        """
        num_asteroids = Config.ASTEROIDS_PER_LEVEL + (level - 1) * Config.LEVEL_INCREMENT
        
        for _ in range(num_asteroids):
            self._spawn_single_asteroid()

    def _spawn_single_asteroid(self):
        """Spawn a single large asteroid at safe distance from player."""
        attempts = 0
        max_attempts = 20
        
        while attempts < max_attempts:
            # Random position with margin from edges
            x = random.uniform(
                Config.ASTEROID_SPAWN_MARGIN,
                Config.SCREEN_WIDTH - Config.ASTEROID_SPAWN_MARGIN
            )
            y = random.uniform(
                Config.ASTEROID_SPAWN_MARGIN,
                Config.SCREEN_HEIGHT - Config.ASTEROID_SPAWN_MARGIN
            )
            
            # Check distance from player
            if self.player:
                dist = math.sqrt((x - self.player.x)**2 + (y - self.player.y)**2)
                if dist >= Config.ASTEROID_MIN_SPAWN_DISTANCE:
                    asteroid = Asteroid(x, y, size_index=0)  # Large asteroid
                    self.add_entity(asteroid)
                    return
            
            attempts += 1
        
        # If can't find safe spot, spawn at edge
        edge = random.choice(['top', 'bottom', 'left', 'right'])
        if edge == 'top':
            x = random.uniform(0, Config.SCREEN_WIDTH)
            y = Config.ASTEROID_SPAWN_MARGIN
        elif edge == 'bottom':
            x = random.uniform(0, Config.SCREEN_WIDTH)
            y = Config.SCREEN_HEIGHT - Config.ASTEROID_SPAWN_MARGIN
        elif edge == 'left':
            x = Config.ASTEROID_SPAWN_MARGIN
            y = random.uniform(0, Config.SCREEN_HEIGHT)
        else:
            x = Config.SCREEN_WIDTH - Config.ASTEROID_SPAWN_MARGIN
            y = random.uniform(0, Config.SCREEN_HEIGHT)
        
        asteroid = Asteroid(x, y, size_index=0)
        self.add_entity(asteroid)

    def split_asteroid(self, asteroid: Asteroid):
        """Split asteroid into two smaller pieces."""
        if not asteroid.can_split():
            return
        
        split_data = asteroid.get_split_data()
        
        # Create two smaller asteroids with slightly different velocities
        for i in range(2):
            new_asteroid = Asteroid(
                split_data['x'],
                split_data['y'],
                split_data['size_index']
            )
            
            # Add some randomness to velocity
            angle_offset = random.uniform(-0.5, 0.5)
            rad = math.atan2(split_data['vy'], split_data['vx']) + angle_offset
            speed = split_data['vx']  # Use x velocity as base speed reference
            new_speed = math.sqrt(split_data['vx']**2 + split_data['vy']**2) * 1.1
            
            new_asteroid.vx = math.cos(rad) * new_speed
            new_asteroid.vy = math.sin(rad) * new_speed
            
            self.add_entity(new_asteroid)

    def update(self, dt: float, input_handler, screen_width: int, screen_height: int):
        """Update all entities."""
        # Update player
        if self.player:
            self.player.update(dt, screen_width, screen_height, input_handler)
        
        # Update other entities
        for entity in self.entities:
            entity.update(dt, screen_width, screen_height)
        
        # Cleanup dead entities
        self.remove_dead_entities()

    def get_all_entities(self) -> List[Entity]:
        """Get all active entities including player."""
        all_entities = list(self.entities)
        if self.player and self.player.alive:
            all_entities.append(self.player)
        return all_entities

    def render(self, renderer):
        """Render all entities."""
        # Render entities
        for entity in self.entities:
            self._render_entity(entity, renderer)
        
        # Render player
        if self.player and self.player.alive:
            self._render_player(renderer)

    def _render_entity(self, entity: Entity, renderer):
        """Render a single entity."""
        if entity.entity_type == "bullet":
            # Render bullet as circle
            renderer.draw_circle(
                entity.x, entity.y, entity.size,
                entity.color, width=0
            )
        else:
            # Render as polygon
            vertices = entity.get_vertices()
            renderer.draw_polygon(vertices, entity.color)

    def _render_player(self, renderer):
        """Render player with special handling for invincibility."""
        if self.player.render_flash():
            # Flash effect when invincible
            import time
            flash = int(time.time() * 10) % 2 == 0
            if flash:
                return  # Skip rendering this frame for flash effect
        
        vertices = self.player.get_vertices()
        renderer.draw_polygon(vertices, self.player.color)
        
        # Draw thrust flame when accelerating
        if hasattr(self, '_input_handler') and self._input_handler.get_thrust() > 0:
            self._render_thrust(renderer)

    def _render_thrust(self, renderer):
        """Render engine thrust effect."""
        if not self.player:
            return
        
        # Calculate thrust position (behind ship)
        rad = math.radians(self.player.angle)
        back_x = self.player.x + math.sin(rad) * self.player.size * 0.8
        back_y = self.player.y - math.cos(rad) * self.player.size * 0.8
        
        # Simple flame triangle
        flame_size = self.player.size * 0.6
        flame_vertices = [
            (back_x, back_y),
            (back_x - math.sin(rad) * flame_size, back_y + math.cos(rad) * flame_size),
            (back_x + math.sin(rad) * flame_size, back_y - math.cos(rad) * flame_size),
        ]
        
        renderer.draw_polygon(flame_vertices, (255, 100, 0))

    def asteroids_cleared(self) -> bool:
        """Check if all asteroids have been destroyed."""
        return len(self.asteroids) == 0
