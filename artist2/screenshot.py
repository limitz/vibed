"""Generate screenshot.png showing the artist2 project results.

Creates a composite image showing the learning progression from lesson 1
through the final masterpiece, with titles and the teacher-student workflow.
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
SCREENSHOT_PATH = os.path.join(os.path.dirname(__file__), "screenshot.png")


def load_lesson_image(filename):
    """Load a lesson output image."""
    path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(path):
        return Image.open(path).convert("RGB")
    return None


def get_font(size):
    """Try to get a good font, fall back to default."""
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()


def get_font_regular(size):
    """Try to get a regular weight font."""
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()


def main():
    # Canvas
    W, H = 1400, 1000
    bg_color = (28, 28, 36)
    accent = (120, 90, 200)
    text_color = (230, 230, 240)
    dim_text = (160, 160, 180)

    img = Image.new("RGB", (W, H), bg_color)
    draw = ImageDraw.Draw(img)

    font_title = get_font(32)
    font_subtitle = get_font(18)
    font_label = get_font(14)
    font_small = get_font_regular(12)

    # Title
    draw.text((W // 2, 25), "Artist 2: Teacher & Student", fill=text_color,
              font=font_title, anchor="mt")
    draw.text((W // 2, 62), "An AI teacher designs lessons, an AI student creates artwork",
              fill=dim_text, font=font_small, anchor="mt")

    # Divider
    draw.line([(50, 85), (W - 50, 85)], fill=accent, width=2)

    # Top row: progression (lessons 1-7 as thumbnails)
    draw.text((W // 2, 95), "Learning Progression", fill=accent,
              font=font_subtitle, anchor="mt")

    lessons = [
        ("lesson_01.png", "1: Lines"),
        ("lesson_02.png", "2: Shapes"),
        ("lesson_03.png", "3: Shading"),
        ("lesson_04.png", "4: Color"),
        ("lesson_05.png", "5: Landscape"),
        ("lesson_06.png", "6: Portraits"),
        ("lesson_07.png", "7: Abstract"),
    ]

    thumb_w = 170
    thumb_h = 110
    total_w = len(lessons) * thumb_w + (len(lessons) - 1) * 10
    start_x = (W - total_w) // 2
    y_top = 125

    for i, (fname, label) in enumerate(lessons):
        x = start_x + i * (thumb_w + 10)
        lesson_img = load_lesson_image(fname)
        if lesson_img:
            # Resize to thumbnail
            aspect = lesson_img.width / lesson_img.height
            if aspect > thumb_w / thumb_h:
                tw = thumb_w
                th = int(tw / aspect)
            else:
                th = thumb_h
                tw = int(th * aspect)
            thumb = lesson_img.resize((tw, th), Image.LANCZOS)

            # Center in slot
            px = x + (thumb_w - tw) // 2
            py = y_top + (thumb_h - th) // 2

            # Border
            draw.rectangle([px - 2, py - 2, px + tw + 1, py + th + 1],
                           outline=(60, 60, 80), width=1)
            img.paste(thumb, (px, py))

        # Label
        draw.text((x + thumb_w // 2, y_top + thumb_h + 8), label,
                  fill=dim_text, font=font_small, anchor="mt")

    # Arrow showing progression
    arrow_y = y_top + thumb_h // 2
    for i in range(len(lessons) - 1):
        x1 = start_x + (i + 1) * (thumb_w + 10) - 8
        x2 = x1 - 1
        # Small arrow indicator between thumbnails (subtle)

    # Divider
    div_y = y_top + thumb_h + 30
    draw.line([(50, div_y), (W - 50, div_y)], fill=accent, width=1)

    # Bottom: Masterpiece (large)
    draw.text((W // 2, div_y + 10), 'Lesson 8 — Masterpiece: "The Dreamer\'s Horizon"',
              fill=text_color, font=font_subtitle, anchor="mt")
    draw.text((W // 2, div_y + 35),
              "2,159 strokes | 57 colors | 5 tools | 1200x800",
              fill=dim_text, font=font_small, anchor="mt")

    masterpiece = load_lesson_image("lesson_08_masterpiece.png")
    if masterpiece:
        # Scale masterpiece to fit
        max_mw = W - 100
        max_mh = H - div_y - 80
        aspect = masterpiece.width / masterpiece.height
        if aspect > max_mw / max_mh:
            mw = max_mw
            mh = int(mw / aspect)
        else:
            mh = max_mh
            mw = int(mh * aspect)

        master_resized = masterpiece.resize((mw, mh), Image.LANCZOS)
        mx = (W - mw) // 2
        my = div_y + 55

        # Border
        draw.rectangle([mx - 3, my - 3, mx + mw + 2, my + mh + 2],
                       outline=accent, width=2)
        img.paste(master_resized, (mx, my))

    # Footer
    draw.text((W // 2, H - 15),
              "Claude Opus 4.6 (claude-opus-4-6) | 8 lessons | Teacher-Student iterative workflow",
              fill=(100, 100, 120), font=font_small, anchor="mb")

    img.save(SCREENSHOT_PATH)
    print(f"Screenshot saved to {SCREENSHOT_PATH}")
    print(f"Size: {W}x{H}")


if __name__ == "__main__":
    main()
