"""Generate a screenshot of the Tetris game in action."""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from PIL import Image, ImageDraw, ImageFont
from pieces import PieceType, SHAPES, get_cells
from board import Board, BOARD_WIDTH, BOARD_HEIGHT
from game import GameState

# Terminal color palette
COLORS = {
    PieceType.I: (0, 220, 220),    # cyan
    PieceType.O: (220, 220, 0),    # yellow
    PieceType.T: (180, 0, 220),    # magenta
    PieceType.S: (0, 220, 0),      # green
    PieceType.Z: (220, 0, 0),      # red
    PieceType.J: (0, 80, 220),     # blue
    PieceType.L: (220, 140, 0),    # orange
}
GHOST_COLOR = (80, 80, 80)
BG_COLOR = (18, 18, 18)
GRID_COLOR = (35, 35, 35)
BORDER_COLOR = (100, 100, 100)
TEXT_COLOR = (200, 200, 200)
TITLE_COLOR = (0, 220, 220)

CELL_SIZE = 28
PADDING = 20


def build_demo_state():
    """Build a mid-game state that looks interesting."""
    gs = GameState(seed=7)

    # Drop several pieces to build up the board
    moves = [
        # piece 1: hard drop
        lambda: gs.hard_drop(),
        # piece 2: move left, drop
        lambda: (gs.move_left(), gs.move_left(), gs.hard_drop()),
        # piece 3: move right, drop
        lambda: (gs.move_right(), gs.move_right(), gs.hard_drop()),
        # piece 4: rotate, drop
        lambda: (gs.rotate_cw(), gs.hard_drop()),
        # piece 5: drop
        lambda: gs.hard_drop(),
        # piece 6: move left, drop
        lambda: (gs.move_left(), gs.move_left(), gs.move_left(), gs.hard_drop()),
        # piece 7: move right, rotate, drop
        lambda: (gs.move_right(), gs.move_right(), gs.rotate_cw(), gs.hard_drop()),
        # piece 8: drop
        lambda: gs.hard_drop(),
        # piece 9: move left, drop
        lambda: (gs.move_left(), gs.hard_drop()),
        # piece 10: rotate, move right, drop
        lambda: (gs.rotate_cw(), gs.move_right(), gs.move_right(), gs.move_right(), gs.hard_drop()),
    ]

    for m in moves:
        if gs.game_over:
            break
        m()

    # Now move the current piece partway down for a nice in-action look
    for _ in range(6):
        gs.move_down()

    return gs


def render_screenshot(gs, output_path):
    """Render the game state to a PNG image."""
    board_w = BOARD_WIDTH * CELL_SIZE
    board_h = BOARD_HEIGHT * CELL_SIZE
    panel_w = 180
    img_w = PADDING * 3 + board_w + panel_w
    img_h = PADDING * 2 + board_h + 40  # extra for title

    img = Image.new('RGB', (img_w, img_h), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Try to load a monospace font
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 22)
        font_med = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 16)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 13)
    except (OSError, IOError):
        font_large = ImageFont.load_default()
        font_med = font_large
        font_small = font_large

    # Title
    title = "T E T R I S"
    draw.text((PADDING + board_w // 2 - 70, PADDING // 2), title, fill=TITLE_COLOR, font=font_large)

    board_x = PADDING
    board_y = PADDING + 30

    # Board background
    draw.rectangle([board_x - 2, board_y - 2, board_x + board_w + 1, board_y + board_h + 1],
                   outline=BORDER_COLOR, width=2)

    # Grid dots
    for r in range(BOARD_HEIGHT):
        for c in range(BOARD_WIDTH):
            x = board_x + c * CELL_SIZE
            y = board_y + r * CELL_SIZE
            draw.rectangle([x + 1, y + 1, x + CELL_SIZE - 2, y + CELL_SIZE - 2],
                           fill=GRID_COLOR, outline=None)

    # Locked cells
    for r in range(BOARD_HEIGHT):
        for c in range(BOARD_WIDTH):
            cell = gs.board.get_cell(r, c)
            if cell is not None:
                x = board_x + c * CELL_SIZE
                y = board_y + r * CELL_SIZE
                color = COLORS[cell]
                draw.rectangle([x + 1, y + 1, x + CELL_SIZE - 2, y + CELL_SIZE - 2],
                               fill=color, outline=tuple(min(255, v + 40) for v in color))
                # Highlight
                draw.rectangle([x + 3, y + 3, x + CELL_SIZE // 2, y + CELL_SIZE // 2],
                               fill=tuple(min(255, v + 60) for v in color), outline=None)

    # Ghost piece
    if gs.current_piece is not None:
        ghost_row = gs.get_ghost_row()
        cells = get_cells(gs.current_piece, gs.current_rotation)
        for dr, dc in cells:
            r, c = ghost_row + dr, gs.current_col + dc
            x = board_x + c * CELL_SIZE
            y = board_y + r * CELL_SIZE
            draw.rectangle([x + 2, y + 2, x + CELL_SIZE - 3, y + CELL_SIZE - 3],
                           fill=None, outline=GHOST_COLOR, width=2)

    # Current piece
    if gs.current_piece is not None:
        cells = get_cells(gs.current_piece, gs.current_rotation)
        color = COLORS[gs.current_piece]
        for dr, dc in cells:
            r, c = gs.current_row + dr, gs.current_col + dc
            x = board_x + c * CELL_SIZE
            y = board_y + r * CELL_SIZE
            draw.rectangle([x + 1, y + 1, x + CELL_SIZE - 2, y + CELL_SIZE - 2],
                           fill=color, outline=tuple(min(255, v + 50) for v in color))
            draw.rectangle([x + 3, y + 3, x + CELL_SIZE // 2, y + CELL_SIZE // 2],
                           fill=tuple(min(255, v + 80) for v in color), outline=None)

    # Side panel
    panel_x = board_x + board_w + PADDING
    panel_y = board_y

    # Next piece
    draw.text((panel_x, panel_y), "NEXT", fill=TEXT_COLOR, font=font_med)
    next_cells = get_cells(gs.next_piece, 0)
    next_color = COLORS[gs.next_piece]
    for dr, dc in next_cells:
        x = panel_x + dc * (CELL_SIZE - 4)
        y = panel_y + 28 + dr * (CELL_SIZE - 4)
        draw.rectangle([x, y, x + CELL_SIZE - 6, y + CELL_SIZE - 6],
                       fill=next_color, outline=tuple(min(255, v + 40) for v in next_color))

    # Score panel
    score_y = panel_y + 110
    draw.text((panel_x, score_y), "SCORE", fill=TEXT_COLOR, font=font_med)
    draw.text((panel_x, score_y + 22), str(gs.score), fill=(255, 255, 255), font=font_large)

    draw.text((panel_x, score_y + 60), "LEVEL", fill=TEXT_COLOR, font=font_med)
    draw.text((panel_x, score_y + 82), str(gs.level), fill=(255, 255, 255), font=font_large)

    draw.text((panel_x, score_y + 120), "LINES", fill=TEXT_COLOR, font=font_med)
    draw.text((panel_x, score_y + 142), str(gs.lines_cleared), fill=(255, 255, 255), font=font_large)

    # Controls
    ctrl_y = score_y + 200
    draw.text((panel_x, ctrl_y), "CONTROLS", fill=GHOST_COLOR, font=font_small)
    controls = [
        "Arrows  Move",
        "Up      Rotate",
        "Z       Rot CCW",
        "Space   Drop",
        "P       Pause",
        "Q       Quit",
    ]
    for i, line in enumerate(controls):
        draw.text((panel_x, ctrl_y + 18 + i * 16), line, fill=GHOST_COLOR, font=font_small)

    img.save(output_path)
    print(f"Screenshot saved to {output_path}")


if __name__ == "__main__":
    gs = build_demo_state()
    render_screenshot(gs, os.path.join(os.path.dirname(__file__), "screenshot.png"))
