"""Generate screenshot.png showing the app as it would appear in a terminal."""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from PIL import Image, ImageDraw, ImageFont

from renderer import ScreenBuffer, Color
from timeline import Timeline
from player import Player
from hud import draw_hud
from scenes import create_all_scenes


# Terminal dimensions
COLS = 100
ROWS = 32

# Font settings
FONT_SIZE = 14
FONT_PATH = "DejaVuSansMono.ttf"
CELL_WIDTH = 8
CELL_HEIGHT = 16

# Color map: Color enum -> RGB tuple
COLOR_RGB = {
    Color.BLACK: (0, 0, 0),
    Color.RED: (170, 0, 0),
    Color.GREEN: (0, 170, 0),
    Color.YELLOW: (170, 170, 0),
    Color.BLUE: (0, 0, 170),
    Color.MAGENTA: (170, 0, 170),
    Color.CYAN: (0, 170, 170),
    Color.WHITE: (170, 170, 170),
    Color.BRIGHT_RED: (255, 85, 85),
    Color.BRIGHT_GREEN: (85, 255, 85),
    Color.BRIGHT_YELLOW: (255, 255, 85),
    Color.BRIGHT_BLUE: (85, 85, 255),
    Color.BRIGHT_MAGENTA: (255, 85, 255),
    Color.BRIGHT_CYAN: (85, 255, 255),
    Color.BRIGHT_WHITE: (255, 255, 255),
    Color.GRAY: (128, 128, 128),
    Color.DARK_GRAY: (64, 64, 64),
    Color.ORANGE: (255, 165, 0),
}


def build_demo_state():
    """Build a realistic mid-action demo state showing Scene 7 (HAL refusing)."""
    scenes = create_all_scenes()
    timeline = Timeline(scenes)
    player = Player(timeline)

    # Position in Scene 7: "I'm Sorry Dave" - HAL refusing to open pod bay doors
    # Scene 7 starts at 25 + 15 + 20 + 15 + 20 + 20 = 115s, lasts 15s
    # Show at about 40% through: dialogue "I'm sorry, Dave..."
    player.position = 115.0 + 6.0  # 6 seconds into the scene
    player.speed = 1.0
    player.play()

    buffer = ScreenBuffer(COLS, ROWS)
    buffer.clear()
    player.get_current_frame(buffer)
    draw_hud(buffer, player)

    return buffer


def render_buffer_to_image(buffer):
    """Render a ScreenBuffer to a PIL Image."""
    # Terminal window chrome
    title_bar_height = 24
    padding = 2

    img_width = buffer.width * CELL_WIDTH + padding * 2
    img_height = buffer.height * CELL_HEIGHT + title_bar_height + padding * 2

    img = Image.new('RGB', (img_width, img_height), (30, 30, 30))
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([0, 0, img_width, title_bar_height], fill=(50, 50, 50))
    # Window buttons
    draw.ellipse([8, 6, 20, 18], fill=(255, 95, 86))
    draw.ellipse([28, 6, 40, 18], fill=(255, 189, 46))
    draw.ellipse([48, 6, 60, 18], fill=(39, 201, 63))
    # Title text
    try:
        title_font = ImageFont.truetype(FONT_PATH, 11)
    except OSError:
        title_font = ImageFont.load_default()
    draw.text((img_width // 2 - 80, 5), "2001: A Space Odyssey — ASCII Re-enactment",
              fill=(180, 180, 180), font=title_font)

    # Terminal background
    term_x = padding
    term_y = title_bar_height + padding
    draw.rectangle(
        [term_x, term_y,
         term_x + buffer.width * CELL_WIDTH,
         term_y + buffer.height * CELL_HEIGHT],
        fill=(0, 0, 0)
    )

    # Load font
    try:
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    except OSError:
        font = ImageFont.load_default()

    # Render each cell
    for y in range(buffer.height):
        for x in range(buffer.width):
            cell = buffer.grid[y][x]
            px = term_x + x * CELL_WIDTH
            py = term_y + y * CELL_HEIGHT

            # Background
            bg_rgb = COLOR_RGB.get(cell.bg, (0, 0, 0))
            if bg_rgb != (0, 0, 0):
                draw.rectangle(
                    [px, py, px + CELL_WIDTH, py + CELL_HEIGHT],
                    fill=bg_rgb
                )

            # Character
            if cell.char != ' ':
                fg_rgb = COLOR_RGB.get(cell.fg, (170, 170, 170))
                draw.text((px, py), cell.char, fill=fg_rgb, font=font)

    return img


def main():
    print("Building demo state...")
    buffer = build_demo_state()

    print("Rendering to image...")
    img = render_buffer_to_image(buffer)

    output_path = os.path.join(os.path.dirname(__file__), "screenshot.png")
    img.save(output_path)
    print(f"Screenshot saved to {output_path}")
    print(f"Image size: {img.width}x{img.height}")


if __name__ == "__main__":
    main()
