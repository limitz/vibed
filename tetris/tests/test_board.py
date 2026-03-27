"""Tests for board module."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from board import Board, BOARD_WIDTH, BOARD_HEIGHT
from pieces import PieceType


class TestBoardInit:
    def test_fresh_board_is_empty(self):
        board = Board()
        assert board.is_empty()

    def test_board_dimensions(self):
        board = Board()
        assert board.width == BOARD_WIDTH
        assert board.height == BOARD_HEIGHT

    def test_all_cells_none(self):
        board = Board()
        for r in range(BOARD_HEIGHT):
            for c in range(BOARD_WIDTH):
                assert board.get_cell(r, c) is None


class TestValidPosition:
    def test_valid_position_center(self):
        board = Board()
        cells = [(0, 0), (0, 1), (1, 0), (1, 1)]  # O-piece shape
        assert board.is_valid_position(cells, 5, 4)

    def test_invalid_left_wall(self):
        board = Board()
        cells = [(0, 0), (0, 1), (0, 2), (0, 3)]  # I-piece horizontal
        assert not board.is_valid_position(cells, 5, -1)

    def test_invalid_right_wall(self):
        board = Board()
        cells = [(0, 0), (0, 1), (0, 2), (0, 3)]
        assert not board.is_valid_position(cells, 5, BOARD_WIDTH - 2)

    def test_invalid_bottom(self):
        board = Board()
        cells = [(0, 0), (1, 0), (2, 0), (3, 0)]  # I-piece vertical
        assert not board.is_valid_position(cells, BOARD_HEIGHT - 2, 0)

    def test_invalid_overlap(self):
        board = Board()
        cells = [(0, 0), (0, 1), (1, 0), (1, 1)]
        board.lock_piece(cells, 10, 4, PieceType.O)
        assert not board.is_valid_position(cells, 10, 4)

    def test_valid_above_locked(self):
        board = Board()
        cells = [(0, 0), (0, 1), (1, 0), (1, 1)]
        board.lock_piece(cells, 10, 4, PieceType.O)
        assert board.is_valid_position(cells, 8, 4)


class TestLockPiece:
    def test_lock_writes_cells(self):
        board = Board()
        cells = [(0, 0), (0, 1), (1, 0), (1, 1)]
        board.lock_piece(cells, 5, 3, PieceType.O)
        assert board.get_cell(5, 3) == PieceType.O
        assert board.get_cell(5, 4) == PieceType.O
        assert board.get_cell(6, 3) == PieceType.O
        assert board.get_cell(6, 4) == PieceType.O

    def test_board_not_empty_after_lock(self):
        board = Board()
        cells = [(0, 0)]
        board.lock_piece(cells, 0, 0, PieceType.T)
        assert not board.is_empty()


class TestLineClear:
    def test_full_row_detected(self):
        board = Board()
        # Fill bottom row completely
        for c in range(BOARD_WIDTH):
            board.lock_piece([(0, 0)], BOARD_HEIGHT - 1, c, PieceType.I)
        assert board.is_row_full(BOARD_HEIGHT - 1)

    def test_incomplete_row_not_full(self):
        board = Board()
        for c in range(BOARD_WIDTH - 1):
            board.lock_piece([(0, 0)], BOARD_HEIGHT - 1, c, PieceType.I)
        assert not board.is_row_full(BOARD_HEIGHT - 1)

    def test_clear_one_line(self):
        board = Board()
        for c in range(BOARD_WIDTH):
            board.lock_piece([(0, 0)], BOARD_HEIGHT - 1, c, PieceType.I)
        cleared = board.clear_lines()
        assert cleared == 1
        # Bottom row should now be empty
        for c in range(BOARD_WIDTH):
            assert board.get_cell(BOARD_HEIGHT - 1, c) is None

    def test_clear_zero_lines(self):
        board = Board()
        board.lock_piece([(0, 0)], BOARD_HEIGHT - 1, 0, PieceType.T)
        cleared = board.clear_lines()
        assert cleared == 0

    def test_clear_multiple_lines(self):
        board = Board()
        # Fill bottom 2 rows
        for r in range(BOARD_HEIGHT - 2, BOARD_HEIGHT):
            for c in range(BOARD_WIDTH):
                board.lock_piece([(0, 0)], r, c, PieceType.I)
        cleared = board.clear_lines()
        assert cleared == 2

    def test_clear_shifts_rows_down(self):
        board = Board()
        # Put a piece on row 18, fill row 19
        board.lock_piece([(0, 0)], BOARD_HEIGHT - 2, 0, PieceType.T)
        for c in range(BOARD_WIDTH):
            board.lock_piece([(0, 0)], BOARD_HEIGHT - 1, c, PieceType.I)
        board.clear_lines()
        # The piece that was on row 18 should now be on row 19
        assert board.get_cell(BOARD_HEIGHT - 1, 0) == PieceType.T

    def test_clear_tetris(self):
        board = Board()
        for r in range(BOARD_HEIGHT - 4, BOARD_HEIGHT):
            for c in range(BOARD_WIDTH):
                board.lock_piece([(0, 0)], r, c, PieceType.I)
        cleared = board.clear_lines()
        assert cleared == 4
