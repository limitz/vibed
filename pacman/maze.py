"""Maze module - handles the game board layout, walls, pellets, and pathfinding."""

from enum import IntEnum
from typing import List, Tuple, Optional
import copy


class Tile(IntEnum):
    EMPTY = 0
    WALL = 1
    PELLET = 2
    POWER_PELLET = 3
    GHOST_HOUSE = 4
    GHOST_DOOR = 5


# Classic 28x31 Pac-Man maze layout
# W = wall, . = pellet, o = power pellet, - = ghost door, G = ghost house, ' ' = empty
CLASSIC_LAYOUT = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",  # 0
    "W............WW............W",  # 1
    "W.WWWW.WWWWW.WW.WWWWW.WWWW.W",  # 2
    "WoWWWW.WWWWW.WW.WWWWW.WWWWoW",  # 3
    "W.WWWW.WWWWW.WW.WWWWW.WWWW.W",  # 4
    "W..........................W",  # 5
    "W.WWWW.WW.WWWWWWWW.WW.WWWW.W",  # 6
    "W......WW....WW....WW......W",  # 7
    "WWWWWW.WWWWW WW WWWWW.WWWWWW",  # 8
    "     W.WWWWW WW WWWWW.W     ",  # 9
    "     W.WW          WW.W     ",  # 10
    "     W.WW WWW--WWW WW.W     ",  # 11
    "WWWWWW.WW WGGGGGGW WW.WWWWWW",  # 12
    "      .   WGGGGGGW   .      ",  # 13
    "WWWWWW.WW WGGGGGGW WW.WWWWWW",  # 14
    "     W.WW WWWWWWWW WW.W     ",  # 15
    "     W.WW          WW.W     ",  # 16
    "     W.WW WWWWWWWW WW.W     ",  # 17
    "WWWWWW.WW WWWWWWWW WW.WWWWWW",  # 18
    "W............WW............W",  # 19
    "W.WWWW.WWWWW.WW.WWWWW.WWWW.W",  # 20
    "Wo..WW................WW..oW",  # 21
    "WWW.WW.WW.WWWWWWWW.WW.WW.WWW",  # 22
    "WWW.WW.WW.WWWWWWWW.WW.WW.WWW",  # 23
    "W......WW....WW....WW......W",  # 24
    "W.WWWWWWWWWW.WW.WWWWWWWWWW.W",  # 25
    "W..........................W",  # 26
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",  # 27
]

_CHAR_TO_TILE = {
    'W': Tile.WALL,
    '.': Tile.PELLET,
    'o': Tile.POWER_PELLET,
    '-': Tile.GHOST_DOOR,
    'G': Tile.GHOST_HOUSE,
    ' ': Tile.EMPTY,
}


class Maze:
    """Represents the Pac-Man maze with walls, pellets, and navigation."""

    def __init__(self, layout: Optional[List[str]] = None):
        if layout is None:
            layout = CLASSIC_LAYOUT
        self._raw_layout = layout
        self._height = len(layout)
        self._width = max(len(row) for row in layout)
        self._grid: List[List[Tile]] = []
        self._initial_grid: List[List[Tile]] = []
        self._parse_layout(layout)

    def _parse_layout(self, layout: List[str]) -> None:
        self._grid = []
        for row_str in layout:
            row = []
            for ch in row_str.ljust(self._width):
                row.append(_CHAR_TO_TILE.get(ch, Tile.EMPTY))
            self._grid.append(row)
        self._initial_grid = copy.deepcopy(self._grid)

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def get_tile(self, row: int, col: int) -> Tile:
        row, col = self.wrap_position(row, col)
        if 0 <= row < self._height and 0 <= col < self._width:
            return self._grid[row][col]
        return Tile.WALL

    def is_wall(self, row: int, col: int) -> bool:
        return self.get_tile(row, col) == Tile.WALL

    def is_walkable(self, row: int, col: int, is_ghost: bool = False) -> bool:
        tile = self.get_tile(row, col)
        if tile == Tile.WALL:
            return False
        if tile == Tile.GHOST_DOOR:
            return is_ghost
        if tile == Tile.GHOST_HOUSE:
            return is_ghost
        return True

    def eat_pellet(self, row: int, col: int) -> Optional[Tile]:
        row, col = self.wrap_position(row, col)
        if 0 <= row < self._height and 0 <= col < self._width:
            tile = self._grid[row][col]
            if tile in (Tile.PELLET, Tile.POWER_PELLET):
                self._grid[row][col] = Tile.EMPTY
                return tile
        return None

    def remaining_pellets(self) -> int:
        count = 0
        for row in self._grid:
            for tile in row:
                if tile in (Tile.PELLET, Tile.POWER_PELLET):
                    count += 1
        return count

    def wrap_position(self, row: int, col: int) -> Tuple[int, int]:
        if col < 0:
            col = self._width - 1
        elif col >= self._width:
            col = 0
        if row < 0:
            row = self._height - 1
        elif row >= self._height:
            row = 0
        return row, col

    def get_valid_moves(self, row: int, col: int, is_ghost: bool = False) -> List[Tuple[int, int]]:
        moves = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = self.wrap_position(row + dr, col + dc)
            if self.is_walkable(nr, nc, is_ghost):
                moves.append((nr, nc))
        return moves

    def get_ghost_house_positions(self) -> List[Tuple[int, int]]:
        positions = []
        for r in range(self._height):
            for c in range(self._width):
                if self._grid[r][c] == Tile.GHOST_HOUSE:
                    positions.append((r, c))
        return positions

    def get_ghost_door_position(self) -> Optional[Tuple[int, int]]:
        for r in range(self._height):
            for c in range(self._width):
                if self._grid[r][c] == Tile.GHOST_DOOR:
                    return (r, c)
        return None

    def reset(self) -> None:
        self._grid = copy.deepcopy(self._initial_grid)
