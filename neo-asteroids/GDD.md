# Neo Asteroids - Game Design Document

## 1. Game Concept Summary

**Neo Asteroids** is a modern reimagining of the classic 1979 arcade game, built with clean architecture and professional game development practices.

### Core Experience
- Fast-paced space shooter action
- Skill-based movement with inertia physics
- Satisfying asteroid destruction with particle effects
- Progressive difficulty through levels
- High score competition

---

## 2. Gameplay Design

### A. Genre
**Space Shooter / Arcade Action**

### B. Gameplay Loop
```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Spawn     │────▶│  Navigate    │────▶│   Shoot     │
│  In Arena   │     │  & Avoid     │     │  Asteroids  │
└─────────────┘     └──────────────┘     └─────────────┘
      ▲                                        │
      │                                        ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Next      │◀────│    Level     │◀────│   Clear     │
│   Level     │     │   Complete   │     │  All Rocks  │
└─────────────┘     └──────────────┘     └─────────────┘
```

### C. Player Mechanics

#### Movement System
- **Rotation:** Angular velocity applied when pressing left/right
- **Thrust:** Acceleration in facing direction when pressing up
- **Inertia:** Momentum preserved with friction coefficient (0.98)
- **Max Speed:** Capped at 500 pixels/second
- **Screen Wrap:** Exiting one edge enters from opposite edge

#### Combat System
- **Shooting:** Fires bullet in facing direction
- **Cooldown:** 0.25 seconds between shots
- **Dash:** Quick boost with brief invincibility (2 second cooldown)

#### Survival Mechanics
- **Lives:** 3 lives per game
- **Invincibility:** 2 seconds after respawn with visual flashing
- **Collision:** Instant death on asteroid contact (when not invincible)

### D. Enemy/NPC Behavior

#### Asteroid Types
| Size | Radius | Speed | Health | Score | Split To |
|------|--------|-------|--------|-------|----------|
| Large | 40px | 50 px/s | 3 hits | 20 | 2 Medium |
| Medium | 25px | 80 px/s | 2 hits | 50 | 2 Small |
| Small | 12px | 120 px/s | 1 hit | 100 | Destroyed |

#### Spawn Rules
- Minimum 150px distance from player
- Spawn margin of 50px from screen edges
- Random positions with retry logic (max 20 attempts)
- Fallback to edge spawning if no valid position found

#### Movement Pattern
- Constant linear velocity
- Random rotation speed (-30 to 30 degrees/second)
- No homing or player tracking (pure obstacle)

### E. Scoring/Progression Systems

#### Points
- Large asteroid: 20 points
- Medium asteroid: 50 points  
- Small asteroid: 100 points
- Total possible per large asteroid chain: 20 + 2×50 + 4×100 = 520 points

#### Level Progression
- Level 1: 4 asteroids
- Each level: +1 asteroid
- No upper limit (infinite scaling)

#### High Score
- Persisted to `highscore.txt`
- Updated only when beaten
- Displayed on main menu and game over

### F. UI/HUD Systems

#### Main Menu
- Game title with stylized coloring
- Current high score display
- Control instructions
- Start prompt

#### In-Game HUD
- **Top Left:** Current score
- **Bottom Left:** Lives remaining
- **Top Right:** Current level

#### Pause Menu
- Semi-transparent overlay
- "PAUSED" text
- Resume instruction

#### Game Over Screen
- "GAME OVER" in danger color
- Final score display
- "NEW HIGH SCORE!" if applicable
- Continue prompt

### G. Audio/Visual Effects

#### Particle Effects
- **Explosions:** 20 particles when asteroid destroyed
- **Hit Sparks:** 8 particles on bullet impact
- **Thrust Particles:** Continuous while accelerating
- Particle lifetime: 0.8 seconds (explosions), 0.4 seconds (hits)
- Drag coefficient: 0.95 per frame

#### Visual Feedback
- Player flash during invincibility (10 Hz)
- Engine thrust flame when accelerating
- Screen wrap visualization for all entities
- Color-coded asteroids by size

#### Audio (Reserved)
- Shooting sound
- Explosion sound
- Thrust sound
- Game over jingle
- Background music

### H. Save/Load Systems

#### Persistent Data
- High score saved to `highscore.txt`
- Plain text format for simplicity
- Auto-saved on game over

#### Session Data
- Score, lives, level reset on new game
- No mid-game save (arcade style)

---

## 3. Technical Architecture

### Entity-Component-System Hybrid

```
┌─────────────────────────────────────────────────┐
│                   Game Class                    │
│  • Manages game states (Menu, Playing, etc.)   │
│  • Runs main loop (Event→Update→Render)        │
│  • Coordinates all systems                      │
└─────────────────────────────────────────────────┘
                        │
         ┌──────────────┼──────────────┐
         ▼              ▼              ▼
┌────────────────┐ ┌────────────────┐ ┌────────────────┐
│ InputHandler   │ │ EntityManager  │ │ CollisionSystem│
│ • Keyboard     │ │ • Spawn        │ │ • Detection    │
│ • State track  │ │ • Update       │ │ • Resolution   │
│ • Queries      │ │ • Cleanup      │ │                │
└────────────────┘ └────────────────┘ └────────────────┘
         │              │                     │
         ▼              ▼                     ▼
┌────────────────┐ ┌────────────────┐ ┌────────────────┐
│ Renderer       │ │ Entities       │ │ ParticleSystem │
│ • Draw calls   │ │ • Player       │ │ • Effects      │
│ • Transforms   │ │ • Asteroids    │ │ • Lifecycle    │
│ • Wrap-around  │ │ • Bullets      │ │ • Rendering    │
└────────────────┘ └────────────────┘ └────────────────┘
```

### Key Classes

#### Core Layer
- `Config`: All tunable constants
- `Game`: Main loop and state machine
- `InputHandler`: Keyboard state management
- `Renderer`: Pygame drawing abstraction

#### Entity Layer
- `Entity`: Abstract base with position, velocity, rotation
- `Player`: User-controlled ship with combat abilities
- `Asteroid`: Destructible obstacles with splitting
- `Bullet`: Short-lived projectiles

#### System Layer
- `EntityManager`: Lifecycle and collection management
- `CollisionSystem`: Circle-based collision detection
- `ParticleSystem`: Visual effect management

#### UI Layer
- `HUD`: In-game information display
- `Menu`: Screen state rendering

### Design Patterns Used

1. **Singleton-ish Config:** Centralized constants
2. **Entity-Component:** Composition over inheritance
3. **System Separation:** Single responsibility principle
4. **State Machine:** Game state management
5. **Factory Method:** Entity spawning
6. **Strategy:** Different entity behaviors

---

## 4. Implementation Details

### Physics System

#### Movement Integration (Euler)
```python
# Velocity update
velocity += acceleration * dt

# Position update  
position += velocity * dt

# Friction application
velocity *= friction_coefficient
```

#### Rotation
```python
angle += angular_velocity * dt
angle = angle % 360  # Normalize
```

### Collision Detection

#### Circle-Circle Test
```python
distance = sqrt((x2-x1)² + (y2-y1)²)
collision = distance < (radius1 + radius2) * tolerance
```

**Tolerance factor (0.9):** Provides slightly forgiving hitboxes for better gameplay feel.

### Performance Optimizations

1. **Dead entity cleanup:** Batch removal instead of immediate
2. **Simple collision shapes:** Circles vs polygons
3. **Fixed time step:** Consistent 60 FPS target
4. **Minimal allocations:** Reuse objects where possible

---

## 5. Balance & Tuning

### Difficulty Curve
- Linear asteroid count increase
- Faster small asteroids require quicker reactions
- More asteroids = more collision avoidance needed

### Player Power
- Dash provides emergency escape
- Invincibility frames prevent spawn kills
- Tight controls reward skill

### Score Balance
- Risk/reward: Small asteroids worth more but harder to hit
- Chain bonus potential: Breaking large → small yields 520 total

---

## 6. Future Enhancement Roadmap

### Phase 1: Polish
- [ ] Sound effects and music
- [ ] Starfield background
- [ ] Screen shake on explosions
- [ ] Glow effects on entities

### Phase 2: Content
- [ ] UFO enemy that shoots at player
- [ ] Power-up drops (shield, rapid fire, bomb)
- [ ] Achievement system
- [ ] Multiple ship types

### Phase 3: Features
- [ ] Online leaderboard
- [ ] Replay system
- [ ] Mobile touch controls
- [ ] Steam integration

### Phase 4: Advanced
- [ ] Particle system GPU acceleration
- [ ] Spatial hashing for collision
- [ ] Mod support
- [ ] Level editor

---

## 7. Testing Checklist

### Functional Tests
- [x] Player movement and rotation
- [x] Shooting mechanics
- [x] Asteroid spawning and splitting
- [x] Collision detection
- [x] Screen wrap-around
- [x] Level progression
- [x] Score tracking
- [x] High score persistence
- [x] Game states (menu, playing, paused, game over)

### Edge Cases
- [ ] Rapid firing (cooldown enforcement)
- [ ] Multiple simultaneous collisions
- [ ] Spawn blocking (asteroid density)
- [ ] Boundary conditions (exact edge positions)

### Performance
- [ ] Stable 60 FPS with max entities
- [ ] No memory leaks
- [ ] Clean entity cleanup

---

*Document Version: 1.0*
*Last Updated: Initial Release*
