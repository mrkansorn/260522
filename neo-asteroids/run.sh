#!/bin/bash
# Neo Asteroids - Quick Start Script

echo "==================================="
echo "     NEO ASTEROIDS"
echo "==================================="
echo ""

# Check Python version
python_version=$(python --version 2>&1 | cut -d' ' -f2)
echo "Python version: $python_version"

# Check pygame installation
python -c "import pygame; print('Pygame version:', pygame.version.ver)" 2>/dev/null || {
    echo ""
    echo "Installing pygame..."
    pip install pygame
}

echo ""
echo "Starting game..."
echo ""

# Run the game
cd "$(dirname "$0")"
python main.py
