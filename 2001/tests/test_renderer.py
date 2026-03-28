"""Tests for renderer module: Cell, Color, ScreenBuffer."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from renderer import Cell, Color, ScreenBuffer


class TestCell:
    def test_default_cell(self):
        c = Cell()
        assert c.char == ' '
        assert c.fg == Color.WHITE
        assert c.bg == Color.BLACK

    def test_custom_cell(self):
        c = Cell('X', Color.RED, Color.BLUE)
        assert c.char == 'X'
        assert c.fg == Color.RED
        assert c.bg == Color.BLUE

    def test_cell_equality(self):
        c1 = Cell('A', Color.RED, Color.BLACK)
        c2 = Cell('A', Color.RED, Color.BLACK)
        c3 = Cell('B', Color.RED, Color.BLACK)
        assert c1 == c2
        assert c1 != c3

    def test_cell_repr(self):
        c = Cell('X', Color.RED, Color.BLACK)
        r = repr(c)
        assert 'X' in r


class TestScreenBuffer:
    def test_create_buffer(self):
        buf = ScreenBuffer(80, 24)
        assert buf.width == 80
        assert buf.height == 24

    def test_initial_cells_are_empty(self):
        buf = ScreenBuffer(10, 5)
        cell = buf.get_cell(0, 0)
        assert cell is not None
        assert cell.char == ' '

    def test_set_and_get_cell(self):
        buf = ScreenBuffer(10, 5)
        buf.set_cell(3, 2, 'X', Color.RED, Color.BLUE)
        cell = buf.get_cell(3, 2)
        assert cell.char == 'X'
        assert cell.fg == Color.RED
        assert cell.bg == Color.BLUE

    def test_set_cell_out_of_bounds_ignored(self):
        buf = ScreenBuffer(10, 5)
        # Should not raise
        buf.set_cell(-1, 0, 'X')
        buf.set_cell(10, 0, 'X')
        buf.set_cell(0, -1, 'X')
        buf.set_cell(0, 5, 'X')

    def test_get_cell_out_of_bounds_returns_none(self):
        buf = ScreenBuffer(10, 5)
        assert buf.get_cell(-1, 0) is None
        assert buf.get_cell(10, 0) is None
        assert buf.get_cell(0, 5) is None

    def test_clear(self):
        buf = ScreenBuffer(10, 5)
        buf.set_cell(3, 2, 'X', Color.RED)
        buf.clear()
        cell = buf.get_cell(3, 2)
        assert cell.char == ' '
        assert cell.fg == Color.WHITE
        assert cell.bg == Color.BLACK

    def test_clear_with_bg(self):
        buf = ScreenBuffer(10, 5)
        buf.clear(bg=Color.BLUE)
        cell = buf.get_cell(0, 0)
        assert cell.bg == Color.BLUE

    def test_draw_text(self):
        buf = ScreenBuffer(20, 5)
        buf.draw_text(2, 1, "Hello", Color.GREEN)
        assert buf.get_cell(2, 1).char == 'H'
        assert buf.get_cell(3, 1).char == 'e'
        assert buf.get_cell(4, 1).char == 'l'
        assert buf.get_cell(5, 1).char == 'l'
        assert buf.get_cell(6, 1).char == 'o'
        assert buf.get_cell(2, 1).fg == Color.GREEN

    def test_draw_text_clips(self):
        buf = ScreenBuffer(5, 3)
        buf.draw_text(3, 0, "Hello")
        assert buf.get_cell(3, 0).char == 'H'
        assert buf.get_cell(4, 0).char == 'e'
        # "llo" should be clipped

    def test_draw_text_centered(self):
        buf = ScreenBuffer(20, 5)
        buf.draw_text_centered(2, "Hi", Color.YELLOW)
        # "Hi" is 2 chars, centered in 20 -> starts at x=9
        assert buf.get_cell(9, 2).char == 'H'
        assert buf.get_cell(10, 2).char == 'i'

    def test_fill_rect(self):
        buf = ScreenBuffer(10, 5)
        buf.fill_rect(1, 1, 3, 2, '#', Color.RED, Color.BLUE)
        for y in range(1, 3):
            for x in range(1, 4):
                cell = buf.get_cell(x, y)
                assert cell.char == '#'
                assert cell.fg == Color.RED
                assert cell.bg == Color.BLUE
        # Outside rect unchanged
        assert buf.get_cell(0, 0).char == ' '

    def test_draw_sprite(self):
        buf = ScreenBuffer(20, 10)
        sprite = [
            " O ",
            "/|\\",
            "/ \\",
        ]
        buf.draw_sprite(5, 3, sprite, Color.WHITE)
        assert buf.get_cell(6, 3).char == 'O'
        assert buf.get_cell(5, 4).char == '/'
        assert buf.get_cell(6, 4).char == '|'
        assert buf.get_cell(7, 4).char == '\\'

    def test_draw_sprite_clips(self):
        buf = ScreenBuffer(5, 3)
        sprite = ["ABCDEFGH"]
        buf.draw_sprite(3, 0, sprite, Color.WHITE)
        assert buf.get_cell(3, 0).char == 'A'
        assert buf.get_cell(4, 0).char == 'B'

    def test_draw_box(self):
        buf = ScreenBuffer(10, 5)
        buf.draw_box(1, 1, 5, 3, Color.WHITE)
        # Corners
        assert buf.get_cell(1, 1).char == '┌'
        assert buf.get_cell(5, 1).char == '┐'
        assert buf.get_cell(1, 3).char == '└'
        assert buf.get_cell(5, 3).char == '┘'
        # Horizontal edges
        assert buf.get_cell(2, 1).char == '─'
        assert buf.get_cell(3, 1).char == '─'
        # Vertical edges
        assert buf.get_cell(1, 2).char == '│'
        assert buf.get_cell(5, 2).char == '│'
