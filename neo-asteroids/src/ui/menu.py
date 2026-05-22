"""
Menu system.
Handles main menu, pause menu, and game over screens.
"""

import pygame
from core.config import Config


class Menu:
    """
    Renders all menu screens.
    Provides UI for game states transitions.
    """

    def __init__(self, config: Config):
        self.config = config
        self.font_title = None
        self.font_large = None
        self.font_medium = None
        self.font_small = None
        self._init_fonts()

    def _init_fonts(self):
        """Initialize fonts for menu text."""
        self.font_title = pygame.font.Font(None, 72)
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 28)

    def render_main_menu(self, screen: pygame.Surface, high_score: int):
        """Render the main menu screen."""
        # Title
        title = "NEO ASTEROIDS"
        title_surface = self.font_title.render(title, True, Config.COLOR_PLAYER)
        title_rect = title_surface.get_rect(center=(
            self.config.SCREEN_WIDTH // 2,
            self.config.SCREEN_HEIGHT // 3
        ))
        screen.blit(title_surface, title_rect)
        
        # High score
        hs_text = f"HIGH SCORE: {high_score}"
        hs_surface = self.font_medium.render(hs_text, True, Config.COLOR_UI)
        hs_rect = hs_surface.get_rect(center=(
            self.config.SCREEN_WIDTH // 2,
            self.config.SCREEN_HEIGHT // 3 + 50
        ))
        screen.blit(hs_surface, hs_rect)
        
        # Instructions
        instructions = [
            "ARROWS / WASD - Move",
            "SPACE - Shoot",
            "SHIFT - Dash",
            "",
            "PRESS ENTER or SPACE TO START",
            "ESC - Pause"
        ]
        
        y_offset = self.config.SCREEN_HEIGHT // 2
        for line in instructions:
            if line:
                surface = self.font_small.render(line, True, Config.COLOR_UI)
                rect = surface.get_rect(center=(
                    self.config.SCREEN_WIDTH // 2,
                    y_offset
                ))
                screen.blit(surface, rect)
                y_offset += 30

    def render_pause_menu(self, screen: pygame.Surface):
        """Render pause overlay."""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = "PAUSED"
        pause_surface = self.font_title.render(pause_text, True, Config.COLOR_UI)
        pause_rect = pause_surface.get_rect(center=(
            self.config.SCREEN_WIDTH // 2,
            self.config.SCREEN_HEIGHT // 2 - 50
        ))
        screen.blit(pause_surface, pause_rect)
        
        # Resume instruction
        resume_text = "Press ESC to Resume"
        resume_surface = self.font_medium.render(resume_text, True, Config.COLOR_UI)
        resume_rect = resume_surface.get_rect(center=(
            self.config.SCREEN_WIDTH // 2,
            self.config.SCREEN_HEIGHT // 2 + 20
        ))
        screen.blit(resume_surface, resume_rect)

    def render_game_over(self, screen: pygame.Surface, score: int, high_score: int):
        """Render game over screen."""
        # Game Over text
        go_text = "GAME OVER"
        go_surface = self.font_title.render(go_text, True, Config.COLOR_DANGER)
        go_rect = go_surface.get_rect(center=(
            self.config.SCREEN_WIDTH // 2,
            self.config.SCREEN_HEIGHT // 3
        ))
        screen.blit(go_surface, go_rect)
        
        # Final score
        score_text = f"FINAL SCORE: {score}"
        score_surface = self.font_large.render(score_text, True, Config.COLOR_UI)
        score_rect = score_surface.get_rect(center=(
            self.config.SCREEN_WIDTH // 2,
            self.config.SCREEN_HEIGHT // 2
        ))
        screen.blit(score_surface, score_rect)
        
        # High score (if beaten)
        if score >= high_score and score > 0:
            hs_text = "NEW HIGH SCORE!"
            hs_surface = self.font_medium.render(hs_text, True, Config.COLOR_PLAYER)
            hs_rect = hs_surface.get_rect(center=(
                self.config.SCREEN_WIDTH // 2,
                self.config.SCREEN_HEIGHT // 2 + 50
            ))
            screen.blit(hs_surface, hs_rect)
        
        # Restart instruction
        restart_text = "Press ENTER or SPACE to Continue"
        restart_surface = self.font_small.render(restart_text, True, Config.COLOR_UI)
        restart_rect = restart_surface.get_rect(center=(
            self.config.SCREEN_WIDTH // 2,
            self.config.SCREEN_HEIGHT * 2 // 3
        ))
        screen.blit(restart_surface, restart_rect)

    def render_controls_help(self, screen: pygame.Surface):
        """Render controls help screen (optional feature)."""
        help_title = "CONTROLS"
        title_surface = self.font_large.render(help_title, True, Config.COLOR_UI)
        title_rect = title_surface.get_rect(center=(
            self.config.SCREEN_WIDTH // 2,
            self.config.SCREEN_HEIGHT // 4
        ))
        screen.blit(title_surface, title_rect)
        
        controls = [
            "LEFT/RIGHT or A/D - Rotate",
            "UP or W - Thrust",
            "SPACE - Fire",
            "SHIFT - Dash Boost",
            "",
            "Press ESC to Return"
        ]
        
        y_offset = self.config.SCREEN_HEIGHT // 2
        for line in controls:
            if line:
                surface = self.font_small.render(line, True, Config.COLOR_UI)
                rect = surface.get_rect(center=(
                    self.config.SCREEN_WIDTH // 2,
                    y_offset
                ))
                screen.blit(surface, rect)
                y_offset += 35
