"""Rendering infrastructure: Cell, Color constants, ScreenBuffer, and CursesRenderer."""

import curses
from enum import IntEnum


class Color(IntEnum):
    """Terminal color constants."""
    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7
    BRIGHT_RED = 8
    BRIGHT_GREEN = 9
    BRIGHT_YELLOW = 10
    BRIGHT_BLUE = 11
    BRIGHT_MAGENTA = 12
    BRIGHT_CYAN = 13
    BRIGHT_WHITE = 14
    GRAY = 15
    DARK_GRAY = 16
    ORANGE = 17


class Cell:
    """A single character cell with foreground and background colors."""
    __slots__ = ('char', 'fg', 'bg')

    def __init__(self, char=' ', fg=Color.WHITE, bg=Color.BLACK):
        self.char = char
        self.fg = fg
        self.bg = bg

    def __eq__(self, other):
        if not isinstance(other, Cell):
            return NotImplemented
        return self.char == other.char and self.fg == other.fg and self.bg == other.bg

    def __repr__(self):
        return f"Cell({self.char!r}, {self.fg}, {self.bg})"


class ScreenBuffer:
    """2D grid of Cells with drawing primitives."""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[Cell() for _ in range(width)] for _ in range(height)]

    def clear(self, bg=Color.BLACK):
        """Clear the buffer to empty cells."""
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                cell.char = ' '
                cell.fg = Color.WHITE
                cell.bg = bg

    def set_cell(self, x, y, char=' ', fg=Color.WHITE, bg=Color.BLACK):
        """Set a single cell. Out-of-bounds writes are silently ignored."""
        if 0 <= x < self.width and 0 <= y < self.height:
            cell = self.grid[y][x]
            cell.char = char
            cell.fg = fg
            cell.bg = bg

    def get_cell(self, x, y):
        """Get a cell at position. Returns None if out of bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    def draw_text(self, x, y, text, fg=Color.WHITE, bg=Color.BLACK):
        """Draw a string horizontally starting at (x, y)."""
        for i, ch in enumerate(text):
            self.set_cell(x + i, y, ch, fg, bg)

    def draw_text_centered(self, y, text, fg=Color.WHITE, bg=Color.BLACK):
        """Draw a string centered on row y."""
        x = (self.width - len(text)) // 2
        self.draw_text(x, y, text, fg, bg)

    def fill_rect(self, x, y, w, h, char=' ', fg=Color.WHITE, bg=Color.BLACK):
        """Fill a rectangular region."""
        for dy in range(h):
            for dx in range(w):
                self.set_cell(x + dx, y + dy, char, fg, bg)

    def draw_sprite(self, x, y, sprite_lines, fg=Color.WHITE, bg=Color.BLACK):
        """Draw a multi-line ASCII sprite at position (x, y).

        sprite_lines is a list of strings, one per row.
        Spaces in the sprite are transparent (not drawn).
        """
        for dy, line in enumerate(sprite_lines):
            for dx, ch in enumerate(line):
                if ch != ' ':
                    self.set_cell(x + dx, y + dy, ch, fg, bg)

    def draw_box(self, x, y, w, h, fg=Color.WHITE, bg=Color.BLACK):
        """Draw a box outline using Unicode box-drawing characters."""
        # Corners
        self.set_cell(x, y, '┌', fg, bg)
        self.set_cell(x + w - 1, y, '┐', fg, bg)
        self.set_cell(x, y + h - 1, '└', fg, bg)
        self.set_cell(x + w - 1, y + h - 1, '┘', fg, bg)
        # Horizontal edges
        for dx in range(1, w - 1):
            self.set_cell(x + dx, y, '─', fg, bg)
            self.set_cell(x + dx, y + h - 1, '─', fg, bg)
        # Vertical edges
        for dy in range(1, h - 1):
            self.set_cell(x, y + dy, '│', fg, bg)
            self.set_cell(x + w - 1, y + dy, '│', fg, bg)


# Mapping from Color enum to curses color constants
_CURSES_COLOR_MAP = {
    Color.BLACK: curses.COLOR_BLACK,
    Color.RED: curses.COLOR_RED,
    Color.GREEN: curses.COLOR_GREEN,
    Color.YELLOW: curses.COLOR_YELLOW,
    Color.BLUE: curses.COLOR_BLUE,
    Color.MAGENTA: curses.COLOR_MAGENTA,
    Color.CYAN: curses.COLOR_CYAN,
    Color.WHITE: curses.COLOR_WHITE,
}


class CursesRenderer:
    """Renders a ScreenBuffer to a curses window."""

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self._color_pairs = {}
        self._next_pair = 1
        self._init_colors()

    def _init_colors(self):
        """Initialize curses color pairs."""
        curses.start_color()
        curses.use_default_colors()
        if curses.can_change_color():
            # Define extended colors
            curses.init_color(8, 1000, 300, 300)   # BRIGHT_RED
            curses.init_color(9, 300, 1000, 300)    # BRIGHT_GREEN
            curses.init_color(10, 1000, 1000, 300)  # BRIGHT_YELLOW
            curses.init_color(11, 300, 300, 1000)   # BRIGHT_BLUE
            curses.init_color(12, 1000, 300, 1000)  # BRIGHT_MAGENTA
            curses.init_color(13, 300, 1000, 1000)  # BRIGHT_CYAN
            curses.init_color(14, 1000, 1000, 1000) # BRIGHT_WHITE
            curses.init_color(15, 700, 700, 700)    # GRAY
            curses.init_color(16, 400, 400, 400)    # DARK_GRAY
            curses.init_color(17, 1000, 600, 0)     # ORANGE

    def _get_curses_color(self, color):
        """Map a Color enum to a curses color number."""
        if color in _CURSES_COLOR_MAP:
            return _CURSES_COLOR_MAP[color]
        # Extended colors map directly to their int value
        return int(color)

    def get_color_pair(self, fg, bg):
        """Get or create a curses color pair for the given fg/bg combo."""
        key = (int(fg), int(bg))
        if key not in self._color_pairs:
            cfn = self._get_curses_color(fg)
            cbg = self._get_curses_color(bg)
            pair_id = self._next_pair
            self._next_pair += 1
            try:
                curses.init_pair(pair_id, cfn, cbg)
            except curses.error:
                return 0
            self._color_pairs[key] = pair_id
        return self._color_pairs[key]

    def render(self, buffer):
        """Render the ScreenBuffer to the curses window."""
        max_y, max_x = self.stdscr.getmaxyx()
        for y in range(min(buffer.height, max_y)):
            for x in range(min(buffer.width, max_x)):
                cell = buffer.grid[y][x]
                pair = self.get_color_pair(cell.fg, cell.bg)
                try:
                    self.stdscr.addch(y, x, cell.char, curses.color_pair(pair))
                except curses.error:
                    pass
        self.stdscr.noutrefresh()
        curses.doupdate()
