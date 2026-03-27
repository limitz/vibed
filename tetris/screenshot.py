"""Generate a screenshot that faithfully reproduces the curses terminal output."""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from PIL import Image, ImageDraw, ImageFont
from pieces import PieceType, COLORS as PIECE_COLOR_IDX, get_cells
from board import BOARD_WIDTH, BOARD_HEIGHT
from game import GameState

# Terminal color palette matching curses colors (black bg + colored fg/bg)
# For piece cells: black text on colored background
PIECE_BG_COLORS = {
    PieceType.I: (0, 190, 190),     # cyan
    PieceType.O: (190, 190, 0),     # yellow
    PieceType.T: (190, 0, 190),     # magenta
    PieceType.S: (0, 190, 0),       # green
    PieceType.Z: (190, 0, 0),       # red
    PieceType.J: (0, 0, 190),       # blue
    PieceType.L: (190, 190, 190),   # white
}
PIECE_FG = (0, 0, 0)  # black text on colored bg

TERM_BG = (0, 0, 0)          # terminal background
TERM_FG = (190, 190, 190)    # default text
TERM_DIM = (100, 100, 100)   # dim text
TERM_CYAN = (0, 190, 190)    # title color
TERM_BOLD = (255, 255, 255)  # bold white
GHOST_FG = (100, 100, 100)   # ghost piece dim white


def build_demo_state():
    """Build a mid-game state that looks interesting."""
    gs = GameState(seed=7)
    moves = [
        lambda: gs.hard_drop(),
        lambda: (gs.move_left(), gs.move_left(), gs.hard_drop()),
        lambda: (gs.move_right(), gs.move_right(), gs.hard_drop()),
        lambda: (gs.rotate_cw(), gs.hard_drop()),
        lambda: gs.hard_drop(),
        lambda: (gs.move_left(), gs.move_left(), gs.move_left(), gs.hard_drop()),
        lambda: (gs.move_right(), gs.move_right(), gs.rotate_cw(), gs.hard_drop()),
        lambda: gs.hard_drop(),
        lambda: (gs.move_left(), gs.hard_drop()),
        lambda: (gs.rotate_cw(), gs.move_right(), gs.move_right(), gs.move_right(), gs.hard_drop()),
    ]
    for m in moves:
        if gs.game_over:
            break
        m()
    for _ in range(6):
        gs.move_down()
    return gs


def build_screen_buffer(gs):
    """Build a 2D buffer of (char, fg_color, bg_color) matching the renderer output."""
    ROWS = 24
    COLS = 50
    board_y, board_x = 2, 2
    cell_w = 2

    # Initialize with spaces
    buf = [[((' ', TERM_FG, TERM_BG)) for _ in range(COLS)] for _ in range(ROWS)]

    def put(r, c, text, fg=TERM_FG, bg=TERM_BG):
        for i, ch in enumerate(text):
            if 0 <= r < ROWS and 0 <= c + i < COLS:
                buf[r][c + i] = (ch, fg, bg)

    # Title
    put(0, board_x + 4, "T E T R I S", fg=TERM_CYAN)

    # Border
    w = BOARD_WIDTH * cell_w
    put(board_y - 1, board_x - 1, "+" + "-" * w + "+", fg=TERM_DIM)
    for r in range(BOARD_HEIGHT):
        put(board_y + r, board_x - 1, "|", fg=TERM_DIM)
        put(board_y + r, board_x + w, "|", fg=TERM_DIM)
    put(board_y + BOARD_HEIGHT, board_x - 1, "+" + "-" * w + "+", fg=TERM_DIM)

    # Empty board cells
    for r in range(BOARD_HEIGHT):
        for c in range(BOARD_WIDTH):
            y = board_y + r
            x = board_x + c * cell_w
            put(y, x, " .", fg=TERM_DIM)

    # Locked cells
    for r in range(BOARD_HEIGHT):
        for c in range(BOARD_WIDTH):
            cell = gs.board.get_cell(r, c)
            if cell is not None:
                y = board_y + r
                x = board_x + c * cell_w
                put(y, x, "[]", fg=PIECE_FG, bg=PIECE_BG_COLORS[cell])

    # Ghost piece
    if gs.current_piece is not None:
        ghost_row = gs.get_ghost_row()
        if ghost_row != gs.current_row:
            cells = get_cells(gs.current_piece, gs.current_rotation)
            for dr, dc in cells:
                y = board_y + ghost_row + dr
                x = board_x + (gs.current_col + dc) * cell_w
                put(y, x, "..", fg=GHOST_FG)

    # Current piece
    if gs.current_piece is not None:
        cells = get_cells(gs.current_piece, gs.current_rotation)
        color = PIECE_BG_COLORS[gs.current_piece]
        for dr, dc in cells:
            y = board_y + gs.current_row + dr
            x = board_x + (gs.current_col + dc) * cell_w
            put(y, x, "[]", fg=PIECE_FG, bg=color)

    # Side panel
    panel_x = board_x + BOARD_WIDTH * cell_w + 3
    panel_y = board_y

    # Next piece
    put(panel_y, panel_x, "NEXT:", fg=TERM_BOLD)
    next_cells = get_cells(gs.next_piece, 0)
    next_color = PIECE_BG_COLORS[gs.next_piece]
    for dr, dc in next_cells:
        put(panel_y + 1 + dr, panel_x + dc * cell_w, "[]", fg=PIECE_FG, bg=next_color)

    # Score panel
    put(panel_y + 5, panel_x, f"SCORE: {gs.score}", fg=TERM_BOLD)
    put(panel_y + 6, panel_x, f"LEVEL: {gs.level}", fg=TERM_BOLD)
    put(panel_y + 7, panel_x, f"LINES: {gs.lines_cleared}", fg=TERM_BOLD)

    # Controls
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
        put(panel_y + 10 + i, panel_x, line, fg=TERM_DIM)

    return buf


def render_screenshot(gs, output_path):
    """Render the screen buffer to a PNG that looks like a terminal."""
    buf = build_screen_buffer(gs)
    rows = len(buf)
    cols = len(buf[0])

    # Load monospace font
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 16)
    except (OSError, IOError):
        font = ImageFont.load_default()

    # Measure character size
    bbox = font.getbbox("X")
    char_w = bbox[2] - bbox[0]
    char_h = int((bbox[3] - bbox[1]) * 1.4)  # line height

    padding = 12
    img_w = cols * char_w + padding * 2
    img_h = rows * char_h + padding * 2

    img = Image.new('RGB', (img_w, img_h), TERM_BG)
    draw = ImageDraw.Draw(img)

    for r, row in enumerate(buf):
        for c, (ch, fg, bg) in enumerate(row):
            x = padding + c * char_w
            y = padding + r * char_h
            # Draw background if not default
            if bg != TERM_BG:
                draw.rectangle([x, y, x + char_w - 1, y + char_h - 1], fill=bg)
            # Draw character
            if ch != ' ':
                draw.text((x, y), ch, fill=fg, font=font)

    img.save(output_path)
    print(f"Screenshot saved to {output_path}")


if __name__ == "__main__":
    gs = build_demo_state()
    render_screenshot(gs, os.path.join(os.path.dirname(__file__), "screenshot.png"))
