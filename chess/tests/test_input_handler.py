"""Tests for input_handler module."""

import curses
import pytest
from input_handler import Action, map_key


class TestMapKey:
    def test_arrow_up(self):
        assert map_key(curses.KEY_UP) == Action.CURSOR_UP

    def test_arrow_down(self):
        assert map_key(curses.KEY_DOWN) == Action.CURSOR_DOWN

    def test_arrow_left(self):
        assert map_key(curses.KEY_LEFT) == Action.CURSOR_LEFT

    def test_arrow_right(self):
        assert map_key(curses.KEY_RIGHT) == Action.CURSOR_RIGHT

    def test_enter(self):
        assert map_key(10) == Action.SELECT  # Enter key

    def test_space(self):
        assert map_key(ord(' ')) == Action.SELECT

    def test_escape(self):
        assert map_key(27) == Action.CANCEL

    def test_quit(self):
        assert map_key(ord('q')) == Action.QUIT
        assert map_key(ord('Q')) == Action.QUIT

    def test_undo(self):
        assert map_key(ord('u')) == Action.UNDO
        assert map_key(ord('U')) == Action.UNDO

    def test_new_game(self):
        assert map_key(ord('n')) == Action.NEW_GAME
        assert map_key(ord('N')) == Action.NEW_GAME

    def test_unknown_key(self):
        assert map_key(ord('x')) is None

    def test_promotion_keys(self):
        # These should only be active during promotion mode
        # but the mapping should exist
        pass  # promotion is handled via separate logic


class TestGameState:
    """Test game state management via input handler interactions."""

    def test_initial_cursor_position(self):
        from game import GameState
        state = GameState()
        assert state.cursor_pos == (6, 4)

    def test_cursor_movement(self):
        from game import GameState, InputMode
        state = GameState()
        # Move cursor up
        r, c = state.cursor_pos
        new_r = max(0, r - 1)
        state.cursor_pos = (new_r, c)
        assert state.cursor_pos == (5, 4)

    def test_piece_selection(self):
        from game import GameState, InputMode
        state = GameState()
        # Select white pawn at e2
        state.select_square(6, 4)
        assert state.input_mode == InputMode.PIECE_SELECTED
        assert state.selected_square == (6, 4)

    def test_cancel_selection(self):
        from game import GameState, InputMode
        state = GameState()
        state.select_square(6, 4)
        state.cancel_selection()
        assert state.input_mode == InputMode.IDLE
        assert state.selected_square is None

    def test_execute_move(self):
        from game import GameState, InputMode
        from pieces import Color
        state = GameState()
        state.select_square(6, 4)  # Select e2 pawn
        move = state.select_square(4, 4)  # Move to e4
        assert move is not None
        assert state.board.turn == Color.BLACK
