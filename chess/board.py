"""Chess board representation with make/unmake move support."""

import copy
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from pieces import Color, Piece, PieceType


@dataclass
class Move:
    """A chess move."""
    from_sq: Tuple[int, int]
    to_sq: Tuple[int, int]
    promotion: Optional[PieceType] = None
    is_castling: bool = False
    is_en_passant: bool = False


@dataclass
class UndoInfo:
    """Information needed to undo a move."""
    captured_piece: Optional[Piece]
    prev_castling_rights: Dict[Color, Dict[str, bool]]
    prev_en_passant: Optional[Tuple[int, int]]
    prev_halfmove_clock: int


class Board:
    """8x8 chess board. Row 0 = rank 8 (black's back rank), row 7 = rank 1 (white's back rank)."""

    def __init__(self) -> None:
        """Initialize board with starting position."""
        self.grid: List[List[Optional[Piece]]] = [[None] * 8 for _ in range(8)]
        self.turn: Color = Color.WHITE
        self.castling_rights: Dict[Color, Dict[str, bool]] = {
            Color.WHITE: {'king': True, 'queen': True},
            Color.BLACK: {'king': True, 'queen': True},
        }
        self.en_passant_target: Optional[Tuple[int, int]] = None
        self.halfmove_clock: int = 0
        self.fullmove_number: int = 1
        self._setup_starting_position()

    def _setup_starting_position(self) -> None:
        """Place all pieces in their starting positions."""
        back_rank = [PieceType.ROOK, PieceType.KNIGHT, PieceType.BISHOP,
                     PieceType.QUEEN, PieceType.KING, PieceType.BISHOP,
                     PieceType.KNIGHT, PieceType.ROOK]

        for col, pt in enumerate(back_rank):
            self.grid[0][col] = Piece(Color.BLACK, pt)
            self.grid[7][col] = Piece(Color.WHITE, pt)

        for col in range(8):
            self.grid[1][col] = Piece(Color.BLACK, PieceType.PAWN)
            self.grid[6][col] = Piece(Color.WHITE, PieceType.PAWN)

    def get_piece(self, row: int, col: int) -> Optional[Piece]:
        """Get piece at (row, col), or None if empty."""
        return self.grid[row][col]

    def set_piece(self, row: int, col: int, piece: Optional[Piece]) -> None:
        """Set piece at (row, col)."""
        self.grid[row][col] = piece

    def make_move(self, move: Move) -> UndoInfo:
        """Execute a move and return undo information."""
        fr, fc = move.from_sq
        tr, tc = move.to_sq
        piece = self.grid[fr][fc]
        captured = self.grid[tr][tc]

        # Save undo info
        undo = UndoInfo(
            captured_piece=captured,
            prev_castling_rights=copy.deepcopy(self.castling_rights),
            prev_en_passant=self.en_passant_target,
            prev_halfmove_clock=self.halfmove_clock,
        )

        # Handle en passant capture
        if move.is_en_passant:
            # The captured pawn is on the same row as the moving pawn, same col as target
            cap_row = fr
            captured = self.grid[cap_row][tc]
            undo.captured_piece = captured
            self.grid[cap_row][tc] = None

        # Move the piece
        self.grid[tr][tc] = piece
        self.grid[fr][fc] = None

        # Handle promotion
        if move.promotion and piece:
            self.grid[tr][tc] = Piece(piece.color, move.promotion)

        # Handle castling - move the rook
        if move.is_castling and piece:
            if tc == 6:  # Kingside
                self.grid[tr][5] = self.grid[tr][7]
                self.grid[tr][7] = None
            elif tc == 2:  # Queenside
                self.grid[tr][3] = self.grid[tr][0]
                self.grid[tr][0] = None

        # Update castling rights
        if piece:
            if piece.piece_type == PieceType.KING:
                self.castling_rights[piece.color]['king'] = False
                self.castling_rights[piece.color]['queen'] = False
            elif piece.piece_type == PieceType.ROOK:
                if fc == 0:
                    self.castling_rights[piece.color]['queen'] = False
                elif fc == 7:
                    self.castling_rights[piece.color]['king'] = False

        # If a rook is captured, remove that side's castling rights
        if captured and captured.piece_type == PieceType.ROOK:
            if tc == 0:
                self.castling_rights[captured.color]['queen'] = False
            elif tc == 7:
                self.castling_rights[captured.color]['king'] = False

        # Update en passant target
        if piece and piece.piece_type == PieceType.PAWN and abs(tr - fr) == 2:
            self.en_passant_target = ((fr + tr) // 2, fc)
        else:
            self.en_passant_target = None

        # Update halfmove clock
        if piece and (piece.piece_type == PieceType.PAWN or captured):
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1

        # Switch turn
        if self.turn == Color.BLACK:
            self.fullmove_number += 1
        self.turn = self.turn.opposite()

        return undo

    def unmake_move(self, move: Move, undo: UndoInfo) -> None:
        """Undo a move using saved undo information."""
        fr, fc = move.from_sq
        tr, tc = move.to_sq
        piece = self.grid[tr][tc]

        # Undo promotion - restore pawn
        if move.promotion and piece:
            piece = Piece(piece.color, PieceType.PAWN)

        # Move piece back
        self.grid[fr][fc] = piece
        self.grid[tr][tc] = undo.captured_piece

        # Undo en passant - restore captured pawn
        if move.is_en_passant:
            self.grid[tr][tc] = None
            self.grid[fr][tc] = undo.captured_piece

        # Undo castling - move rook back
        if move.is_castling:
            if tc == 6:  # Kingside
                self.grid[tr][7] = self.grid[tr][5]
                self.grid[tr][5] = None
            elif tc == 2:  # Queenside
                self.grid[tr][0] = self.grid[tr][3]
                self.grid[tr][3] = None

        # Restore state
        self.castling_rights = undo.prev_castling_rights
        self.en_passant_target = undo.prev_en_passant
        self.halfmove_clock = undo.prev_halfmove_clock
        self.turn = self.turn.opposite()
        if self.turn == Color.BLACK:
            self.fullmove_number -= 1

    def find_king(self, color: Color) -> Tuple[int, int]:
        """Find the position of the king of the given color."""
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p and p.color == color and p.piece_type == PieceType.KING:
                    return (r, c)
        raise ValueError(f"No {color} king found")

    def get_position_key(self) -> str:
        """Return a string key representing the current position (for repetition detection)."""
        parts = []
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p:
                    parts.append(f"{r}{c}{p.color.value}{p.piece_type.value}")
                else:
                    parts.append(f"{r}{c}.")
        parts.append(str(self.turn.value))
        parts.append(str(self.castling_rights))
        parts.append(str(self.en_passant_target))
        return '|'.join(parts)
