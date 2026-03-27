"""Tests for moves module."""

import pytest
from board import Board, Move
from pieces import Color, Piece, PieceType
from moves import (
    get_pseudo_legal_moves, get_legal_moves, is_square_attacked,
    is_in_check, is_checkmate, is_stalemate, move_to_algebraic,
)


def empty_board():
    """Create an empty board (no pieces)."""
    b = Board()
    for r in range(8):
        for c in range(8):
            b.grid[r][c] = None
    b.castling_rights = {
        Color.WHITE: {'king': False, 'queen': False},
        Color.BLACK: {'king': False, 'queen': False},
    }
    return b


class TestPawnMoves:
    def test_white_pawn_forward_one(self):
        b = empty_board()
        b.set_piece(6, 4, Piece(Color.WHITE, PieceType.PAWN))
        b.set_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        b.set_piece(0, 4, Piece(Color.BLACK, PieceType.KING))
        moves = get_legal_moves(b, Color.WHITE)
        targets = {m.to_sq for m in moves if m.from_sq == (6, 4)}
        assert (5, 4) in targets

    def test_white_pawn_forward_two_from_start(self):
        b = empty_board()
        b.set_piece(6, 4, Piece(Color.WHITE, PieceType.PAWN))
        b.set_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        b.set_piece(0, 4, Piece(Color.BLACK, PieceType.KING))
        moves = get_legal_moves(b, Color.WHITE)
        targets = {m.to_sq for m in moves if m.from_sq == (6, 4)}
        assert (4, 4) in targets

    def test_white_pawn_blocked(self):
        b = empty_board()
        b.set_piece(6, 4, Piece(Color.WHITE, PieceType.PAWN))
        b.set_piece(5, 4, Piece(Color.BLACK, PieceType.PAWN))
        b.set_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        b.set_piece(0, 4, Piece(Color.BLACK, PieceType.KING))
        moves = get_legal_moves(b, Color.WHITE)
        pawn_moves = [m for m in moves if m.from_sq == (6, 4)]
        forward = [m for m in pawn_moves if m.to_sq[1] == 4]
        assert len(forward) == 0

    def test_white_pawn_diagonal_capture(self):
        b = empty_board()
        b.set_piece(4, 4, Piece(Color.WHITE, PieceType.PAWN))
        b.set_piece(3, 5, Piece(Color.BLACK, PieceType.PAWN))
        b.set_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        b.set_piece(0, 4, Piece(Color.BLACK, PieceType.KING))
        moves = get_legal_moves(b, Color.WHITE)
        targets = {m.to_sq for m in moves if m.from_sq == (4, 4)}
        assert (3, 5) in targets

    def test_en_passant(self):
        b = empty_board()
        b.set_piece(3, 4, Piece(Color.WHITE, PieceType.PAWN))
        b.set_piece(3, 3, Piece(Color.BLACK, PieceType.PAWN))
        b.en_passant_target = (2, 3)
        b.set_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        b.set_piece(0, 4, Piece(Color.BLACK, PieceType.KING))
        moves = get_legal_moves(b, Color.WHITE)
        ep_moves = [m for m in moves if m.is_en_passant]
        assert len(ep_moves) == 1
        assert ep_moves[0].to_sq == (2, 3)

    def test_promotion_generates_four_moves(self):
        b = empty_board()
        b.set_piece(1, 0, Piece(Color.WHITE, PieceType.PAWN))
        b.set_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        b.set_piece(0, 4, Piece(Color.BLACK, PieceType.KING))
        moves = get_legal_moves(b, Color.WHITE)
        promo_moves = [m for m in moves if m.from_sq == (1, 0) and m.promotion]
        assert len(promo_moves) == 4
        promo_types = {m.promotion for m in promo_moves}
        assert promo_types == {PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP, PieceType.KNIGHT}

    def test_black_pawn_forward(self):
        b = empty_board()
        b.set_piece(1, 4, Piece(Color.BLACK, PieceType.PAWN))
        b.set_piece(0, 4, Piece(Color.BLACK, PieceType.KING))
        b.set_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        b.turn = Color.BLACK
        moves = get_legal_moves(b, Color.BLACK)
        targets = {m.to_sq for m in moves if m.from_sq == (1, 4)}
        assert (2, 4) in targets
        assert (3, 4) in targets


class TestKnightMoves:
    def test_center_knight(self):
        b = empty_board()
        b.set_piece(4, 4, Piece(Color.WHITE, PieceType.KNIGHT))
        b.set_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        b.set_piece(0, 4, Piece(Color.BLACK, PieceType.KING))
        moves = get_legal_moves(b, Color.WHITE)
        knight_moves = [m for m in moves if m.from_sq == (4, 4)]
        assert len(knight_moves) == 8

    def test_corner_knight(self):
        b = empty_board()
        b.set_piece(0, 0, Piece(Color.WHITE, PieceType.KNIGHT))
        b.set_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        b.set_piece(0, 7, Piece(Color.BLACK, PieceType.KING))
        moves = get_legal_moves(b, Color.WHITE)
        knight_moves = [m for m in moves if m.from_sq == (0, 0)]
        assert len(knight_moves) == 2

    def test_knight_no_friendly_capture(self):
        b = empty_board()
        b.set_piece(4, 4, Piece(Color.WHITE, PieceType.KNIGHT))
        b.set_piece(2, 3, Piece(Color.WHITE, PieceType.PAWN))
        b.set_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        b.set_piece(0, 4, Piece(Color.BLACK, PieceType.KING))
        moves = get_legal_moves(b, Color.WHITE)
        knight_targets = {m.to_sq for m in moves if m.from_sq == (4, 4)}
        assert (2, 3) not in knight_targets


class TestBishopMoves:
    def test_bishop_sliding(self):
        b = empty_board()
        b.set_piece(4, 4, Piece(Color.WHITE, PieceType.BISHOP))
        b.set_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        b.set_piece(0, 4, Piece(Color.BLACK, PieceType.KING))
        moves = get_legal_moves(b, Color.WHITE)
        bishop_moves = [m for m in moves if m.from_sq == (4, 4)]
        assert len(bishop_moves) == 13  # diagonals from e4

    def test_bishop_blocked(self):
        b = empty_board()
        b.set_piece(4, 4, Piece(Color.WHITE, PieceType.BISHOP))
        b.set_piece(3, 3, Piece(Color.WHITE, PieceType.PAWN))
        b.set_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        b.set_piece(0, 4, Piece(Color.BLACK, PieceType.KING))
        moves = get_legal_moves(b, Color.WHITE)
        bishop_targets = {m.to_sq for m in moves if m.from_sq == (4, 4)}
        assert (3, 3) not in bishop_targets
        assert (2, 2) not in bishop_targets


class TestRookMoves:
    def test_rook_sliding(self):
        b = empty_board()
        b.set_piece(4, 4, Piece(Color.WHITE, PieceType.ROOK))
        b.set_piece(7, 0, Piece(Color.WHITE, PieceType.KING))
        b.set_piece(0, 0, Piece(Color.BLACK, PieceType.KING))
        moves = get_legal_moves(b, Color.WHITE)
        rook_moves = [m for m in moves if m.from_sq == (4, 4)]
        assert len(rook_moves) == 14  # 7 horizontal + 7 vertical

    def test_rook_captures_enemy(self):
        b = empty_board()
        b.set_piece(4, 4, Piece(Color.WHITE, PieceType.ROOK))
        b.set_piece(4, 6, Piece(Color.BLACK, PieceType.PAWN))
        b.set_piece(7, 0, Piece(Color.WHITE, PieceType.KING))
        b.set_piece(0, 0, Piece(Color.BLACK, PieceType.KING))
        moves = get_legal_moves(b, Color.WHITE)
        rook_targets = {m.to_sq for m in moves if m.from_sq == (4, 4)}
        assert (4, 6) in rook_targets  # can capture
        assert (4, 7) not in rook_targets  # blocked after capture


class TestQueenMoves:
    def test_queen_combines_rook_and_bishop(self):
        b = empty_board()
        b.set_piece(4, 4, Piece(Color.WHITE, PieceType.QUEEN))
        b.set_piece(7, 0, Piece(Color.WHITE, PieceType.KING))
        b.set_piece(0, 0, Piece(Color.BLACK, PieceType.KING))
        moves = get_legal_moves(b, Color.WHITE)
        queen_moves = [m for m in moves if m.from_sq == (4, 4)]
        assert len(queen_moves) == 27  # 14 rook + 13 bishop


class TestKingMoves:
    def test_king_basic_moves(self):
        b = empty_board()
        b.set_piece(4, 4, Piece(Color.WHITE, PieceType.KING))
        b.set_piece(0, 0, Piece(Color.BLACK, PieceType.KING))
        moves = get_legal_moves(b, Color.WHITE)
        king_moves = [m for m in moves if m.from_sq == (4, 4)]
        assert len(king_moves) == 8

    def test_king_no_move_into_check(self):
        b = empty_board()
        b.set_piece(4, 4, Piece(Color.WHITE, PieceType.KING))
        b.set_piece(0, 0, Piece(Color.BLACK, PieceType.KING))
        b.set_piece(2, 5, Piece(Color.BLACK, PieceType.ROOK))  # attacks col 5
        moves = get_legal_moves(b, Color.WHITE)
        king_targets = {m.to_sq for m in moves if m.from_sq == (4, 4)}
        assert (4, 5) not in king_targets
        assert (3, 5) not in king_targets
        assert (5, 5) not in king_targets


class TestCastling:
    def test_kingside_castling(self):
        b = empty_board()
        b.set_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        b.set_piece(7, 7, Piece(Color.WHITE, PieceType.ROOK))
        b.set_piece(0, 4, Piece(Color.BLACK, PieceType.KING))
        b.castling_rights[Color.WHITE]['king'] = True
        moves = get_legal_moves(b, Color.WHITE)
        castle_moves = [m for m in moves if m.is_castling]
        assert any(m.to_sq == (7, 6) for m in castle_moves)

    def test_queenside_castling(self):
        b = empty_board()
        b.set_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        b.set_piece(7, 0, Piece(Color.WHITE, PieceType.ROOK))
        b.set_piece(0, 4, Piece(Color.BLACK, PieceType.KING))
        b.castling_rights[Color.WHITE]['queen'] = True
        moves = get_legal_moves(b, Color.WHITE)
        castle_moves = [m for m in moves if m.is_castling]
        assert any(m.to_sq == (7, 2) for m in castle_moves)

    def test_no_castling_through_pieces(self):
        b = empty_board()
        b.set_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        b.set_piece(7, 7, Piece(Color.WHITE, PieceType.ROOK))
        b.set_piece(7, 5, Piece(Color.WHITE, PieceType.BISHOP))
        b.set_piece(0, 4, Piece(Color.BLACK, PieceType.KING))
        b.castling_rights[Color.WHITE]['king'] = True
        moves = get_legal_moves(b, Color.WHITE)
        castle_moves = [m for m in moves if m.is_castling]
        assert len(castle_moves) == 0

    def test_no_castling_when_in_check(self):
        b = empty_board()
        b.set_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        b.set_piece(7, 7, Piece(Color.WHITE, PieceType.ROOK))
        b.set_piece(0, 4, Piece(Color.BLACK, PieceType.ROOK))  # checking the king
        b.castling_rights[Color.WHITE]['king'] = True
        moves = get_legal_moves(b, Color.WHITE)
        castle_moves = [m for m in moves if m.is_castling]
        assert len(castle_moves) == 0

    def test_no_castling_through_attacked_square(self):
        b = empty_board()
        b.set_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        b.set_piece(7, 7, Piece(Color.WHITE, PieceType.ROOK))
        b.set_piece(0, 5, Piece(Color.BLACK, PieceType.ROOK))  # attacks f1
        b.set_piece(0, 0, Piece(Color.BLACK, PieceType.KING))
        b.castling_rights[Color.WHITE]['king'] = True
        moves = get_legal_moves(b, Color.WHITE)
        castle_moves = [m for m in moves if m.is_castling]
        assert len(castle_moves) == 0

    def test_no_castling_without_rights(self):
        b = empty_board()
        b.set_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        b.set_piece(7, 7, Piece(Color.WHITE, PieceType.ROOK))
        b.set_piece(0, 4, Piece(Color.BLACK, PieceType.KING))
        b.castling_rights[Color.WHITE]['king'] = False
        moves = get_legal_moves(b, Color.WHITE)
        castle_moves = [m for m in moves if m.is_castling]
        assert len(castle_moves) == 0


class TestCheckDetection:
    def test_is_square_attacked_by_rook(self):
        b = empty_board()
        b.set_piece(0, 4, Piece(Color.BLACK, PieceType.ROOK))
        assert is_square_attacked(b, 7, 4, Color.BLACK) is True
        assert is_square_attacked(b, 0, 0, Color.BLACK) is True
        assert is_square_attacked(b, 3, 3, Color.BLACK) is False

    def test_is_square_attacked_by_knight(self):
        b = empty_board()
        b.set_piece(4, 4, Piece(Color.BLACK, PieceType.KNIGHT))
        assert is_square_attacked(b, 2, 3, Color.BLACK) is True
        assert is_square_attacked(b, 3, 3, Color.BLACK) is False

    def test_is_square_attacked_by_pawn(self):
        b = empty_board()
        b.set_piece(3, 4, Piece(Color.BLACK, PieceType.PAWN))
        # Black pawn attacks diagonally forward (downward)
        assert is_square_attacked(b, 4, 3, Color.BLACK) is True
        assert is_square_attacked(b, 4, 5, Color.BLACK) is True
        assert is_square_attacked(b, 2, 3, Color.BLACK) is False

    def test_is_in_check(self):
        b = empty_board()
        b.set_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        b.set_piece(0, 4, Piece(Color.BLACK, PieceType.ROOK))
        assert is_in_check(b, Color.WHITE) is True

    def test_not_in_check(self):
        b = empty_board()
        b.set_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        b.set_piece(0, 3, Piece(Color.BLACK, PieceType.ROOK))
        assert is_in_check(b, Color.WHITE) is False


class TestLegalMoves:
    def test_pinned_piece_cannot_move(self):
        b = empty_board()
        b.set_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        b.set_piece(6, 4, Piece(Color.WHITE, PieceType.BISHOP))  # pinned by rook
        b.set_piece(0, 4, Piece(Color.BLACK, PieceType.ROOK))
        b.set_piece(0, 0, Piece(Color.BLACK, PieceType.KING))
        moves = get_legal_moves(b, Color.WHITE)
        bishop_moves = [m for m in moves if m.from_sq == (6, 4)]
        assert len(bishop_moves) == 0

    def test_must_block_or_capture_in_check(self):
        b = empty_board()
        b.set_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        b.set_piece(6, 3, Piece(Color.WHITE, PieceType.ROOK))
        b.set_piece(0, 4, Piece(Color.BLACK, PieceType.ROOK))  # checking
        b.set_piece(0, 0, Piece(Color.BLACK, PieceType.KING))
        moves = get_legal_moves(b, Color.WHITE)
        # King can move, and rook can block on col 4
        rook_moves = [m for m in moves if m.from_sq == (6, 3)]
        assert all(m.to_sq[1] == 4 for m in rook_moves)  # rook must move to col 4

    def test_starting_position_move_count(self):
        b = Board()
        moves = get_legal_moves(b, Color.WHITE)
        assert len(moves) == 20  # 16 pawn moves + 4 knight moves


class TestCheckmate:
    def test_scholars_mate(self):
        """Test scholar's mate: Qxf7# with bishop support, all escape blocked."""
        b = empty_board()
        # Standard scholar's mate position after 1.e4 e5 2.Bc4 Nc6 3.Qh5 Nf6?? 4.Qxf7#
        b.set_piece(0, 4, Piece(Color.BLACK, PieceType.KING))
        b.set_piece(1, 5, Piece(Color.WHITE, PieceType.QUEEN))  # Qf7#
        b.set_piece(4, 2, Piece(Color.WHITE, PieceType.BISHOP))  # Bc4 supports
        b.set_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        # Black pieces blocking king escape
        b.set_piece(0, 3, Piece(Color.BLACK, PieceType.QUEEN))
        b.set_piece(1, 3, Piece(Color.BLACK, PieceType.PAWN))
        b.set_piece(1, 4, Piece(Color.BLACK, PieceType.PAWN))
        b.set_piece(0, 5, Piece(Color.BLACK, PieceType.BISHOP))
        b.turn = Color.BLACK
        assert is_checkmate(b, Color.BLACK) is True

    def test_back_rank_mate(self):
        b = empty_board()
        b.set_piece(0, 7, Piece(Color.BLACK, PieceType.KING))
        b.set_piece(1, 5, Piece(Color.BLACK, PieceType.PAWN))
        b.set_piece(1, 6, Piece(Color.BLACK, PieceType.PAWN))
        b.set_piece(1, 7, Piece(Color.BLACK, PieceType.PAWN))
        b.set_piece(0, 0, Piece(Color.WHITE, PieceType.ROOK))  # back rank mate
        b.set_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        b.turn = Color.BLACK
        assert is_checkmate(b, Color.BLACK) is True

    def test_not_checkmate_can_block(self):
        b = empty_board()
        b.set_piece(0, 7, Piece(Color.BLACK, PieceType.KING))
        b.set_piece(1, 6, Piece(Color.BLACK, PieceType.PAWN))
        b.set_piece(1, 7, Piece(Color.BLACK, PieceType.PAWN))
        b.set_piece(0, 0, Piece(Color.WHITE, PieceType.ROOK))
        b.set_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        b.set_piece(5, 3, Piece(Color.BLACK, PieceType.ROOK))  # can block
        b.turn = Color.BLACK
        assert is_checkmate(b, Color.BLACK) is False


class TestStalemate:
    def test_stalemate(self):
        b = empty_board()
        b.set_piece(0, 0, Piece(Color.BLACK, PieceType.KING))
        b.set_piece(2, 1, Piece(Color.WHITE, PieceType.QUEEN))
        b.set_piece(7, 7, Piece(Color.WHITE, PieceType.KING))
        b.turn = Color.BLACK
        assert is_stalemate(b, Color.BLACK) is True
        assert is_checkmate(b, Color.BLACK) is False

    def test_not_stalemate_has_moves(self):
        b = empty_board()
        b.set_piece(0, 0, Piece(Color.BLACK, PieceType.KING))
        b.set_piece(7, 7, Piece(Color.WHITE, PieceType.KING))
        b.turn = Color.BLACK
        assert is_stalemate(b, Color.BLACK) is False


class TestMoveToAlgebraic:
    def test_pawn_move(self):
        b = Board()
        move = Move((6, 4), (4, 4))  # e2-e4
        notation = move_to_algebraic(b, move)
        assert notation == "e4"

    def test_knight_move(self):
        b = Board()
        move = Move((7, 1), (5, 2))  # Nb1-c3
        notation = move_to_algebraic(b, move)
        assert notation == "Nc3"

    def test_capture(self):
        b = empty_board()
        b.set_piece(4, 4, Piece(Color.WHITE, PieceType.PAWN))
        b.set_piece(3, 5, Piece(Color.BLACK, PieceType.PAWN))
        b.set_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        b.set_piece(0, 4, Piece(Color.BLACK, PieceType.KING))
        move = Move((4, 4), (3, 5))
        notation = move_to_algebraic(b, move)
        assert notation == "exf5"

    def test_kingside_castling(self):
        b = Board()
        move = Move((7, 4), (7, 6), is_castling=True)
        notation = move_to_algebraic(b, move)
        assert notation == "O-O"

    def test_queenside_castling(self):
        b = Board()
        move = Move((7, 4), (7, 2), is_castling=True)
        notation = move_to_algebraic(b, move)
        assert notation == "O-O-O"

    def test_promotion(self):
        b = empty_board()
        b.set_piece(1, 0, Piece(Color.WHITE, PieceType.PAWN))
        b.set_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        b.set_piece(0, 4, Piece(Color.BLACK, PieceType.KING))
        move = Move((1, 0), (0, 0), promotion=PieceType.QUEEN)
        notation = move_to_algebraic(b, move)
        assert notation == "a8=Q"
