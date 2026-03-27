"""Tests for board module."""

import copy
import pytest
from board import Board, Move, UndoInfo
from pieces import Color, Piece, PieceType


class TestBoardInit:
    def test_dimensions(self):
        b = Board()
        assert len(b.grid) == 8
        for row in b.grid:
            assert len(row) == 8

    def test_white_back_rank(self):
        b = Board()
        assert b.get_piece(7, 0) == Piece(Color.WHITE, PieceType.ROOK)
        assert b.get_piece(7, 1) == Piece(Color.WHITE, PieceType.KNIGHT)
        assert b.get_piece(7, 2) == Piece(Color.WHITE, PieceType.BISHOP)
        assert b.get_piece(7, 3) == Piece(Color.WHITE, PieceType.QUEEN)
        assert b.get_piece(7, 4) == Piece(Color.WHITE, PieceType.KING)
        assert b.get_piece(7, 5) == Piece(Color.WHITE, PieceType.BISHOP)
        assert b.get_piece(7, 6) == Piece(Color.WHITE, PieceType.KNIGHT)
        assert b.get_piece(7, 7) == Piece(Color.WHITE, PieceType.ROOK)

    def test_black_back_rank(self):
        b = Board()
        assert b.get_piece(0, 0) == Piece(Color.BLACK, PieceType.ROOK)
        assert b.get_piece(0, 1) == Piece(Color.BLACK, PieceType.KNIGHT)
        assert b.get_piece(0, 2) == Piece(Color.BLACK, PieceType.BISHOP)
        assert b.get_piece(0, 3) == Piece(Color.BLACK, PieceType.QUEEN)
        assert b.get_piece(0, 4) == Piece(Color.BLACK, PieceType.KING)
        assert b.get_piece(0, 5) == Piece(Color.BLACK, PieceType.BISHOP)
        assert b.get_piece(0, 6) == Piece(Color.BLACK, PieceType.KNIGHT)
        assert b.get_piece(0, 7) == Piece(Color.BLACK, PieceType.ROOK)

    def test_white_pawns(self):
        b = Board()
        for col in range(8):
            assert b.get_piece(6, col) == Piece(Color.WHITE, PieceType.PAWN)

    def test_black_pawns(self):
        b = Board()
        for col in range(8):
            assert b.get_piece(1, col) == Piece(Color.BLACK, PieceType.PAWN)

    def test_empty_middle(self):
        b = Board()
        for row in range(2, 6):
            for col in range(8):
                assert b.get_piece(row, col) is None

    def test_initial_turn_white(self):
        b = Board()
        assert b.turn == Color.WHITE

    def test_initial_castling_rights(self):
        b = Board()
        for color in Color:
            assert b.castling_rights[color]['king'] is True
            assert b.castling_rights[color]['queen'] is True

    def test_initial_en_passant_none(self):
        b = Board()
        assert b.en_passant_target is None


class TestGetSetPiece:
    def test_get_piece(self):
        b = Board()
        assert b.get_piece(7, 4) == Piece(Color.WHITE, PieceType.KING)

    def test_get_empty(self):
        b = Board()
        assert b.get_piece(4, 4) is None

    def test_set_piece(self):
        b = Board()
        p = Piece(Color.WHITE, PieceType.QUEEN)
        b.set_piece(4, 4, p)
        assert b.get_piece(4, 4) == p

    def test_set_none_clears(self):
        b = Board()
        b.set_piece(7, 0, None)
        assert b.get_piece(7, 0) is None


class TestMakeMove:
    def test_simple_move(self):
        b = Board()
        move = Move((6, 4), (4, 4))  # e2-e4
        b.make_move(move)
        assert b.get_piece(4, 4) == Piece(Color.WHITE, PieceType.PAWN)
        assert b.get_piece(6, 4) is None

    def test_capture(self):
        b = Board()
        # Set up a capture scenario
        b.set_piece(4, 4, Piece(Color.WHITE, PieceType.PAWN))
        b.set_piece(3, 5, Piece(Color.BLACK, PieceType.PAWN))
        move = Move((4, 4), (3, 5))
        undo = b.make_move(move)
        assert b.get_piece(3, 5) == Piece(Color.WHITE, PieceType.PAWN)
        assert b.get_piece(4, 4) is None
        assert undo.captured_piece == Piece(Color.BLACK, PieceType.PAWN)

    def test_pawn_double_push_sets_en_passant(self):
        b = Board()
        move = Move((6, 4), (4, 4))  # e2-e4
        b.make_move(move)
        assert b.en_passant_target == (5, 4)

    def test_single_pawn_push_no_en_passant(self):
        b = Board()
        move = Move((6, 4), (5, 4))  # e2-e3
        b.make_move(move)
        assert b.en_passant_target is None

    def test_en_passant_capture(self):
        b = Board()
        # White pawn on e5, black pawn just double-pushed to d5
        b.set_piece(3, 4, Piece(Color.WHITE, PieceType.PAWN))
        b.set_piece(3, 3, Piece(Color.BLACK, PieceType.PAWN))
        b.en_passant_target = (2, 3)
        move = Move((3, 4), (2, 3), is_en_passant=True)
        undo = b.make_move(move)
        assert b.get_piece(2, 3) == Piece(Color.WHITE, PieceType.PAWN)
        assert b.get_piece(3, 3) is None  # captured pawn removed
        assert undo.captured_piece == Piece(Color.BLACK, PieceType.PAWN)

    def test_kingside_castling_white(self):
        b = Board()
        # Clear pieces between king and rook
        b.set_piece(7, 5, None)
        b.set_piece(7, 6, None)
        move = Move((7, 4), (7, 6), is_castling=True)
        b.make_move(move)
        assert b.get_piece(7, 6) == Piece(Color.WHITE, PieceType.KING)
        assert b.get_piece(7, 5) == Piece(Color.WHITE, PieceType.ROOK)
        assert b.get_piece(7, 4) is None
        assert b.get_piece(7, 7) is None

    def test_queenside_castling_white(self):
        b = Board()
        b.set_piece(7, 1, None)
        b.set_piece(7, 2, None)
        b.set_piece(7, 3, None)
        move = Move((7, 4), (7, 2), is_castling=True)
        b.make_move(move)
        assert b.get_piece(7, 2) == Piece(Color.WHITE, PieceType.KING)
        assert b.get_piece(7, 3) == Piece(Color.WHITE, PieceType.ROOK)
        assert b.get_piece(7, 0) is None

    def test_promotion(self):
        b = Board()
        b.set_piece(1, 0, Piece(Color.WHITE, PieceType.PAWN))
        b.set_piece(0, 0, None)
        move = Move((1, 0), (0, 0), promotion=PieceType.QUEEN)
        b.make_move(move)
        assert b.get_piece(0, 0) == Piece(Color.WHITE, PieceType.QUEEN)

    def test_king_move_removes_castling(self):
        b = Board()
        b.set_piece(7, 5, None)  # Clear f1
        move = Move((7, 4), (7, 5))  # Ke1-f1
        b.make_move(move)
        assert b.castling_rights[Color.WHITE]['king'] is False
        assert b.castling_rights[Color.WHITE]['queen'] is False

    def test_rook_move_removes_castling_side(self):
        b = Board()
        b.set_piece(6, 7, None)  # Clear pawn
        move = Move((7, 7), (6, 7))  # Rh1-h2
        b.make_move(move)
        assert b.castling_rights[Color.WHITE]['king'] is False
        assert b.castling_rights[Color.WHITE]['queen'] is True

    def test_turn_switches(self):
        b = Board()
        assert b.turn == Color.WHITE
        b.make_move(Move((6, 4), (4, 4)))
        assert b.turn == Color.BLACK


class TestUnmakeMove:
    def test_simple_unmake(self):
        b = Board()
        move = Move((6, 4), (4, 4))
        undo = b.make_move(move)
        b.unmake_move(move, undo)
        assert b.get_piece(6, 4) == Piece(Color.WHITE, PieceType.PAWN)
        assert b.get_piece(4, 4) is None
        assert b.turn == Color.WHITE

    def test_unmake_capture(self):
        b = Board()
        b.set_piece(4, 4, Piece(Color.WHITE, PieceType.PAWN))
        b.set_piece(3, 5, Piece(Color.BLACK, PieceType.PAWN))
        move = Move((4, 4), (3, 5))
        undo = b.make_move(move)
        b.unmake_move(move, undo)
        assert b.get_piece(4, 4) == Piece(Color.WHITE, PieceType.PAWN)
        assert b.get_piece(3, 5) == Piece(Color.BLACK, PieceType.PAWN)

    def test_unmake_en_passant(self):
        b = Board()
        b.set_piece(3, 4, Piece(Color.WHITE, PieceType.PAWN))
        b.set_piece(3, 3, Piece(Color.BLACK, PieceType.PAWN))
        b.en_passant_target = (2, 3)
        move = Move((3, 4), (2, 3), is_en_passant=True)
        undo = b.make_move(move)
        b.unmake_move(move, undo)
        assert b.get_piece(3, 4) == Piece(Color.WHITE, PieceType.PAWN)
        assert b.get_piece(3, 3) == Piece(Color.BLACK, PieceType.PAWN)
        assert b.get_piece(2, 3) is None
        assert b.en_passant_target == (2, 3)

    def test_unmake_castling(self):
        b = Board()
        b.set_piece(7, 5, None)
        b.set_piece(7, 6, None)
        move = Move((7, 4), (7, 6), is_castling=True)
        undo = b.make_move(move)
        b.unmake_move(move, undo)
        assert b.get_piece(7, 4) == Piece(Color.WHITE, PieceType.KING)
        assert b.get_piece(7, 7) == Piece(Color.WHITE, PieceType.ROOK)
        assert b.get_piece(7, 5) is None
        assert b.get_piece(7, 6) is None
        assert b.castling_rights[Color.WHITE]['king'] is True

    def test_unmake_promotion(self):
        b = Board()
        b.set_piece(1, 0, Piece(Color.WHITE, PieceType.PAWN))
        b.set_piece(0, 0, None)
        move = Move((1, 0), (0, 0), promotion=PieceType.QUEEN)
        undo = b.make_move(move)
        b.unmake_move(move, undo)
        assert b.get_piece(1, 0) == Piece(Color.WHITE, PieceType.PAWN)
        assert b.get_piece(0, 0) is None

    def test_unmake_restores_castling_rights(self):
        b = Board()
        b.set_piece(7, 5, None)
        move = Move((7, 4), (7, 5))  # King move
        undo = b.make_move(move)
        assert b.castling_rights[Color.WHITE]['king'] is False
        b.unmake_move(move, undo)
        assert b.castling_rights[Color.WHITE]['king'] is True
        assert b.castling_rights[Color.WHITE]['queen'] is True


class TestFindKing:
    def test_find_white_king(self):
        b = Board()
        assert b.find_king(Color.WHITE) == (7, 4)

    def test_find_black_king(self):
        b = Board()
        assert b.find_king(Color.BLACK) == (0, 4)

    def test_find_moved_king(self):
        b = Board()
        b.set_piece(7, 4, None)
        b.set_piece(5, 4, Piece(Color.WHITE, PieceType.KING))
        assert b.find_king(Color.WHITE) == (5, 4)


class TestPositionKey:
    def test_initial_position_key(self):
        b = Board()
        key = b.get_position_key()
        assert isinstance(key, str)
        assert len(key) > 0

    def test_same_position_same_key(self):
        b1 = Board()
        b2 = Board()
        assert b1.get_position_key() == b2.get_position_key()

    def test_different_position_different_key(self):
        b1 = Board()
        b2 = Board()
        b2.make_move(Move((6, 4), (4, 4)))
        assert b1.get_position_key() != b2.get_position_key()
