"""
HUD (Heads-Up Display) system.
Renders score, lives, level, and other game information.
"""

import pygame
from core.config import Config


class HUD:
    """
    Renders game information overlay.
    Displays score, lives, level, and status messages.
    """

    def __init__(self, config: Config):
        self.config = config
        self.font_large = None
        self.font_medium = None
        self.font_small = None
        self._init_fonts()

    def _init_fonts(self):
        """Initialize fonts for different text sizes."""
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)

    def render(self, screen: pygame.Surface, score: int, 
               lives: int, level: int):
        """Render main HUD elements."""
        # Score (top left)
        score_text = f"SCORE: {score}"
        score_surface = self.font_medium.render(score_text, True, Config.COLOR_UI)
        screen.blit(score_surface, (10, 10))
        
        # Lives (bottom left)
        self._render_lives(screen, lives)
        
        # Level (top right)
        level_text = f"LEVEL {level}"
        level_surface = self.font_medium.render(level_text, True, Config.COLOR_UI)
        level_rect = level_surface.get_rect(topright=(self.config.SCREEN_WIDTH - 10, 10))
        screen.blit(level_surface, level_rect)

    def _render_lives(self, screen: pygame.Surface, lives: int):
        """Render lives as ship icons."""
        x = 10
        y = self.config.SCREEN_HEIGHT - 40
        
        life_text = f"LIVES: {lives}"
        life_surface = self.font_medium.render(life_text, True, Config.COLOR_UI)
        screen.blit(life_surface, (x, y))

    def render_level_complete(self, screen: pygame.Surface, level: int):
        """Render level complete message."""
        text = f"LEVEL {level} COMPLETE!"
        surface = self.font_large.render(text, True, Config.COLOR_UI)
        rect = surface.get_rect(center=(
            self.config.SCREEN_WIDTH // 2,
            self.config.SCREEN_HEIGHT // 2
        ))
        screen.blit(surface, rect)

    def render_message(self, screen: pygame.Surface, message: str, 
                       y: int = None, size: int = 32):
        """Render a centered message."""
        if y is None:
            y = self.config.SCREEN_HEIGHT // 2
        
        font = pygame.font.Font(None, size)
        surface = font.render(message, True, Config.COLOR_UI)
        rect = surface.get_rect(center=(self.config.SCREEN_WIDTH // 2, y))
        screen.blit(surface, rect)
