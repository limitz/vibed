"""Curses-based terminal rendering for Tetris."""

import curses
from pieces import PieceType, COLORS, get_cells
from game import GameState


# Color pair indices match COLORS dict values (1-7), plus ghost (8)
COLOR_MAP = {
    PieceType.I: curses.COLOR_CYAN,
    PieceType.O: curses.COLOR_YELLOW,
    PieceType.T: curses.COLOR_MAGENTA,
    PieceType.S: curses.COLOR_GREEN,
    PieceType.Z: curses.COLOR_RED,
    PieceType.J: curses.COLOR_BLUE,
    PieceType.L: curses.COLOR_WHITE,
}

GHOST_PAIR = 8
BORDER_PAIR = 9
TITLE_PAIR = 10


class Renderer:
    def __init__(self, stdscr: curses.window):
        self.stdscr = stdscr
        self.board_y = 2   # top-left of the board area
        self.board_x = 2
        self.cell_width = 2  # each cell = 2 chars wide
        self.setup_colors()

    def setup_colors(self) -> None:
        curses.start_color()
        curses.use_default_colors()
        for pt, color in COLOR_MAP.items():
            curses.init_pair(COLORS[pt], curses.COLOR_BLACK, color)
        curses.init_pair(GHOST_PAIR, curses.COLOR_WHITE, -1)
        curses.init_pair(BORDER_PAIR, curses.COLOR_WHITE, -1)
        curses.init_pair(TITLE_PAIR, curses.COLOR_CYAN, -1)

    def draw(self, state: GameState) -> None:
        self.stdscr.erase()
        self.draw_title()
        self.draw_border(state)
        self.draw_board(state)
        self.draw_ghost_piece(state)
        self.draw_current_piece(state)
        self.draw_next_piece(state)
        self.draw_score_panel(state)
        self.draw_controls()
        if state.game_over:
            self.draw_game_over()
        self.refresh()

    def draw_title(self) -> None:
        title = "T E T R I S"
        x = self.board_x + 4
        try:
            self.stdscr.addstr(0, x, title, curses.color_pair(TITLE_PAIR) | curses.A_BOLD)
        except curses.error:
            pass

    def draw_border(self, state: GameState) -> None:
        h = state.board.height
        w = state.board.width * self.cell_width
        by, bx = self.board_y, self.board_x
        attr = curses.color_pair(BORDER_PAIR) | curses.A_DIM

        # Top border
        try:
            self.stdscr.addstr(by - 1, bx - 1, "+" + "-" * w + "+", attr)
        except curses.error:
            pass
        # Side borders
        for r in range(h):
            try:
                self.stdscr.addstr(by + r, bx - 1, "|", attr)
                self.stdscr.addstr(by + r, bx + w, "|", attr)
            except curses.error:
                pass
        # Bottom border
        try:
            self.stdscr.addstr(by + h, bx - 1, "+" + "-" * w + "+", attr)
        except curses.error:
            pass

    def draw_board(self, state: GameState) -> None:
        for r in range(state.board.height):
            for c in range(state.board.width):
                cell = state.board.get_cell(r, c)
                y = self.board_y + r
                x = self.board_x + c * self.cell_width
                if cell is not None:
                    try:
                        self.stdscr.addstr(y, x, "[]", curses.color_pair(COLORS[cell]))
                    except curses.error:
                        pass
                else:
                    try:
                        self.stdscr.addstr(y, x, " .", curses.A_DIM)
                    except curses.error:
                        pass

    def draw_current_piece(self, state: GameState) -> None:
        if state.current_piece is None:
            return
        cells = get_cells(state.current_piece, state.current_rotation)
        color = curses.color_pair(COLORS[state.current_piece])
        for dr, dc in cells:
            y = self.board_y + state.current_row + dr
            x = self.board_x + (state.current_col + dc) * self.cell_width
            try:
                self.stdscr.addstr(y, x, "[]", color | curses.A_BOLD)
            except curses.error:
                pass

    def draw_ghost_piece(self, state: GameState) -> None:
        if state.current_piece is None:
            return
        ghost_row = state.get_ghost_row()
        if ghost_row == state.current_row:
            return
        cells = get_cells(state.current_piece, state.current_rotation)
        attr = curses.color_pair(GHOST_PAIR) | curses.A_DIM
        for dr, dc in cells:
            y = self.board_y + ghost_row + dr
            x = self.board_x + (state.current_col + dc) * self.cell_width
            try:
                self.stdscr.addstr(y, x, "..", attr)
            except curses.error:
                pass

    def draw_next_piece(self, state: GameState) -> None:
        panel_x = self.board_x + state.board.width * self.cell_width + 3
        panel_y = self.board_y
        attr_label = curses.A_BOLD
        try:
            self.stdscr.addstr(panel_y, panel_x, "NEXT:", attr_label)
        except curses.error:
            pass
        cells = get_cells(state.next_piece, 0)
        color = curses.color_pair(COLORS[state.next_piece])
        for dr, dc in cells:
            try:
                self.stdscr.addstr(panel_y + 1 + dr, panel_x + dc * self.cell_width, "[]", color)
            except curses.error:
                pass

    def draw_score_panel(self, state: GameState) -> None:
        panel_x = self.board_x + state.board.width * self.cell_width + 3
        panel_y = self.board_y + 5
        attr = curses.A_BOLD
        try:
            self.stdscr.addstr(panel_y, panel_x, f"SCORE: {state.score}", attr)
            self.stdscr.addstr(panel_y + 1, panel_x, f"LEVEL: {state.level}", attr)
            self.stdscr.addstr(panel_y + 2, panel_x, f"LINES: {state.lines_cleared}", attr)
        except curses.error:
            pass

    def draw_controls(self) -> None:
        panel_x = self.board_x + 10 * self.cell_width + 3
        panel_y = self.board_y + 10
        controls = [
            "CONTROLS:",
            "← →  Move",
            "↑    Rotate",
            "Z    Rot CCW",
            "↓    Soft drop",
            "SPACE Hard drop",
            "P    Pause",
            "Q    Quit",
        ]
        for i, line in enumerate(controls):
            try:
                self.stdscr.addstr(panel_y + i, panel_x, line, curses.A_DIM)
            except curses.error:
                pass

    def draw_game_over(self) -> None:
        h, w = self.stdscr.getmaxyx()
        msg = " GAME OVER "
        sub = " Press Q to quit or R to restart "
        y = h // 2
        x1 = max(0, (w - len(msg)) // 2)
        x2 = max(0, (w - len(sub)) // 2)
        attr = curses.A_REVERSE | curses.A_BOLD
        try:
            self.stdscr.addstr(y, x1, msg, attr)
            self.stdscr.addstr(y + 1, x2, sub, attr)
        except curses.error:
            pass

    def refresh(self) -> None:
        self.stdscr.refresh()
