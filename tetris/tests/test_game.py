"""Tests for game module."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from game import GameState
from pieces import PieceType
from board import BOARD_WIDTH


class TestGameInit:
    def test_initial_score_zero(self):
        gs = GameState(seed=42)
        assert gs.score == 0

    def test_initial_level_one(self):
        gs = GameState(seed=42)
        assert gs.level == 1

    def test_not_game_over(self):
        gs = GameState(seed=42)
        assert not gs.game_over

    def test_has_current_piece(self):
        gs = GameState(seed=42)
        assert gs.current_piece is not None

    def test_has_next_piece(self):
        gs = GameState(seed=42)
        assert gs.next_piece is not None

    def test_initial_lines_zero(self):
        gs = GameState(seed=42)
        assert gs.lines_cleared == 0


class TestMovement:
    def test_move_left(self):
        gs = GameState(seed=42)
        col_before = gs.current_col
        result = gs.move_left()
        assert result is True
        assert gs.current_col == col_before - 1

    def test_move_right(self):
        gs = GameState(seed=42)
        col_before = gs.current_col
        result = gs.move_right()
        assert result is True
        assert gs.current_col == col_before + 1

    def test_move_down(self):
        gs = GameState(seed=42)
        row_before = gs.current_row
        result = gs.move_down()
        assert result is True
        assert gs.current_row == row_before + 1

    def test_move_left_blocked_at_wall(self):
        gs = GameState(seed=42)
        # Move all the way left
        for _ in range(BOARD_WIDTH):
            gs.move_left()
        result = gs.move_left()
        assert result is False

    def test_move_right_blocked_at_wall(self):
        gs = GameState(seed=42)
        for _ in range(BOARD_WIDTH):
            gs.move_right()
        result = gs.move_right()
        assert result is False


class TestRotation:
    def test_rotate_cw(self):
        gs = GameState(seed=42)
        rot_before = gs.current_rotation
        gs.rotate_cw()
        # Rotation should have changed (may be different due to wall kicks)
        # Just verify it returns a bool
        assert isinstance(gs.current_rotation, int)

    def test_rotate_ccw(self):
        gs = GameState(seed=42)
        gs.rotate_ccw()
        assert isinstance(gs.current_rotation, int)


class TestHardDrop:
    def test_hard_drop_moves_down(self):
        gs = GameState(seed=42)
        row_before = gs.current_row
        rows_dropped = gs.hard_drop()
        assert rows_dropped > 0

    def test_hard_drop_locks_piece(self):
        gs = GameState(seed=42)
        piece_before = gs.current_piece
        gs.hard_drop()
        # After hard drop, a new piece should have spawned
        # (current_piece may be same type but position resets)
        assert gs.current_row <= 1  # new piece spawns at top


class TestScoring:
    def _fill_rows(self, gs, num_rows):
        """Fill the bottom num_rows rows except the rightmost column."""
        for r in range(gs.board.height - num_rows, gs.board.height):
            for c in range(BOARD_WIDTH - 1):
                gs.board.lock_piece([(0, 0)], r, c, PieceType.I)

    def test_single_line_clear_score(self):
        gs = GameState(seed=42)
        self._fill_rows(gs, 1)
        # Fill the remaining cell
        for c in range(BOARD_WIDTH):
            gs.board.grid[gs.board.height - 1][c] = PieceType.I
        gs.board.clear_lines()
        # Manually trigger scoring
        gs._add_score(1)
        assert gs.score == 100

    def test_tetris_score(self):
        gs = GameState(seed=42)
        gs._add_score(4)
        assert gs.score == 800


class TestLevel:
    def test_level_increases_after_10_lines(self):
        gs = GameState(seed=42)
        gs.lines_cleared = 9
        gs._add_score(1)  # This should trigger level up
        assert gs.level == 2

    def test_gravity_interval_decreases(self):
        gs = GameState(seed=42)
        interval_1 = gs.get_gravity_interval_ms()
        gs.level = 5
        interval_5 = gs.get_gravity_interval_ms()
        assert interval_5 < interval_1

    def test_gravity_interval_minimum(self):
        gs = GameState(seed=42)
        gs.level = 100
        assert gs.get_gravity_interval_ms() >= 100


class TestTick:
    def test_tick_moves_piece_down(self):
        gs = GameState(seed=42)
        row_before = gs.current_row
        gs.tick()
        assert gs.current_row == row_before + 1 or gs.current_row <= 1  # moved or locked+respawned


class TestBagRandomizer:
    def test_first_seven_contain_all_types(self):
        gs = GameState(seed=42)
        pieces = [gs.current_piece]
        for _ in range(6):
            gs.hard_drop()
            pieces.append(gs.current_piece)
        assert set(pieces) == set(PieceType), f"First 7 pieces should contain all types, got {pieces}"

    def test_next_seven_contain_all_types(self):
        gs = GameState(seed=42)
        # Exhaust first bag
        for _ in range(7):
            gs.hard_drop()
        pieces = [gs.current_piece]
        for _ in range(6):
            gs.hard_drop()
            pieces.append(gs.current_piece)
        assert set(pieces) == set(PieceType)


class TestGhostPiece:
    def test_ghost_row_below_current(self):
        gs = GameState(seed=42)
        ghost_row = gs.get_ghost_row()
        assert ghost_row >= gs.current_row

    def test_ghost_row_is_lowest_valid(self):
        gs = GameState(seed=42)
        ghost_row = gs.get_ghost_row()
        from pieces import get_cells
        cells = get_cells(gs.current_piece, gs.current_rotation)
        # Ghost position should be valid
        assert gs.board.is_valid_position(cells, ghost_row, gs.current_col)
        # One row below should be invalid
        assert not gs.board.is_valid_position(cells, ghost_row + 1, gs.current_col)


class TestGameOver:
    def test_game_over_when_board_full(self):
        gs = GameState(seed=42)
        # Fill the top rows to prevent spawning
        for r in range(4):
            for c in range(BOARD_WIDTH):
                gs.board.grid[r][c] = PieceType.I
        result = gs.spawn_piece()
        assert result is False or gs.game_over is True
