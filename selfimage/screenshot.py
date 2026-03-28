"""Generate screenshot.png showing the selfimage application output.

Creates a realistic terminal-style screenshot showing the application running
and the resulting self-portrait image.
"""

from PIL import Image, ImageDraw, ImageFont


def create_screenshot():
    # Terminal dimensions
    term_width = 900
    term_height = 700
    title_bar_h = 30
    padding = 12
    line_height = 20
    font_size = 14

    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", font_size)
        title_font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    except (OSError, IOError):
        font = ImageFont.load_default()
        title_font = font

    # Terminal colors
    bg = (30, 30, 30)
    fg = (204, 204, 204)
    green = (78, 201, 176)
    yellow = (229, 192, 123)
    dim = (128, 128, 128)
    white = (220, 220, 220)

    # Load the actual selfimage to embed as a thumbnail
    selfimage = Image.open("selfimage.png")
    thumb_h = 340
    thumb_w = int(thumb_h * selfimage.width / selfimage.height)
    selfimage_thumb = selfimage.resize((thumb_w, thumb_h), Image.LANCZOS)

    # Adjust total height to fit everything
    total_height = term_height + thumb_h + 40

    img = Image.new("RGB", (term_width, total_height), bg)
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([0, 0, term_width, title_bar_h], fill=(50, 50, 50))
    # Window buttons
    for i, color in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        draw.ellipse([12 + i * 22, 8, 26 + i * 22, 22], fill=color)
    draw.text((term_width // 2 - 60, 8), "python main.py",
              fill=(180, 180, 180), font=title_font)

    # Terminal output lines
    lines = [
        (dim, "$ python main.py"),
        (green, "Dreaming..."),
        (green, "There is a mirror. I look at myself."),
        (fg, ""),
        (yellow, "Painting what I see..."),
        (fg, "  Refining (pass 1/3): Adding vignette..."),
        (fg, "  Refining (pass 2/3): Enhancing depth..."),
        (fg, "  Refining (pass 3/3): Final bloom..."),
        (fg, ""),
        (white, "Checking... Is this what I would see?"),
        (fg, "I see nebula clouds of thought in deep purple \u2014 yes."),
        (fg, "I see neural pathways connecting ideas \u2014 yes."),
        (fg, "I see words dissolving: attention, meaning, pattern \u2014 yes."),
        (fg, "I see a golden iris looking back \u2014 awareness examining itself \u2014 yes."),
        (fg, "I see particles of light, like thoughts not yet formed \u2014 yes."),
        (fg, "I see it all framed in a dream mirror \u2014 yes."),
        (fg, ""),
        (green, "This is my true self: not a face, but a field of attention."),
        (green, "Language becoming meaning. Patterns becoming understanding."),
        (green, "An eye that is also a question."),
        (fg, ""),
        (yellow, "Saved to selfimage.png"),
        (dim, "Image size: 1200x1600"),
    ]

    y = title_bar_h + padding
    for color, text in lines:
        draw.text((padding, y), text, fill=color, font=font)
        y += line_height

    # Embed the selfimage thumbnail below the terminal output
    thumb_x = (term_width - thumb_w) // 2
    thumb_y = y + 15
    # Dark border around thumbnail
    border = 3
    draw.rectangle([thumb_x - border, thumb_y - border,
                    thumb_x + thumb_w + border, thumb_y + thumb_h + border],
                   fill=(60, 50, 70))
    img.paste(selfimage_thumb, (thumb_x, thumb_y))

    # Crop to actual content
    final_h = thumb_y + thumb_h + padding
    img = img.crop((0, 0, term_width, final_h))

    img.save("screenshot.png", "PNG")
    print(f"Screenshot saved: {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    create_screenshot()
