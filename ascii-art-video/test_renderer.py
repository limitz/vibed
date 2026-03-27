"""Tests for the renderer module."""

import unittest
from renderer import Cell, Color, ScreenBuffer


class TestCell(unittest.TestCase):
    def test_default_cell(self):
        cell = Cell()
        self.assertEqual(cell.char, ' ')
        self.assertEqual(cell.fg, Color.WHITE)
        self.assertEqual(cell.bg, Color.BLACK)

    def test_custom_cell(self):
        cell = Cell('X', Color.RED, Color.BLUE)
        self.assertEqual(cell.char, 'X')
        self.assertEqual(cell.fg, Color.RED)
        self.assertEqual(cell.bg, Color.BLUE)

    def test_cell_equality(self):
        c1 = Cell('A', Color.RED, Color.BLACK)
        c2 = Cell('A', Color.RED, Color.BLACK)
        c3 = Cell('B', Color.RED, Color.BLACK)
        self.assertEqual(c1, c2)
        self.assertNotEqual(c1, c3)

    def test_cell_inequality_with_non_cell(self):
        cell = Cell()
        self.assertNotEqual(cell, "not a cell")


class TestScreenBuffer(unittest.TestCase):
    def setUp(self):
        self.buf = ScreenBuffer(20, 10)

    def test_dimensions(self):
        self.assertEqual(self.buf.width, 20)
        self.assertEqual(self.buf.height, 10)

    def test_clear(self):
        self.buf.set_cell(5, 5, 'X', Color.RED)
        self.buf.clear()
        cell = self.buf.get_cell(5, 5)
        self.assertEqual(cell.char, ' ')
        self.assertEqual(cell.fg, Color.WHITE)

    def test_set_get_cell(self):
        self.buf.set_cell(3, 4, 'Z', Color.GREEN, Color.BLUE)
        cell = self.buf.get_cell(3, 4)
        self.assertEqual(cell.char, 'Z')
        self.assertEqual(cell.fg, Color.GREEN)
        self.assertEqual(cell.bg, Color.BLUE)

    def test_out_of_bounds_set(self):
        # Should not raise
        self.buf.set_cell(-1, 0, 'X')
        self.buf.set_cell(0, -1, 'X')
        self.buf.set_cell(20, 0, 'X')
        self.buf.set_cell(0, 10, 'X')

    def test_out_of_bounds_get(self):
        self.assertIsNone(self.buf.get_cell(-1, 0))
        self.assertIsNone(self.buf.get_cell(20, 0))

    def test_draw_text(self):
        self.buf.draw_text(2, 3, "Hello", Color.CYAN)
        for i, ch in enumerate("Hello"):
            cell = self.buf.get_cell(2 + i, 3)
            self.assertEqual(cell.char, ch)
            self.assertEqual(cell.fg, Color.CYAN)

    def test_draw_text_centered(self):
        self.buf.draw_text_centered(5, "Hi", Color.RED)
        # "Hi" centered in width 20 -> x = 9
        cell = self.buf.get_cell(9, 5)
        self.assertEqual(cell.char, 'H')

    def test_draw_box(self):
        self.buf.draw_box(0, 0, 5, 3, Color.WHITE)
        self.assertEqual(self.buf.get_cell(0, 0).char, '\u250c')  # top-left
        self.assertEqual(self.buf.get_cell(4, 0).char, '\u2510')  # top-right
        self.assertEqual(self.buf.get_cell(0, 2).char, '\u2514')  # bottom-left
        self.assertEqual(self.buf.get_cell(4, 2).char, '\u2518')  # bottom-right

    def test_fill_rect(self):
        self.buf.fill_rect(1, 1, 3, 2, '#', Color.RED)
        for dy in range(2):
            for dx in range(3):
                cell = self.buf.get_cell(1 + dx, 1 + dy)
                self.assertEqual(cell.char, '#')
                self.assertEqual(cell.fg, Color.RED)

    def test_draw_sprite(self):
        sprite = ["AB", "CD"]
        self.buf.draw_sprite(5, 5, sprite, Color.GREEN)
        self.assertEqual(self.buf.get_cell(5, 5).char, 'A')
        self.assertEqual(self.buf.get_cell(6, 5).char, 'B')
        self.assertEqual(self.buf.get_cell(5, 6).char, 'C')
        self.assertEqual(self.buf.get_cell(6, 6).char, 'D')

    def test_draw_sprite_transparent(self):
        self.buf.set_cell(5, 5, 'X', Color.RED)
        sprite = [". ", " ."]
        self.buf.draw_sprite(5, 5, sprite, Color.GREEN, transparent=' ')
        self.assertEqual(self.buf.get_cell(5, 5).char, '.')
        # Space should not overwrite the X... wait, 6,5 was blank
        # Actually (5,5) is '.', (6,5) is transparent so keeps original
        cell_6_5 = self.buf.get_cell(6, 5)
        self.assertEqual(cell_6_5.char, ' ')  # was never set to X

    def test_copy(self):
        self.buf.set_cell(0, 0, 'Z', Color.RED)
        copy = self.buf.copy()
        self.assertEqual(copy.get_cell(0, 0).char, 'Z')
        # Modifying copy shouldn't affect original
        copy.set_cell(0, 0, 'W')
        self.assertEqual(self.buf.get_cell(0, 0).char, 'Z')

    def test_overlay(self):
        other = ScreenBuffer(5, 5)
        other.set_cell(0, 0, 'X', Color.RED)
        self.buf.overlay(other, 3, 3)
        self.assertEqual(self.buf.get_cell(3, 3).char, 'X')


class TestTerminalRenderer(unittest.TestCase):
    def test_ansi_color_fg_basic(self):
        from renderer import TerminalRenderer
        r = TerminalRenderer()
        self.assertEqual(r._ansi_color_fg(0), "\033[30m")
        self.assertEqual(r._ansi_color_fg(7), "\033[37m")

    def test_ansi_color_fg_bright(self):
        from renderer import TerminalRenderer
        r = TerminalRenderer()
        self.assertEqual(r._ansi_color_fg(9), "\033[91m")

    def test_ansi_color_fg_256(self):
        from renderer import TerminalRenderer
        r = TerminalRenderer()
        self.assertEqual(r._ansi_color_fg(208), "\033[38;5;208m")

    def test_ansi_color_bg_basic(self):
        from renderer import TerminalRenderer
        r = TerminalRenderer()
        self.assertEqual(r._ansi_color_bg(0), "\033[40m")


if __name__ == '__main__':
    unittest.main()
