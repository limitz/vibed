"""Input handling and game loop for the chess game."""

import curses
import time
from enum import Enum, auto
from typing import Optional

from game import GameState, GameStatus, InputMode
from pieces import Color, PieceType
from renderer import Renderer


class Action(Enum):
    """Player actions."""
    CURSOR_UP = auto()
    CURSOR_DOWN = auto()
    CURSOR_LEFT = auto()
    CURSOR_RIGHT = auto()
    SELECT = auto()
    CANCEL = auto()
    UNDO = auto()
    RESIGN = auto()
    QUIT = auto()
    NEW_GAME = auto()
    PROMOTE_QUEEN = auto()
    PROMOTE_ROOK = auto()
    PROMOTE_BISHOP = auto()
    PROMOTE_KNIGHT = auto()


KEY_MAP = {
    curses.KEY_UP: Action.CURSOR_UP,
    curses.KEY_DOWN: Action.CURSOR_DOWN,
    curses.KEY_LEFT: Action.CURSOR_LEFT,
    curses.KEY_RIGHT: Action.CURSOR_RIGHT,
    10: Action.SELECT,              # Enter
    13: Action.SELECT,              # Carriage return
    ord(' '): Action.SELECT,
    27: Action.CANCEL,              # Escape
    curses.KEY_BACKSPACE: Action.CANCEL,
    ord('q'): Action.QUIT,
    ord('Q'): Action.QUIT,
    ord('u'): Action.UNDO,
    ord('U'): Action.UNDO,
    ord('n'): Action.NEW_GAME,
    ord('N'): Action.NEW_GAME,
    ord('r'): Action.RESIGN,
    ord('R'): Action.RESIGN,
}

PROMOTION_KEY_MAP = {
    ord('q'): PieceType.QUEEN,
    ord('Q'): PieceType.QUEEN,
    ord('r'): PieceType.ROOK,
    ord('R'): PieceType.ROOK,
    ord('b'): PieceType.BISHOP,
    ord('B'): PieceType.BISHOP,
    ord('n'): PieceType.KNIGHT,
    ord('N'): PieceType.KNIGHT,
}


def map_key(key: int) -> Optional[Action]:
    """Map a curses key code to an Action."""
    return KEY_MAP.get(key)


class GameLoop:
    """Main game loop handling input, AI, and rendering."""

    def __init__(self, stdscr: 'curses.window') -> None:
        """Initialize game loop."""
        self.stdscr = stdscr
        self.state = GameState()
        self.renderer = Renderer(stdscr)
        self.running = True
        stdscr.nodelay(True)
        stdscr.keypad(True)

    def run(self) -> None:
        """Run the main game loop."""
        while self.running:
            self.renderer.draw(self.state)

            try:
                key = self.stdscr.getch()
            except curses.error:
                key = -1

            if key != -1:
                self._handle_key(key)

            time.sleep(0.016)  # ~60 FPS

    def _handle_key(self, key: int) -> None:
        """Process a raw key press."""
        # Handle promotion mode separately
        if self.state.input_mode == InputMode.PROMOTING:
            if key == 27:  # Escape
                self.state.cancel_selection()
                return
            promo_type = PROMOTION_KEY_MAP.get(key)
            if promo_type:
                move = self.state.promote(promo_type)
                if move and self.state.board.turn == Color.BLACK:
                    self._do_ai_turn()
            return

        action = map_key(key)
        if action is None:
            return

        self.handle_action(action)

    def handle_action(self, action: Action) -> None:
        """Process a player action."""
        state = self.state

        if action == Action.QUIT:
            self.running = False
            return

        if action == Action.NEW_GAME:
            state.new_game()
            return

        if state.input_mode == InputMode.GAME_OVER:
            return

        if state.input_mode == InputMode.AI_THINKING:
            return

        if action == Action.CURSOR_UP:
            r, c = state.cursor_pos
            state.cursor_pos = (max(0, r - 1), c)
        elif action == Action.CURSOR_DOWN:
            r, c = state.cursor_pos
            state.cursor_pos = (min(7, r + 1), c)
        elif action == Action.CURSOR_LEFT:
            r, c = state.cursor_pos
            state.cursor_pos = (r, max(0, c - 1))
        elif action == Action.CURSOR_RIGHT:
            r, c = state.cursor_pos
            state.cursor_pos = (r, min(7, c + 1))
        elif action == Action.SELECT:
            if state.board.turn == Color.WHITE:
                r, c = state.cursor_pos
                move = state.select_square(r, c)
                if move and state.board.turn == Color.BLACK and state.input_mode != InputMode.GAME_OVER:
                    self._do_ai_turn()
        elif action == Action.CANCEL:
            state.cancel_selection()
        elif action == Action.UNDO:
            if state.undo_stack:
                state.undo_last_move()
        elif action == Action.RESIGN:
            state.status = GameStatus.RESIGNED
            state.message = "White resigned. Black wins!"
            state.input_mode = InputMode.GAME_OVER

    def _do_ai_turn(self) -> None:
        """Execute the AI's turn with a visual update."""
        self.state.input_mode = InputMode.AI_THINKING
        self.state.message = "Computer thinking..."
        self.renderer.draw(self.state)
        self.state.execute_ai_move()
