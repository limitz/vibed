#!/usr/bin/env python3
"""Generate screenshot.png by faithfully reproducing the curses renderer output."""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from PIL import Image, ImageDraw, ImageFont
from pieces import Color, Piece, PieceType, UNICODE_SYMBOLS
from board import Board, Move

# Colors matching the curses renderer
BG_COLOR = (30, 30, 30)           # Terminal background
LIGHT_SQUARE = (230, 217, 191)    # Warm cream
DARK_SQUARE = (115, 150, 87)      # Forest green
WHITE_PIECE = (255, 255, 255)
BLACK_PIECE = (40, 40, 40)
BORDER_COLOR = (200, 200, 200)
TITLE_COLOR = (80, 200, 200)
STATUS_COLOR = (220, 200, 80)
CURSOR_COLOR = (255, 230, 77)
LAST_MOVE_LIGHT = (230, 230, 153)
LAST_MOVE_DARK = (153, 179, 89)
LEGAL_MOVE_BG = (128, 204, 128)
SELECTED_BG = (102, 191, 217)
CHECK_BG = (230, 77, 77)

# Layout
CELL_SIZE = 56
BOARD_MARGIN_TOP = 60
BOARD_MARGIN_LEFT = 50
PANEL_OFFSET = BOARD_MARGIN_LEFT + CELL_SIZE * 8 + 40
IMG_WIDTH = PANEL_OFFSET + 250
IMG_HEIGHT = BOARD_MARGIN_TOP + CELL_SIZE * 8 + 60


def get_font(size):
    """Try to load a good monospace font, falling back to default."""
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeMono.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def get_piece_font(size):
    """Load a font that supports chess Unicode symbols."""
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def setup_demo_state():
    """Create a mid-game demo state programmatically.

    Simulates an Italian Game position after several moves:
    1.e4 e5 2.Nf3 Nc6 3.Bc4 Bc5 4.d3 d6 5.Nc3 Nf6 6.Bg5
    """
    board = Board()
    moves = [
        Move((6, 4), (4, 4)),  # 1. e4
        Move((1, 4), (3, 4)),  # e5
        Move((7, 6), (5, 5)),  # 2. Nf3
        Move((0, 1), (2, 2)),  # Nc6
        Move((7, 5), (4, 2)),  # 3. Bc4
        Move((0, 5), (3, 2)),  # Bc5
        Move((6, 3), (5, 3)),  # 4. d3
        Move((1, 3), (3, 3)),  # d6 (actually d5 target is row 3, but d6 = row 2)
    ]
    # Let's manually set up the position instead for accuracy
    board = Board()
    # Clear the board
    for r in range(8):
        for c in range(8):
            board.grid[r][c] = None

    # Set up a nice mid-game Italian Game position
    # White pieces
    board.set_piece(7, 0, Piece(Color.WHITE, PieceType.ROOK))
    board.set_piece(7, 4, Piece(Color.WHITE, PieceType.KING))
    board.set_piece(7, 7, Piece(Color.WHITE, PieceType.ROOK))
    board.set_piece(7, 3, Piece(Color.WHITE, PieceType.QUEEN))
    board.set_piece(5, 5, Piece(Color.WHITE, PieceType.KNIGHT))  # Nf3
    board.set_piece(5, 2, Piece(Color.WHITE, PieceType.KNIGHT))  # Nc3
    board.set_piece(4, 2, Piece(Color.WHITE, PieceType.BISHOP))  # Bc4
    board.set_piece(3, 6, Piece(Color.WHITE, PieceType.BISHOP))  # Bg5
    board.set_piece(6, 0, Piece(Color.WHITE, PieceType.PAWN))    # a2
    board.set_piece(6, 1, Piece(Color.WHITE, PieceType.PAWN))    # b2
    board.set_piece(6, 2, Piece(Color.WHITE, PieceType.PAWN))    # c2
    board.set_piece(5, 3, Piece(Color.WHITE, PieceType.PAWN))    # d3
    board.set_piece(4, 4, Piece(Color.WHITE, PieceType.PAWN))    # e4
    board.set_piece(6, 5, Piece(Color.WHITE, PieceType.PAWN))    # f2
    board.set_piece(6, 6, Piece(Color.WHITE, PieceType.PAWN))    # g2
    board.set_piece(6, 7, Piece(Color.WHITE, PieceType.PAWN))    # h2

    # Black pieces
    board.set_piece(0, 0, Piece(Color.BLACK, PieceType.ROOK))
    board.set_piece(0, 4, Piece(Color.BLACK, PieceType.KING))
    board.set_piece(0, 7, Piece(Color.BLACK, PieceType.ROOK))
    board.set_piece(0, 3, Piece(Color.BLACK, PieceType.QUEEN))
    board.set_piece(2, 2, Piece(Color.BLACK, PieceType.KNIGHT))  # Nc6
    board.set_piece(2, 5, Piece(Color.BLACK, PieceType.KNIGHT))  # Nf6
    board.set_piece(3, 2, Piece(Color.BLACK, PieceType.BISHOP))  # Bc5
    board.set_piece(0, 2, Piece(Color.BLACK, PieceType.BISHOP))  # Bc8
    board.set_piece(1, 0, Piece(Color.BLACK, PieceType.PAWN))    # a7
    board.set_piece(1, 1, Piece(Color.BLACK, PieceType.PAWN))    # b7
    board.set_piece(2, 3, Piece(Color.BLACK, PieceType.PAWN))    # d6
    board.set_piece(3, 4, Piece(Color.BLACK, PieceType.PAWN))    # e5
    board.set_piece(1, 5, Piece(Color.BLACK, PieceType.PAWN))    # f7
    board.set_piece(1, 6, Piece(Color.BLACK, PieceType.PAWN))    # g7
    board.set_piece(1, 7, Piece(Color.BLACK, PieceType.PAWN))    # h7

    return board


def draw_screenshot():
    """Generate the screenshot image."""
    img = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font = get_font(16)
    font_small = get_font(13)
    piece_font = get_piece_font(32)
    title_font = get_font(22)

    board = setup_demo_state()

    # Demo state
    cursor_pos = (2, 5)  # Cursor on Nf6
    selected_square = None
    last_move = Move((7, 2, ), (3, 6))  # Bg5 was last move
    move_history = [
        "1. e4   e5",
        "2. Nf3  Nc6",
        "3. Bc4  Bc5",
        "4. d3   d6",
        "5. Nc3  Nf6",
        "6. Bg5",
    ]
    status_msg = "Black to move"

    # Draw title
    title = "C H E S S"
    title_x = (BOARD_MARGIN_LEFT + CELL_SIZE * 4) - len(title) * 6
    draw.text((title_x, 15), title, fill=TITLE_COLOR, font=title_font)

    # Draw file labels (top)
    files = "abcdefgh"
    for c in range(8):
        x = BOARD_MARGIN_LEFT + c * CELL_SIZE + CELL_SIZE // 2 - 4
        draw.text((x, BOARD_MARGIN_TOP - 18), files[c], fill=BORDER_COLOR, font=font_small)

    # Draw board
    for row in range(8):
        rank = str(8 - row)
        # Rank label (left)
        ry = BOARD_MARGIN_TOP + row * CELL_SIZE + CELL_SIZE // 2 - 8
        draw.text((BOARD_MARGIN_LEFT - 20, ry), rank, fill=BORDER_COLOR, font=font)

        for col in range(8):
            x = BOARD_MARGIN_LEFT + col * CELL_SIZE
            y = BOARD_MARGIN_TOP + row * CELL_SIZE
            is_light = (row + col) % 2 == 0

            # Determine square color
            sq = (row, col)
            if sq == cursor_pos:
                bg = CURSOR_COLOR
            elif last_move and sq in (last_move.from_sq, last_move.to_sq):
                bg = LAST_MOVE_LIGHT if is_light else LAST_MOVE_DARK
            else:
                bg = LIGHT_SQUARE if is_light else DARK_SQUARE

            # Draw square
            draw.rectangle([x, y, x + CELL_SIZE, y + CELL_SIZE], fill=bg)

            # Draw piece
            piece = board.get_piece(row, col)
            if piece:
                symbol = piece.symbol()
                # Center the piece symbol
                bbox = piece_font.getbbox(symbol)
                tw = bbox[2] - bbox[0]
                th = bbox[3] - bbox[1]
                px = x + (CELL_SIZE - tw) // 2
                py = y + (CELL_SIZE - th) // 2 - 4

                # Draw piece with outline for visibility
                piece_color = WHITE_PIECE if piece.color == Color.WHITE else BLACK_PIECE
                outline_color = BLACK_PIECE if piece.color == Color.WHITE else (180, 180, 180)

                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx != 0 or dy != 0:
                            draw.text((px + dx, py + dy), symbol,
                                      fill=outline_color, font=piece_font)
                draw.text((px, py), symbol, fill=piece_color, font=piece_font)

        # Rank label (right)
        draw.text((BOARD_MARGIN_LEFT + 8 * CELL_SIZE + 8, ry), rank,
                  fill=BORDER_COLOR, font=font)

    # Draw file labels (bottom)
    for c in range(8):
        x = BOARD_MARGIN_LEFT + c * CELL_SIZE + CELL_SIZE // 2 - 4
        draw.text((x, BOARD_MARGIN_TOP + 8 * CELL_SIZE + 5), files[c],
                  fill=BORDER_COLOR, font=font_small)

    # Side panel
    px = PANEL_OFFSET
    py = BOARD_MARGIN_TOP

    # Captured pieces (none in this demo)
    draw.text((px, py), "Captured:", fill=BORDER_COLOR, font=font)
    py += 22
    draw.text((px + 10, py), "-", fill=BORDER_COLOR, font=font)
    py += 20
    draw.text((px + 10, py), "-", fill=BORDER_COLOR, font=font)
    py += 30

    # Status
    draw.text((px, py), status_msg, fill=STATUS_COLOR, font=font)
    py += 30

    # Move history
    draw.text((px, py), "Moves:", fill=BORDER_COLOR, font=font)
    py += 22
    for move_text in move_history:
        draw.text((px + 10, py), move_text, fill=BORDER_COLOR, font=font_small)
        py += 18

    # Controls
    py = BOARD_MARGIN_TOP + CELL_SIZE * 6
    controls = [
        "Controls:",
        "  Arrows: Move cursor",
        "  Enter: Select/Place",
        "  Esc: Cancel",
        "  U: Undo  N: New",
        "  Q: Quit",
    ]
    for line in controls:
        draw.text((px, py), line, fill=BORDER_COLOR, font=font_small)
        py += 17

    # Save
    output_path = os.path.join(os.path.dirname(__file__), 'screenshot.png')
    img.save(output_path)
    print(f"Screenshot saved to {output_path}")


if __name__ == '__main__':
    draw_screenshot()
