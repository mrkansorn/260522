"""
Collision detection system.
Implements circle-based collision for performance.
"""

import math
from typing import List, Tuple, Optional

from entities.entity import Entity


class CollisionSystem:
    """
    Handles collision detection between entities.
    Uses circle-circle collision for simplicity and performance.
    """

    def check_collisions(self, entities: List[Entity]) -> List[Tuple[Entity, Entity]]:
        """
        Check all possible collisions between entities.
        
        Args:
            entities: List of all active entities
        
        Returns:
            List of colliding entity pairs
        """
        collisions = []
        n = len(entities)
        
        # O(n²) check - acceptable for small entity counts
        for i in range(n):
            for j in range(i + 1, n):
                entity_a = entities[i]
                entity_b = entities[j]
                
                if self._entities_collide(entity_a, entity_b):
                    collisions.append((entity_a, entity_b))
        
        return collisions

    def _entities_collide(self, a: Entity, b: Entity) -> bool:
        """
        Check if two entities collide using circle collision.
        
        Tradeoff: Circle collision is less accurate than polygon collision
        but much faster and sufficient for this game's needs.
        """
        # Get collision circles
        ax, ay, aradius = a.get_collision_circle()
        bx, by, bradius = b.get_collision_circle()
        
        # Calculate distance between centers
        dx = bx - ax
        dy = by - ay
        distance = math.sqrt(dx * dx + dy * dy)
        
        # Check if circles overlap
        min_distance = aradius + bradius
        
        # Add slight tolerance for better feel
        return distance < min_distance * 0.9

    def _distance_squared(self, x1: float, y1: float, 
                          x2: float, y2: float) -> float:
        """Calculate squared distance (avoids sqrt for performance)."""
        dx = x2 - x1
        dy = y2 - y1
        return dx * dx + dy * dy

    def get_nearest_entity(self, x: float, y: float, 
                           entities: List[Entity], 
                           max_distance: float = float('inf')) -> Optional[Entity]:
        """
        Find nearest entity to a position.
        Useful for AI or targeting systems.
        """
        nearest = None
        nearest_dist_sq = max_distance * max_distance
        
        for entity in entities:
            dist_sq = self._distance_squared(x, y, entity.x, entity.y)
            if dist_sq < nearest_dist_sq:
                nearest_dist_sq = dist_sq
                nearest = entity
        
        return nearest
