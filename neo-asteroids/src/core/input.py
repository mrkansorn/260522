"""
Input handling system.
Manages keyboard state and provides clean input queries.
"""

import pygame


class InputHandler:
    """
    Handles all input from keyboard.
    Provides both instant and sustained input states.
    """

    def __init__(self):
        self.keys_pressed = set()
        self.keys_just_pressed = set()
        self.keys_just_released = set()
        
        # Movement input state
        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False
        
        # Action input state
        self.shoot = False
        self.dash = False

    def update(self):
        """Update input state each frame."""
        self.keys_just_pressed = set()
        self.keys_just_released = set()
        
        # Get current pressed keys
        current_keys = set(pygame.key.get_pressed())
        
        # Detect newly pressed and released keys
        for key in current_keys - self.keys_pressed:
            self.keys_just_pressed.add(key)
        
        for key in self.keys_pressed - current_keys:
            self.keys_just_released.add(key)
        
        self.keys_pressed = current_keys
        
        # Update movement state
        self.move_left = (pygame.K_LEFT in self.keys_pressed or 
                         pygame.K_a in self.keys_pressed)
        self.move_right = (pygame.K_RIGHT in self.keys_pressed or 
                          pygame.K_d in self.keys_pressed)
        self.move_up = (pygame.K_UP in self.keys_pressed or 
                       pygame.K_w in self.keys_pressed)
        self.move_down = (pygame.K_DOWN in self.keys_pressed or 
                         pygame.K_s in self.keys_pressed)
        
        # Update action state
        self.shoot = pygame.K_SPACE in self.keys_pressed
        self.dash = pygame.K_LSHIFT in self.keys_pressed or pygame.K_RSHIFT in self.keys_pressed

    def is_key_pressed(self, key: int) -> bool:
        """Check if a key is currently held down."""
        return key in self.keys_pressed

    def is_key_just_pressed(self, key: int) -> bool:
        """Check if a key was just pressed this frame."""
        return key in self.keys_just_pressed

    def is_key_just_released(self, key: int) -> bool:
        """Check if a key was just released this frame."""
        return key in self.keys_just_released

    def get_rotation_direction(self) -> int:
        """Get rotation direction: -1 for left, 1 for right, 0 for none."""
        if self.move_left:
            return -1
        elif self.move_right:
            return 1
        return 0

    def get_thrust(self) -> float:
        """Get thrust value: 1.0 for forward, 0.0 for none."""
        return 1.0 if self.move_up else 0.0
