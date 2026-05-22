"""
Neo Asteroids - Main Entry Point
Run: python main.py
Controls: Arrow keys/WASD to move, Space to shoot, Shift to dash
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.game import Game


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
