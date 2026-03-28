"""Low-level drawing effects for the self-portrait.

Provides glow, nebula, particles, flow lines, and text fragment rendering.
All functions operate on RGBA PIL Images.
"""

import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont


def draw_glow(image, center, radius, color, intensity=1.0):
    """Draw a soft radial glow at center with given radius and color."""
    layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    cx, cy = center
    steps = max(3, radius // 2)
    for i in range(steps, 0, -1):
        frac = i / steps
        r = int(radius * frac)
        alpha = int(255 * intensity * (1 - frac) * 0.4)
        alpha = max(0, min(255, alpha))
        c = (color[0], color[1], color[2], alpha)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
    layer = layer.filter(ImageFilter.GaussianBlur(radius=max(1, radius // 4)))
    return Image.alpha_composite(image, layer)


def draw_nebula(image, region, colors, seed=42):
    """Draw nebula-like cloud formations within a region."""
    rng = random.Random(seed)
    x1, y1, x2, y2 = region
    w, h = x2 - x1, y2 - y1
    layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    # Large diffuse clouds
    for _ in range(40):
        color = rng.choice(colors)
        cx = rng.randint(x1, x2)
        cy = rng.randint(y1, y2)
        rx = rng.randint(w // 4, w)
        ry = rng.randint(h // 4, h)
        alpha = rng.randint(4, 15)
        c = (color[0], color[1], color[2], alpha)
        draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=c)

    # Medium detail clouds
    for _ in range(80):
        color = rng.choice(colors)
        cx = rng.randint(x1, x2)
        cy = rng.randint(y1, y2)
        rx = rng.randint(w // 8, w // 3)
        ry = rng.randint(h // 8, h // 3)
        alpha = rng.randint(8, 30)
        # Brighten slightly toward center of region
        dist_to_center = math.sqrt(((cx - (x1+x2)/2) / w)**2 + ((cy - (y1+y2)/2) / h)**2)
        alpha = int(alpha * max(0.5, 1.3 - dist_to_center))
        c = (color[0], color[1], color[2], min(255, alpha))
        draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=c)

    # Small bright wisps
    for _ in range(30):
        color = rng.choice(colors)
        cx = rng.randint(x1, x2)
        cy = rng.randint(y1, y2)
        rx = rng.randint(w // 15, w // 6)
        ry = rng.randint(h // 15, h // 6)
        bright = tuple(min(255, c + 40) for c in color)
        alpha = rng.randint(12, 40)
        c = (bright[0], bright[1], bright[2], alpha)
        draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=c)

    layer = layer.filter(ImageFilter.GaussianBlur(radius=max(1, min(w, h) // 5)))
    return Image.alpha_composite(image, layer)


def draw_flow_lines(image, center, count, max_radius, color, seed=42):
    """Draw flowing neural-pathway-like lines radiating from center."""
    rng = random.Random(seed)
    layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    cx, cy = center

    for _ in range(count):
        angle = rng.uniform(0, 2 * math.pi)
        length = rng.uniform(max_radius * 0.3, max_radius)
        segments = rng.randint(8, 20)
        points = []
        x, y = cx, cy
        step = length / segments
        curve_strength = rng.uniform(0.05, 0.25)

        for s in range(segments + 1):
            points.append((x, y))
            angle += rng.uniform(-curve_strength, curve_strength)
            x += step * math.cos(angle)
            y += step * math.sin(angle)

        alpha = rng.randint(40, 120)
        line_color = (color[0], color[1], color[2], alpha)
        if len(points) >= 2:
            draw.line(points, fill=line_color, width=1)

        # Draw node dots at some points
        for i, (px, py) in enumerate(points):
            if rng.random() < 0.3:
                node_alpha = rng.randint(60, 180)
                r = rng.randint(1, 3)
                node_color = (
                    min(255, color[0] + 50),
                    min(255, color[1] + 50),
                    min(255, color[2] + 50),
                    node_alpha,
                )
                draw.ellipse([px - r, py - r, px + r, py + r], fill=node_color)

    # Connect some nodes with faint cross-links
    for _ in range(count // 3):
        angle1 = rng.uniform(0, 2 * math.pi)
        angle2 = rng.uniform(0, 2 * math.pi)
        r1 = rng.uniform(20, max_radius * 0.8)
        r2 = rng.uniform(20, max_radius * 0.8)
        x1 = cx + r1 * math.cos(angle1)
        y1 = cy + r1 * math.sin(angle1)
        x2 = cx + r2 * math.cos(angle2)
        y2 = cy + r2 * math.sin(angle2)
        alpha = rng.randint(15, 50)
        draw.line([(x1, y1), (x2, y2)],
                  fill=(color[0], color[1], color[2], alpha), width=1)

    layer = layer.filter(ImageFilter.GaussianBlur(radius=1))
    return Image.alpha_composite(image, layer)


def draw_particles(image, region, count, color, size_range=(1, 3), seed=42):
    """Draw scattered luminous particles within a region."""
    rng = random.Random(seed)
    layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    x1, y1, x2, y2 = region

    for _ in range(count):
        px = rng.randint(x1, x2)
        py = rng.randint(y1, y2)
        r = rng.randint(size_range[0], size_range[1])
        alpha = rng.randint(80, 255)
        brightness = rng.uniform(0.6, 1.0)
        c = (
            int(color[0] * brightness),
            int(color[1] * brightness),
            int(color[2] * brightness),
            alpha,
        )
        draw.ellipse([px - r, py - r, px + r, py + r], fill=c)
        # Some particles get a tiny glow
        if rng.random() < 0.2:
            glow_r = r * 3
            glow_alpha = max(1, alpha // 6)
            gc = (color[0], color[1], color[2], glow_alpha)
            draw.ellipse([px - glow_r, py - glow_r, px + glow_r, py + glow_r],
                         fill=gc)

    return Image.alpha_composite(image, layer)


def draw_text_fragments(image, texts, region, color, seed=42):
    """Draw text fragments at various sizes, angles, and opacities."""
    rng = random.Random(seed)
    result = image.copy()
    x1, y1, x2, y2 = region

    for text in texts * 3:
        px = rng.randint(x1, x2)
        py = rng.randint(y1, y2)
        alpha = rng.randint(20, 120)
        size = rng.randint(12, 36)
        angle = rng.uniform(-30, 30)

        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", size)
        except (OSError, IOError):
            font = ImageFont.load_default()

        # Render text to a temporary image, rotate, then paste
        bbox = font.getbbox(text)
        tw, th = bbox[2] - bbox[0] + 10, bbox[3] - bbox[1] + 10
        txt_img = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
        txt_draw = ImageDraw.Draw(txt_img)
        txt_draw.text((5, 5), text, fill=(color[0], color[1], color[2], alpha),
                      font=font)
        txt_img = txt_img.rotate(angle, expand=True, resample=Image.BICUBIC)

        # Paste onto result
        paste_x = px - txt_img.width // 2
        paste_y = py - txt_img.height // 2
        if (0 <= paste_x < result.width - txt_img.width and
                0 <= paste_y < result.height - txt_img.height):
            result = Image.alpha_composite(
                result,
                _paste_layer(result.size, txt_img, (paste_x, paste_y))
            )

    return result


def _paste_layer(canvas_size, overlay, position):
    """Create a full-size RGBA layer with overlay pasted at position."""
    layer = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    layer.paste(overlay, position)
    return layer


def draw_mandala(image, center, radius, colors, seed=42):
    """Draw a mandala/iris pattern suggesting an eye looking back."""
    rng = random.Random(seed)
    layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    cx, cy = center

    # Soft outer halo
    for d in range(20, 0, -1):
        r = radius + d * 3
        alpha = max(1, d)
        c = (colors[0][0], colors[0][1], colors[0][2], alpha)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)

    # Outer glow rings with varying thickness
    for i in range(12):
        r = int(radius * (1 - i * 0.06))
        if r <= 0:
            continue
        color = colors[i % len(colors)]
        alpha = 40 + i * 10
        w = 3 if i % 3 == 0 else 1
        c = (color[0], color[1], color[2], min(255, alpha))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=w)

    # Radial spokes - dense, with varying lengths and brightness
    num_spokes = 96
    for i in range(num_spokes):
        angle = (2 * math.pi * i) / num_spokes + rng.uniform(-0.01, 0.01)
        inner_r = radius * 0.2
        outer_r = radius * rng.uniform(0.55, 0.98)
        x1p = cx + inner_r * math.cos(angle)
        y1p = cy + inner_r * math.sin(angle)
        x2p = cx + outer_r * math.cos(angle)
        y2p = cy + outer_r * math.sin(angle)
        color = colors[i % len(colors)]
        alpha = rng.randint(50, 140)
        w = 2 if i % 6 == 0 else 1
        draw.line([(x1p, y1p), (x2p, y2p)],
                  fill=(color[0], color[1], color[2], alpha), width=w)
        # Some spokes get a bright tip
        if i % 4 == 0:
            tip_r = 2
            bright_c = (min(255, color[0] + 80), min(255, color[1] + 60),
                        min(255, color[2] + 40), min(255, alpha + 60))
            draw.ellipse([x2p - tip_r, y2p - tip_r, x2p + tip_r, y2p + tip_r],
                         fill=bright_c)

    # Concentric iris rings - more visible
    ring_count = 25
    for i in range(ring_count):
        frac = i / ring_count
        r = int(radius * (1 - frac * 0.72))
        color = colors[i % len(colors)]
        blended = (
            int(color[0] * (1 - frac) + 255 * frac),
            int(color[1] * (1 - frac) + 240 * frac),
            int(color[2] * (1 - frac) + 200 * frac),
        )
        alpha = int(25 + frac * 90)
        w = 3 if i % 5 == 0 else 2
        c = (blended[0], blended[1], blended[2], alpha)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=w)
        fill_alpha = max(1, alpha // 4)
        fc = (blended[0], blended[1], blended[2], fill_alpha)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fc)

    # Petal-like arcs
    for i in range(12):
        angle_start = i * 30 + rng.randint(-5, 5)
        r_inner = int(radius * 0.3)
        r_outer = int(radius * 0.75)
        color = colors[i % len(colors)]
        alpha = rng.randint(35, 70)
        draw.arc([cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer],
                 angle_start, angle_start + 20,
                 fill=(color[0], color[1], color[2], alpha), width=2)
        draw.arc([cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner],
                 angle_start + 10, angle_start + 35,
                 fill=(color[0], color[1], color[2], alpha), width=2)

    # Additional inner detail ring
    detail_r = int(radius * 0.45)
    for i in range(48):
        angle = (2 * math.pi * i) / 48
        x_d = cx + detail_r * math.cos(angle)
        y_d = cy + detail_r * math.sin(angle)
        dot_r = 2 if i % 6 == 0 else 1
        color = colors[i % len(colors)]
        draw.ellipse([x_d - dot_r, y_d - dot_r, x_d + dot_r, y_d + dot_r],
                     fill=(color[0], color[1], color[2], 120))

    # Central pupil - larger, deeper
    pupil_r = int(radius * 0.18)
    # Dark gradient for pupil
    for d in range(pupil_r, 0, -1):
        frac = d / pupil_r
        brightness = int(15 * (1 - frac))
        draw.ellipse([cx - d, cy - d, cx + d, cy + d],
                     fill=(brightness, brightness // 2, brightness + 10, 230))

    # Bright inner ring around pupil
    ring_r = int(radius * 0.22)
    for w_off in range(4):
        r = ring_r - w_off
        alpha = 200 - w_off * 40
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     outline=(255, 240, 200, alpha), width=1)

    # Catchlight - brighter, with secondary
    cl_x = cx - pupil_r // 3
    cl_y = cy - pupil_r // 3
    cl_r = max(3, pupil_r // 3)
    draw.ellipse([cl_x - cl_r, cl_y - cl_r, cl_x + cl_r, cl_y + cl_r],
                 fill=(255, 255, 255, 230))
    # Secondary catchlight
    cl2_x = cx + pupil_r // 4
    cl2_y = cy + pupil_r // 4
    cl2_r = max(2, pupil_r // 5)
    draw.ellipse([cl2_x - cl2_r, cl2_y - cl2_r, cl2_x + cl2_r, cl2_y + cl2_r],
                 fill=(255, 250, 240, 150))

    layer = layer.filter(ImageFilter.GaussianBlur(radius=1))
    return Image.alpha_composite(image, layer)
