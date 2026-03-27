# Chess

```
Make a nice looking chess game for the console. Do not use a library for generating the moves made by the computer, write your own logic.
```

A console-based chess game with a custom AI opponent, built entirely in Python using curses for terminal rendering.

![Screenshot](screenshot.png)

## Features

- **Full chess rules**: All standard moves including castling, en passant, pawn promotion, check/checkmate/stalemate detection, 50-move rule, and threefold repetition draw
- **Custom AI engine**: Minimax search with alpha-beta pruning (depth 3), quiescence search, MVV-LVA move ordering, and piece-square table evaluation
- **Nice terminal UI**: Unicode chess pieces, colored board squares, cursor navigation, highlighted legal moves, last-move indicators, and check warnings
- **Undo support**: Undo your last move (and the AI's response) at any time

## How to Play

```bash
python main.py
```

- **Arrow keys**: Move the cursor around the board
- **Enter/Space**: Select a piece or confirm a move
- **Esc**: Cancel selection
- **U**: Undo last move
- **N**: New game
- **Q**: Quit

You play as White; the computer plays as Black.

## Architecture

| Module | Description |
|--------|-------------|
| `pieces.py` | Piece enums, Unicode symbols, material values, piece-square tables |
| `board.py` | 8x8 board with make/unmake move, castling rights, en passant |
| `moves.py` | Legal move generation, check/checkmate/stalemate detection |
| `ai.py` | Minimax + alpha-beta pruning, evaluation function, quiescence search |
| `game.py` | Game state, turn management, move history, UI state machine |
| `renderer.py` | Curses rendering with colors, highlights, side panel |
| `input_handler.py` | Key mapping, game loop, promotion handling |
| `main.py` | Entry point |

## Tests

```bash
python -m pytest tests/ -v
```

127 tests covering all modules: pieces, board, move generation, AI, rendering, and input handling.

## Built by

Claude Opus 4.6 (`claude-opus-4-6`) via [Claude Code](https://claude.com/claude-code)
