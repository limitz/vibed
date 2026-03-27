"""Game state machine, scoring, levels, and 7-bag randomizer."""

from typing import Optional, List
import random

from pieces import PieceType, get_cells, rotate_cw, rotate_ccw, get_wall_kicks
from board import Board

SCORE_TABLE = {0: 0, 1: 100, 2: 300, 3: 500, 4: 800}
SPAWN_ROW = 0
SPAWN_COL = 3


class GameState:
    def __init__(self, seed: Optional[int] = None):
        self.board = Board()
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self._rng = random.Random(seed)
        self._bag: List[PieceType] = []
        self.current_piece: Optional[PieceType] = None
        self.current_rotation = 0
        self.current_row = 0
        self.current_col = 0
        self.next_piece = self._next_from_bag()
        self.spawn_piece()

    def _next_from_bag(self) -> PieceType:
        if not self._bag:
            self._bag = list(PieceType)
            self._rng.shuffle(self._bag)
        return self._bag.pop()

    def spawn_piece(self) -> bool:
        self.current_piece = self.next_piece
        self.next_piece = self._next_from_bag()
        self.current_rotation = 0
        self.current_row = SPAWN_ROW
        self.current_col = SPAWN_COL
        cells = get_cells(self.current_piece, self.current_rotation)
        if not self.board.is_valid_position(cells, self.current_row, self.current_col):
            self.game_over = True
            return False
        return True

    def move_left(self) -> bool:
        cells = get_cells(self.current_piece, self.current_rotation)
        if self.board.is_valid_position(cells, self.current_row, self.current_col - 1):
            self.current_col -= 1
            return True
        return False

    def move_right(self) -> bool:
        cells = get_cells(self.current_piece, self.current_rotation)
        if self.board.is_valid_position(cells, self.current_row, self.current_col + 1):
            self.current_col += 1
            return True
        return False

    def move_down(self) -> bool:
        cells = get_cells(self.current_piece, self.current_rotation)
        if self.board.is_valid_position(cells, self.current_row + 1, self.current_col):
            self.current_row += 1
            return True
        return False

    def rotate_cw(self) -> bool:
        new_rot = rotate_cw(self.current_rotation)
        return self._try_rotate(new_rot)

    def rotate_ccw(self) -> bool:
        new_rot = rotate_ccw(self.current_rotation)
        return self._try_rotate(new_rot)

    def _try_rotate(self, new_rot: int) -> bool:
        kicks = get_wall_kicks(self.current_piece, self.current_rotation, new_rot)
        new_cells = get_cells(self.current_piece, new_rot)
        for dr, dc in kicks:
            if self.board.is_valid_position(new_cells, self.current_row + dr, self.current_col + dc):
                self.current_row += dr
                self.current_col += dc
                self.current_rotation = new_rot
                return True
        return False

    def hard_drop(self) -> int:
        ghost = self.get_ghost_row()
        rows_dropped = ghost - self.current_row
        self.current_row = ghost
        self._lock_and_advance()
        return rows_dropped

    def tick(self) -> None:
        if not self.move_down():
            self._lock_and_advance()

    def get_ghost_row(self) -> int:
        cells = get_cells(self.current_piece, self.current_rotation)
        row = self.current_row
        while self.board.is_valid_position(cells, row + 1, self.current_col):
            row += 1
        return row

    def get_gravity_interval_ms(self) -> int:
        return max(100, 1000 - (self.level - 1) * 80)

    def _lock_and_advance(self) -> None:
        cells = get_cells(self.current_piece, self.current_rotation)
        self.board.lock_piece(cells, self.current_row, self.current_col, self.current_piece)
        cleared = self.board.clear_lines()
        if cleared > 0:
            self._add_score(cleared)
        self.spawn_piece()

    def _add_score(self, lines: int) -> None:
        self.score += SCORE_TABLE.get(lines, 0) * self.level
        self.lines_cleared += lines
        self.level = self.lines_cleared // 10 + 1
