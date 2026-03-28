"""Procedural visual effects: star fields, transitions, and generators."""

import math
import struct
import hashlib

from renderer import Color


def hash_float(seed, index):
    """Deterministic hash to float in [0, 1) for procedural generation."""
    data = struct.pack('>II', seed & 0xFFFFFFFF, index & 0xFFFFFFFF)
    h = hashlib.md5(data).digest()
    return (int.from_bytes(h[:4], 'big') & 0x7FFFFFFF) / 0x7FFFFFFF


STAR_CHARS = ['.', '.', '.', '+', '*', 'o']
STAR_COLORS = [Color.WHITE, Color.GRAY, Color.BRIGHT_WHITE, Color.CYAN, Color.YELLOW]


def star_field(buffer, progress, seed=42, density=0.02, twinkle=True):
    """Draw a star field background with optional twinkling."""
    total = int(buffer.width * buffer.height * density)
    for i in range(total):
        x = int(hash_float(seed, i * 3) * buffer.width)
        y = int(hash_float(seed, i * 3 + 1) * buffer.height)
        char_idx = int(hash_float(seed, i * 3 + 2) * len(STAR_CHARS))
        color_idx = int(hash_float(seed, i * 5 + 100) * len(STAR_COLORS))
        ch = STAR_CHARS[char_idx]
        fg = STAR_COLORS[color_idx]
        if twinkle:
            phase = hash_float(seed, i * 7 + 200) * math.pi * 2
            brightness = 0.5 + 0.5 * math.sin(progress * math.pi * 4 + phase)
            if brightness < 0.3:
                ch = '.'
                fg = Color.DARK_GRAY
        buffer.set_cell(x, y, ch, fg, Color.BLACK)


def fade_in(buffer, progress, threshold=0.2):
    """Return effective alpha (0.0-1.0) for fade-in effect."""
    if progress >= threshold:
        return 1.0
    if threshold <= 0:
        return 1.0
    return progress / threshold


def fade_out(buffer, progress, threshold=0.8):
    """Return effective alpha (0.0-1.0) for fade-out effect."""
    if progress <= threshold:
        return 1.0
    remaining = 1.0 - threshold
    if remaining <= 0:
        return 0.0
    return 1.0 - (progress - threshold) / remaining


def dissolve_transition(buffer, progress, char_set=None):
    """Fill screen with random characters for a dissolve effect."""
    if char_set is None:
        char_set = ['░', '▒', '▓', '█', '·', ':', '.']
    coverage = progress
    for y in range(buffer.height):
        for x in range(buffer.width):
            h = hash_float(x * 1000 + y, 99)
            if h < coverage:
                ch_idx = int(hash_float(x + y * 1000, 77) * len(char_set))
                buffer.set_cell(x, y, char_set[ch_idx], Color.GRAY, Color.BLACK)


def speed_lines(buffer, progress, direction='horizontal'):
    """Draw speed/motion lines across the screen."""
    num_lines = buffer.height // 2
    for i in range(num_lines):
        y = int(hash_float(42, i * 3) * buffer.height)
        length = int(hash_float(42, i * 3 + 1) * buffer.width * 0.6) + 5
        offset = int(progress * buffer.width * 3 + hash_float(42, i * 3 + 2) * buffer.width)
        offset = offset % (buffer.width + length)
        start_x = offset - length
        ch = '-' if direction == 'horizontal' else '|'
        colors = [Color.WHITE, Color.CYAN, Color.BRIGHT_WHITE, Color.GRAY]
        fg = colors[i % len(colors)]
        for dx in range(length):
            x = start_x + dx
            if 0 <= x < buffer.width:
                buffer.set_cell(x, y, ch, fg, Color.BLACK)


def tunnel_effect(buffer, progress):
    """Draw concentric rectangles shrinking toward center."""
    cx, cy = buffer.width // 2, buffer.height // 2
    max_layers = min(cx, cy)
    offset = int(progress * max_layers * 3) % max_layers
    chars = ['█', '▓', '▒', '░', '·']
    colors = [Color.BRIGHT_WHITE, Color.WHITE, Color.CYAN, Color.BLUE, Color.DARK_GRAY]
    for layer in range(max_layers):
        adjusted = (layer + offset) % max_layers
        size_x = adjusted
        size_y = adjusted
        if size_x >= cx or size_y >= cy:
            continue
        ch = chars[layer % len(chars)]
        fg = colors[layer % len(colors)]
        x1, y1 = cx - size_x, cy - size_y
        x2, y2 = cx + size_x, cy + size_y
        for x in range(x1, x2 + 1):
            buffer.set_cell(x, y1, ch, fg, Color.BLACK)
            buffer.set_cell(x, y2, ch, fg, Color.BLACK)
        for y in range(y1, y2 + 1):
            buffer.set_cell(x1, y, ch, fg, Color.BLACK)
            buffer.set_cell(x2, y, ch, fg, Color.BLACK)


def draw_circle(buffer, cx, cy, radius, char='*', fg=None, bg=None):
    """Draw a circle outline using midpoint algorithm."""
    if fg is None:
        fg = Color.WHITE
    if bg is None:
        bg = Color.BLACK
    x = radius
    y = 0
    d = 1 - radius
    while x >= y:
        for px, py in [(cx+x, cy+y), (cx-x, cy+y), (cx+x, cy-y), (cx-x, cy-y),
                        (cx+y, cy+x), (cx-y, cy+x), (cx+y, cy-x), (cx-y, cy-x)]:
            buffer.set_cell(px, py, char, fg, bg)
        y += 1
        if d < 0:
            d += 2 * y + 1
        else:
            x -= 1
            d += 2 * (y - x) + 1


def draw_filled_circle(buffer, cx, cy, radius, char='*', fg=None, bg=None):
    """Draw a filled circle."""
    if fg is None:
        fg = Color.WHITE
    if bg is None:
        bg = Color.BLACK
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            if dx * dx + dy * dy <= radius * radius:
                buffer.set_cell(cx + dx, cy + dy, char, fg, bg)


def wave_pattern(buffer, progress, amplitude=3, frequency=1.0):
    """Draw sine-wave based pattern across the screen."""
    for x in range(buffer.width):
        phase = progress * math.pi * 4
        y_center = buffer.height // 2
        y_offset = int(amplitude * math.sin(x * frequency * 0.2 + phase))
        y = y_center + y_offset
        chars = ['~', '≈', '∿', '∼']
        ch = chars[x % len(chars)]
        colors = [Color.CYAN, Color.BLUE, Color.BRIGHT_CYAN, Color.WHITE]
        fg = colors[x % len(colors)]
        buffer.set_cell(x, y, ch, fg, Color.BLACK)
        # Draw trail
        if y > 0:
            buffer.set_cell(x, y - 1, '·', Color.DARK_GRAY, Color.BLACK)
        if y < buffer.height - 1:
            buffer.set_cell(x, y + 1, '·', Color.DARK_GRAY, Color.BLACK)
