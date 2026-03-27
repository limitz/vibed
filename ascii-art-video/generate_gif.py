#!/usr/bin/env python3
"""
Generate an animated GIF of the entire ASCII Art Video sequence.

Renders every frame using the actual scene logic, converts each to
an image, and combines them into an optimized animated GIF.
"""

import sys
import os
import random

sys.path.insert(0, os.path.dirname(__file__))

from PIL import Image, ImageDraw, ImageFont
from renderer import ScreenBuffer, Color
from animation import Scene, Timeline
from scenes import (
    render_title, FightChoreography, FunnyMoment,
    render_fade_out, render_credits,
)

# ── colour palette (same as screenshot.py) ──────────────────────────────────

COLOR_MAP = {
    0: (0, 0, 0),
    1: (205, 49, 49),
    2: (13, 188, 121),
    3: (229, 229, 16),
    4: (36, 114, 200),
    5: (188, 63, 188),
    6: (17, 168, 205),
    7: (204, 204, 204),
    9: (255, 85, 85),
    10: (85, 255, 85),
    11: (255, 255, 85),
    12: (85, 85, 255),
    13: (255, 85, 255),
    14: (85, 255, 255),
    15: (255, 255, 255),
    208: (255, 135, 0),
    236: (48, 48, 48),
    240: (88, 88, 88),
    250: (188, 188, 188),
}


def get_color(code: int) -> tuple:
    if code in COLOR_MAP:
        return COLOR_MAP[code]
    if 16 <= code <= 231:
        c = code - 16
        return ((c // 36) * 51, ((c % 36) // 6) * 51, (c % 6) * 51)
    if 232 <= code <= 255:
        g = (code - 232) * 10 + 8
        return (g, g, g)
    return (204, 204, 204)


# ── rendering helpers ────────────────────────────────────────────────────────

CELL_W = 7
CELL_H = 14
TITLE_BAR_H = 24
BORDER = 2
TERM_COLS = 80
TERM_ROWS = 24


def load_font():
    for path in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
    ]:
        try:
            return ImageFont.truetype(path, 12)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


FONT = load_font()

IMG_W = TERM_COLS * CELL_W + BORDER * 2
IMG_H = TERM_ROWS * CELL_H + TITLE_BAR_H + BORDER * 2


def _render_chrome(draw: ImageDraw.Draw):
    """Draw the terminal title-bar chrome (once per frame)."""
    draw.rectangle([0, 0, IMG_W, TITLE_BAR_H], fill=(50, 50, 50))
    draw.ellipse([8, 6, 18, 16], fill=(255, 95, 86))
    draw.ellipse([22, 6, 32, 16], fill=(255, 189, 46))
    draw.ellipse([36, 6, 46, 16], fill=(39, 201, 63))
    draw.text((IMG_W // 2 - 70, 5), "ASCII FIGHT - Terminal",
              fill=(180, 180, 180), font=FONT)


def buffer_to_image(buf: ScreenBuffer) -> Image.Image:
    """Convert a ScreenBuffer to a PIL Image with terminal chrome."""
    img = Image.new("RGB", (IMG_W, IMG_H), (40, 40, 40))
    draw = ImageDraw.Draw(img)
    _render_chrome(draw)

    ox = BORDER
    oy = TITLE_BAR_H + BORDER

    for y in range(buf.height):
        for x in range(buf.width):
            cell = buf.buffer[y][x]
            px = ox + x * CELL_W
            py = oy + y * CELL_H

            bg = get_color(cell.bg)
            if bg != (0, 0, 0):
                draw.rectangle([px, py, px + CELL_W - 1, py + CELL_H - 1], fill=bg)

            if cell.char != " ":
                draw.text((px + 1, py), cell.char, fill=get_color(cell.fg), font=FONT)

    return img


# ── timeline (matches main.py durations) ─────────────────────────────────────

def build_timeline() -> Timeline:
    tl = Timeline()
    tl.add_scene(Scene("title", 7.0, render_title))
    fight = FightChoreography()
    tl.add_scene(Scene("fight", 20.0, fight.render))
    funny = FunnyMoment()
    tl.add_scene(Scene("funny", 16.0, funny.render))
    tl.add_scene(Scene("fade_out", 8.0, render_fade_out))
    tl.add_scene(Scene("credits", 14.0, render_credits))
    return tl


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    gif_fps = 10
    frame_dt = 1.0 / gif_fps
    frame_ms = int(1000 / gif_fps)

    timeline = build_timeline()
    total = timeline.total_duration
    n_frames = int(total * gif_fps)

    print(f"Rendering {n_frames} frames at {gif_fps} fps "
          f"({total:.0f}s, {IMG_W}x{IMG_H} px) ...")

    frames: list[Image.Image] = []
    for i in range(n_frames):
        t = i * frame_dt
        random.seed(int(t * 1000))  # deterministic randomness per frame

        buf = ScreenBuffer(TERM_COLS, TERM_ROWS)
        result = timeline.get_scene_at(t)
        if result is None:
            break
        scene, progress = result
        scene.render(buf, progress)

        frames.append(buffer_to_image(buf))

        if (i + 1) % 50 == 0 or i == n_frames - 1:
            pct = (i + 1) / n_frames * 100
            print(f"  frame {i + 1}/{n_frames}  ({pct:.0f}%)")

    if not frames:
        print("No frames rendered!")
        sys.exit(1)

    out = os.path.join(os.path.dirname(__file__), "demo.gif")
    print(f"Assembling GIF ({len(frames)} frames) ...")

    frames[0].save(
        out,
        save_all=True,
        append_images=frames[1:],
        duration=frame_ms,
        loop=0,
        optimize=True,
    )

    size_mb = os.path.getsize(out) / (1024 * 1024)
    print(f"Saved {out}  ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
