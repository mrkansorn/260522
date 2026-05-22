"""
Core game engine and state management.
Handles the main game loop, state transitions, and system coordination.
"""

import pygame
import sys
from typing import Optional, Dict, Any

from core.config import Config
from core.input import InputHandler
from core.renderer import Renderer
from systems.entity_manager import EntityManager
from systems.collision import CollisionSystem
from systems.particle import ParticleSystem
from ui.hud import HUD
from ui.menu import Menu


class GameState:
    """Enum-like class for game states."""
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    LEVEL_TRANSITION = "level_transition"


class Game:
    """
    Main game class implementing the core game loop.
    Uses a component-based architecture with entity-component-system pattern.
    """

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.config = Config()
        self.screen = pygame.display.set_mode(
            (self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Neo Asteroids")
        
        self.clock = pygame.time.Clock()
        self.state = GameState.MENU
        self.running = True
        
        # Core systems
        self.input_handler = InputHandler()
        self.renderer = Renderer(self.screen)
        self.entity_manager = EntityManager()
        self.collision_system = CollisionSystem()
        self.particle_system = ParticleSystem()
        
        # UI systems
        self.hud = HUD(self.config)
        self.menu = Menu(self.config)
        
        # Game data
        self.score = 0
        self.level = 1
        self.lives = 3
        self.high_score = self._load_high_score()
        
        # Delta time for frame-independent movement
        self.dt = 0.0

    def _load_high_score(self) -> int:
        """Load high score from file."""
        try:
            with open("highscore.txt", "r") as f:
                return int(f.read().strip())
        except (FileNotFoundError, ValueError):
            return 0

    def _save_high_score(self):
        """Save high score to file."""
        if self.score > self.high_score:
            with open("highscore.txt", "w") as f:
                f.write(str(self.score))

    def start_game(self):
        """Initialize a new game session."""
        self.score = 0
        self.level = 1
        self.lives = 3
        self.entity_manager.clear()
        self.particle_system.clear()
        self.entity_manager.spawn_player(self.config.SCREEN_WIDTH // 2, 
                                          self.config.SCREEN_HEIGHT // 2)
        self.entity_manager.spawn_asteroids(self.level)
        self.state = GameState.PLAYING

    def handle_events(self):
        """Process pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.PLAYING:
                        self.state = GameState.PAUSED
                    elif self.state == GameState.PAUSED:
                        self.state = GameState.PLAYING
                
                if self.state == GameState.MENU:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.start_game()
                
                elif self.state == GameState.GAME_OVER:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.state = GameState.MENU
                
                elif self.state == GameState.PLAYING:
                    if event.key == pygame.K_SPACE:
                        self.entity_manager.player_shoot()
            
            if event.type == pygame.USEREVENT + 1:  # Level complete
                self.handle_level_complete()

    def handle_level_complete(self):
        """Handle transition to next level."""
        self.level += 1
        self.entity_manager.spawn_asteroids(self.level)
        self.state = GameState.LEVEL_TRANSITION
        # Brief pause before resuming
        pygame.time.wait(1000)
        self.state = GameState.PLAYING

    def update(self):
        """Update all game systems."""
        if self.state != GameState.PLAYING:
            return
        
        self.dt = self.clock.get_time() / 1000.0  # Convert to seconds
        
        # Update input
        self.input_handler.update()
        
        # Update entities
        self.entity_manager.update(self.dt, self.input_handler, 
                                   self.config.SCREEN_WIDTH, 
                                   self.config.SCREEN_HEIGHT)
        
        # Update particles
        self.particle_system.update(self.dt)
        
        # Handle collisions
        collisions = self.collision_system.check_collisions(
            self.entity_manager.get_all_entities()
        )
        self.handle_collisions(collisions)
        
        # Check player status
        if not self.entity_manager.has_player():
            self.lives -= 1
            if self.lives <= 0:
                self.game_over()
            else:
                self.entity_manager.respawn_player()
        
        # Check level completion
        if self.entity_manager.asteroids_cleared():
            self.handle_level_complete()

    def handle_collisions(self, collisions: list):
        """Process collision results."""
        for collision in collisions:
            entity_a, entity_b = collision
            
            # Player hits asteroid
            if entity_a.entity_type == "player" and entity_b.entity_type == "asteroid":
                entity_a.take_damage(1)
                entity_b.destroy()
                self.particle_system.create_explosion(
                    entity_b.x, entity_b.y, entity_b.size
                )
                self.score += entity_b.get_score()
            
            elif entity_a.entity_type == "asteroid" and entity_b.entity_type == "player":
                entity_b.take_damage(1)
                entity_a.destroy()
                self.particle_system.create_explosion(
                    entity_a.x, entity_a.y, entity_a.size
                )
                self.score += entity_a.get_score()
            
            # Bullet hits asteroid
            elif entity_a.entity_type == "bullet" and entity_b.entity_type == "asteroid":
                entity_a.destroy()
                entity_b.hit()
                self.particle_system.create_hit_effect(
                    entity_b.x, entity_b.y
                )
                self.score += entity_b.get_score()
                
                # Split asteroid if large enough
                if entity_b.should_split():
                    self.entity_manager.split_asteroid(entity_b)
            
            elif entity_a.entity_type == "asteroid" and entity_b.entity_type == "bullet":
                entity_b.destroy()
                entity_a.hit()
                self.particle_system.create_hit_effect(
                    entity_a.x, entity_a.y
                )
                self.score += entity_a.get_score()
                
                if entity_a.should_split():
                    self.entity_manager.split_asteroid(entity_a)

    def render(self):
        """Render all game elements."""
        self.screen.fill((0, 0, 0))  # Clear screen
        
        if self.state == GameState.MENU:
            self.menu.render_main_menu(self.screen, self.high_score)
        
        elif self.state == GameState.PLAYING:
            # Render game world
            self.entity_manager.render(self.renderer)
            self.particle_system.render(self.renderer)
            
            # Render HUD
            self.hud.render(self.screen, self.score, self.lives, self.level)
        
        elif self.state == GameState.PAUSED:
            self.entity_manager.render(self.renderer)
            self.hud.render(self.screen, self.score, self.lives, self.level)
            self.menu.render_pause_menu(self.screen)
        
        elif self.state == GameState.GAME_OVER:
            self.menu.render_game_over(self.screen, self.score, self.high_score)
        
        elif self.state == GameState.LEVEL_TRANSITION:
            self.entity_manager.render(self.renderer)
            self.hud.render_level_complete(self.screen, self.level)
        
        pygame.display.flip()

    def game_over(self):
        """Handle game over state."""
        self._save_high_score()
        self.state = GameState.GAME_OVER

    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.config.FPS)
        
        pygame.quit()
        sys.exit()
