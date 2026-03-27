#!/usr/bin/env python3
"""Generate screenshot.png by faithfully reproducing the curses renderer output.

Builds the exact same text buffer the renderer produces and draws it
character-by-character in a monospace font on a black background.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from PIL import Image, ImageDraw, ImageFont
from pieces import Color, Piece, PieceType

# --- Renderer constants (must match renderer.py exactly) ---
BOARD_TOP = 2
BOARD_LEFT = 4
CELL_WIDTH = 3
CELL_HEIGHT = 1
PANEL_LEFT = BOARD_LEFT + CELL_WIDTH * 8 + 4  # 32

# Terminal dimensions to simulate
TERM_COLS = 60
TERM_ROWS = 20

# Character cell size in pixels
CHAR_W = 10
CHAR_H = 20

# Colors (RGB) - matching curses color definitions
# 256-color mode custom colors from renderer.py (scaled from 0-1000 to 0-255)
BG = (0, 0, 0)  # Terminal background
LIGHT_SQ_BG = (230, 217, 191)     # init_color(16, 900,850,750)
DARK_SQ_BG = (115, 150, 87)       # init_color(17, 450,590,340)
CURSOR_BG = (255, 230, 77)        # init_color(18, 1000,900,300)
LAST_LIGHT_BG = (230, 230, 153)   # init_color(21, 900,900,600)
LAST_DARK_BG = (153, 179, 89)     # init_color(22, 600,700,350)

WHITE_FG = (255, 255, 255)
BLACK_FG = (0, 0, 0)
CYAN_FG = (0, 255, 255)
YELLOW_FG = (255, 255, 0)
BORDER_FG = (255, 255, 255)


def get_font(size):
    """Load a monospace font (must support chess Unicode U+2654-265F)."""
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeMono.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def setup_board():
    """Set up an Italian Game position (same as before)."""
    from board import Board
    board = Board()
    for r in range(8):
        for c in range(8):
            board.grid[r][c] = None

    # White
    board.set_piece(7, 0, Piece(Color.WHITE, PieceType.ROOK))
    board.set_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
    board.set_piece(7, 7, Piece(Color.WHITE, PieceType.ROOK))
    board.set_piece(7, 3, Piece(Color.WHITE, PieceType.QUEEN))
    board.set_piece(5, 5, Piece(Color.WHITE, PieceType.KNIGHT))
    board.set_piece(5, 2, Piece(Color.WHITE, PieceType.KNIGHT))
    board.set_piece(4, 2, Piece(Color.WHITE, PieceType.BISHOP))
    board.set_piece(3, 6, Piece(Color.WHITE, PieceType.BISHOP))
    board.set_piece(6, 0, Piece(Color.WHITE, PieceType.PAWN))
    board.set_piece(6, 1, Piece(Color.WHITE, PieceType.PAWN))
    board.set_piece(6, 2, Piece(Color.WHITE, PieceType.PAWN))
    board.set_piece(5, 3, Piece(Color.WHITE, PieceType.PAWN))
    board.set_piece(4, 4, Piece(Color.WHITE, PieceType.PAWN))
    board.set_piece(6, 5, Piece(Color.WHITE, PieceType.PAWN))
    board.set_piece(6, 6, Piece(Color.WHITE, PieceType.PAWN))
    board.set_piece(6, 7, Piece(Color.WHITE, PieceType.PAWN))

    # Black
    board.set_piece(0, 0, Piece(Color.BLACK, PieceType.ROOK))
    board.set_piece(0, 4, Piece(Color.BLACK, PieceType.KING))
    board.set_piece(0, 7, Piece(Color.BLACK, PieceType.ROOK))
    board.set_piece(0, 3, Piece(Color.BLACK, PieceType.QUEEN))
    board.set_piece(2, 2, Piece(Color.BLACK, PieceType.KNIGHT))
    board.set_piece(2, 5, Piece(Color.BLACK, PieceType.KNIGHT))
    board.set_piece(3, 2, Piece(Color.BLACK, PieceType.BISHOP))
    board.set_piece(0, 2, Piece(Color.BLACK, PieceType.BISHOP))
    board.set_piece(1, 0, Piece(Color.BLACK, PieceType.PAWN))
    board.set_piece(1, 1, Piece(Color.BLACK, PieceType.PAWN))
    board.set_piece(2, 3, Piece(Color.BLACK, PieceType.PAWN))
    board.set_piece(3, 4, Piece(Color.BLACK, PieceType.PAWN))
    board.set_piece(1, 5, Piece(Color.BLACK, PieceType.PAWN))
    board.set_piece(1, 6, Piece(Color.BLACK, PieceType.PAWN))
    board.set_piece(1, 7, Piece(Color.BLACK, PieceType.PAWN))

    return board


def build_screen_buffer(board):
    """Build the exact text buffer and color map the renderer produces.

    Returns a list of rows, where each row is a list of (char, fg_color, bg_color).
    """
    # Initialize buffer with spaces on black background
    buf = [[((' ', BORDER_FG, BG)) for _ in range(TERM_COLS)] for _ in range(TERM_ROWS)]

    def put(row, col, text, fg, bg=BG):
        for i, ch in enumerate(text):
            c = col + i
            if 0 <= row < TERM_ROWS and 0 <= c < TERM_COLS:
                buf[row][c] = (ch, fg, bg)

    # Demo state
    cursor_pos = (2, 5)  # On the black knight at f6
    last_move_from = (7, 2)  # Bc1-g5 (approximate)
    last_move_to = (3, 6)
    last_move_squares = {last_move_from, last_move_to}

    # Title (row 0)
    title = " C H E S S "
    title_x = max(0, (min(TERM_COLS, PANEL_LEFT + 20) - len(title)) // 2)
    put(0, title_x, title, CYAN_FG)

    # File labels (row BOARD_TOP = 2)
    col_labels = "  a  b  c  d  e  f  g  h"
    put(BOARD_TOP, BOARD_LEFT - 1, col_labels, BORDER_FG)

    # Board rows
    for row in range(8):
        rank = str(8 - row)
        screen_y = BOARD_TOP + 1 + row

        # Rank label left
        put(screen_y, BOARD_LEFT - 3, rank, BORDER_FG)

        for col in range(8):
            piece = board.get_piece(row, col)
            is_light = (row + col) % 2 == 0
            sq = (row, col)

            # Determine background color
            if sq == cursor_pos:
                cell_bg = CURSOR_BG
                cell_fg = BLACK_FG
            elif sq in last_move_squares:
                cell_bg = LAST_LIGHT_BG if is_light else LAST_DARK_BG
                cell_fg = BLACK_FG
            else:
                cell_bg = LIGHT_SQ_BG if is_light else DARK_SQ_BG
                cell_fg = BLACK_FG

            # Override fg for pieces
            if piece:
                if sq == cursor_pos or sq in last_move_squares:
                    cell_fg = WHITE_FG if piece.color == Color.WHITE else BLACK_FG
                elif piece.color == Color.WHITE:
                    cell_fg = WHITE_FG
                else:
                    cell_fg = BLACK_FG

            # Build cell string (3 chars)
            if piece:
                symbol = piece.symbol()
                cell_str = f" {symbol} "
            else:
                cell_str = "   "

            screen_x = BOARD_LEFT + col * CELL_WIDTH
            for i, ch in enumerate(cell_str):
                cx = screen_x + i
                if 0 <= cx < TERM_COLS:
                    buf[screen_y][cx] = (ch, cell_fg, cell_bg)

        # Rank label right
        put(screen_y, BOARD_LEFT + 8 * CELL_WIDTH + 1, rank, BORDER_FG)

    # Bottom file labels
    put(BOARD_TOP + 1 + 8, BOARD_LEFT - 1, col_labels, BORDER_FG)

    # Side panel
    x = PANEL_LEFT
    y = BOARD_TOP

    put(y, x, "Captured:", BORDER_FG)
    y += 1
    put(y, x, "  -", BORDER_FG)
    y += 1
    put(y, x, "  -", BORDER_FG)
    y += 2

    put(y, x, "Black to move", YELLOW_FG)
    y += 2

    put(y, x, "Moves:", BORDER_FG)
    y += 1
    moves = [
        " 1. e4   e5",
        " 2. Nf3  Nc6",
        " 3. Bc4  Bc5",
        " 4. d3   d6",
        " 5. Nc3  Nf6",
        " 6. Bg5",
    ]
    for m in moves:
        put(y, x, m, BORDER_FG)
        y += 1

    # Controls
    y = max(y + 1, BOARD_TOP + 10)
    controls = [
        "Controls:",
        "  Arrows: Move cursor",
        "  Enter: Select/Place",
        "  Esc: Cancel",
        "  U: Undo  N: New",
        "  Q: Quit",
    ]
    for line in controls:
        if y < TERM_ROWS:
            put(y, x, line, BORDER_FG)
            y += 1

    return buf


def draw_screenshot():
    """Render the text buffer to an image, character by character.

    Uses a single monospace font for all characters (including chess pieces),
    just like a real terminal emulator would.
    """
    from board import Board

    board = setup_board()
    buf = build_screen_buffer(board)

    font = get_font(18)

    # Measure character cell size from the monospace font
    # Use font.getmetrics() for consistent line height
    ascent, descent = font.getmetrics()
    char_h = ascent + descent + 4  # small padding like a terminal
    # Monospace width: all chars same width
    char_w = font.getbbox("M")[2] - font.getbbox("M")[0]

    pad = 8
    img_w = TERM_COLS * char_w + 2 * pad
    img_h = TERM_ROWS * char_h + 2 * pad
    img = Image.new('RGB', (img_w, img_h), BG)
    draw = ImageDraw.Draw(img)

    for row_i, row in enumerate(buf):
        for col_i, (ch, fg, cell_bg) in enumerate(row):
            px = pad + col_i * char_w
            py = pad + row_i * char_h

            # Draw background cell
            if cell_bg != BG:
                draw.rectangle([px, py, px + char_w, py + char_h], fill=cell_bg)

            # Draw character at the fixed grid position
            if ch != ' ':
                draw.text((px, py + 2), ch, fill=fg, font=font)

    output_path = os.path.join(os.path.dirname(__file__), 'screenshot.png')
    img.save(output_path)
    print(f"Screenshot saved to {output_path}")


if __name__ == '__main__':
    draw_screenshot()
