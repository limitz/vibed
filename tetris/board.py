"""Game board / grid logic."""

from typing import List, Optional, Tuple
from pieces import PieceType

BOARD_WIDTH = 10
BOARD_HEIGHT = 20


class Board:
    def __init__(self, width: int = BOARD_WIDTH, height: int = BOARD_HEIGHT):
        self.width = width
        self.height = height
        self.grid: List[List[Optional[PieceType]]] = [
            [None] * width for _ in range(height)
        ]

    def is_valid_position(self, cells: List[Tuple[int, int]], row: int, col: int) -> bool:
        """Check if piece cells at (row, col) are within bounds and not overlapping."""
        for dr, dc in cells:
            r, c = row + dr, col + dc
            if r < 0 or r >= self.height or c < 0 or c >= self.width:
                return False
            if self.grid[r][c] is not None:
                return False
        return True

    def lock_piece(self, cells: List[Tuple[int, int]], row: int, col: int, piece_type: PieceType) -> None:
        """Lock a piece into the grid."""
        for dr, dc in cells:
            self.grid[row + dr][col + dc] = piece_type

    def clear_lines(self) -> int:
        """Clear completed lines, shift rows down, return count cleared."""
        cleared = 0
        new_grid = []
        for row in self.grid:
            if all(cell is not None for cell in row):
                cleared += 1
            else:
                new_grid.append(row)
        # Add empty rows at the top
        for _ in range(cleared):
            new_grid.insert(0, [None] * self.width)
        self.grid = new_grid
        return cleared

    def get_cell(self, row: int, col: int) -> Optional[PieceType]:
        """Get the contents of a cell."""
        return self.grid[row][col]

    def is_row_full(self, row: int) -> bool:
        """Check if a row is completely filled."""
        return all(cell is not None for cell in self.grid[row])

    def is_empty(self) -> bool:
        """Check if the entire board is empty."""
        return all(cell is None for row in self.grid for cell in row)
