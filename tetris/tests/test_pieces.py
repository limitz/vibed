"""Tests for pieces module."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pieces import PieceType, get_cells, rotate_cw, rotate_ccw, get_wall_kicks, SHAPES


class TestPieceDefinitions:
    def test_all_seven_piece_types_exist(self):
        assert len(PieceType) == 7

    def test_all_pieces_have_four_rotations(self):
        for pt in PieceType:
            assert len(SHAPES[pt]) == 4, f"{pt} should have 4 rotations"

    def test_all_rotations_have_four_cells(self):
        for pt in PieceType:
            for rot_idx, rot in enumerate(SHAPES[pt]):
                assert len(rot) == 4, f"{pt} rotation {rot_idx} should have 4 cells"

    def test_o_piece_rotations_identical(self):
        rotations = SHAPES[PieceType.O]
        for i in range(1, 4):
            assert sorted(rotations[i]) == sorted(rotations[0]), \
                "O-piece rotations should all be identical"

    def test_i_piece_rotation_0_is_horizontal(self):
        cells = SHAPES[PieceType.I][0]
        rows = {r for r, c in cells}
        cols = {c for r, c in cells}
        assert len(rows) == 1, "I-piece rotation 0 should be 1 row"
        assert len(cols) == 4, "I-piece rotation 0 should be 4 cols wide"


class TestRotation:
    def test_rotate_cw_cycles(self):
        assert rotate_cw(0) == 1
        assert rotate_cw(1) == 2
        assert rotate_cw(2) == 3
        assert rotate_cw(3) == 0

    def test_rotate_ccw_cycles(self):
        assert rotate_ccw(0) == 3
        assert rotate_ccw(1) == 0
        assert rotate_ccw(2) == 1
        assert rotate_ccw(3) == 2

    def test_cw_then_ccw_is_identity(self):
        for r in range(4):
            assert rotate_ccw(rotate_cw(r)) == r


class TestGetCells:
    def test_returns_correct_cells(self):
        for pt in PieceType:
            for rot in range(4):
                cells = get_cells(pt, rot)
                assert cells == SHAPES[pt][rot]


class TestWallKicks:
    def test_wall_kicks_return_nonempty_list(self):
        for pt in PieceType:
            for from_rot in range(4):
                to_rot = rotate_cw(from_rot)
                kicks = get_wall_kicks(pt, from_rot, to_rot)
                assert len(kicks) > 0, f"Wall kicks should not be empty for {pt}"

    def test_wall_kicks_are_tuples(self):
        kicks = get_wall_kicks(PieceType.T, 0, 1)
        for kick in kicks:
            assert isinstance(kick, tuple)
            assert len(kick) == 2
