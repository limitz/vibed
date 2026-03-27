"""
Effects module - Visual effects for the ASCII art animation.

Provides particle systems, explosions, screen shake, flash, fade,
sparkles, fire, and other visual effects.
"""

import random
import math
from typing import Optional
from renderer import ScreenBuffer, Color


class Particle:
    """A single particle with position, velocity, and appearance."""
    __slots__ = ('x', 'y', 'vx', 'vy', 'char', 'fg', 'bg', 'life', 'max_life', 'gravity')

    def __init__(self, x: float, y: float, vx: float, vy: float,
                 char: str, fg: int = Color.WHITE, life: float = 1.0,
                 gravity: float = 0.0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.char = char
        self.fg = fg
        self.bg = Color.BLACK
        self.life = life
        self.max_life = life
        self.gravity = gravity

    @property
    def alive(self) -> bool:
        return self.life > 0

    def update(self, dt: float):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += self.gravity * dt
        self.life -= dt


class ParticleSystem:
    """Manages collections of particles."""

    def __init__(self):
        self.particles: list[Particle] = []

    def add(self, particle: Particle):
        self.particles.append(particle)

    def update(self, dt: float):
        for p in self.particles:
            p.update(dt)
        self.particles = [p for p in self.particles if p.alive]

    def draw(self, buffer: ScreenBuffer):
        for p in self.particles:
            if p.alive:
                ix, iy = int(p.x), int(p.y)
                # Fade character as life decreases
                ratio = p.life / p.max_life
                if ratio < 0.3:
                    char = '.'
                elif ratio < 0.6:
                    char = p.char if p.char not in ('*', '#', '@') else 'o'
                else:
                    char = p.char
                buffer.set_cell(ix, iy, char, p.fg, p.bg)

    @property
    def active_count(self) -> int:
        return len(self.particles)


def spawn_explosion(ps: ParticleSystem, x: float, y: float, count: int = 20,
                    chars: str = "*#@+.o", colors: Optional[list[int]] = None,
                    speed: float = 15.0, life: float = 1.5):
    """Spawn an explosion of particles."""
    if colors is None:
        colors = [Color.RED, Color.BRIGHT_RED, Color.YELLOW, Color.BRIGHT_YELLOW, Color.ORANGE]
    for _ in range(count):
        angle = random.uniform(0, 2 * math.pi)
        spd = random.uniform(speed * 0.3, speed)
        vx = math.cos(angle) * spd
        vy = math.sin(angle) * spd * 0.5  # Squash vertically for terminal aspect ratio
        char = random.choice(chars)
        fg = random.choice(colors)
        p_life = random.uniform(life * 0.5, life)
        ps.add(Particle(x, y, vx, vy, char, fg, p_life, gravity=5.0))


def spawn_sparks(ps: ParticleSystem, x: float, y: float, count: int = 8,
                 direction: float = 0.0, spread: float = 0.5):
    """Spawn directional sparks."""
    chars = "*+.'"
    colors = [Color.YELLOW, Color.BRIGHT_YELLOW, Color.WHITE, Color.BRIGHT_WHITE]
    for _ in range(count):
        angle = direction + random.uniform(-spread, spread)
        spd = random.uniform(5, 20)
        vx = math.cos(angle) * spd
        vy = math.sin(angle) * spd * 0.5
        char = random.choice(chars)
        fg = random.choice(colors)
        life = random.uniform(0.2, 0.6)
        ps.add(Particle(x, y, vx, vy, char, fg, life))


def spawn_fireworks(ps: ParticleSystem, x: float, y: float, count: int = 30):
    """Spawn a firework burst."""
    base_color = random.choice([Color.RED, Color.GREEN, Color.BLUE, Color.MAGENTA,
                                 Color.CYAN, Color.YELLOW])
    bright = base_color + 8 if base_color < 8 else base_color
    colors = [base_color, bright, Color.WHITE]
    chars = "*+.:o"
    for _ in range(count):
        angle = random.uniform(0, 2 * math.pi)
        spd = random.uniform(3, 12)
        vx = math.cos(angle) * spd
        vy = math.sin(angle) * spd * 0.5
        char = random.choice(chars)
        fg = random.choice(colors)
        life = random.uniform(0.8, 2.0)
        ps.add(Particle(x, y, vx, vy, char, fg, life, gravity=3.0))


def apply_screen_shake(buffer: ScreenBuffer, intensity: float) -> ScreenBuffer:
    """Apply a screen shake effect by offsetting the buffer."""
    if intensity <= 0:
        return buffer
    ox = int(random.uniform(-intensity, intensity))
    oy = int(random.uniform(-intensity, intensity))
    new_buf = ScreenBuffer(buffer.width, buffer.height)
    new_buf.overlay(buffer, ox, oy)
    return new_buf


def apply_fade(buffer: ScreenBuffer, amount: float):
    """Apply a fade effect (0.0 = fully visible, 1.0 = fully black).

    Progressively replaces characters with darker versions.
    """
    fade_chars = ['@', '#', '&', '%', '$', '*', '+', '=', '-', ':', '.', ' ']
    threshold = amount

    for y in range(buffer.height):
        for x in range(buffer.width):
            cell = buffer.buffer[y][x]
            if cell.char == ' ':
                continue
            if random.random() < threshold:
                # Replace with a "darker" character or blank
                if amount > 0.8:
                    cell.char = ' '
                elif amount > 0.5:
                    cell.char = random.choice(['.', ' ', ' '])
                else:
                    cell.char = random.choice(['.', ':', '-', cell.char])
                cell.fg = Color.DARK_GRAY


def apply_flash(buffer: ScreenBuffer, intensity: float):
    """Flash the screen white."""
    if intensity <= 0:
        return
    for y in range(buffer.height):
        for x in range(buffer.width):
            if random.random() < intensity:
                cell = buffer.buffer[y][x]
                cell.fg = Color.BRIGHT_WHITE
                cell.bg = Color.WHITE if intensity > 0.5 else cell.bg


def draw_fire(buffer: ScreenBuffer, y: int, width: int, intensity: float = 1.0):
    """Draw a fire effect along the bottom."""
    fire_chars = [' ', '.', ':', '^', '*', '#', '%', '@']
    fire_colors = [Color.RED, Color.BRIGHT_RED, Color.ORANGE, Color.YELLOW, Color.BRIGHT_YELLOW]

    height = int(5 * intensity)
    for dy in range(height):
        for x in range(width):
            fy = y - dy
            if 0 <= fy < buffer.height:
                prob = (1.0 - dy / max(height, 1)) * intensity
                if random.random() < prob:
                    ci = min(int((1 - dy / max(height, 1)) * len(fire_colors)), len(fire_colors) - 1)
                    char = fire_chars[min(int(prob * len(fire_chars)), len(fire_chars) - 1)]
                    buffer.set_cell(x, fy, char, fire_colors[ci])


def draw_lightning(buffer: ScreenBuffer, x: int, y1: int, y2: int, fg: int = Color.BRIGHT_WHITE):
    """Draw a lightning bolt from y1 to y2."""
    cx = x
    for y in range(y1, y2):
        buffer.set_cell(cx, y, '|', fg)
        drift = random.choice([-1, 0, 0, 1])
        cx += drift
        if drift != 0:
            buffer.set_cell(cx, y, '/' if drift < 0 else '\\', fg)


def draw_star_field(buffer: ScreenBuffer, density: float = 0.01, seed: int = 42):
    """Draw a static star field background."""
    rng = random.Random(seed)
    star_chars = ['.', '+', '*', '.', '.']
    star_colors = [Color.WHITE, Color.BRIGHT_WHITE, Color.YELLOW, Color.GRAY, Color.LIGHT_GRAY]
    for y in range(buffer.height):
        for x in range(buffer.width):
            if rng.random() < density:
                buffer.set_cell(x, y, rng.choice(star_chars), rng.choice(star_colors))


def draw_rain(buffer: ScreenBuffer, progress: float, intensity: float = 0.03):
    """Draw animated rain."""
    for y in range(buffer.height):
        for x in range(buffer.width):
            # Use a hash to make rain pattern repeatable but animated
            h = hash((x, (y + int(progress * 40)) % buffer.height))
            if (h % 1000) / 1000.0 < intensity:
                buffer.set_cell(x, y, '|', Color.BLUE)


def draw_scrolling_text(buffer: ScreenBuffer, lines: list[str], y_offset: float,
                        fg: int = Color.WHITE, bg: int = Color.BLACK):
    """Draw vertically scrolling text (for credits)."""
    for i, line in enumerate(lines):
        y = int(y_offset + i)
        if 0 <= y < buffer.height:
            buffer.draw_text_centered(y, line, fg, bg)


def draw_matrix_rain(buffer: ScreenBuffer, progress: float, intensity: float = 0.15):
    """Draw Matrix-style falling green characters."""
    w, h = buffer.width, buffer.height
    rng = random.Random(42)
    columns = []
    for x in range(w):
        speed = rng.uniform(0.5, 2.0)
        offset = rng.uniform(0, h * 2)
        columns.append((speed, offset))

    chars = "abcdefghijklmnopqrstuvwxyz0123456789@#$%&*(){}[]<>!?"
    for x in range(w):
        speed, offset = columns[x]
        head_y = int((progress * 40 * speed + offset) % (h * 1.5))
        trail_len = rng.randint(5, 15)
        for dy in range(trail_len):
            y = head_y - dy
            if 0 <= y < h:
                if rng.random() < intensity:
                    if dy == 0:
                        ch = random.choice(chars)
                        buffer.set_cell(x, y, ch, Color.BRIGHT_WHITE)
                    elif dy < 3:
                        ch = random.choice(chars)
                        buffer.set_cell(x, y, ch, Color.BRIGHT_GREEN)
                    else:
                        ch = random.choice(chars)
                        buffer.set_cell(x, y, ch, Color.GREEN)


def draw_shockwave(buffer: ScreenBuffer, cx: int, cy: int, radius: float,
                   fg: int = Color.BRIGHT_WHITE):
    """Draw an expanding ring shockwave."""
    chars = ".-=*#@"
    for angle_deg in range(0, 360, 3):
        angle = math.radians(angle_deg)
        x = int(cx + math.cos(angle) * radius)
        y = int(cy + math.sin(angle) * radius * 0.5)  # Aspect correction
        if 0 <= x < buffer.width and 0 <= y < buffer.height:
            ci = min(int(radius / 3) % len(chars), len(chars) - 1)
            buffer.set_cell(x, y, chars[ci], fg)


def draw_combo_text(buffer: ScreenBuffer, combo: int, x: int, y: int):
    """Draw a flashy combo counter."""
    if combo < 2:
        return
    text = f"{combo}x COMBO!"
    colors = [Color.BRIGHT_YELLOW, Color.BRIGHT_RED, Color.BRIGHT_MAGENTA,
              Color.BRIGHT_CYAN, Color.BRIGHT_GREEN]
    fg = colors[min(combo - 2, len(colors) - 1)]
    buffer.draw_text(x, y, text, fg)
    # Add emphasis
    if combo >= 5:
        buffer.draw_text(x - 1, y - 1, ">" * len(text), Color.BRIGHT_RED)
    if combo >= 8:
        buffer.draw_text(x, y + 1, "~" * len(text), Color.BRIGHT_YELLOW)


def draw_speed_lines(buffer: ScreenBuffer, direction: str = "horizontal",
                     intensity: float = 0.5):
    """Draw motion/speed lines across the screen."""
    w, h = buffer.width, buffer.height
    char = '-' if direction == "horizontal" else '|'
    for _ in range(int(intensity * 20)):
        if direction == "horizontal":
            y = random.randint(0, h - 1)
            x = random.randint(0, w - 10)
            length = random.randint(3, 10)
            for dx in range(length):
                buffer.set_cell(x + dx, y, char, Color.GRAY)
        else:
            x = random.randint(0, w - 1)
            y = random.randint(0, h - 5)
            length = random.randint(2, 5)
            for dy in range(length):
                buffer.set_cell(x, y + dy, char, Color.GRAY)


def draw_dramatic_zoom_text(buffer: ScreenBuffer, text: str, progress: float,
                            fg: int = Color.BRIGHT_RED):
    """Draw text that zooms in dramatically (gets larger with progress)."""
    w, h = buffer.width, buffer.height
    cy = h // 2

    if progress < 0.5:
        # Small text zooming in
        buffer.draw_text_centered(cy, text, fg)
    else:
        # Large block text
        for i, ch in enumerate(text):
            x = (w - len(text) * 3) // 2 + i * 3
            # Draw each char as a 2x2 block
            buffer.set_cell(x, cy - 1, ch, fg)
            buffer.set_cell(x + 1, cy - 1, ch, fg)
            buffer.set_cell(x, cy, ch, fg)
            buffer.set_cell(x + 1, cy, ch, fg)


def draw_energy_aura(buffer: ScreenBuffer, x: int, y: int, radius: float,
                     fg: int = Color.BRIGHT_CYAN, progress: float = 0.0):
    """Draw a pulsing energy aura around a point."""
    chars = ".+*#@"
    pulse = math.sin(progress * math.pi * 6) * 0.3 + 1.0
    r = radius * pulse
    for angle_deg in range(0, 360, 15):
        angle = math.radians(angle_deg)
        px = int(x + math.cos(angle) * r)
        py = int(y + math.sin(angle) * r * 0.5)
        if 0 <= px < buffer.width and 0 <= py < buffer.height:
            ci = int((progress * 10 + angle_deg / 60) % len(chars))
            buffer.set_cell(px, py, chars[ci], fg)
