"""
Renderer module - Screen buffer and terminal rendering engine.

Provides a 2D character grid with color support that can be rendered
to the terminal using ANSI escape codes.
"""

import os
import sys
import shutil
from typing import Optional, Tuple


# ANSI color codes
class Color:
    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7
    BRIGHT_RED = 9
    BRIGHT_GREEN = 10
    BRIGHT_YELLOW = 11
    BRIGHT_BLUE = 12
    BRIGHT_MAGENTA = 13
    BRIGHT_CYAN = 14
    BRIGHT_WHITE = 15
    ORANGE = 208
    GRAY = 240
    DARK_GRAY = 236
    LIGHT_GRAY = 250


class Cell:
    """A single character cell with foreground and background colors."""
    __slots__ = ('char', 'fg', 'bg')

    def __init__(self, char: str = ' ', fg: int = Color.WHITE, bg: int = Color.BLACK):
        self.char = char
        self.fg = fg
        self.bg = bg

    def __eq__(self, other):
        if not isinstance(other, Cell):
            return False
        return self.char == other.char and self.fg == other.fg and self.bg == other.bg

    def __repr__(self):
        return f"Cell('{self.char}', fg={self.fg}, bg={self.bg})"


class ScreenBuffer:
    """2D grid of character cells that can be rendered to terminal."""

    def __init__(self, width: int = 80, height: int = 24):
        self.width = width
        self.height = height
        self.buffer: list[list[Cell]] = []
        self.clear()

    def clear(self, bg: int = Color.BLACK):
        """Clear the entire buffer."""
        self.buffer = [
            [Cell(' ', Color.WHITE, bg) for _ in range(self.width)]
            for _ in range(self.height)
        ]

    def set_cell(self, x: int, y: int, char: str, fg: int = Color.WHITE, bg: int = Color.BLACK):
        """Set a single cell. Out-of-bounds writes are silently ignored."""
        if 0 <= x < self.width and 0 <= y < self.height:
            cell = self.buffer[y][x]
            cell.char = char
            cell.fg = fg
            cell.bg = bg

    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        """Get a cell at position. Returns None if out of bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.buffer[y][x]
        return None

    def draw_text(self, x: int, y: int, text: str, fg: int = Color.WHITE, bg: int = Color.BLACK):
        """Draw a string of text starting at (x, y)."""
        for i, char in enumerate(text):
            self.set_cell(x + i, y, char, fg, bg)

    def draw_text_centered(self, y: int, text: str, fg: int = Color.WHITE, bg: int = Color.BLACK):
        """Draw text centered on the given row."""
        x = (self.width - len(text)) // 2
        self.draw_text(x, y, text, fg, bg)

    def draw_box(self, x: int, y: int, w: int, h: int, fg: int = Color.WHITE, bg: int = Color.BLACK,
                 double: bool = False):
        """Draw a box outline."""
        if double:
            tl, tr, bl, br, hz, vt = '\u2554', '\u2557', '\u255a', '\u255d', '\u2550', '\u2551'
        else:
            tl, tr, bl, br, hz, vt = '\u250c', '\u2510', '\u2514', '\u2518', '\u2500', '\u2502'

        self.set_cell(x, y, tl, fg, bg)
        self.set_cell(x + w - 1, y, tr, fg, bg)
        self.set_cell(x, y + h - 1, bl, fg, bg)
        self.set_cell(x + w - 1, y + h - 1, br, fg, bg)

        for i in range(1, w - 1):
            self.set_cell(x + i, y, hz, fg, bg)
            self.set_cell(x + i, y + h - 1, hz, fg, bg)

        for j in range(1, h - 1):
            self.set_cell(x, y + j, vt, fg, bg)
            self.set_cell(x + w - 1, y + j, vt, fg, bg)

    def fill_rect(self, x: int, y: int, w: int, h: int, char: str = ' ',
                  fg: int = Color.WHITE, bg: int = Color.BLACK):
        """Fill a rectangular area."""
        for dy in range(h):
            for dx in range(w):
                self.set_cell(x + dx, y + dy, char, fg, bg)

    def draw_sprite(self, x: int, y: int, sprite_lines: list[str],
                    fg: int = Color.WHITE, bg: int = Color.BLACK,
                    transparent: str = None):
        """Draw a multi-line sprite. If transparent is set, that char is skipped."""
        for dy, line in enumerate(sprite_lines):
            for dx, char in enumerate(line):
                if transparent and char == transparent:
                    continue
                self.set_cell(x + dx, y + dy, char, fg, bg)

    def overlay(self, other: 'ScreenBuffer', ox: int = 0, oy: int = 0, alpha_char: str = None):
        """Overlay another buffer on top of this one."""
        for y in range(other.height):
            for x in range(other.width):
                cell = other.buffer[y][x]
                if alpha_char and cell.char == alpha_char:
                    continue
                self.set_cell(ox + x, oy + y, cell.char, cell.fg, cell.bg)

    def copy(self) -> 'ScreenBuffer':
        """Create a deep copy of this buffer."""
        new_buf = ScreenBuffer(self.width, self.height)
        for y in range(self.height):
            for x in range(self.width):
                src = self.buffer[y][x]
                new_buf.buffer[y][x] = Cell(src.char, src.fg, src.bg)
        return new_buf


class TerminalRenderer:
    """Renders a ScreenBuffer to the terminal using ANSI escape codes."""

    def __init__(self):
        self.prev_buffer: Optional[ScreenBuffer] = None

    @staticmethod
    def _ansi_color_fg(color: int) -> str:
        """Get ANSI escape for foreground color."""
        if color < 8:
            return f"\033[3{color}m"
        elif color < 16:
            return f"\033[9{color - 8}m"
        else:
            return f"\033[38;5;{color}m"

    @staticmethod
    def _ansi_color_bg(color: int) -> str:
        """Get ANSI escape for background color."""
        if color < 8:
            return f"\033[4{color}m"
        elif color < 16:
            return f"\033[10{color - 8}m"
        else:
            return f"\033[48;5;{color}m"

    def render(self, buffer: ScreenBuffer):
        """Render a buffer to the terminal."""
        output = []
        output.append("\033[H")  # Move cursor to top-left

        for y in range(buffer.height):
            for x in range(buffer.width):
                cell = buffer.buffer[y][x]
                # Only update cells that changed
                if self.prev_buffer:
                    prev = self.prev_buffer.buffer[y][x]
                    if cell == prev:
                        continue

                output.append(f"\033[{y+1};{x+1}H")  # Move cursor
                output.append(self._ansi_color_fg(cell.fg))
                output.append(self._ansi_color_bg(cell.bg))
                output.append(cell.char)

        output.append("\033[0m")  # Reset colors
        sys.stdout.write(''.join(output))
        sys.stdout.flush()
        self.prev_buffer = buffer.copy()

    @staticmethod
    def setup():
        """Set up terminal for rendering."""
        sys.stdout.write("\033[?25l")  # Hide cursor
        sys.stdout.write("\033[2J")    # Clear screen
        sys.stdout.flush()

    @staticmethod
    def cleanup():
        """Restore terminal state."""
        sys.stdout.write("\033[?25h")  # Show cursor
        sys.stdout.write("\033[0m")    # Reset colors
        sys.stdout.write("\033[2J")    # Clear screen
        sys.stdout.write("\033[H")     # Move to top-left
        sys.stdout.flush()

    @staticmethod
    def get_terminal_size() -> Tuple[int, int]:
        """Get terminal dimensions."""
        size = shutil.get_terminal_size((80, 24))
        return size.columns, size.lines
