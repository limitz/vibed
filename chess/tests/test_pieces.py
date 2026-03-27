"""Tests for pieces module."""

import pytest
from pieces import Color, PieceType, Piece, UNICODE_SYMBOLS, PIECE_VALUES, PIECE_SQUARE_TABLES


class TestColor:
    def test_has_white_and_black(self):
        assert Color.WHITE is not None
        assert Color.BLACK is not None

    def test_opposite(self):
        assert Color.WHITE.opposite() == Color.BLACK
        assert Color.BLACK.opposite() == Color.WHITE

    def test_only_two_colors(self):
        assert len(Color) == 2


class TestPieceType:
    def test_has_all_types(self):
        assert PieceType.PAWN is not None
        assert PieceType.KNIGHT is not None
        assert PieceType.BISHOP is not None
        assert PieceType.ROOK is not None
        assert PieceType.QUEEN is not None
        assert PieceType.KING is not None

    def test_exactly_six_types(self):
        assert len(PieceType) == 6


class TestPiece:
    def test_creation(self):
        p = Piece(Color.WHITE, PieceType.KING)
        assert p.color == Color.WHITE
        assert p.piece_type == PieceType.KING

    def test_frozen(self):
        p = Piece(Color.WHITE, PieceType.PAWN)
        with pytest.raises(AttributeError):
            p.color = Color.BLACK

    def test_equality(self):
        p1 = Piece(Color.WHITE, PieceType.QUEEN)
        p2 = Piece(Color.WHITE, PieceType.QUEEN)
        assert p1 == p2

    def test_inequality(self):
        p1 = Piece(Color.WHITE, PieceType.QUEEN)
        p2 = Piece(Color.BLACK, PieceType.QUEEN)
        assert p1 != p2

    def test_hashable(self):
        p = Piece(Color.WHITE, PieceType.ROOK)
        s = {p}
        assert p in s

    def test_symbol(self):
        p = Piece(Color.WHITE, PieceType.KING)
        sym = p.symbol()
        assert isinstance(sym, str)
        assert len(sym) == 1

    def test_value(self):
        p = Piece(Color.WHITE, PieceType.QUEEN)
        assert p.value() == 900


class TestUnicodeSymbols:
    def test_all_combinations_present(self):
        for color in Color:
            for pt in PieceType:
                assert (color, pt) in UNICODE_SYMBOLS
                assert isinstance(UNICODE_SYMBOLS[(color, pt)], str)

    def test_white_and_black_symbols_differ(self):
        for pt in PieceType:
            assert UNICODE_SYMBOLS[(Color.WHITE, pt)] != UNICODE_SYMBOLS[(Color.BLACK, pt)]


class TestPieceValues:
    def test_all_types_have_values(self):
        for pt in PieceType:
            assert pt in PIECE_VALUES
            assert PIECE_VALUES[pt] > 0

    def test_relative_values(self):
        assert PIECE_VALUES[PieceType.PAWN] < PIECE_VALUES[PieceType.KNIGHT]
        assert PIECE_VALUES[PieceType.KNIGHT] < PIECE_VALUES[PieceType.ROOK]
        assert PIECE_VALUES[PieceType.ROOK] < PIECE_VALUES[PieceType.QUEEN]
        assert PIECE_VALUES[PieceType.QUEEN] < PIECE_VALUES[PieceType.KING]


class TestPieceSquareTables:
    def test_all_types_have_tables(self):
        for pt in PieceType:
            assert pt in PIECE_SQUARE_TABLES

    def test_table_dimensions(self):
        for pt in PieceType:
            table = PIECE_SQUARE_TABLES[pt]
            assert len(table) == 8
            for row in table:
                assert len(row) == 8

    def test_values_are_integers(self):
        for pt in PieceType:
            for row in PIECE_SQUARE_TABLES[pt]:
                for val in row:
                    assert isinstance(val, int)
