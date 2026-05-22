# Neo Asteroids

A modern reimagining of the classic arcade game Asteroids, built with Python and Pygame.

## Game Concept

**Genre:** Space Shooter / Arcade  
**Inspiration:** Classic Asteroids (1979) with modern enhancements

### Gameplay Loop
1. Spawn in space surrounded by asteroids
2. Rotate and thrust to navigate
3. Shoot asteroids to break them into smaller pieces
4. Avoid collisions with asteroids
5. Clear all asteroids to advance to the next level
6. Survive as long as possible and achieve high score

### Player Mechanics
- **Rotation:** Left/Right arrows or A/D keys
- **Thrust:** Up arrow or W key (inertia-based movement)
- **Shoot:** Spacebar
- **Dash:** Shift key (quick boost with invincibility frames)

### Enemy Behavior
- Asteroids spawn at screen edges
- Move with constant velocity and rotation
- Split into 2 smaller asteroids when destroyed
- Large → Medium → Small → Destroyed

### Scoring System
- Large asteroid: 20 points
- Medium asteroid: 50 points
- Small asteroid: 100 points
- High score saved locally

### UI/HUD
- Score display (top left)
- Lives counter (bottom left)
- Level indicator (top right)
- Main menu with instructions
- Pause menu
- Game over screen

### Visual Effects
- Particle explosions when asteroids destroyed
- Hit spark effects
- Engine thrust particles
- Screen wrap-around for all entities
- Player invincibility flashing

## Architecture Overview

The game uses a hybrid **Entity-Component-System (ECS)** architecture:

```
┌─────────────────────────────────────────────────────────┐
│                      Game Loop                          │
│  (Event → Update → Render cycle managed by Game class)  │
└─────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│    Input      │  │   Entities    │  │  Systems      │
│   Handler     │  │   Manager     │  │  (Collision,  │
│               │  │               │  │   Particles)  │
└───────────────┘  └───────────────┘  └───────────────┘
        │                  │                  │
        ▼                  ▼                  ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│   Renderer    │  │    Player     │  │      UI       │
│               │  │  Asteroids    │  │   (HUD,Menu)  │
│               │  │    Bullets    │  │               │
└───────────────┘  └───────────────┘  └───────────────┘
```

### Key Design Decisions

1. **Circle-based collision:** Less accurate than polygon collision but much faster. Perfect for arcade gameplay feel.

2. **Screen wrap-around:** Classic asteroids behavior where entities exiting one edge appear on the opposite edge.

3. **Delta-time movement:** All movement is frame-rate independent using dt calculations.

4. **Entity pooling:** Simple list-based management with dead entity cleanup each frame.

## Folder Structure

```
neo-asteroids/
├── main.py                 # Entry point
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py       # Game constants and settings
│   │   ├── game.py         # Main game loop and state
│   │   ├── input.py        # Input handling system
│   │   └── renderer.py     # Rendering utilities
│   ├── entities/
│   │   ├── __init__.py
│   │   ├── entity.py       # Base entity class
│   │   ├── player.py       # Player spaceship
│   │   ├── asteroid.py     # Asteroid entities
│   │   └── bullet.py       # Projectile entities
│   ├── systems/
│   │   ├── __init__.py
│   │   ├── entity_manager.py  # Entity lifecycle management
│   │   ├── collision.py    # Collision detection
│   │   └── particle.py     # Particle effects system
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── hud.py          # In-game HUD
│   │   └── menu.py         # Menu screens
│   ├── audio/
│   │   └── __init__.py     # (Reserved for future audio)
│   └── utils/
│       └── __init__.py     # (Reserved for utilities)
└── assets/                 # (Reserved for future assets)
```

## How to Run

### Prerequisites
- Python 3.8+
- Pygame 2.0+

### Installation

```bash
# Install dependencies
pip install pygame

# Navigate to game directory
cd neo-asteroids

# Run the game
python main.py
```

### Controls

| Action | Key |
|--------|-----|
| Rotate Left | ← or A |
| Rotate Right | → or D |
| Thrust | ↑ or W |
| Shoot | Space |
| Dash | Shift |
| Pause | ESC |

## Core Systems

### Entity System
All game objects inherit from the base `Entity` class which provides:
- Position and velocity
- Rotation and angular velocity
- Screen wrap-around behavior
- Collision circle definition

### Entity Manager
Centralized management of all game entities:
- Spawning players, asteroids, bullets
- Updating all entities each frame
- Cleaning up dead entities
- Rendering coordination

### Collision System
Efficient O(n²) circle-circle collision detection:
- Checks all entity pairs
- Uses simplified circle bounds for performance
- Returns collision pairs for game logic处理

### Particle System
Visual effects system:
- Explosion particles when asteroids destroyed
- Hit spark effects
- Alpha fading based on lifetime
- Automatic cleanup of dead particles

## Future Improvements

1. **Audio System:** Add sound effects and background music
2. **Power-ups:** Shield, rapid fire, smart bombs
3. **Enemy Ships:** UFO enemies that shoot back
4. **Visual Polish:** Glow effects, screen shake, starfield background
5. **Leaderboard:** Online high score submission
6. **Gamepad Support:** Controller input handling
7. **Particle Optimization:** Spatial hashing for large particle counts
8. **Mobile Support:** Touch controls for mobile devices

## Code Quality Notes

- **Modular design:** Each system is isolated and testable
- **Configuration-driven:** Easy to balance gameplay via Config class
- **Type hints:** Full type annotations for better IDE support
- **Documentation:** Docstrings on all public classes and methods
- **No magic numbers:** All tunable values in Config class
