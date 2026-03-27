# Tetris

```
Make a cool Tetris game for the console.
```

A console-based Tetris game written in Python using curses.

Built entirely by **Claude Opus 4.6** (model ID: `claude-opus-4-6`), Anthropic's most capable AI model.

![Tetris Screenshot](screenshot.png)

## Features

- All 7 standard tetrominoes (I, O, T, S, Z, J, L)
- SRS (Super Rotation System) wall kicks
- 7-bag randomizer for fair piece distribution
- Ghost piece showing where the current piece will land
- Next piece preview
- Scoring: 100/300/500/800 points for 1/2/3/4 lines, multiplied by level
- Increasing difficulty — gravity speeds up every 10 lines
- Colorful terminal UI with box-drawing borders

## How to Play

```bash
python main.py
```

### Controls

| Key       | Action              |
|-----------|---------------------|
| ← →       | Move left/right     |
| ↑         | Rotate clockwise    |
| Z         | Rotate counter-clockwise |
| ↓         | Soft drop           |
| Space     | Hard drop           |
| P         | Pause               |
| Q         | Quit                |
| R         | Restart             |

## Architecture

| Module             | Purpose                                      |
|--------------------|----------------------------------------------|
| `pieces.py`        | Tetromino shapes, rotations, SRS wall kicks  |
| `board.py`         | 10x20 grid, collision detection, line clearing |
| `game.py`          | Game state, scoring, levels, 7-bag randomizer |
| `renderer.py`      | Curses-based terminal rendering with colors  |
| `input_handler.py` | Key mapping and game loop                    |
| `main.py`          | Entry point                                  |

## Tests

```bash
python -m pytest tests/ -v
```

68 unit tests covering pieces, board logic, game state, rendering, and input handling.
