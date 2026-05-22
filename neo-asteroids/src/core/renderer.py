"""
Rendering system.
Handles all drawing operations with support for transformations.
"""

import pygame
import math
from typing import List, Tuple


class Renderer:
    """
    Centralized rendering system.
    Provides methods for drawing game entities with proper transformations.
    """

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

    def draw_polygon(self, points: List[Tuple[float, float]], 
                     color: Tuple[int, int, int], width: int = 2):
        """Draw a polygon shape."""
        if len(points) >= 3:
            pygame.draw.polygon(self.screen, color, points, width)

    def draw_circle(self, x: float, y: float, radius: float,
                    color: Tuple[int, int, int], width: int = 2):
        """Draw a circle."""
        pygame.draw.circle(self.screen, color, (int(x), int(y)), 
                          int(radius), width)

    def draw_line(self, start: Tuple[float, float], 
                  end: Tuple[float, float], 
                  color: Tuple[int, int, int], width: int = 2):
        """Draw a line between two points."""
        pygame.draw.line(self.screen, color, 
                        (int(start[0]), int(start[1])),
                        (int(end[0]), int(end[1])), width)

    def draw_text(self, text: str, x: int, y: int, 
                  color: Tuple[int, int, int], size: int = 24,
                  center: bool = False):
        """Draw text at specified position."""
        font = pygame.font.Font(None, size)
        surface = font.render(text, True, color)
        rect = surface.get_rect()
        
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        
        self.screen.blit(surface, rect)

    def draw_text_centered(self, text: str, y: int,
                           color: Tuple[int, int, int], size: int = 36):
        """Draw centered text."""
        font = pygame.font.Font(None, size)
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(self.screen_width // 2, y))
        self.screen.blit(surface, rect)

    def transform_points(self, vertices: List[Tuple[float, float]],
                         x: float, y: float, angle: float = 0) -> List[Tuple[float, float]]:
        """
        Transform vertex positions based on entity position and rotation.
        
        Args:
            vertices: Local vertex coordinates relative to entity center
            x: Entity world X position
            y: Entity world Y position
            angle: Entity rotation in degrees
        
        Returns:
            Transformed world coordinates
        """
        rad = math.radians(angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        
        transformed = []
        for vx, vy in vertices:
            # Rotate then translate
            rx = vx * cos_a - vy * sin_a
            ry = vx * sin_a + vy * cos_a
            transformed.append((x + rx, y + ry))
        
        return transformed

    def wrap_position(self, x: float, y: float) -> Tuple[float, float]:
        """Wrap position around screen edges."""
        x = x % self.screen_width
        y = y % self.screen_height
        return x, y

    def draw_wrapped_polygon(self, vertices: List[Tuple[float, float]],
                             x: float, y: float, angle: float,
                             color: Tuple[int, int, int], width: int = 2):
        """
        Draw a polygon that wraps around screen edges.
        This creates the classic asteroids wrap-around effect.
        """
        transformed = self.transform_points(vertices, x, y, angle)
        
        # Draw main shape
        self.draw_polygon(transformed, color, width)
        
        # Draw wrapped copies at screen edges
        wrap_positions = [
            (self.screen_width, 0),
            (-self.screen_width, 0),
            (0, self.screen_height),
            (0, -self.screen_height),
            (self.screen_width, self.screen_height),
            (self.screen_width, -self.screen_height),
            (-self.screen_width, self.screen_height),
            (-self.screen_width, -self.screen_height),
        ]
        
        for wx, wy in wrap_positions:
            wrapped = self.transform_points(vertices, x + wx, y + wy, angle)
            
            # Only draw if partially on screen
            if self._is_partially_on_screen(wrapped):
                self.draw_polygon(wrapped, color, width)

    def _is_partially_on_screen(self, points: List[Tuple[float, float]]) -> bool:
        """Check if any part of a polygon is visible on screen."""
        margin = 50
        for x, y in points:
            if (-margin <= x <= self.screen_width + margin and
                -margin <= y <= self.screen_height + margin):
                return True
        return False

    def clear(self, color: Tuple[int, int, int] = (0, 0, 0)):
        """Clear screen with specified color."""
        self.screen.fill(color)
