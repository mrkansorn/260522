"""
Particle system for visual effects.
Handles explosions, hit effects, and thrust particles.
"""

import math
import random
from typing import List, Tuple
from dataclasses import dataclass

from core.config import Config


@dataclass
class Particle:
    """Individual particle with position, velocity, and lifetime."""
    x: float
    y: float
    vx: float
    vy: float
    lifetime: float
    max_lifetime: float
    size: float
    color: Tuple[int, int, int]
    
    def update(self, dt: float):
        """Update particle position and lifetime."""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.lifetime -= dt
        
        # Apply drag
        self.vx *= Config.PARTICLE_DECAY
        self.vy *= Config.PARTICLE_DECAY
    
    def is_alive(self) -> bool:
        """Check if particle should still be rendered."""
        return self.lifetime > 0
    
    def get_alpha(self) -> float:
        """Get particle transparency based on lifetime."""
        return self.lifetime / self.max_lifetime


class ParticleSystem:
    """
    Manages all particle effects.
    Provides explosion, hit, and other visual effects.
    """

    def __init__(self):
        self.particles: List[Particle] = []

    def clear(self):
        """Remove all particles."""
        self.particles.clear()

    def create_explosion(self, x: float, y: float, size: float):
        """
        Create explosion effect.
        
        Args:
            x, y: Center position of explosion
            size: Size of explosion (affects particle count and spread)
        """
        count = Config.PARTICLE_COUNT_EXPLOSION
        
        for _ in range(count):
            # Random direction
            angle = random.uniform(0, 2 * math.pi)
            
            # Speed based on explosion size
            speed = random.uniform(50, 150) * (size / 40)
            
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            # Varying particle sizes
            particle_size = random.uniform(2, 5) * (size / 40)
            
            particle = Particle(
                x=x,
                y=y,
                vx=vx,
                vy=vy,
                lifetime=Config.PARTICLE_LIFETIME,
                max_lifetime=Config.PARTICLE_LIFETIME,
                size=particle_size,
                color=Config.COLOR_PARTICLE
            )
            
            self.particles.append(particle)

    def create_hit_effect(self, x: float, y: float):
        """
        Create small hit spark effect.
        
        Args:
            x, y: Position of hit
        """
        count = Config.PARTICLE_COUNT_HIT
        
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(30, 80)
            
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            particle = Particle(
                x=x,
                y=y,
                vx=vx,
                vy=vy,
                lifetime=Config.PARTICLE_LIFETIME * 0.5,
                max_lifetime=Config.PARTICLE_LIFETIME * 0.5,
                size=random.uniform(1, 3),
                color=(255, 255, 200)
            )
            
            self.particles.append(particle)

    def create_thrust_particle(self, x: float, y: float, angle: float):
        """
        Create engine thrust particle.
        
        Args:
            x, y: Position at back of ship
            angle: Ship angle (particles go opposite direction)
        """
        # Particles go opposite to thrust direction
        rad = math.radians(angle + 180)
        speed = random.uniform(20, 50)
        
        vx = math.cos(rad) * speed
        vy = math.sin(rad) * speed
        
        # Add some spread
        vx += random.uniform(-10, 10)
        vy += random.uniform(-10, 10)
        
        particle = Particle(
            x=x + random.uniform(-3, 3),
            y=y + random.uniform(-3, 3),
            vx=vx,
            vy=vy,
            lifetime=0.3,
            max_lifetime=0.3,
            size=random.uniform(2, 4),
            color=(255, 150, 50)
        )
        
        self.particles.append(particle)

    def update(self, dt: float):
        """Update all particles and remove dead ones."""
        for particle in self.particles:
            particle.update(dt)
        
        # Remove dead particles
        self.particles = [p for p in self.particles if p.is_alive()]

    def render(self, renderer):
        """Render all particles."""
        for particle in self.particles:
            alpha = particle.get_alpha()
            
            # Simple fade effect by reducing size
            current_size = particle.size * alpha
            
            if current_size > 0.5:
                renderer.draw_circle(
                    particle.x, particle.y, 
                    current_size, particle.color, width=0
                )

    def get_particle_count(self) -> int:
        """Get current number of active particles."""
        return len(self.particles)
