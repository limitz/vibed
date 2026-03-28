"""Generate screenshot.png: a composite showing the artist project in action."""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(__file__)
OUTPUT = os.path.join(HERE, "output")


def make_screenshot():
    """Create a composite screenshot showing the drawing engine and course results."""
    W, H = 1920, 1080
    bg_color = (32, 32, 36)
    canvas = Image.new("RGB", (W, H), bg_color)
    draw = ImageDraw.Draw(canvas)

    # Try to load a monospace font
    font_size = 16
    title_size = 22
    small_size = 13
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", font_size)
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", title_size)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", small_size)
    except (OSError, IOError):
        font = ImageFont.load_default()
        title_font = font
        small_font = font

    # === Header bar ===
    header_h = 40
    draw.rectangle([(0, 0), (W, header_h)], fill=(50, 50, 58))
    draw.text((15, 10), "Artist — Stylus Drawing Engine & Art Course", fill=(200, 200, 210), font=title_font)
    draw.text((W - 300, 12), "Claude Opus 4.6", fill=(130, 130, 150), font=font)

    # === Left panel: Stage 1 tool sampler + scene ===
    panel_y = header_h + 10
    panel_x = 15

    draw.text((panel_x, panel_y), "STAGE 1: Drawing Engine", fill=(100, 180, 255), font=font)
    panel_y += 25

    # Load and place tool sampler
    sampler_path = os.path.join(OUTPUT, "stage1", "line_sampler.png")
    if os.path.exists(sampler_path):
        sampler = Image.open(sampler_path)
        sampler = sampler.resize((420, int(420 * sampler.height / sampler.width)))
        # Add border
        draw.rectangle([(panel_x - 1, panel_y - 1),
                         (panel_x + 420, panel_y + sampler.height)], outline=(80, 80, 90))
        canvas.paste(sampler, (panel_x, panel_y))
        draw.text((panel_x + 5, panel_y + 5), "Tool Sampler", fill=(40, 40, 40), font=small_font)
        panel_y += sampler.height + 10

    # Scene test
    scene_path = os.path.join(OUTPUT, "stage1", "scene_test.png")
    if os.path.exists(scene_path):
        scene = Image.open(scene_path)
        scene = scene.resize((420, int(420 * scene.height / scene.width)))
        draw.rectangle([(panel_x - 1, panel_y - 1),
                         (panel_x + 420, panel_y + scene.height)], outline=(80, 80, 90))
        canvas.paste(scene, (panel_x, panel_y))
        draw.text((panel_x + 5, panel_y + 5), "Scene Test", fill=(40, 40, 40), font=small_font)
        panel_y += scene.height + 10

    # Color test
    color_path = os.path.join(OUTPUT, "stage1", "color_test.png")
    if os.path.exists(color_path):
        color_img = Image.open(color_path)
        color_img = color_img.resize((420, int(420 * color_img.height / color_img.width)))
        cih = min(color_img.height, H - panel_y - 20)
        draw.rectangle([(panel_x - 1, panel_y - 1),
                         (panel_x + 420, panel_y + cih)], outline=(80, 80, 90))
        canvas.paste(color_img.crop((0, 0, 420, cih)), (panel_x, panel_y))
        draw.text((panel_x + 5, panel_y + 5), "Color Palette", fill=(40, 40, 40), font=small_font)

    # === Center panel: Lesson gallery (3x3 grid) ===
    grid_x = 460
    grid_y = header_h + 10
    draw.text((grid_x, grid_y), "STAGE 3: Art Course (20 Lessons)", fill=(100, 180, 255), font=font)
    grid_y += 25

    lesson_files = [
        ("L1: Lines", "lesson_01_attempt_1.png"),
        ("L4: Hatching", "lesson_04_attempt_1.png"),
        ("L7: Sphere", "lesson_07_attempt_1.png"),
        ("L9: Shadows", "lesson_09_attempt_1.png"),
        ("L13: Tree", "lesson_13_attempt_1.png"),
        ("L14: Landscape", "lesson_14_attempt_1.png"),
        ("L15: Water", "lesson_15_attempt_1.png"),
        ("L18: Portrait", "lesson_18_attempt_1.png"),
        ("L19: Abstract", "lesson_19_attempt_1.png"),
    ]

    thumb_w, thumb_h = 195, 145
    cols = 3
    for i, (label, fname) in enumerate(lesson_files):
        row, col = divmod(i, cols)
        tx = grid_x + col * (thumb_w + 8)
        ty = grid_y + row * (thumb_h + 22)

        fpath = os.path.join(OUTPUT, "stage3", fname)
        if os.path.exists(fpath):
            img = Image.open(fpath)
            img = img.resize((thumb_w, thumb_h))
            draw.rectangle([(tx - 1, ty - 1), (tx + thumb_w, ty + thumb_h)], outline=(80, 80, 90))
            canvas.paste(img, (tx, ty))
        draw.text((tx + 3, ty + thumb_h + 2), label, fill=(180, 180, 190), font=small_font)

    # === Right panel: Masterpiece ===
    mp_x = grid_x + cols * (thumb_w + 8) + 30
    mp_y = header_h + 10
    draw.text((mp_x, mp_y), "STAGE 4: Masterpiece", fill=(255, 200, 80), font=font)
    mp_y += 25

    mp_path = os.path.join(OUTPUT, "masterpiece.png")
    if os.path.exists(mp_path):
        mp = Image.open(mp_path)
        mp_w = W - mp_x - 15
        mp_h = int(mp_w * mp.height / mp.width)
        mp = mp.resize((mp_w, mp_h))
        # Decorative border
        draw.rectangle([(mp_x - 3, mp_y - 3), (mp_x + mp_w + 2, mp_y + mp_h + 2)],
                       outline=(180, 150, 80), width=2)
        canvas.paste(mp, (mp_x, mp_y))
        mp_y += mp_h + 15

    # Skills summary below masterpiece
    draw.text((mp_x, mp_y), "Skills Learned:", fill=(100, 180, 255), font=font)
    mp_y += 22
    skills_lines = [
        "pen_pressure:     0.60 → 0.95",
        "pencil_pressure:  0.50 → 0.95",
        "brush_pressure:   0.50 → 0.95",
        "hatching_spacing:  6.0 → 1.5",
        "fill_spacing:      2.0 → 1.5",
        "",
        "Lessons passed:   20/20",
        "Techniques:        38 entries",
    ]
    for line in skills_lines:
        if line:
            draw.text((mp_x + 5, mp_y), line, fill=(160, 160, 170), font=small_font)
        mp_y += 17

    # === Bottom status bar ===
    bar_y = H - 28
    draw.rectangle([(0, bar_y), (W, H)], fill=(50, 50, 58))
    draw.text((15, bar_y + 5), "4 stages completed | 2827 strokes in masterpiece | skills.md persisted",
              fill=(130, 130, 150), font=small_font)
    draw.text((W - 250, bar_y + 5), "output/masterpiece.png",
              fill=(100, 180, 255), font=small_font)

    # Save
    out_path = os.path.join(HERE, "screenshot.png")
    canvas.save(out_path, quality=95)
    print(f"Screenshot saved to {out_path}")
    return out_path


if __name__ == "__main__":
    make_screenshot()
