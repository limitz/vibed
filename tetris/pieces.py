"""Tetromino definitions, rotations, and wall kick data (SRS)."""

from enum import Enum, auto
from typing import List, Tuple


class PieceType(Enum):
    I = auto()
    O = auto()
    T = auto()
    S = auto()
    Z = auto()
    J = auto()
    L = auto()


# Each piece has 4 rotation states, each state is a list of (row, col) offsets
# Rotation 0 = spawn orientation
SHAPES = {
    PieceType.I: [
        [(0, 0), (0, 1), (0, 2), (0, 3)],       # horizontal
        [(0, 2), (1, 2), (2, 2), (3, 2)],         # vertical
        [(2, 0), (2, 1), (2, 2), (2, 3)],         # horizontal flipped
        [(0, 1), (1, 1), (2, 1), (3, 1)],         # vertical flipped
    ],
    PieceType.O: [
        [(0, 0), (0, 1), (1, 0), (1, 1)],
        [(0, 0), (0, 1), (1, 0), (1, 1)],
        [(0, 0), (0, 1), (1, 0), (1, 1)],
        [(0, 0), (0, 1), (1, 0), (1, 1)],
    ],
    PieceType.T: [
        [(0, 1), (1, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (1, 2), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (2, 1)],
        [(0, 1), (1, 0), (1, 1), (2, 1)],
    ],
    PieceType.S: [
        [(0, 1), (0, 2), (1, 0), (1, 1)],
        [(0, 1), (1, 1), (1, 2), (2, 2)],
        [(1, 1), (1, 2), (2, 0), (2, 1)],
        [(0, 0), (1, 0), (1, 1), (2, 1)],
    ],
    PieceType.Z: [
        [(0, 0), (0, 1), (1, 1), (1, 2)],
        [(0, 2), (1, 1), (1, 2), (2, 1)],
        [(1, 0), (1, 1), (2, 1), (2, 2)],
        [(0, 1), (1, 0), (1, 1), (2, 0)],
    ],
    PieceType.J: [
        [(0, 0), (1, 0), (1, 1), (1, 2)],
        [(0, 1), (0, 2), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (2, 2)],
        [(0, 1), (1, 1), (2, 0), (2, 1)],
    ],
    PieceType.L: [
        [(0, 2), (1, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (2, 2)],
        [(1, 0), (1, 1), (1, 2), (2, 0)],
        [(0, 0), (0, 1), (1, 1), (2, 1)],
    ],
}

# Color pair indices (will be mapped to curses colors in renderer)
COLORS = {
    PieceType.I: 1,   # cyan
    PieceType.O: 2,   # yellow
    PieceType.T: 3,   # magenta
    PieceType.S: 4,   # green
    PieceType.Z: 5,   # red
    PieceType.J: 6,   # blue
    PieceType.L: 7,   # white/orange
}

# SRS wall kick data
# For J, L, S, T, Z pieces
_JLSTZ_KICKS = {
    (0, 1): [(0, 0), (0, -1), (-1, -1), (2, 0), (2, -1)],
    (1, 0): [(0, 0), (0, 1), (1, 1), (-2, 0), (-2, 1)],
    (1, 2): [(0, 0), (0, 1), (-1, 1), (2, 0), (2, 1)],
    (2, 1): [(0, 0), (0, -1), (1, -1), (-2, 0), (-2, -1)],
    (2, 3): [(0, 0), (0, 1), (-1, 1), (2, 0), (2, 1)],
    (3, 2): [(0, 0), (0, -1), (1, -1), (-2, 0), (-2, -1)],
    (3, 0): [(0, 0), (0, -1), (-1, -1), (2, 0), (2, -1)],
    (0, 3): [(0, 0), (0, 1), (1, 1), (-2, 0), (-2, 1)],
}

# For I piece
_I_KICKS = {
    (0, 1): [(0, 0), (0, -2), (0, 1), (-1, -2), (2, 1)],
    (1, 0): [(0, 0), (0, 2), (0, -1), (1, 2), (-2, -1)],
    (1, 2): [(0, 0), (0, -1), (0, 2), (2, -1), (-1, 2)],
    (2, 1): [(0, 0), (0, 1), (0, -2), (-2, 1), (1, -2)],
    (2, 3): [(0, 0), (0, 2), (0, -1), (1, 2), (-2, -1)],
    (3, 2): [(0, 0), (0, -2), (0, 1), (-1, -2), (2, 1)],
    (3, 0): [(0, 0), (0, 1), (0, -2), (-2, 1), (1, -2)],
    (0, 3): [(0, 0), (0, -1), (0, 2), (2, -1), (-1, 2)],
}


def get_cells(piece_type: PieceType, rotation: int) -> List[Tuple[int, int]]:
    """Return the cell offsets for a piece in a given rotation state."""
    return SHAPES[piece_type][rotation % 4]


def rotate_cw(rotation: int) -> int:
    """Return the next clockwise rotation state."""
    return (rotation + 1) % 4


def rotate_ccw(rotation: int) -> int:
    """Return the next counter-clockwise rotation state."""
    return (rotation - 1) % 4


def get_wall_kicks(piece_type: PieceType, from_rot: int, to_rot: int) -> List[Tuple[int, int]]:
    """Return SRS wall kick offsets for a rotation transition."""
    if piece_type == PieceType.O:
        return [(0, 0)]
    key = (from_rot % 4, to_rot % 4)
    if piece_type == PieceType.I:
        return _I_KICKS[key]
    return _JLSTZ_KICKS[key]
