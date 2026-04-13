# Maze Runner

A Python maze game built with Pygame where players navigate through procedurally generated mazes across 10 levels.

## Features

- **Procedurally Generated Mazes**: Each level creates a unique maze using a depth-first search algorithm
- **10 Progressive Levels**: Difficulty increases with more walls as you advance
- **Lives System**: 3 lives with 3 failures allowed before game reset
- **Time Pressure**: Countdown timer that decreases with each level
- **Save/Load**: Progress is automatically saved after each level
- **Arrow Keys or WASD**: Flexible movement controls

## Requirements

- Python 3.x
- Pygame

```bash
pip install pygame
```

## How to Play

1. Run the game:
   ```bash
   python maze_game.py
   ```

2. Use the menu to start a **New Game** or **Load** a saved game

3. Navigate the blue player to the green exit before time runs out

4. Controls:
   - **Arrow Keys** or **WASD** to move

5. Complete all 10 levels to win!

## Game Rules

- **Lives**: Start with 3 lives
- **Failures**: 3 failures reset you to level 1
- **Timer**: Starts at 60 seconds, decreases by 3 seconds per level (minimum 20s)
- **Walls**: Difficulty increases with more walls at higher levels

## Project Structure

```
maze-game/
├── maze_game.py      # Main game file
├── savegame.json     # Saved progress
└── README.md         # This file
```

## Screenshots

- Main menu with New Game, Load Game, and Exit options
- Maze view with player (blue), walls (gray), and exit (green)
- UI showing current level, lives, and remaining time

## License

MIT License
