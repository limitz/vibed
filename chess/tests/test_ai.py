"""Tests for AI module."""

import pytest
from board import Board, Move
from pieces import Color, Piece, PieceType
from ai import evaluate, order_moves, find_best_move
from moves import get_legal_moves


def empty_board():
    b = Board()
    for r in range(8):
        for c in range(8):
            b.grid[r][c] = None
    b.castling_rights = {
        Color.WHITE: {'king': False, 'queen': False},
        Color.BLACK: {'king': False, 'queen': False},
    }
    return b


class TestEvaluation:
    def test_starting_position_near_zero(self):
        b = Board()
        score = evaluate(b)
        assert abs(score) < 50  # Should be roughly balanced

    def test_material_advantage(self):
        b = empty_board()
        b.set_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        b.set_piece(0, 4, Piece(Color.BLACK, PieceType.KING))
        b.set_piece(4, 4, Piece(Color.WHITE, PieceType.QUEEN))
        score = evaluate(b)
        assert score > 800  # White has a queen advantage

    def test_black_advantage_negative(self):
        b = empty_board()
        b.set_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        b.set_piece(0, 4, Piece(Color.BLACK, PieceType.KING))
        b.set_piece(4, 4, Piece(Color.BLACK, PieceType.QUEEN))
        score = evaluate(b)
        assert score < -800

    def test_piece_square_tables_affect_score(self):
        b1 = empty_board()
        b1.set_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        b1.set_piece(0, 4, Piece(Color.BLACK, PieceType.KING))
        b1.set_piece(4, 4, Piece(Color.WHITE, PieceType.KNIGHT))  # center
        b2 = empty_board()
        b2.set_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        b2.set_piece(0, 4, Piece(Color.BLACK, PieceType.KING))
        b2.set_piece(7, 0, Piece(Color.WHITE, PieceType.KNIGHT))  # corner
        assert evaluate(b1) > evaluate(b2)


class TestMoveOrdering:
    def test_captures_first(self):
        b = empty_board()
        b.set_piece(4, 4, Piece(Color.WHITE, PieceType.ROOK))
        b.set_piece(4, 6, Piece(Color.BLACK, PieceType.QUEEN))
        b.set_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        b.set_piece(0, 4, Piece(Color.BLACK, PieceType.KING))
        moves = get_legal_moves(b, Color.WHITE)
        ordered = order_moves(b, moves)
        # First move should be a capture (the queen)
        first = ordered[0]
        assert b.get_piece(first.to_sq[0], first.to_sq[1]) is not None


class TestFindBestMove:
    def test_returns_legal_move(self):
        b = Board()
        move = find_best_move(b, Color.WHITE, depth=2)
        assert move is not None
        legal = get_legal_moves(b, Color.WHITE)
        assert any(m.from_sq == move.from_sq and m.to_sq == move.to_sq for m in legal)

    def test_captures_free_piece(self):
        b = empty_board()
        b.set_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        b.set_piece(0, 0, Piece(Color.BLACK, PieceType.KING))
        b.set_piece(4, 4, Piece(Color.WHITE, PieceType.ROOK))
        b.set_piece(4, 7, Piece(Color.BLACK, PieceType.QUEEN))  # free queen
        move = find_best_move(b, Color.WHITE, depth=2)
        assert move is not None
        assert move.to_sq == (4, 7)

    def test_finds_mate_in_one(self):
        b = empty_board()
        b.set_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
        b.set_piece(6, 0, Piece(Color.WHITE, PieceType.ROOK))
        b.set_piece(1, 7, Piece(Color.WHITE, PieceType.ROOK))
        b.set_piece(0, 4, Piece(Color.BLACK, PieceType.KING))
        # Ra8# is mate
        move = find_best_move(b, Color.WHITE, depth=2)
        assert move is not None
        assert move.to_sq[0] == 0  # move to back rank for mate

    def test_no_move_when_none_available(self):
        b = empty_board()
        b.set_piece(0, 0, Piece(Color.BLACK, PieceType.KING))
        b.set_piece(2, 1, Piece(Color.WHITE, PieceType.QUEEN))
        b.set_piece(7, 7, Piece(Color.WHITE, PieceType.KING))
        b.turn = Color.BLACK
        move = find_best_move(b, Color.BLACK, depth=2)
        assert move is None  # stalemate - no legal moves

    def test_ai_plays_as_black(self):
        b = Board()
        b.make_move(Move((6, 4), (4, 4)))  # e4
        move = find_best_move(b, Color.BLACK, depth=2)
        assert move is not None
