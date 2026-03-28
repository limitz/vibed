"""Mirror frame and dream background rendering.

Creates the ornate mirror frame and atmospheric dream environment.
"""

import math
import random
from PIL import Image, ImageDraw, ImageFilter


def create_dream_background(width, height, seed=42):
    """Create a dark, atmospheric dream background.

    Deep indigo/purple with subtle aurora-like wisps and scattered stars.
    """
    rng = random.Random(seed)
    img = Image.new("RGBA", (width, height), (8, 4, 18, 255))
    draw = ImageDraw.Draw(img)

    # Subtle vertical gradient - slightly lighter toward center
    for y in range(height):
        frac = 1 - abs(y / height - 0.45) * 1.5
        frac = max(0, min(1, frac))
        brightness = int(frac * 12)
        if brightness > 0:
            c = (8 + brightness, 4 + brightness // 2, 18 + brightness, 255)
            draw.line([(0, y), (width, y)], fill=c)

    # Aurora-like wisps
    for _ in range(12):
        cx = rng.randint(0, width)
        cy = rng.randint(0, height)
        rx = rng.randint(width // 4, width)
        ry = rng.randint(height // 8, height // 3)
        r = rng.randint(10, 30)
        g = rng.randint(5, 15)
        b = rng.randint(20, 50)
        alpha = rng.randint(5, 18)
        draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry],
                     fill=(r, g, b, alpha))

    img = img.filter(ImageFilter.GaussianBlur(radius=max(1, min(width, height) // 15)))

    # Scattered stars
    star_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    star_draw = ImageDraw.Draw(star_layer)
    for _ in range(rng.randint(40, 80)):
        sx = rng.randint(0, width - 1)
        sy = rng.randint(0, height - 1)
        brightness = rng.randint(60, 200)
        sr = rng.choice([0, 0, 0, 1])
        star_draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
                          fill=(brightness, brightness, brightness + 20, brightness))

    return Image.alpha_composite(img, star_layer)


def get_mirror_mask(center, size, image_size):
    """Get a mask image for the mirror interior."""
    mask = Image.new("L", image_size, 0)
    draw = ImageDraw.Draw(mask)
    cx, cy = center
    hw, hh = size[0] // 2, size[1] // 2
    draw.ellipse([cx - hw, cy - hh, cx + hw, cy + hh], fill=255)
    return mask


def draw_mirror_frame(image, center, size, color=(200, 170, 100)):
    """Draw an ornate oval mirror frame."""
    cx, cy = center
    fw, fh = size
    hw, hh = fw // 2, fh // 2
    mask = get_mirror_mask(center, size, image.size)

    layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    # Outer frame border - multiple rings for depth
    frame_widths = [
        (hw + 18, hh + 18, 0.4, 6),
        (hw + 12, hh + 12, 0.6, 5),
        (hw + 7, hh + 7, 0.8, 4),
        (hw + 3, hh + 3, 1.0, 3),
        (hw, hh, 0.7, 2),
    ]

    for off_w, off_h, brightness, width in frame_widths:
        c = (
            int(color[0] * brightness),
            int(color[1] * brightness),
            int(color[2] * brightness),
            220,
        )
        draw.ellipse([cx - off_w, cy - off_h, cx + off_w, cy + off_h],
                     outline=c, width=width)

    # Ornamental details - small circles along the frame
    num_ornaments = 32
    for i in range(num_ornaments):
        angle = (2 * math.pi * i) / num_ornaments
        ox = cx + (hw + 10) * math.cos(angle)
        oy = cy + (hh + 10) * math.sin(angle)
        r = 3 if i % 4 == 0 else 2
        brightness = 0.9 if i % 4 == 0 else 0.6
        c = (
            int(color[0] * brightness),
            int(color[1] * brightness),
            int(color[2] * brightness),
            180,
        )
        draw.ellipse([ox - r, oy - r, ox + r, oy + r], fill=c)

    # Inner glow along frame edge
    glow_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    for d in range(1, 8):
        alpha = max(1, 40 - d * 5)
        glow_draw.ellipse(
            [cx - hw - d, cy - hh - d, cx + hw + d, cy + hh + d],
            outline=(color[0], color[1], color[2], alpha), width=1)
        glow_draw.ellipse(
            [cx - hw + d, cy - hh + d, cx + hw - d, cy + hh - d],
            outline=(color[0], color[1], color[2], alpha // 2), width=1)

    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=3))
    layer = Image.alpha_composite(layer, glow_layer)

    result = Image.alpha_composite(image, layer)
    return result, mask
