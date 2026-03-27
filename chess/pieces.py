"""Chess piece definitions: enums, dataclass, symbols, values, and piece-square tables."""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Tuple


class Color(Enum):
    """Player color."""
    WHITE = auto()
    BLACK = auto()

    def opposite(self) -> 'Color':
        """Return the opposite color."""
        return Color.BLACK if self == Color.WHITE else Color.WHITE


class PieceType(Enum):
    """Chess piece types."""
    PAWN = auto()
    KNIGHT = auto()
    BISHOP = auto()
    ROOK = auto()
    QUEEN = auto()
    KING = auto()


@dataclass(frozen=True)
class Piece:
    """A chess piece with color and type."""
    color: Color
    piece_type: PieceType

    def symbol(self) -> str:
        """Return the Unicode symbol for this piece."""
        return UNICODE_SYMBOLS[(self.color, self.piece_type)]

    def value(self) -> int:
        """Return the material value of this piece."""
        return PIECE_VALUES[self.piece_type]


# Unicode chess symbols
UNICODE_SYMBOLS: Dict[Tuple[Color, PieceType], str] = {
    (Color.WHITE, PieceType.KING):   '\u2654',
    (Color.WHITE, PieceType.QUEEN):  '\u2655',
    (Color.WHITE, PieceType.ROOK):   '\u2656',
    (Color.WHITE, PieceType.BISHOP): '\u2657',
    (Color.WHITE, PieceType.KNIGHT): '\u2658',
    (Color.WHITE, PieceType.PAWN):   '\u2659',
    (Color.BLACK, PieceType.KING):   '\u265a',
    (Color.BLACK, PieceType.QUEEN):  '\u265b',
    (Color.BLACK, PieceType.ROOK):   '\u265c',
    (Color.BLACK, PieceType.BISHOP): '\u265d',
    (Color.BLACK, PieceType.KNIGHT): '\u265e',
    (Color.BLACK, PieceType.PAWN):   '\u265f',
}

# Material values
PIECE_VALUES: Dict[PieceType, int] = {
    PieceType.PAWN:   100,
    PieceType.KNIGHT: 320,
    PieceType.BISHOP: 330,
    PieceType.ROOK:   500,
    PieceType.QUEEN:  900,
    PieceType.KING:   20000,
}

# Piece-square tables (from white's perspective, row 0 = rank 8)
# For black, mirror vertically (read row 7 as row 0, etc.)
PIECE_SQUARE_TABLES: Dict[PieceType, List[List[int]]] = {
    PieceType.PAWN: [
        [  0,   0,   0,   0,   0,   0,   0,   0],
        [ 50,  50,  50,  50,  50,  50,  50,  50],
        [ 10,  10,  20,  30,  30,  20,  10,  10],
        [  5,   5,  10,  25,  25,  10,   5,   5],
        [  0,   0,   0,  20,  20,   0,   0,   0],
        [  5,  -5, -10,   0,   0, -10,  -5,   5],
        [  5,  10,  10, -20, -20,  10,  10,   5],
        [  0,   0,   0,   0,   0,   0,   0,   0],
    ],
    PieceType.KNIGHT: [
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20,   0,   0,   0,   0, -20, -40],
        [-30,   0,  10,  15,  15,  10,   0, -30],
        [-30,   5,  15,  20,  20,  15,   5, -30],
        [-30,   0,  15,  20,  20,  15,   0, -30],
        [-30,   5,  10,  15,  15,  10,   5, -30],
        [-40, -20,   0,   5,   5,   0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50],
    ],
    PieceType.BISHOP: [
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10,   0,   0,   0,   0,   0,   0, -10],
        [-10,   0,  10,  10,  10,  10,   0, -10],
        [-10,   5,   5,  10,  10,   5,   5, -10],
        [-10,   0,   5,  10,  10,   5,   0, -10],
        [-10,  10,  10,  10,  10,  10,  10, -10],
        [-10,   5,   0,   0,   0,   0,   5, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20],
    ],
    PieceType.ROOK: [
        [  0,   0,   0,   0,   0,   0,   0,   0],
        [  5,  10,  10,  10,  10,  10,  10,   5],
        [ -5,   0,   0,   0,   0,   0,   0,  -5],
        [ -5,   0,   0,   0,   0,   0,   0,  -5],
        [ -5,   0,   0,   0,   0,   0,   0,  -5],
        [ -5,   0,   0,   0,   0,   0,   0,  -5],
        [ -5,   0,   0,   0,   0,   0,   0,  -5],
        [  0,   0,   0,   5,   5,   0,   0,   0],
    ],
    PieceType.QUEEN: [
        [-20, -10, -10,  -5,  -5, -10, -10, -20],
        [-10,   0,   0,   0,   0,   0,   0, -10],
        [-10,   0,   5,   5,   5,   5,   0, -10],
        [ -5,   0,   5,   5,   5,   5,   0,  -5],
        [  0,   0,   5,   5,   5,   5,   0,  -5],
        [-10,   5,   5,   5,   5,   5,   0, -10],
        [-10,   0,   5,   0,   0,   0,   0, -10],
        [-20, -10, -10,  -5,  -5, -10, -10, -20],
    ],
    PieceType.KING: [
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-20, -30, -30, -40, -40, -30, -30, -20],
        [-10, -20, -20, -20, -20, -20, -20, -10],
        [ 20,  20,   0,   0,   0,   0,  20,  20],
        [ 20,  30,  10,   0,   0,  10,  30,  20],
    ],
}
