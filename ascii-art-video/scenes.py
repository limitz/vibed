"""
Scenes module - All scene content for the ASCII art video.

Scenes: title page, stick figure fight, funny moment, fade out, end credits.
Each scene is a function that takes (buffer, progress) and draws the frame.
"""

import math
import random
from renderer import ScreenBuffer, Color
from effects import (
    ParticleSystem, spawn_explosion, spawn_sparks, spawn_fireworks,
    apply_screen_shake, apply_fade, apply_flash, draw_fire,
    draw_lightning, draw_star_field, draw_rain, draw_scrolling_text,
    draw_matrix_rain, draw_shockwave, draw_combo_text, draw_speed_lines,
    draw_dramatic_zoom_text, draw_energy_aura
)
from animation import ease_in_out, ease_in, ease_out, lerp, bounce


# ─────────────────────────────── STICK FIGURES ───────────────────────────────

STICK_IDLE = [
    "  O  ",
    " /|\\ ",
    " / \\ ",
]

STICK_PUNCH_RIGHT = [
    "  O   ",
    " /|\\--",
    " / \\  ",
]

STICK_PUNCH_LEFT = [
    "  O   ",
    "--/|\\ ",
    "  / \\ ",
]

STICK_KICK_RIGHT = [
    "  O  ",
    " /|\\ ",
    " /  \\__",
]

STICK_KICK_LEFT = [
    "    O  ",
    "   /|\\ ",
    "__/  \\ ",
]

STICK_BLOCK = [
    "  O  ",
    " /|\\ ",
    "  |  ",
    " / \\ ",
]

STICK_UPPERCUT = [
    "  O / ",
    " /|/  ",
    " / \\  ",
]

STICK_FLYING_KICK = [
    "    O ",
    "---/|\\",
    "   /  ",
]

STICK_HIT = [
    " \\O/ ",
    "  |  ",
    " / \\ ",
]

STICK_FALLEN = [
    "         ",
    "  ___O/  ",
    " /       ",
]

STICK_VICTORY = [
    " \\O/ ",
    "  |  ",
    " / \\ ",
]

STICK_HADOUKEN = [
    "  O    ",
    " /|\\=>>",
    " / \\   ",
]

STICK_JUMP = [
    "  O  ",
    " /|\\ ",
    " | | ",
]

STICK_CROUCH = [
    "     ",
    " _O_ ",
    " /|\\ ",
]

STICK_DIZZY = [
    " @O@ ",
    "  |  ",
    " / \\ ",
]

# Mirror a sprite horizontally
def mirror_sprite(sprite: list[str]) -> list[str]:
    """Mirror a sprite horizontally."""
    mirrored = []
    max_len = max(len(line) for line in sprite)
    for line in sprite:
        padded = line.ljust(max_len)
        flipped = padded[::-1]
        # Swap directional characters
        result = ""
        for ch in flipped:
            if ch == '/':
                result += '\\'
            elif ch == '\\':
                result += '/'
            elif ch == '>':
                result += '<'
            elif ch == '<':
                result += '>'
            else:
                result += ch
        mirrored.append(result)
    return mirrored


# ─────────────────────────────── ENERGY BALL ─────────────────────────────────

ENERGY_BALL_FRAMES = [
    ["  ", "()", "  "],
    [" *", "()", "* "],
    ["**", "()", "**"],
    ["*#", "()", "#*"],
]

HADOUKEN_PROJECTILE = [
    " ~*~ ",
    "~(O)~",
    " ~*~ ",
]

SHORYUKEN_TRAIL = [
    "  /  ",
    " / * ",
    "/  * ",
]


# ─────────────────────────────── SCENE: TITLE ────────────────────────────────

def render_title(buffer: ScreenBuffer, progress: float):
    """Epic title screen with Matrix rain intro and animated effects."""
    w, h = buffer.width, buffer.height

    # Phase 1: Matrix rain intro (0.0 - 0.25)
    if progress < 0.25:
        p = progress / 0.25
        draw_matrix_rain(buffer, progress, intensity=0.15 * (1.0 - p * 0.5))
        # Title materializes out of the matrix
        if p > 0.4:
            title_alpha = (p - 0.4) / 0.6
            _draw_title_text(buffer, w, h, title_alpha, progress)
        return

    # Star field background (fades in after matrix)
    matrix_fade = min(1.0, (progress - 0.25) * 8)
    if matrix_fade < 1.0:
        draw_matrix_rain(buffer, progress, intensity=0.15 * (1.0 - matrix_fade))
    draw_star_field(buffer, density=0.02 * matrix_fade, seed=42)

    # Title text
    _draw_title_text(buffer, w, h, 1.0, progress)

    # Subtitle
    title_lines = _get_title_lines(w)
    title_y = h // 2 - len(title_lines) // 2 - 3
    subtitle = "- - - U L T I M A T E   S H O W D O W N - - -"
    sub_y = title_y + len(title_lines) + 2
    if progress > 0.35:
        sub_fade = min(1.0, (progress - 0.35) * 5)
        if int(progress * 10) % 2 == 0 or sub_fade >= 1.0:
            buffer.draw_text_centered(sub_y, subtitle, Color.BRIGHT_YELLOW)

    # Animated border sparks
    if progress > 0.5:
        spark_chars = "*.+*.:*+.~"
        for i in range(w):
            if random.random() < 0.15:
                c = random.choice([Color.BRIGHT_YELLOW, Color.BRIGHT_RED, Color.ORANGE])
                buffer.set_cell(i, 0, random.choice(spark_chars), c)
                buffer.set_cell(i, h - 1, random.choice(spark_chars), c)
        for j in range(h):
            if random.random() < 0.1:
                c = random.choice([Color.BRIGHT_YELLOW, Color.BRIGHT_RED])
                buffer.set_cell(0, j, random.choice(spark_chars), c)
                buffer.set_cell(w - 1, j, random.choice(spark_chars), c)

    # VS fighters silhouette preview
    if progress > 0.55:
        prev_p = (progress - 0.55) / 0.45
        p1_x = int(5 + prev_p * 3)
        p2_x = int(w - 10 - prev_p * 3)
        if prev_p < 0.5 or int(progress * 6) % 2 == 0:
            buffer.draw_sprite(p1_x, h - 8, STICK_IDLE, Color.BRIGHT_CYAN, transparent=' ')
            buffer.draw_sprite(p2_x, h - 8, mirror_sprite(STICK_IDLE), Color.BRIGHT_RED, transparent=' ')
            # Energy auras
            draw_energy_aura(buffer, p1_x + 2, h - 7, 4, Color.BRIGHT_CYAN, progress)
            draw_energy_aura(buffer, p2_x + 2, h - 7, 4, Color.BRIGHT_RED, progress)

    # "Press any key" blinking
    if progress > 0.6 and int(progress * 4) % 2 == 0:
        buffer.draw_text_centered(h - 3, "[ PRESS ANY KEY TO BEGIN ]", Color.GRAY)

    # Fire at bottom
    if progress > 0.4:
        fire_intensity = min(1.0, (progress - 0.4) * 3)
        draw_fire(buffer, h - 1, w, fire_intensity * 0.6)

    # Lightning strikes on the sides
    if progress > 0.7 and random.random() < 0.08:
        lx = random.choice([random.randint(2, 10), random.randint(w - 10, w - 2)])
        draw_lightning(buffer, lx, 1, h - 6, Color.BRIGHT_YELLOW)


def _get_title_lines(w: int) -> list[str]:
    """Get appropriate title lines for screen width."""
    if w >= 70:
        return [
            "  ___   _____ _____ _____ _____    _____ _____  _____ _   _ _____ ",
            " / _ \\ /  ___|  ___/ __  \\_   _|  |  ___|_   _|/ ____| | | |_   _|",
            "/ /_\\ \\\\ `--.| |   `' / /' | |    | |_    | | | |  __| |_| | | |  ",
            "|  _  | `--. \\ |     / /   | |    |  _|   | | | | |_ |  _  | | |  ",
            "| | | |/\\__/ / |___.' /    | |    | |    _| |_| |__| | | | | | |  ",
            "\\_| |_/\\____/\\____/\\_/     \\_/    \\_|    \\___/ \\_____|_| |_/ \\_/  ",
        ]
    return [
        " █▀█ █▀ █▀▀ █ █   █▀▀ █ █▀▀ █ █ ▀█▀ ",
        " █▀█ ▄█ █▄▄ █ █   █▀  █ █▄█ █▀█  █  ",
    ]


def _draw_title_text(buffer: ScreenBuffer, w: int, h: int, alpha: float, progress: float):
    """Draw the title text with effects."""
    title = _get_title_lines(w)
    title_y = h // 2 - len(title) // 2 - 3
    fade_t = min(1.0, alpha)

    for i, line in enumerate(title):
        wave_offset = int(math.sin(progress * 8 + i * 0.5) * (1 - fade_t) * 5)
        x = (w - len(line)) // 2 + wave_offset

        # Rainbow color cycling
        colors = [Color.BRIGHT_RED, Color.BRIGHT_YELLOW, Color.BRIGHT_GREEN,
                  Color.BRIGHT_CYAN, Color.BRIGHT_BLUE, Color.BRIGHT_MAGENTA]
        ci = int((progress * 4 + i * 0.3) % len(colors))
        fg = colors[ci]

        if fade_t > i / max(len(title), 1):
            # Character-by-character reveal for extra drama
            visible_chars = int(len(line) * min(1.0, alpha * 2))
            buffer.draw_text(x, title_y + i, line[:visible_chars], fg)


# ────────────────────────────── SCENE: FIGHT ─────────────────────────────────

class FightChoreography:
    """Choreographed stick figure fight with multiple phases."""

    def __init__(self):
        self.ps = ParticleSystem()
        self._last_spark_time = 0
        self.p1_health = 100
        self.p2_health = 100
        self.combo_count = 0
        self.last_hit_phase = -1
        self.shockwave_time = -1
        self.shockwave_x = 0
        self.shockwave_y = 0

    def render(self, buffer: ScreenBuffer, progress: float):
        w, h = buffer.width, buffer.height

        # Arena background - subtle grid pattern
        if progress > 0.05:
            for y in range(4, h - 5):
                if y % 4 == 0:
                    for x in range(0, w, 8):
                        buffer.set_cell(x, y, '.', Color.DARK_GRAY)

        # Ground line with texture
        ground_y = h - 5
        for x in range(w):
            buffer.set_cell(x, ground_y, '=' if x % 3 == 0 else '_', Color.GRAY)

        # Health bars
        self._draw_health_bars(buffer, w)

        # Timer display
        timer = int((1.0 - progress) * 99)
        buffer.draw_text_centered(1, f"{timer:02d}", Color.BRIGHT_YELLOW)

        # VS indicator with dramatic zoom
        if progress < 0.05:
            p = progress / 0.05
            if p < 0.3:
                draw_dramatic_zoom_text(buffer, "R O U N D  1", p / 0.3, Color.BRIGHT_WHITE)
            elif p < 0.7:
                draw_dramatic_zoom_text(buffer, "F I G H T !", (p - 0.3) / 0.4, Color.BRIGHT_RED)
                if int(p * 20) % 2 == 0:
                    draw_shockwave(buffer, w // 2, h // 2, (p - 0.3) * 30, Color.BRIGHT_YELLOW)
            else:
                apply_flash(buffer, (1.0 - p) * 0.5)

        # Fight phases
        dt = 1 / 30.0
        phase = progress

        if phase < 0.15:
            self._phase_approach(buffer, phase / 0.15, w, ground_y)
        elif phase < 0.30:
            p = (phase - 0.15) / 0.15
            self._phase_punch_exchange(buffer, p, w, ground_y, dt)
        elif phase < 0.45:
            p = (phase - 0.30) / 0.15
            self._phase_kick_combo(buffer, p, w, ground_y, dt)
        elif phase < 0.55:
            p = (phase - 0.45) / 0.10
            self._phase_hadouken(buffer, p, w, ground_y, dt)
        elif phase < 0.70:
            p = (phase - 0.55) / 0.15
            self._phase_intense_exchange(buffer, p, w, ground_y, dt)
        elif phase < 0.80:
            p = (phase - 0.70) / 0.10
            self._phase_flying_kick(buffer, p, w, ground_y, dt)
        elif phase < 0.90:
            p = (phase - 0.80) / 0.10
            self._phase_uppercut(buffer, p, w, ground_y, dt)
        else:
            p = (phase - 0.90) / 0.10
            self._phase_standoff(buffer, p, w, ground_y)

        # Combo counter
        if self.combo_count >= 2:
            draw_combo_text(buffer, self.combo_count, w // 2 - 5, 4)

        # Shockwave effect
        if self.shockwave_time >= 0:
            sw_progress = progress - self.shockwave_time
            if sw_progress < 0.05:
                radius = sw_progress / 0.05 * 20
                draw_shockwave(buffer, self.shockwave_x, self.shockwave_y,
                              radius, Color.BRIGHT_WHITE)

        # Update and draw particles
        self.ps.update(dt)
        self.ps.draw(buffer)

        # Screen shake during impacts - more intense
        if 0.15 < phase < 0.90:
            shake_intensity = 0
            if int(phase * 100) % 7 == 0:
                shake_intensity = 1.0
            elif int(phase * 100) % 11 == 0:
                shake_intensity = 0.5
            if shake_intensity > 0:
                return apply_screen_shake(buffer, shake_intensity)

        # Speed lines during intense moments
        if 0.55 < phase < 0.70:
            draw_speed_lines(buffer, "horizontal", intensity=0.3)

        return buffer

    def _trigger_hit(self, progress: float, x: int, y: int, big: bool = False):
        """Register a hit for combo and shockwave tracking."""
        current_phase = int(progress * 20)
        if current_phase != self.last_hit_phase:
            self.combo_count += 1
            self.last_hit_phase = current_phase
        if big:
            self.shockwave_time = progress
            self.shockwave_x = x
            self.shockwave_y = y

    def _draw_health_bars(self, buffer: ScreenBuffer, w: int):
        bar_width = 20
        # Player 1
        buffer.draw_text(2, 1, "P1 FIGHTER", Color.BRIGHT_CYAN)
        filled = int(self.p1_health / 100 * bar_width)
        bar = '[' + '█' * filled + '░' * (bar_width - filled) + ']'
        color = Color.GREEN if self.p1_health > 50 else (Color.YELLOW if self.p1_health > 25 else Color.RED)
        buffer.draw_text(2, 2, bar, color)

        # Player 2
        p2_label = "P2 FIGHTER"
        buffer.draw_text(w - 2 - len(p2_label), 1, p2_label, Color.BRIGHT_RED)
        filled = int(self.p2_health / 100 * bar_width)
        bar = '[' + '█' * filled + '░' * (bar_width - filled) + ']'
        color = Color.GREEN if self.p2_health > 50 else (Color.YELLOW if self.p2_health > 25 else Color.RED)
        buffer.draw_text(w - 2 - bar_width - 2, 2, bar, color)

    def _draw_fighter(self, buffer: ScreenBuffer, x: int, y: int,
                      sprite: list[str], fg: int, mirror: bool = False):
        s = mirror_sprite(sprite) if mirror else sprite
        buffer.draw_sprite(x, y - len(s) + 1, s, fg, transparent=' ')

    def _phase_approach(self, buffer, p, w, gy):
        p1_x = int(lerp(5, w // 2 - 10, ease_in_out(p)))
        p2_x = int(lerp(w - 10, w // 2 + 5, ease_in_out(p)))
        # Alternate walking sprites
        step = int(p * 8) % 2
        s1 = STICK_IDLE if step == 0 else STICK_JUMP
        s2 = STICK_IDLE if step == 1 else STICK_JUMP
        self._draw_fighter(buffer, p1_x, gy, s1, Color.BRIGHT_CYAN)
        self._draw_fighter(buffer, p2_x, gy, s2, Color.BRIGHT_RED, mirror=True)

        # "FIGHT!" text
        if p > 0.7:
            buffer.draw_text_centered(gy - 8, "F I G H T !", Color.BRIGHT_YELLOW)

    def _phase_punch_exchange(self, buffer, p, w, gy, dt):
        cx = w // 2
        p1_x = cx - 10
        p2_x = cx + 3

        beat = int(p * 6) % 4
        if beat == 0:
            self._draw_fighter(buffer, p1_x, gy, STICK_PUNCH_RIGHT, Color.BRIGHT_CYAN)
            self._draw_fighter(buffer, p2_x, gy, STICK_HIT, Color.BRIGHT_RED, mirror=True)
            spawn_sparks(self.ps, p2_x + 1, gy - 2, 3, direction=0)
            self.p2_health = max(0, self.p2_health - 0.3)
            buffer.draw_text(p2_x - 2, gy - 5, "POW!", Color.BRIGHT_YELLOW)
        elif beat == 1:
            self._draw_fighter(buffer, p1_x, gy, STICK_IDLE, Color.BRIGHT_CYAN)
            self._draw_fighter(buffer, p2_x, gy, STICK_IDLE, Color.BRIGHT_RED, mirror=True)
        elif beat == 2:
            self._draw_fighter(buffer, p1_x, gy, STICK_HIT, Color.BRIGHT_CYAN)
            self._draw_fighter(buffer, p2_x, gy, STICK_PUNCH_LEFT, Color.BRIGHT_RED, mirror=True)
            spawn_sparks(self.ps, p1_x + 3, gy - 2, 3, direction=math.pi)
            self.p1_health = max(0, self.p1_health - 0.3)
            buffer.draw_text(p1_x, gy - 5, "BAM!", Color.BRIGHT_YELLOW)
        else:
            self._draw_fighter(buffer, p1_x, gy, STICK_BLOCK, Color.BRIGHT_CYAN)
            self._draw_fighter(buffer, p2_x, gy, STICK_PUNCH_RIGHT, Color.BRIGHT_RED, mirror=True)
            buffer.draw_text(p1_x + 1, gy - 5, "BLOCK!", Color.BRIGHT_GREEN)

    def _phase_kick_combo(self, buffer, p, w, gy, dt):
        cx = w // 2
        p1_x = cx - 10
        p2_x = cx + 3

        beat = int(p * 8) % 4
        if beat == 0:
            self._draw_fighter(buffer, p1_x, gy, STICK_KICK_RIGHT, Color.BRIGHT_CYAN)
            self._draw_fighter(buffer, p2_x, gy, STICK_HIT, Color.BRIGHT_RED, mirror=True)
            spawn_sparks(self.ps, p2_x, gy - 1, 5, direction=0, spread=0.8)
            self.p2_health = max(0, self.p2_health - 0.5)
            buffer.draw_text(p2_x - 1, gy - 5, "WHAM!", Color.BRIGHT_MAGENTA)
        elif beat == 1:
            self._draw_fighter(buffer, p1_x, gy, STICK_CROUCH, Color.BRIGHT_CYAN)
            self._draw_fighter(buffer, p2_x, gy, STICK_KICK_RIGHT, Color.BRIGHT_RED, mirror=True)
            buffer.draw_text(p1_x + 1, gy - 4, "DUCK!", Color.BRIGHT_GREEN)
        elif beat == 2:
            self._draw_fighter(buffer, p1_x, gy, STICK_UPPERCUT, Color.BRIGHT_CYAN)
            self._draw_fighter(buffer, p2_x + 1, gy - 1, STICK_HIT, Color.BRIGHT_RED, mirror=True)
            spawn_sparks(self.ps, p2_x + 2, gy - 3, 8, direction=-math.pi / 2)
            self.p2_health = max(0, self.p2_health - 0.7)
            buffer.draw_text(p2_x, gy - 6, "UPPERCUT!", Color.BRIGHT_YELLOW)
        else:
            self._draw_fighter(buffer, p1_x, gy, STICK_IDLE, Color.BRIGHT_CYAN)
            self._draw_fighter(buffer, p2_x, gy, STICK_DIZZY, Color.BRIGHT_RED, mirror=True)

    def _phase_hadouken(self, buffer, p, w, gy, dt):
        cx = w // 2
        p1_x = cx - 12

        # P1 charges and fires hadouken
        if p < 0.3:
            # Charging
            self._draw_fighter(buffer, p1_x, gy, STICK_CROUCH, Color.BRIGHT_CYAN)
            # Energy gathering effect
            charge = p / 0.3
            if int(charge * 10) % 2 == 0:
                buffer.draw_text(p1_x + 6, gy - 2, "((" + "*" * int(charge * 3) + "))",
                                Color.BRIGHT_CYAN)
            buffer.draw_text_centered(gy - 7, "HADOUKEN!!!", Color.BRIGHT_CYAN)
            self._draw_fighter(buffer, cx + 6, gy, STICK_IDLE, Color.BRIGHT_RED, mirror=True)
        elif p < 0.7:
            # Firing
            proj_p = (p - 0.3) / 0.4
            self._draw_fighter(buffer, p1_x, gy, STICK_HADOUKEN, Color.BRIGHT_CYAN)
            proj_x = int(lerp(p1_x + 8, cx + 6, proj_p))
            buffer.draw_sprite(proj_x, gy - 3, HADOUKEN_PROJECTILE, Color.BRIGHT_CYAN, transparent=' ')
            # Trail
            for i in range(3):
                tx = proj_x - i * 2 - 2
                if 0 <= tx < w:
                    buffer.set_cell(tx, gy - 2, '~', Color.CYAN)
            self._draw_fighter(buffer, cx + 6, gy, STICK_BLOCK, Color.BRIGHT_RED, mirror=True)
        else:
            # Impact!
            imp_p = (p - 0.7) / 0.3
            self._draw_fighter(buffer, p1_x, gy, STICK_IDLE, Color.BRIGHT_CYAN)
            p2_x = int(lerp(cx + 6, cx + 12, ease_out(imp_p)))
            self._draw_fighter(buffer, p2_x, gy, STICK_HIT, Color.BRIGHT_RED, mirror=True)
            if imp_p < 0.3:
                spawn_explosion(self.ps, cx + 6, gy - 2, 15)
                apply_flash(buffer, 0.3)
            self.p2_health = max(0, self.p2_health - 1.0)

    def _phase_intense_exchange(self, buffer, p, w, gy, dt):
        cx = w // 2
        speed = 3 + p * 10  # Gets faster
        beat = int(p * speed) % 6

        p1_x = cx - 9
        p2_x = cx + 3

        sprites_p1 = [STICK_PUNCH_RIGHT, STICK_KICK_RIGHT, STICK_UPPERCUT,
                       STICK_PUNCH_RIGHT, STICK_CROUCH, STICK_KICK_RIGHT]
        sprites_p2 = [STICK_HIT, STICK_BLOCK, STICK_HIT,
                       STICK_BLOCK, STICK_KICK_RIGHT, STICK_HIT]
        labels = ["COMBO!", "BLOCK!", "CRITICAL!", "MISS!", "COUNTER!", "K.O.!"]
        label_colors = [Color.BRIGHT_YELLOW, Color.BRIGHT_GREEN, Color.BRIGHT_RED,
                        Color.GRAY, Color.BRIGHT_MAGENTA, Color.BRIGHT_RED]

        self._draw_fighter(buffer, p1_x, gy, sprites_p1[beat], Color.BRIGHT_CYAN)
        self._draw_fighter(buffer, p2_x, gy, sprites_p2[beat], Color.BRIGHT_RED, mirror=True)

        buffer.draw_text_centered(gy - 7, labels[beat], label_colors[beat])

        if beat in (0, 2, 5):
            spawn_sparks(self.ps, cx, gy - 2, 4)
            self.p2_health = max(0, self.p2_health - 0.4)

        # Speed lines background
        if p > 0.5:
            for i in range(5):
                y = random.randint(gy - 6, gy)
                line_len = random.randint(3, 8)
                sx = random.choice([0, w - line_len])
                for j in range(line_len):
                    buffer.set_cell(sx + j, y, '-', Color.GRAY)

    def _phase_flying_kick(self, buffer, p, w, gy, dt):
        cx = w // 2

        if p < 0.4:
            # P2 jumps
            jump_h = int(math.sin(p / 0.4 * math.pi) * 6)
            p2_x = int(lerp(cx + 8, cx - 2, p / 0.4))
            self._draw_fighter(buffer, p2_x, gy - jump_h, STICK_FLYING_KICK,
                              Color.BRIGHT_RED, mirror=True)
            self._draw_fighter(buffer, cx - 10, gy, STICK_IDLE, Color.BRIGHT_CYAN)

            # Motion trail
            for i in range(3):
                trail_x = p2_x + (i + 1) * 3
                trail_y = gy - jump_h + i
                if 0 <= trail_y < buffer.height and 0 <= trail_x < w:
                    buffer.set_cell(trail_x, trail_y, '.', Color.DARK_GRAY)
        elif p < 0.6:
            # Impact
            self._draw_fighter(buffer, cx - 10, gy, STICK_HIT, Color.BRIGHT_CYAN)
            self._draw_fighter(buffer, cx - 4, gy, STICK_KICK_RIGHT, Color.BRIGHT_RED, mirror=True)
            spawn_explosion(self.ps, cx - 5, gy - 2, 12,
                           colors=[Color.BRIGHT_RED, Color.ORANGE, Color.YELLOW])
            self.p1_health = max(0, self.p1_health - 1.5)
            buffer.draw_text_centered(gy - 8, "DEVASTATING!", Color.BRIGHT_RED)
            apply_flash(buffer, 0.2)
        else:
            # Recovery
            self._draw_fighter(buffer, cx - 12, gy, STICK_DIZZY, Color.BRIGHT_CYAN)
            self._draw_fighter(buffer, cx + 2, gy, STICK_VICTORY, Color.BRIGHT_RED, mirror=True)

    def _phase_uppercut(self, buffer, p, w, gy, dt):
        cx = w // 2
        p1_x = cx - 10
        p2_x = cx + 3

        if p < 0.3:
            # Windup
            self._draw_fighter(buffer, p1_x, gy, STICK_CROUCH, Color.BRIGHT_CYAN)
            self._draw_fighter(buffer, p2_x, gy, STICK_IDLE, Color.BRIGHT_RED, mirror=True)
            if int(p * 20) % 2 == 0:
                buffer.draw_text(p1_x - 2, gy - 4, "...", Color.BRIGHT_YELLOW)
        elif p < 0.5:
            # SHORYUKEN!
            up_p = (p - 0.3) / 0.2
            jump_h = int(up_p * 8)
            self._draw_fighter(buffer, p1_x + 2, gy - jump_h, STICK_UPPERCUT, Color.BRIGHT_CYAN)
            # Hit P2 upward
            p2_h = int(up_p * 6)
            self._draw_fighter(buffer, p2_x, gy - p2_h, STICK_HIT, Color.BRIGHT_RED, mirror=True)
            buffer.draw_text_centered(gy - 10, "SHORYUKEN!!!", Color.BRIGHT_YELLOW)
            spawn_sparks(self.ps, p2_x + 2, gy - p2_h - 1, 6, direction=-math.pi / 2)
            # Shoryuken trail
            for i in range(jump_h):
                buffer.set_cell(p1_x + 3, gy - i, '|', Color.BRIGHT_YELLOW)
            self.p2_health = max(0, self.p2_health - 2.0)
        else:
            # P2 falls
            fall_p = (p - 0.5) / 0.5
            self._draw_fighter(buffer, p1_x + 2, gy, STICK_VICTORY, Color.BRIGHT_CYAN)
            fall_y = int(lerp(gy - 6, gy + 1, ease_in(fall_p)))
            if fall_y <= gy:
                self._draw_fighter(buffer, p2_x + 2, fall_y, STICK_HIT, Color.BRIGHT_RED, mirror=True)
            else:
                # Fallen
                buffer.draw_sprite(p2_x - 1, gy - 1, mirror_sprite(STICK_FALLEN),
                                  Color.BRIGHT_RED, transparent=' ')
            if fall_p > 0.7:
                spawn_explosion(self.ps, p2_x + 2, gy - 1, 5)

    def _phase_standoff(self, buffer, p, w, gy):
        cx = w // 2
        p1_x = cx - 10
        p2_x = cx + 3

        self._draw_fighter(buffer, p1_x, gy, STICK_IDLE, Color.BRIGHT_CYAN)
        # P2 gets back up slowly
        if p < 0.5:
            buffer.draw_sprite(p2_x - 1, gy - 1, mirror_sprite(STICK_FALLEN),
                              Color.BRIGHT_RED, transparent=' ')
            buffer.draw_text(p2_x, gy - 4, "...", Color.BRIGHT_RED)
        else:
            self._draw_fighter(buffer, p2_x, gy, STICK_DIZZY, Color.BRIGHT_RED, mirror=True)
            buffer.draw_text_centered(gy - 8, "ROUND 2?", Color.BRIGHT_YELLOW)


# ─────────────────────────── SCENE: FUNNY MOMENT ─────────────────────────────

class FunnyMoment:
    """The really funny thing that happens - a banana peel slip chain reaction!"""

    def __init__(self):
        self.ps = ParticleSystem()

    def render(self, buffer: ScreenBuffer, progress: float):
        w, h = buffer.width, buffer.height
        gy = h - 5

        # Ground
        for x in range(w):
            buffer.set_cell(x, gy, '_', Color.GRAY)

        dt = 1 / 30.0

        if progress < 0.10:
            # Both fighters face off, intense staring
            p = progress / 0.10
            cx = w // 2
            self._draw_fighter(buffer, cx - 10, gy, STICK_IDLE, Color.BRIGHT_CYAN)
            self._draw_fighter(buffer, cx + 5, gy, STICK_IDLE, Color.BRIGHT_RED, mirror=True)
            # Tension marks
            if int(p * 10) % 2 == 0:
                buffer.draw_text(cx - 2, gy - 8, "!!!", Color.BRIGHT_YELLOW)
            # Lightning between them
            draw_lightning(buffer, cx, gy - 6, gy - 1, Color.BRIGHT_YELLOW)

        elif progress < 0.20:
            # A banana peel falls from the sky
            p = (progress - 0.10) / 0.10
            cx = w // 2
            self._draw_fighter(buffer, cx - 10, gy, STICK_IDLE, Color.BRIGHT_CYAN)
            self._draw_fighter(buffer, cx + 5, gy, STICK_IDLE, Color.BRIGHT_RED, mirror=True)

            banana_y = int(lerp(0, gy - 1, ease_in(p)))
            banana = "  _  \n //\\ \n \\\\_/"
            buffer.draw_sprite(cx - 2, banana_y, banana.split('\n'), Color.BRIGHT_YELLOW, transparent=' ')
            buffer.draw_text_centered(2, "?", Color.BRIGHT_WHITE)

        elif progress < 0.35:
            # P1 charges but slips on banana!
            p = (progress - 0.20) / 0.15
            cx = w // 2
            banana_x = cx - 2

            # Draw banana on ground
            buffer.draw_text(banana_x, gy - 1, "\\\\_/", Color.BRIGHT_YELLOW)

            if p < 0.4:
                # P1 charges
                p1_x = int(lerp(cx - 10, cx - 3, p / 0.4))
                self._draw_fighter(buffer, p1_x, gy, STICK_PUNCH_RIGHT, Color.BRIGHT_CYAN)
            elif p < 0.6:
                # SLIP!
                slip_p = (p - 0.4) / 0.2
                p1_x = cx - 3
                slip_y = gy - int(math.sin(slip_p * math.pi) * 3)
                slip_sprite = [
                    "  \\O  ",
                    "   |\\ ",
                    "  /   ",
                ]
                buffer.draw_sprite(p1_x, slip_y - 2, slip_sprite, Color.BRIGHT_CYAN, transparent=' ')
                buffer.draw_text(p1_x - 3, slip_y - 4, "WHOOOAA!", Color.BRIGHT_YELLOW)
                spawn_sparks(self.ps, p1_x + 2, gy - 1, 4)
            else:
                # P1 crashes into P2!
                crash_p = (p - 0.6) / 0.4
                p1_x = int(lerp(cx - 3, cx + 5, crash_p))
                crash_sprite = [
                    " O\\   ",
                    "/|  O/",
                    "/ \\/| ",
                    "   / \\",
                ]
                buffer.draw_sprite(p1_x, gy - 3, crash_sprite, Color.BRIGHT_MAGENTA, transparent=' ')
                if crash_p > 0.5:
                    buffer.draw_text_centered(gy - 7, "B O N K !", Color.BRIGHT_RED)
                    spawn_explosion(self.ps, cx + 3, gy - 2, 10,
                                   chars="*#!?@$", colors=[Color.BRIGHT_YELLOW, Color.BRIGHT_RED])

            self._draw_fighter(buffer, cx + 5, gy, STICK_IDLE, Color.BRIGHT_RED, mirror=True)

        elif progress < 0.50:
            # Both tumble off screen in a cartoon fight cloud
            p = (progress - 0.35) / 0.15
            cx = w // 2
            cloud_x = int(lerp(cx - 5, cx + 10, math.sin(p * math.pi * 3) * 0.3 + p * 0.5))
            cloud_y = gy - 3

            # Cartoon fight cloud
            cloud = [
                "  .**##**. ",
                " *# POW! #*",
                "*# BANG! #*",
                " *# ZAP!#* ",
                "  '**##**' ",
            ]
            fight_words = ["POW!", "BANG!", "ZAP!", "OOF!", "BAM!", "BONK!", "CRASH!"]
            word = fight_words[int(p * 20) % len(fight_words)]
            cloud[2] = f"*#  {word:^6s} #*"

            colors = [Color.BRIGHT_YELLOW, Color.BRIGHT_RED, Color.BRIGHT_MAGENTA,
                      Color.BRIGHT_CYAN, Color.BRIGHT_GREEN]
            fg = colors[int(p * 15) % len(colors)]

            buffer.draw_sprite(cloud_x, cloud_y, cloud, fg, transparent=' ')

            # Random limbs sticking out
            limbs = ["/", "\\", "O", "|", "_"]
            for i in range(4):
                lx = cloud_x + random.randint(-2, 12)
                ly = cloud_y + random.randint(-1, 5)
                buffer.set_cell(lx, ly, random.choice(limbs), Color.BRIGHT_WHITE)

            spawn_sparks(self.ps, cloud_x + 5, cloud_y, 2)

        elif progress < 0.65:
            # They separate - both dizzy
            p = (progress - 0.50) / 0.15
            cx = w // 2
            p1_x = int(lerp(cx, cx - 12, ease_out(p)))
            p2_x = int(lerp(cx, cx + 8, ease_out(p)))

            self._draw_fighter(buffer, p1_x, gy, STICK_DIZZY, Color.BRIGHT_CYAN)
            self._draw_fighter(buffer, p2_x, gy, STICK_DIZZY, Color.BRIGHT_RED, mirror=True)

            # Stars circling heads
            star_chars = "*+.*"
            for i in range(3):
                angle = p * 10 + i * 2.1
                sx1 = p1_x + 2 + int(math.cos(angle) * 3)
                sy1 = gy - 4 + int(math.sin(angle) * 1)
                buffer.set_cell(sx1, sy1, star_chars[i % len(star_chars)], Color.BRIGHT_YELLOW)
                sx2 = p2_x + 2 + int(math.cos(angle + 1) * 3)
                sy2 = gy - 4 + int(math.sin(angle + 1) * 1)
                buffer.set_cell(sx2, sy2, star_chars[(i + 1) % len(star_chars)], Color.BRIGHT_YELLOW)

            buffer.draw_text_centered(3, "...did that just happen?", Color.GRAY)

        elif progress < 0.75:
            # They look at each other, then at the banana
            p = (progress - 0.65) / 0.10
            cx = w // 2
            self._draw_fighter(buffer, cx - 12, gy, STICK_IDLE, Color.BRIGHT_CYAN)
            self._draw_fighter(buffer, cx + 8, gy, STICK_IDLE, Color.BRIGHT_RED, mirror=True)

            # Banana still on ground
            buffer.draw_text(cx - 2, gy - 1, "\\\\_/", Color.BRIGHT_YELLOW)

            # Both look down at banana
            if int(p * 4) % 2 == 0:
                buffer.draw_text(cx - 6, gy - 6, "?", Color.BRIGHT_CYAN)
                buffer.draw_text(cx + 10, gy - 6, "?", Color.BRIGHT_RED)
            # Arrow pointing at banana
            buffer.draw_text(cx - 1, gy - 3, "v", Color.BRIGHT_WHITE)

        elif progress < 0.85:
            # They both start laughing!
            p = (progress - 0.75) / 0.10
            cx = w // 2

            laugh_sprite_1 = [
                " \\O/ ",
                "  |  ",
                " / \\ ",
            ]
            laugh_sprite_2 = mirror_sprite(laugh_sprite_1)

            # Bouncing with laughter
            bounce_h1 = int(abs(math.sin(p * math.pi * 5)) * 2)
            bounce_h2 = int(abs(math.sin(p * math.pi * 5 + 1)) * 2)

            buffer.draw_sprite(cx - 12, gy - 2 - bounce_h1, laugh_sprite_1,
                              Color.BRIGHT_CYAN, transparent=' ')
            buffer.draw_sprite(cx + 8, gy - 2 - bounce_h2, laugh_sprite_2,
                              Color.BRIGHT_RED, transparent=' ')

            # "HA HA HA" text floating up
            ha_texts = ["HA!", "HAHA!", "LOL!", "ROFL!", "LMAO!"]
            for i in range(3):
                tx = cx - 5 + i * 6 + int(math.sin(p * 8 + i) * 2)
                ty = int(gy - 5 - p * 3 - i * 2)
                if 0 <= ty < buffer.height:
                    buffer.draw_text(tx, ty, ha_texts[i % len(ha_texts)],
                                    Color.BRIGHT_YELLOW if i % 2 else Color.BRIGHT_GREEN)

            # Banana on ground
            buffer.draw_text(cx - 2, gy - 1, "\\\\_/", Color.BRIGHT_YELLOW)

        else:
            # They become friends! Walk off together
            p = (progress - 0.85) / 0.15
            cx = w // 2

            # Walking together to the right
            walk_x = int(lerp(cx - 5, w + 5, ease_in_out(p)))

            friend_sprite = [
                " O   O ",
                "/|\\ /|\\",
                "/ \\ / \\",
            ]
            buffer.draw_sprite(walk_x, gy - 2, friend_sprite, Color.BRIGHT_GREEN, transparent=' ')

            # Heart above them
            heart = [
                " ** ** ",
                "*****  ",
                " ***   ",
                "  *    ",
            ]
            # Wait, let me fix that heart
            heart = [
                " ** **",
                "******",
                " **** ",
                "  **  ",
                "   *  ",
            ]
            buffer.draw_sprite(walk_x + 1, gy - 7, heart, Color.BRIGHT_RED, transparent=' ')

            buffer.draw_text_centered(3, "FRIENDSHIP WINS!", Color.BRIGHT_GREEN)

            # Fireworks!
            if int(p * 10) % 3 == 0:
                fx = random.randint(5, w - 5)
                fy = random.randint(3, gy - 8)
                spawn_fireworks(self.ps, fx, fy, 15)

        self.ps.update(dt)
        self.ps.draw(buffer)
        return buffer

    def _draw_fighter(self, buffer, x, y, sprite, fg, mirror=False):
        s = mirror_sprite(sprite) if mirror else sprite
        buffer.draw_sprite(x, y - len(s) + 1, s, fg, transparent=' ')


# ─────────────────────────── SCENE: FADE OUT ─────────────────────────────────

def render_fade_out(buffer: ScreenBuffer, progress: float):
    """Fade to black with final message."""
    w, h = buffer.width, buffer.height

    if progress < 0.3:
        # Final scene - sunset
        p = progress / 0.3
        # Sky gradient
        sky_colors = [Color.BLUE, Color.BRIGHT_BLUE, Color.CYAN, Color.YELLOW,
                      Color.ORANGE, Color.RED]
        for y in range(h - 5):
            ci = int(y / (h - 5) * len(sky_colors))
            ci = min(ci, len(sky_colors) - 1)
            for x in range(w):
                buffer.set_cell(x, y, ' ', Color.WHITE, sky_colors[ci])

        # Sun
        sun_y = int(lerp(h // 2 - 3, h - 6, p))
        sun = [
            "  \\|/  ",
            " --O-- ",
            "  /|\\  ",
        ]
        buffer.draw_sprite(w // 2 - 3, sun_y, sun, Color.BRIGHT_YELLOW, transparent=' ')

        # Ground
        for x in range(w):
            for y in range(h - 5, h):
                buffer.set_cell(x, y, '~' if y == h - 5 else ' ', Color.GREEN, Color.GREEN)

        # Two tiny figures in silhouette walking into sunset
        walk_x = int(lerp(w // 2 - 5, w // 2 + 5, p))
        tiny_friends = ["o o", "|||", "^ ^"]
        buffer.draw_sprite(walk_x, h - 7, tiny_friends, Color.BLACK, transparent=' ')

    elif progress < 0.7:
        # Fade to black
        p = (progress - 0.3) / 0.4
        # Render the sunset scene at frozen state
        for y in range(h - 5):
            sky_colors = [Color.BLUE, Color.BRIGHT_BLUE, Color.CYAN, Color.YELLOW,
                          Color.ORANGE, Color.RED]
            ci = int(y / (h - 5) * len(sky_colors))
            ci = min(ci, len(sky_colors) - 1)
            for x in range(w):
                buffer.set_cell(x, y, ' ', Color.WHITE, sky_colors[ci])

        for x in range(w):
            for y in range(h - 5, h):
                buffer.set_cell(x, y, ' ', Color.GREEN, Color.GREEN)

        apply_fade(buffer, p)

    else:
        # Fully black with message
        p = (progress - 0.7) / 0.3
        if p > 0.3 and p < 0.8:
            msg = "And they lived happily ever after..."
            visible = int(len(msg) * ((p - 0.3) / 0.5))
            buffer.draw_text_centered(h // 2, msg[:visible], Color.GRAY)


# ────────────────────────── SCENE: END CREDITS ───────────────────────────────

def render_credits(buffer: ScreenBuffer, progress: float):
    """Star Wars style scrolling credits with fireworks."""
    w, h = buffer.width, buffer.height

    # Star background
    draw_star_field(buffer, density=0.015, seed=99)

    credits_lines = [
        "",
        "",
        "╔══════════════════════════════════════╗",
        "║      A S C I I   F I G H T          ║",
        "║      ULTIMATE SHOWDOWN               ║",
        "╚══════════════════════════════════════╝",
        "",
        "",
        "- - - - - C R E D I T S - - - - -",
        "",
        "",
        "DIRECTED BY",
        "Claude Opus 4.6",
        "",
        "PRODUCED BY",
        "The ASCII Arts Council",
        "",
        "STARRING",
        "Stick Figure #1 ... as THE HERO",
        "Stick Figure #2 ... as THE RIVAL",
        "Banana Peel ..... as ITSELF",
        "",
        "CHOREOGRAPHY",
        "International Stick Figure",
        "Fighting Association",
        "",
        "SPECIAL EFFECTS",
        "Particle Systems Inc.",
        "& ASCII Explosions Ltd.",
        "",
        "CATERING",
        "One (1) Banana",
        "",
        "STUNT COORDINATOR",
        "No stick figures were harmed",
        "in the making of this video",
        "(they're just lines)",
        "",
        "MUSIC",
        "The sound of your keyboard",
        "",
        "BANANA WRANGLER",
        "Professional Banana Handler",
        "",
        "WRITTEN IN",
        "Python, with love",
        "",
        "",
        "SPECIAL THANKS",
        "You, for watching!",
        "",
        "",
        "   * * * * * * * * * * * *   ",
        "  * THE END * THE END *  ",
        "   * * * * * * * * * * * *   ",
        "",
        "",
        "",
    ]

    # Scroll credits upward
    total_lines = len(credits_lines)
    y_offset = h - progress * (total_lines + h)

    for i, line in enumerate(credits_lines):
        y = int(y_offset + i)
        if 0 <= y < h:
            # Color based on content
            if '═' in line or '║' in line or '╔' in line or '╗' in line or '╚' in line or '╝' in line:
                fg = Color.BRIGHT_YELLOW
            elif "DIRECTED" in line or "PRODUCED" in line or "STARRING" in line or \
                 "CHOREOGRAPHY" in line or "SPECIAL" in line or "CATERING" in line or \
                 "STUNT" in line or "MUSIC" in line or "BANANA" in line or \
                 "WRITTEN" in line:
                fg = Color.BRIGHT_CYAN
            elif "THE END" in line:
                fg = Color.BRIGHT_YELLOW if int(progress * 10) % 2 == 0 else Color.BRIGHT_RED
            elif "* * *" in line:
                fg = Color.BRIGHT_MAGENTA
            else:
                fg = Color.WHITE
            buffer.draw_text_centered(y, line, fg)

    # Occasional fireworks
    if int(progress * 20) % 5 == 0:
        ps = ParticleSystem()
        fx = random.randint(5, w - 5)
        fy = random.randint(2, h // 2)
        spawn_fireworks(ps, fx, fy, 8)
        ps.draw(buffer)

    # Fade out at the very end
    if progress > 0.9:
        fade_p = (progress - 0.9) / 0.1
        apply_fade(buffer, fade_p)
