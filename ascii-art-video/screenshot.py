#!/usr/bin/env python3
"""
Generate a screenshot of the ASCII Art Video application.

Renders a mid-fight scene to an image that looks like a terminal window.
Uses the actual rendering logic to build the screen buffer.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from PIL import Image, ImageDraw, ImageFont
from renderer import ScreenBuffer, Color, Cell
from scenes import (
    FightChoreography, render_title, FunnyMoment,
    STICK_IDLE, STICK_PUNCH_RIGHT, STICK_HIT, STICK_UPPERCUT,
    mirror_sprite, STICK_HADOUKEN, HADOUKEN_PROJECTILE
)
from effects import (
    draw_star_field, draw_fire, spawn_sparks, spawn_explosion,
    ParticleSystem, draw_energy_aura, draw_speed_lines
)
from animation import lerp
import math
import random


# Terminal color palette (256 color approximation)
COLOR_MAP = {
    0: (0, 0, 0),          # BLACK
    1: (205, 49, 49),      # RED
    2: (13, 188, 121),     # GREEN
    3: (229, 229, 16),     # YELLOW
    4: (36, 114, 200),     # BLUE
    5: (188, 63, 188),     # MAGENTA
    6: (17, 168, 205),     # CYAN
    7: (204, 204, 204),    # WHITE
    9: (255, 85, 85),      # BRIGHT_RED
    10: (85, 255, 85),     # BRIGHT_GREEN
    11: (255, 255, 85),    # BRIGHT_YELLOW
    12: (85, 85, 255),     # BRIGHT_BLUE
    13: (255, 85, 255),    # BRIGHT_MAGENTA
    14: (85, 255, 255),    # BRIGHT_CYAN
    15: (255, 255, 255),   # BRIGHT_WHITE
    208: (255, 135, 0),    # ORANGE
    236: (48, 48, 48),     # DARK_GRAY
    240: (88, 88, 88),     # GRAY
    250: (188, 188, 188),  # LIGHT_GRAY
}


def get_color(code: int) -> tuple:
    """Convert color code to RGB tuple."""
    if code in COLOR_MAP:
        return COLOR_MAP[code]
    # 256 color approximation
    if 16 <= code <= 231:
        code -= 16
        r = (code // 36) * 51
        g = ((code % 36) // 6) * 51
        b = (code % 6) * 51
        return (r, g, b)
    if 232 <= code <= 255:
        gray = (code - 232) * 10 + 8
        return (gray, gray, gray)
    return (204, 204, 204)


def render_buffer_to_image(buffer: ScreenBuffer, cell_width: int = 8, cell_height: int = 16) -> Image.Image:
    """Render a ScreenBuffer to a PIL Image that looks like a terminal."""
    w = buffer.width * cell_width
    h = buffer.height * cell_height

    # Add terminal chrome
    title_bar_height = 28
    border = 2
    total_w = w + border * 2
    total_h = h + title_bar_height + border * 2

    img = Image.new('RGB', (total_w, total_h), (40, 40, 40))
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([0, 0, total_w, title_bar_height], fill=(50, 50, 50))
    # Window buttons
    draw.ellipse([10, 8, 22, 20], fill=(255, 95, 86))    # Close
    draw.ellipse([28, 8, 40, 20], fill=(255, 189, 46))   # Minimize
    draw.ellipse([46, 8, 58, 20], fill=(39, 201, 63))    # Maximize
    # Title text
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 12)
    except (OSError, IOError):
        title_font = ImageFont.load_default()
    draw.text((total_w // 2 - 80, 7), "ASCII FIGHT - Terminal", fill=(180, 180, 180), font=title_font)

    # Try to load a monospace font
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 13)
    except (OSError, IOError):
        font = ImageFont.load_default()

    # Render each cell
    ox = border
    oy = title_bar_height + border

    for y in range(buffer.height):
        for x in range(buffer.width):
            cell = buffer.buffer[y][x]
            px = ox + x * cell_width
            py = oy + y * cell_height

            # Background
            bg_color = get_color(cell.bg)
            if bg_color != (0, 0, 0):
                draw.rectangle([px, py, px + cell_width - 1, py + cell_height - 1],
                              fill=bg_color)

            # Foreground character
            if cell.char != ' ':
                fg_color = get_color(cell.fg)
                # Center the character in the cell
                draw.text((px + 1, py), cell.char, fill=fg_color, font=font)

    return img


def build_fight_scene() -> ScreenBuffer:
    """Build a dramatic mid-fight scene for the screenshot."""
    random.seed(42)
    buf = ScreenBuffer(80, 24)
    w, h = buf.width, buf.height

    # Arena background
    for y in range(4, h - 5):
        if y % 4 == 0:
            for x in range(0, w, 8):
                buf.set_cell(x, y, '.', Color.DARK_GRAY)

    # Ground
    ground_y = h - 5
    for x in range(w):
        buf.set_cell(x, ground_y, '=' if x % 3 == 0 else '_', Color.GRAY)

    # Health bars
    bar_width = 20
    buf.draw_text(2, 1, "P1 FIGHTER", Color.BRIGHT_CYAN)
    p1_health = 65
    filled = int(p1_health / 100 * bar_width)
    bar = '[' + '█' * filled + '░' * (bar_width - filled) + ']'
    buf.draw_text(2, 2, bar, Color.YELLOW)

    p2_label = "P2 FIGHTER"
    buf.draw_text(w - 2 - len(p2_label), 1, p2_label, Color.BRIGHT_RED)
    p2_health = 30
    filled = int(p2_health / 100 * bar_width)
    bar = '[' + '█' * filled + '░' * (bar_width - filled) + ']'
    buf.draw_text(w - 2 - bar_width - 2, 2, bar, Color.RED)

    # Timer
    buf.draw_text_centered(1, "42", Color.BRIGHT_YELLOW)

    # P1 doing a hadouken
    p1_x = w // 2 - 15
    hadouken_sprite = [
        "  O    ",
        " /|\\=>>",
        " / \\   ",
    ]
    buf.draw_sprite(p1_x, ground_y - 2, hadouken_sprite, Color.BRIGHT_CYAN, transparent=' ')

    # Energy aura around P1
    draw_energy_aura(buf, p1_x + 2, ground_y - 2, 4, Color.BRIGHT_CYAN, 0.3)

    # Hadouken projectile in flight
    proj_x = w // 2
    projectile = [
        " ~*~ ",
        "~(O)~",
        " ~*~ ",
    ]
    buf.draw_sprite(proj_x, ground_y - 3, projectile, Color.BRIGHT_CYAN, transparent=' ')

    # Trail behind projectile
    for i in range(5):
        tx = proj_x - i * 2 - 2
        if 0 <= tx < w:
            buf.set_cell(tx, ground_y - 2, '~', Color.CYAN)
            if i < 3:
                buf.set_cell(tx, ground_y - 3, '.', Color.BRIGHT_CYAN)

    # P2 in a blocking stance
    p2_x = w // 2 + 12
    block_sprite = mirror_sprite([
        "  O  ",
        " /|\\ ",
        "  |  ",
        " / \\ ",
    ])
    buf.draw_sprite(p2_x, ground_y - 3, block_sprite, Color.BRIGHT_RED, transparent=' ')

    # Sparks at impact point
    spark_chars = ['*', '+', '.', "'"]
    spark_colors = [Color.YELLOW, Color.BRIGHT_YELLOW, Color.WHITE, Color.BRIGHT_WHITE]
    for i in range(12):
        sx = proj_x + 6 + random.randint(-3, 3)
        sy = ground_y - 2 + random.randint(-2, 1)
        if 0 <= sx < w and 0 <= sy < h:
            buf.set_cell(sx, sy, random.choice(spark_chars), random.choice(spark_colors))

    # "HADOUKEN!!!" text
    buf.draw_text_centered(ground_y - 9, "HADOUKEN!!!", Color.BRIGHT_CYAN)

    # Combo counter
    buf.draw_text(w // 2 - 5, 4, "5x COMBO!", Color.BRIGHT_YELLOW)
    buf.draw_text(w // 2 - 6, 3, ">" * 11, Color.BRIGHT_RED)

    # Speed lines in background
    speed_positions = [(5, 8, 6), (70, 12, 5), (3, 15, 8), (65, 7, 4),
                       (10, 10, 7), (60, 14, 5), (15, 6, 6)]
    for sx, sy, slen in speed_positions:
        for dx in range(slen):
            if 0 <= sx + dx < w and 0 <= sy < h:
                buf.set_cell(sx + dx, sy, '-', Color.GRAY)

    # Fire effect at bottom
    fire_chars = ['.', ':', '^', '*', '#']
    fire_colors = [Color.RED, Color.BRIGHT_RED, Color.ORANGE, Color.YELLOW, Color.BRIGHT_YELLOW]
    for x in range(w):
        for dy in range(3):
            fy = h - 1 - dy
            if random.random() < 0.3 * (1 - dy / 3):
                ci = min(dy, len(fire_colors) - 1)
                buf.set_cell(x, fy, random.choice(fire_chars), fire_colors[ci])

    # Explosion particles scattered around
    explosion_chars = ['*', '#', '@', '+', 'o']
    explosion_colors = [Color.BRIGHT_RED, Color.BRIGHT_YELLOW, Color.ORANGE]
    for _ in range(15):
        ex = random.randint(w // 2 - 5, w // 2 + 15)
        ey = random.randint(ground_y - 6, ground_y - 1)
        if 0 <= ex < w and 0 <= ey < h:
            buf.set_cell(ex, ey, random.choice(explosion_chars),
                        random.choice(explosion_colors))

    return buf


def main():
    """Generate the screenshot."""
    buf = build_fight_scene()
    img = render_buffer_to_image(buf, cell_width=8, cell_height=16)

    output_path = os.path.join(os.path.dirname(__file__), "screenshot.png")
    img.save(output_path, "PNG")
    print(f"Screenshot saved to {output_path}")
    print(f"Image size: {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
