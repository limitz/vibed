"""Move generation, check detection, and game-ending condition detection."""

from typing import List, Optional, Tuple

from board import Board, Move
from pieces import Color, Piece, PieceType


# Direction vectors
KNIGHT_OFFSETS = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                  (1, -2), (1, 2), (2, -1), (2, 1)]
BISHOP_DIRS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
ROOK_DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
QUEEN_DIRS = BISHOP_DIRS + ROOK_DIRS
KING_OFFSETS = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                (0, 1), (1, -1), (1, 0), (1, 1)]

PROMOTION_PIECES = [PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP, PieceType.KNIGHT]
COL_NAMES = 'abcdefgh'
PIECE_LETTERS = {
    PieceType.KNIGHT: 'N', PieceType.BISHOP: 'B', PieceType.ROOK: 'R',
    PieceType.QUEEN: 'Q', PieceType.KING: 'K',
}


def _in_bounds(r: int, c: int) -> bool:
    return 0 <= r < 8 and 0 <= c < 8


def _slide_moves(board: Board, r: int, c: int, directions: list, color: Color) -> List[Move]:
    """Generate sliding moves along given directions."""
    moves = []
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        while _in_bounds(nr, nc):
            target = board.get_piece(nr, nc)
            if target is None:
                moves.append(Move((r, c), (nr, nc)))
            elif target.color != color:
                moves.append(Move((r, c), (nr, nc)))
                break
            else:
                break
            nr += dr
            nc += dc
    return moves


def _pawn_moves(board: Board, r: int, c: int, color: Color) -> List[Move]:
    """Generate pawn moves including promotion and en passant."""
    moves = []
    direction = -1 if color == Color.WHITE else 1
    start_row = 6 if color == Color.WHITE else 1
    promo_row = 0 if color == Color.WHITE else 7

    # Forward one
    nr = r + direction
    if _in_bounds(nr, c) and board.get_piece(nr, c) is None:
        if nr == promo_row:
            for pt in PROMOTION_PIECES:
                moves.append(Move((r, c), (nr, c), promotion=pt))
        else:
            moves.append(Move((r, c), (nr, c)))
            # Forward two from start
            if r == start_row:
                nnr = r + 2 * direction
                if board.get_piece(nnr, c) is None:
                    moves.append(Move((r, c), (nnr, c)))

    # Diagonal captures
    for dc in [-1, 1]:
        nc = c + dc
        nr = r + direction
        if not _in_bounds(nr, nc):
            continue
        target = board.get_piece(nr, nc)
        if target and target.color != color:
            if nr == promo_row:
                for pt in PROMOTION_PIECES:
                    moves.append(Move((r, c), (nr, nc), promotion=pt))
            else:
                moves.append(Move((r, c), (nr, nc)))
        # En passant
        if board.en_passant_target == (nr, nc):
            moves.append(Move((r, c), (nr, nc), is_en_passant=True))

    return moves


def _knight_moves(board: Board, r: int, c: int, color: Color) -> List[Move]:
    moves = []
    for dr, dc in KNIGHT_OFFSETS:
        nr, nc = r + dr, c + dc
        if _in_bounds(nr, nc):
            target = board.get_piece(nr, nc)
            if target is None or target.color != color:
                moves.append(Move((r, c), (nr, nc)))
    return moves


def _king_moves(board: Board, r: int, c: int, color: Color) -> List[Move]:
    moves = []
    for dr, dc in KING_OFFSETS:
        nr, nc = r + dr, c + dc
        if _in_bounds(nr, nc):
            target = board.get_piece(nr, nc)
            if target is None or target.color != color:
                moves.append(Move((r, c), (nr, nc)))

    # Castling
    back_rank = 7 if color == Color.WHITE else 0
    if r == back_rank and c == 4:
        # Kingside
        if board.castling_rights[color]['king']:
            if (board.get_piece(back_rank, 5) is None and
                    board.get_piece(back_rank, 6) is None and
                    board.get_piece(back_rank, 7) is not None):
                if (not is_square_attacked(board, back_rank, 4, color.opposite()) and
                        not is_square_attacked(board, back_rank, 5, color.opposite()) and
                        not is_square_attacked(board, back_rank, 6, color.opposite())):
                    moves.append(Move((r, c), (back_rank, 6), is_castling=True))
        # Queenside
        if board.castling_rights[color]['queen']:
            if (board.get_piece(back_rank, 1) is None and
                    board.get_piece(back_rank, 2) is None and
                    board.get_piece(back_rank, 3) is None and
                    board.get_piece(back_rank, 0) is not None):
                if (not is_square_attacked(board, back_rank, 4, color.opposite()) and
                        not is_square_attacked(board, back_rank, 3, color.opposite()) and
                        not is_square_attacked(board, back_rank, 2, color.opposite())):
                    moves.append(Move((r, c), (back_rank, 2), is_castling=True))

    return moves


def get_pseudo_legal_moves(board: Board, color: Color) -> List[Move]:
    """Generate all pseudo-legal moves (may leave king in check)."""
    moves = []
    for r in range(8):
        for c in range(8):
            piece = board.get_piece(r, c)
            if piece is None or piece.color != color:
                continue
            pt = piece.piece_type
            if pt == PieceType.PAWN:
                moves.extend(_pawn_moves(board, r, c, color))
            elif pt == PieceType.KNIGHT:
                moves.extend(_knight_moves(board, r, c, color))
            elif pt == PieceType.BISHOP:
                moves.extend(_slide_moves(board, r, c, BISHOP_DIRS, color))
            elif pt == PieceType.ROOK:
                moves.extend(_slide_moves(board, r, c, ROOK_DIRS, color))
            elif pt == PieceType.QUEEN:
                moves.extend(_slide_moves(board, r, c, QUEEN_DIRS, color))
            elif pt == PieceType.KING:
                moves.extend(_king_moves(board, r, c, color))
    return moves


def is_square_attacked(board: Board, row: int, col: int, by_color: Color) -> bool:
    """Check if a square is attacked by any piece of the given color."""
    # Knight attacks
    for dr, dc in KNIGHT_OFFSETS:
        nr, nc = row + dr, col + dc
        if _in_bounds(nr, nc):
            p = board.get_piece(nr, nc)
            if p and p.color == by_color and p.piece_type == PieceType.KNIGHT:
                return True

    # Pawn attacks
    # White pawns move upward (row decreases) and attack diagonally upward
    # Black pawns move downward (row increases) and attack diagonally downward
    # So a pawn of by_color attacks this square if the pawn is one row "behind"
    pawn_row_offset = 1 if by_color == Color.WHITE else -1  # row offset to find attacking pawn
    for dc in [-1, 1]:
        pr, pc = row + pawn_row_offset, col + dc
        if _in_bounds(pr, pc):
            p = board.get_piece(pr, pc)
            if p and p.color == by_color and p.piece_type == PieceType.PAWN:
                return True

    # King attacks
    for dr, dc in KING_OFFSETS:
        nr, nc = row + dr, col + dc
        if _in_bounds(nr, nc):
            p = board.get_piece(nr, nc)
            if p and p.color == by_color and p.piece_type == PieceType.KING:
                return True

    # Sliding attacks (bishop/queen diagonals, rook/queen orthogonals)
    for dr, dc in BISHOP_DIRS:
        nr, nc = row + dr, col + dc
        while _in_bounds(nr, nc):
            p = board.get_piece(nr, nc)
            if p:
                if p.color == by_color and p.piece_type in (PieceType.BISHOP, PieceType.QUEEN):
                    return True
                break
            nr += dr
            nc += dc

    for dr, dc in ROOK_DIRS:
        nr, nc = row + dr, col + dc
        while _in_bounds(nr, nc):
            p = board.get_piece(nr, nc)
            if p:
                if p.color == by_color and p.piece_type in (PieceType.ROOK, PieceType.QUEEN):
                    return True
                break
            nr += dr
            nc += dc

    return False


def is_in_check(board: Board, color: Color) -> bool:
    """Check if the given color's king is in check."""
    king_pos = board.find_king(color)
    return is_square_attacked(board, king_pos[0], king_pos[1], color.opposite())


def get_legal_moves(board: Board, color: Color) -> List[Move]:
    """Generate all legal moves for the given color."""
    pseudo = get_pseudo_legal_moves(board, color)
    legal = []
    for move in pseudo:
        undo = board.make_move(move)
        if not is_in_check(board, color):
            legal.append(move)
        board.unmake_move(move, undo)
    return legal


def is_checkmate(board: Board, color: Color) -> bool:
    """Check if the given color is in checkmate."""
    return is_in_check(board, color) and len(get_legal_moves(board, color)) == 0


def is_stalemate(board: Board, color: Color) -> bool:
    """Check if the given color is in stalemate."""
    return not is_in_check(board, color) and len(get_legal_moves(board, color)) == 0


def move_to_algebraic(board: Board, move: Move) -> str:
    """Convert a move to algebraic notation (e.g., 'Nf3', 'e4', 'O-O')."""
    if move.is_castling:
        return "O-O" if move.to_sq[1] == 6 else "O-O-O"

    piece = board.get_piece(move.from_sq[0], move.from_sq[1])
    if piece is None:
        return "???"

    dest_col = COL_NAMES[move.to_sq[1]]
    dest_row = str(8 - move.to_sq[0])
    dest = dest_col + dest_row

    captured = board.get_piece(move.to_sq[0], move.to_sq[1])
    is_capture = captured is not None or move.is_en_passant

    if piece.piece_type == PieceType.PAWN:
        result = ""
        if is_capture:
            result = COL_NAMES[move.from_sq[1]] + "x"
        result += dest
        if move.promotion:
            result += "=" + PIECE_LETTERS.get(move.promotion, "?")
        return result
    else:
        letter = PIECE_LETTERS.get(piece.piece_type, "?")
        capture_str = "x" if is_capture else ""
        return letter + capture_str + dest
