"""Curses-based chess board renderer with Unicode pieces and colored squares."""

import curses
from typing import Optional, Set, Tuple

from game import GameState, GameStatus, InputMode
from pieces import Color, Piece, PieceType, UNICODE_SYMBOLS


# Color pair IDs
PAIR_LIGHT_SQUARE = 1
PAIR_DARK_SQUARE = 2
PAIR_WHITE_ON_LIGHT = 3
PAIR_WHITE_ON_DARK = 4
PAIR_BLACK_ON_LIGHT = 5
PAIR_BLACK_ON_DARK = 6
PAIR_CURSOR = 7
PAIR_SELECTED = 8
PAIR_LEGAL_MOVE = 9
PAIR_LAST_MOVE_LIGHT = 10
PAIR_LAST_MOVE_DARK = 11
PAIR_CHECK = 12
PAIR_TITLE = 13
PAIR_STATUS = 14
PAIR_BORDER = 15

# Board display constants
BOARD_TOP = 2
BOARD_LEFT = 4
CELL_WIDTH = 3  # Characters per cell
CELL_HEIGHT = 1
PANEL_LEFT = BOARD_LEFT + CELL_WIDTH * 8 + 4


class Renderer:
    """Renders the chess game to a curses terminal."""

    def __init__(self, stdscr: 'curses.window') -> None:
        """Initialize renderer with color pairs."""
        self.stdscr = stdscr
        self.setup_colors()
        try:
            curses.curs_set(0)
        except curses.error:
            pass

    def setup_colors(self) -> None:
        """Initialize curses color pairs for the board."""
        curses.start_color()
        try:
            curses.use_default_colors()
        except curses.error:
            pass

        can_change = curses.can_change_color()

        if can_change and curses.COLORS >= 256:
            # Define custom colors for a nicer board
            LIGHT_SQ = 16   # Warm cream
            DARK_SQ = 17    # Forest green
            HIGHLIGHT = 18  # Bright yellow
            SELECTED_BG = 19  # Cyan
            LEGAL_BG = 20   # Green tint
            LAST_LIGHT = 21  # Yellow tint on light
            LAST_DARK = 22   # Yellow tint on dark
            CHECK_BG = 23    # Red

            curses.init_color(LIGHT_SQ, 900, 850, 750)
            curses.init_color(DARK_SQ, 450, 590, 340)
            curses.init_color(HIGHLIGHT, 1000, 900, 300)
            curses.init_color(SELECTED_BG, 400, 750, 850)
            curses.init_color(LEGAL_BG, 500, 800, 500)
            curses.init_color(LAST_LIGHT, 900, 900, 600)
            curses.init_color(LAST_DARK, 600, 700, 350)
            curses.init_color(CHECK_BG, 900, 300, 300)

            curses.init_pair(PAIR_LIGHT_SQUARE, curses.COLOR_BLACK, LIGHT_SQ)
            curses.init_pair(PAIR_DARK_SQUARE, curses.COLOR_BLACK, DARK_SQ)
            curses.init_pair(PAIR_WHITE_ON_LIGHT, curses.COLOR_WHITE, LIGHT_SQ)
            curses.init_pair(PAIR_WHITE_ON_DARK, curses.COLOR_WHITE, DARK_SQ)
            curses.init_pair(PAIR_BLACK_ON_LIGHT, curses.COLOR_BLACK, LIGHT_SQ)
            curses.init_pair(PAIR_BLACK_ON_DARK, curses.COLOR_BLACK, DARK_SQ)
            curses.init_pair(PAIR_CURSOR, curses.COLOR_BLACK, HIGHLIGHT)
            curses.init_pair(PAIR_SELECTED, curses.COLOR_BLACK, SELECTED_BG)
            curses.init_pair(PAIR_LEGAL_MOVE, curses.COLOR_BLACK, LEGAL_BG)
            curses.init_pair(PAIR_LAST_MOVE_LIGHT, curses.COLOR_BLACK, LAST_LIGHT)
            curses.init_pair(PAIR_LAST_MOVE_DARK, curses.COLOR_BLACK, LAST_DARK)
            curses.init_pair(PAIR_CHECK, curses.COLOR_WHITE, CHECK_BG)
            curses.init_pair(PAIR_TITLE, curses.COLOR_CYAN, -1)
            curses.init_pair(PAIR_STATUS, curses.COLOR_YELLOW, -1)
            curses.init_pair(PAIR_BORDER, curses.COLOR_WHITE, -1)
        else:
            # Fallback for basic terminals
            curses.init_pair(PAIR_LIGHT_SQUARE, curses.COLOR_BLACK, curses.COLOR_WHITE)
            curses.init_pair(PAIR_DARK_SQUARE, curses.COLOR_WHITE, curses.COLOR_BLACK)
            curses.init_pair(PAIR_WHITE_ON_LIGHT, curses.COLOR_RED, curses.COLOR_WHITE)
            curses.init_pair(PAIR_WHITE_ON_DARK, curses.COLOR_RED, curses.COLOR_BLACK)
            curses.init_pair(PAIR_BLACK_ON_LIGHT, curses.COLOR_BLUE, curses.COLOR_WHITE)
            curses.init_pair(PAIR_BLACK_ON_DARK, curses.COLOR_BLUE, curses.COLOR_BLACK)
            curses.init_pair(PAIR_CURSOR, curses.COLOR_BLACK, curses.COLOR_YELLOW)
            curses.init_pair(PAIR_SELECTED, curses.COLOR_BLACK, curses.COLOR_CYAN)
            curses.init_pair(PAIR_LEGAL_MOVE, curses.COLOR_BLACK, curses.COLOR_GREEN)
            curses.init_pair(PAIR_LAST_MOVE_LIGHT, curses.COLOR_BLACK, curses.COLOR_YELLOW)
            curses.init_pair(PAIR_LAST_MOVE_DARK, curses.COLOR_WHITE, curses.COLOR_YELLOW)
            curses.init_pair(PAIR_CHECK, curses.COLOR_WHITE, curses.COLOR_RED)
            curses.init_pair(PAIR_TITLE, curses.COLOR_CYAN, curses.COLOR_BLACK)
            curses.init_pair(PAIR_STATUS, curses.COLOR_YELLOW, curses.COLOR_BLACK)
            curses.init_pair(PAIR_BORDER, curses.COLOR_WHITE, curses.COLOR_BLACK)

    def _get_cell_attr(self, state: GameState, row: int, col: int, piece: Optional[Piece]) -> int:
        """Determine the curses attribute for a cell based on game state."""
        is_light = (row + col) % 2 == 0
        sq = (row, col)

        # Cursor position
        if sq == state.cursor_pos and state.input_mode in (InputMode.IDLE, InputMode.PIECE_SELECTED):
            return curses.color_pair(PAIR_CURSOR) | curses.A_BOLD

        # Selected piece square
        if sq == state.selected_square:
            return curses.color_pair(PAIR_SELECTED) | curses.A_BOLD

        # Check highlight on king
        if (piece and piece.piece_type == PieceType.KING and
                state.status in (GameStatus.CHECK, GameStatus.CHECKMATE) and
                piece.color == state.board.turn):
            return curses.color_pair(PAIR_CHECK) | curses.A_BOLD

        # Legal move target
        if state.input_mode == InputMode.PIECE_SELECTED:
            if any(m.to_sq == sq for m in state.selected_piece_moves):
                return curses.color_pair(PAIR_LEGAL_MOVE) | curses.A_BOLD

        # Last move highlight
        if state.last_move and sq in (state.last_move.from_sq, state.last_move.to_sq):
            return curses.color_pair(PAIR_LAST_MOVE_LIGHT if is_light else PAIR_LAST_MOVE_DARK)

        # Normal square
        if piece:
            if piece.color == Color.WHITE:
                return curses.color_pair(PAIR_WHITE_ON_LIGHT if is_light else PAIR_WHITE_ON_DARK) | curses.A_BOLD
            else:
                return curses.color_pair(PAIR_BLACK_ON_LIGHT if is_light else PAIR_BLACK_ON_DARK) | curses.A_BOLD
        else:
            return curses.color_pair(PAIR_LIGHT_SQUARE if is_light else PAIR_DARK_SQUARE)

    def draw(self, state: GameState) -> None:
        """Draw the complete game state."""
        self.stdscr.erase()
        max_y, max_x = self.stdscr.getmaxyx()

        self.draw_title(max_x)
        self.draw_board(state, max_y, max_x)
        self.draw_side_panel(state, max_y, max_x)

        self.stdscr.refresh()

    def draw_title(self, max_x: int) -> None:
        """Draw the title bar."""
        title = " C H E S S "
        x = max(0, (min(max_x, PANEL_LEFT + 20) - len(title)) // 2)
        try:
            self.stdscr.addstr(0, x, title, curses.color_pair(PAIR_TITLE) | curses.A_BOLD)
        except curses.error:
            pass

    def draw_board(self, state: GameState, max_y: int, max_x: int) -> None:
        """Draw the chess board with pieces."""
        col_labels = "  a  b  c  d  e  f  g  h"
        try:
            self.stdscr.addstr(BOARD_TOP, BOARD_LEFT - 1, col_labels,
                               curses.color_pair(PAIR_BORDER))
        except curses.error:
            pass

        for row in range(8):
            rank = str(8 - row)
            screen_y = BOARD_TOP + 1 + row * CELL_HEIGHT

            if screen_y >= max_y:
                break

            # Rank label
            try:
                self.stdscr.addstr(screen_y, BOARD_LEFT - 3, rank,
                                   curses.color_pair(PAIR_BORDER))
            except curses.error:
                pass

            for col in range(8):
                piece = state.board.get_piece(row, col)
                attr = self._get_cell_attr(state, row, col, piece)
                screen_x = BOARD_LEFT + col * CELL_WIDTH

                if screen_x + CELL_WIDTH > max_x:
                    break

                if piece:
                    symbol = piece.symbol()
                    cell_str = f" {symbol} "
                else:
                    cell_str = "   "

                # Draw legal move dot for empty squares
                if (state.input_mode == InputMode.PIECE_SELECTED and
                        piece is None and
                        any(m.to_sq == (row, col) for m in state.selected_piece_moves)):
                    cell_str = " \u00b7 "  # center dot

                try:
                    self.stdscr.addstr(screen_y, screen_x, cell_str, attr)
                except curses.error:
                    pass

            # Rank label (right side)
            try:
                self.stdscr.addstr(screen_y, BOARD_LEFT + 8 * CELL_WIDTH + 1, rank,
                                   curses.color_pair(PAIR_BORDER))
            except curses.error:
                pass

        # Bottom file labels
        try:
            self.stdscr.addstr(BOARD_TOP + 1 + 8, BOARD_LEFT - 1, col_labels,
                               curses.color_pair(PAIR_BORDER))
        except curses.error:
            pass

    def draw_side_panel(self, state: GameState, max_y: int, max_x: int) -> None:
        """Draw captured pieces, status, move history, and controls."""
        x = PANEL_LEFT
        if x >= max_x - 5:
            return

        y = BOARD_TOP

        # Captured pieces
        try:
            self.stdscr.addstr(y, x, "Captured:", curses.color_pair(PAIR_BORDER) | curses.A_BOLD)
            y += 1
            white_cap = " ".join(p.symbol() for p in sorted(state.captured_white, key=lambda p: p.value(), reverse=True))
            black_cap = " ".join(p.symbol() for p in sorted(state.captured_black, key=lambda p: p.value(), reverse=True))
            self.stdscr.addstr(y, x, f"  {white_cap}" if white_cap else "  -", curses.color_pair(PAIR_BORDER))
            y += 1
            self.stdscr.addstr(y, x, f"  {black_cap}" if black_cap else "  -", curses.color_pair(PAIR_BORDER))
            y += 2
        except curses.error:
            pass

        # Status message
        try:
            attr = curses.color_pair(PAIR_STATUS) | curses.A_BOLD
            self.stdscr.addstr(y, x, state.message[:max_x - x - 1], attr)
            y += 2
        except curses.error:
            pass

        # Move history
        try:
            self.stdscr.addstr(y, x, "Moves:", curses.color_pair(PAIR_BORDER) | curses.A_BOLD)
            y += 1
            # Show last N moves that fit
            display_moves = state.move_history_text[-(max_y - y - 6):]
            for move_text in display_moves:
                if y >= max_y - 6:
                    break
                self.stdscr.addstr(y, x + 1, move_text[:max_x - x - 2], curses.color_pair(PAIR_BORDER))
                y += 1
        except curses.error:
            pass

        # Controls at the bottom
        controls_y = max(y + 1, BOARD_TOP + 10)
        controls = [
            "Controls:",
            "  Arrow keys: Move cursor",
            "  Enter/Space: Select/Place",
            "  Esc: Cancel selection",
            "  U: Undo move",
            "  N: New game",
            "  Q: Quit",
        ]
        for i, line in enumerate(controls):
            cy = controls_y + i
            if cy >= max_y:
                break
            try:
                self.stdscr.addstr(cy, x, line[:max_x - x - 1], curses.color_pair(PAIR_BORDER))
            except curses.error:
                pass

        # Promotion hint
        if state.input_mode == InputMode.PROMOTING:
            try:
                self.stdscr.addstr(controls_y + len(controls) + 1, x,
                                   "Promote: Q/R/B/N",
                                   curses.color_pair(PAIR_STATUS) | curses.A_BOLD)
            except curses.error:
                pass
