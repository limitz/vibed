# Pac-Man

**Prompt:**
> `pacman`

A console-based Pac-Man game built in Python using curses.

![Screenshot](screenshot.png)

## Features

- Classic 28-column maze with walls, pellets, power pellets, and tunnel wrapping
- 4 ghosts with unique AI personalities:
  - **Blinky** (red) - targets Pac-Man directly
  - **Pinky** (pink) - targets 4 tiles ahead of Pac-Man
  - **Inky** (cyan) - uses Blinky's position to compute an ambush target
  - **Clyde** (orange) - chases when far, scatters when close
- Ghost modes: chase, scatter, frightened, and eaten
- Power pellets that frighten ghosts (eat them for bonus points!)
- Sequential ghost eating multiplier (200, 400, 800, 1600)
- Scoring system with pellet and ghost eating points
- 3 lives with position reset on death
- Level progression when all pellets are eaten
- Pause/unpause with P key
- Arrow keys and WASD controls

## Controls

| Key | Action |
|-----|--------|
| Arrow keys / WASD | Move Pac-Man |
| P | Pause / Unpause |
| Q / ESC | Quit |

## Running

```bash
cd pacman
python main.py
```

## Architecture

- `maze.py` - Maze layout, wall detection, pellet management, tunnel wrapping
- `entities.py` - Pac-Man and Ghost classes with movement and AI behavior
- `game.py` - Game state management, scoring, lives, level progression
- `renderer.py` - Curses-based terminal rendering with colors
- `main.py` - Entry point, game loop, input handling

## Testing

```bash
python -m pytest test_maze.py test_entities.py test_game.py -v
```

59 unit tests covering maze navigation, entity behavior, scoring, and game logic.

## Built with

Claude Opus 4.6 (`claude-opus-4-6`) — implementation by Claude Code
