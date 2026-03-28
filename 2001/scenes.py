"""Scene definitions for 2001: A Space Odyssey ASCII art re-enactment."""

import math
from timeline import Scene, Dialogue
from renderer import Color
from effects import (
    star_field, fade_in, fade_out, hash_float,
    speed_lines, tunnel_effect, draw_circle, draw_filled_circle,
    wave_pattern, dissolve_transition
)


def create_all_scenes():
    """Create and return the list of all 10 scenes in order."""
    return [
        scene_dawn_of_man(),
        scene_match_cut(),
        scene_space_station(),
        scene_moon_monolith(),
        scene_discovery_one(),
        scene_hal_9000(),
        scene_sorry_dave(),
        scene_disconnecting_hal(),
        scene_stargate(),
        scene_star_child(),
    ]


# ---------------------------------------------------------------------------
# ASCII Art Sprites
# ---------------------------------------------------------------------------

APE_STANDING = [
    "  .o.  ",
    " /|||  ",
    "  |'|  ",
    " / | \\ ",
    "/  |  \\",
]

APE_ARM_UP = [
    "  .o./|",
    " /||| |",
    "  |'|  ",
    " / |   ",
    "/  |   ",
]

BONE = [
    "o====o",
]

BONE_VERTICAL = [
    " o ",
    " | ",
    " | ",
    " | ",
    " o ",
]

MONOLITH = [
    "┌──┐",
    "│  │",
    "│  │",
    "│  │",
    "│  │",
    "│  │",
    "│  │",
    "│  │",
    "│  │",
    "└──┘",
]

SPACE_STATION_RING = [
    "    .----.    ",
    "  /        \\  ",
    " |    --    | ",
    " |   |  |   | ",
    " |    --    | ",
    "  \\        /  ",
    "    '----'    ",
]

SHUTTLE = [
    "  /\\  ",
    " /  \\ ",
    "|    |",
    " \\__/ ",
]

DISCOVERY_ONE = [
    "              ___     ",
    "  ===========|   |    ",
    " /           |___|----",
    " \\           |   |----",
    "  ===========|___|    ",
    "                      ",
]

HAL_EYE = [
    "     .-------.     ",
    "   /           \\   ",
    "  |   .-----.   |  ",
    "  |  /       \\  |  ",
    "  | |  (( ))  | |  ",
    "  |  \\       /  |  ",
    "  |   '-----'   |  ",
    "   \\           /   ",
    "     '-------'     ",
]

ASTRONAUT = [
    " [O] ",
    " /|\\ ",
    " / \\ ",
]

EARTH_SPRITE = [
    "      ____      ",
    "    /      \\    ",
    "  /  ~~  .   \\  ",
    " |  ~~~~ ..   | ",
    " | ~~  ~~~ .  | ",
    " |   ~~~~  .  | ",
    "  \\  ~~  .   /  ",
    "    \\______/    ",
]

STAR_CHILD = [
    "    *    ",
    "  * . *  ",
    " * .o. * ",
    "  * . *  ",
    "    *    ",
]


# ---------------------------------------------------------------------------
# Scene 1: Dawn of Man
# ---------------------------------------------------------------------------

def _render_dawn_of_man(buffer, progress):
    alpha_in = fade_in(buffer, progress, 0.1)
    alpha_out = fade_out(buffer, progress, 0.95)

    # Landscape
    ground_y = buffer.height - 6
    for x in range(buffer.width):
        # Terrain variation
        h = int(2 * math.sin(x * 0.15) + 1.5 * math.sin(x * 0.07))
        for dy in range(3 + h):
            y = ground_y + dy
            if 0 <= y < buffer.height:
                ch = '.' if dy == 0 else ','
                fg = Color.YELLOW if dy == 0 else Color.GREEN
                if alpha_in < 1.0 and hash_float(x, y) > alpha_in:
                    continue
                buffer.set_cell(x, y, ch, fg, Color.BLACK)

    # Rocks
    for i in range(5):
        rx = int(hash_float(100, i) * buffer.width * 0.8) + 5
        buffer.set_cell(rx, ground_y - 1, 'A', Color.GRAY, Color.BLACK)
        buffer.set_cell(rx + 1, ground_y - 1, 'A', Color.GRAY, Color.BLACK)

    # Apes appear after progress 0.15
    if progress > 0.15:
        ape_x = 10
        ape_y = ground_y - 5
        buffer.draw_sprite(ape_x, ape_y, APE_STANDING, Color.YELLOW)
        buffer.draw_sprite(ape_x + 12, ape_y, APE_STANDING, Color.YELLOW)

    # Monolith appears at 0.3
    if progress > 0.3:
        mx = buffer.width // 2 - 2
        my = ground_y - len(MONOLITH)
        buffer.draw_sprite(mx, my, MONOLITH, Color.BRIGHT_WHITE)

    # Ape with bone at 0.6
    if progress > 0.6:
        buffer.draw_sprite(10, ground_y - 5, APE_ARM_UP, Color.YELLOW)
        buffer.draw_text(17, ground_y - 6, "o====o", Color.WHITE)

    # Sky gradient
    if alpha_in < 1.0:
        return
    sun_x = int(progress * buffer.width * 0.6) + 5
    buffer.set_cell(sun_x, 1, 'O', Color.BRIGHT_YELLOW, Color.BLACK)
    buffer.set_cell(sun_x - 1, 1, '-', Color.YELLOW, Color.BLACK)
    buffer.set_cell(sun_x + 1, 1, '-', Color.YELLOW, Color.BLACK)


def scene_dawn_of_man():
    return Scene(
        "dawn_of_man", "THE DAWN OF MAN", 25.0,
        _render_dawn_of_man,
        [
            Dialogue(0.0, 0.15, "Africa. Four million years ago."),
            Dialogue(0.35, 0.55, "The monolith appears..."),
            Dialogue(0.65, 0.85, "The first tool."),
        ]
    )


# ---------------------------------------------------------------------------
# Scene 2: Match Cut - Bone to Space Station
# ---------------------------------------------------------------------------

def _render_match_cut(buffer, progress):
    if progress < 0.4:
        # Bone tumbling upward
        sub = progress / 0.4
        bone_y = int(buffer.height * (1.0 - sub) * 0.8)
        bone_x = buffer.width // 2 - 3
        # Rotate bone through orientations
        if sub < 0.33:
            buffer.draw_text(bone_x, bone_y, "o====o", Color.WHITE)
        elif sub < 0.66:
            bone_x = buffer.width // 2 - 1
            for i, line in enumerate(BONE_VERTICAL):
                buffer.draw_text(bone_x, bone_y + i - 2, line, Color.WHITE)
        else:
            buffer.draw_text(bone_x, bone_y, "o====o", Color.WHITE)
        # Blue sky
        for x in range(buffer.width):
            if hash_float(x, 999) < 0.02:
                buffer.set_cell(x, int(hash_float(x, 998) * bone_y), '.', Color.WHITE)

    elif progress < 0.6:
        # Transition dissolve
        sub = (progress - 0.4) / 0.2
        dissolve_transition(buffer, sub)

    else:
        # Space station with stars
        sub = (progress - 0.6) / 0.4
        star_field(buffer, sub, seed=100)
        # Station rotating
        sx = buffer.width // 2 - 7
        sy = buffer.height // 2 - 3
        buffer.draw_sprite(sx, sy, SPACE_STATION_RING, Color.BRIGHT_WHITE)
        # "The Blue Danube" reference
        buffer.draw_text_centered(buffer.height - 5, "♪ The Blue Danube ♪", Color.CYAN)


def scene_match_cut():
    return Scene(
        "match_cut", "THE MATCH CUT", 15.0,
        _render_match_cut,
        [
            Dialogue(0.0, 0.35, "The bone rises..."),
            Dialogue(0.65, 0.95, "Four million years later."),
        ]
    )


# ---------------------------------------------------------------------------
# Scene 3: Space Station
# ---------------------------------------------------------------------------

def _render_space_station(buffer, progress):
    star_field(buffer, progress, seed=200)

    # Rotating station - simulate rotation by shifting characters
    cx = buffer.width // 2
    cy = buffer.height // 2 - 2
    angle = progress * math.pi * 2

    # Draw station as rotating ring
    radius = 8
    for i in range(32):
        a = angle + i * math.pi * 2 / 32
        x = int(cx + radius * math.cos(a) * 2)  # *2 for aspect ratio
        y = int(cy + radius * math.sin(a))
        ch = '=' if i % 4 == 0 else '-'
        buffer.set_cell(x, y, ch, Color.BRIGHT_WHITE, Color.BLACK)

    # Hub
    buffer.set_cell(cx, cy, '+', Color.WHITE, Color.BLACK)
    buffer.set_cell(cx - 1, cy, '[', Color.WHITE, Color.BLACK)
    buffer.set_cell(cx + 1, cy, ']', Color.WHITE, Color.BLACK)

    # Shuttle approaching
    if progress > 0.3:
        shuttle_sub = (progress - 0.3) / 0.7
        shuttle_y = int(buffer.height - 2 - shuttle_sub * (buffer.height // 2 - 2))
        sx = cx - 3
        buffer.draw_sprite(sx, shuttle_y, SHUTTLE, Color.GRAY)


def scene_space_station():
    return Scene(
        "space_station", "SPACE STATION V", 20.0,
        _render_space_station,
        [
            Dialogue(0.0, 0.25, "Earth orbit. Space Station V."),
            Dialogue(0.4, 0.7, "Shuttle approaching for docking."),
        ]
    )


# ---------------------------------------------------------------------------
# Scene 4: Moon Monolith TMA-1
# ---------------------------------------------------------------------------

def _render_moon_monolith(buffer, progress):
    # Lunar surface
    ground_y = buffer.height - 7
    for x in range(buffer.width):
        variation = int(1.5 * math.sin(x * 0.1) + math.sin(x * 0.23))
        for dy in range(4 + variation):
            y = ground_y + dy
            if 0 <= y < buffer.height:
                ch = '~' if dy == 0 else ':'
                buffer.set_cell(x, y, ch, Color.GRAY, Color.BLACK)

    # Craters
    for i in range(3):
        cx = int(hash_float(300, i) * buffer.width * 0.8) + 5
        buffer.set_cell(cx, ground_y, 'U', Color.DARK_GRAY, Color.BLACK)
        buffer.set_cell(cx - 1, ground_y, '_', Color.DARK_GRAY, Color.BLACK)
        buffer.set_cell(cx + 1, ground_y, '_', Color.DARK_GRAY, Color.BLACK)

    # Excavation pit
    pit_x = buffer.width // 2 - 5
    pit_y = ground_y + 1
    buffer.draw_text(pit_x, pit_y, "\\________/", Color.DARK_GRAY)

    # Astronauts
    if progress > 0.1:
        for i in range(3):
            ax = pit_x - 8 + i * 6
            ay = ground_y - 3
            buffer.draw_sprite(ax, ay, ASTRONAUT, Color.WHITE)

    # Monolith revealed
    if progress > 0.3:
        mx = buffer.width // 2 - 2
        my = ground_y - len(MONOLITH) + 1
        buffer.draw_sprite(mx, my, MONOLITH, Color.BRIGHT_WHITE)

    # Signal burst at 0.8
    if progress > 0.8:
        sub = (progress - 0.8) / 0.2
        num_rays = int(sub * 20) + 4
        mx = buffer.width // 2
        my = ground_y - len(MONOLITH) // 2
        for i in range(num_rays):
            angle = i * math.pi * 2 / num_rays
            for r in range(2, int(sub * 15) + 3):
                rx = int(mx + r * math.cos(angle) * 2)
                ry = int(my + r * math.sin(angle))
                chars = ['|', '/', '-', '\\']
                ch = chars[i % 4]
                buffer.set_cell(rx, ry, ch, Color.BRIGHT_WHITE, Color.BLACK)

    # Stars
    star_field(buffer, progress, seed=300, density=0.01)

    # Earth in sky
    buffer.set_cell(buffer.width - 10, 2, 'O', Color.BRIGHT_BLUE, Color.BLACK)
    buffer.set_cell(buffer.width - 11, 2, '(', Color.BLUE, Color.BLACK)
    buffer.set_cell(buffer.width - 9, 2, ')', Color.BLUE, Color.BLACK)


def scene_moon_monolith():
    return Scene(
        "moon_monolith", "TYCHO MAGNETIC ANOMALY ONE", 15.0,
        _render_moon_monolith,
        [
            Dialogue(0.0, 0.25, "The Moon. Tycho Crater."),
            Dialogue(0.35, 0.6, "Deliberately buried. Four million years ago."),
            Dialogue(0.82, 0.98, "The signal."),
        ]
    )


# ---------------------------------------------------------------------------
# Scene 5: Discovery One
# ---------------------------------------------------------------------------

def _render_discovery_one(buffer, progress):
    star_field(buffer, progress, seed=400)

    # Ship drifts across screen
    ship_x = int(buffer.width * 1.2 - progress * buffer.width * 1.8)
    ship_y = buffer.height // 2 - 3
    buffer.draw_sprite(ship_x, ship_y, DISCOVERY_ONE, Color.GRAY)

    # "DISCOVERY" label
    label_x = ship_x + 2
    if 0 <= label_x < buffer.width - 9:
        buffer.draw_text(label_x, ship_y - 1, "DISCOVERY", Color.BRIGHT_WHITE)

    # Jupiter ahead (grows as we approach)
    if progress > 0.4:
        sub = (progress - 0.4) / 0.6
        jx = buffer.width - 8
        jy = buffer.height // 2
        radius = int(sub * 6) + 1
        draw_filled_circle(buffer, jx, jy, radius, '░', Color.ORANGE, Color.BLACK)
        # Jupiter bands
        for band in range(max(1, radius - 1)):
            by = jy - radius + band * 2 + 1
            if 0 <= by < buffer.height:
                for bx in range(jx - radius, jx + radius + 1):
                    if 0 <= bx < buffer.width:
                        cell = buffer.get_cell(bx, by)
                        if cell and cell.char == '░':
                            buffer.set_cell(bx, by, '▒', Color.YELLOW, Color.BLACK)

    # "18 MONTHS LATER" subtitle timing
    pass


def scene_discovery_one():
    return Scene(
        "discovery_one", "JUPITER MISSION", 20.0,
        _render_discovery_one,
        [
            Dialogue(0.0, 0.2, "18 months later. Discovery One."),
            Dialogue(0.3, 0.5, "Mission to Jupiter."),
            Dialogue(0.7, 0.9, "Jupiter approaches."),
        ]
    )


# ---------------------------------------------------------------------------
# Scene 6: HAL 9000
# ---------------------------------------------------------------------------

def _render_hal_9000(buffer, progress):
    # Dark room background
    buffer.clear(Color.BLACK)

    # HAL's eye - centered, pulsing red
    ex = buffer.width // 2 - 10
    ey = buffer.height // 2 - 4

    # Eye housing
    buffer.draw_sprite(ex, ey, HAL_EYE, Color.GRAY)

    # Red glow in the center - pulsing
    pulse = 0.7 + 0.3 * math.sin(progress * math.pi * 6)
    cx = buffer.width // 2
    cy = buffer.height // 2
    if pulse > 0.5:
        fg = Color.BRIGHT_RED
    else:
        fg = Color.RED
    draw_filled_circle(buffer, cx, cy, 2, '●', fg, Color.BLACK)
    buffer.set_cell(cx, cy, '@', Color.BRIGHT_RED, Color.RED)

    # "HAL 9000" label
    buffer.draw_text_centered(ey + len(HAL_EYE) + 1, "HAL 9000", Color.RED)

    # Ambient panel lights
    for i in range(4):
        lx = int(hash_float(500, i) * buffer.width * 0.3) + 3
        ly = int(hash_float(500, i + 10) * buffer.height * 0.3) + 2
        buffer.set_cell(lx, ly, '□', Color.DARK_GRAY, Color.BLACK)
        lx2 = buffer.width - lx
        buffer.set_cell(lx2, ly, '□', Color.DARK_GRAY, Color.BLACK)


def scene_hal_9000():
    return Scene(
        "hal_9000", "HAL 9000", 20.0,
        _render_hal_9000,
        [
            Dialogue(0.0, 0.15, "Good afternoon, Dave."),
            Dialogue(0.2, 0.4, "HAL: Everything is running smoothly."),
            Dialogue(0.45, 0.65, "HAL: I am putting myself to the fullest possible use."),
            Dialogue(0.7, 0.9,
                     "HAL: I am, by any practical definition, foolproof and incapable of error."),
        ]
    )


# ---------------------------------------------------------------------------
# Scene 7: "I'm Sorry Dave"
# ---------------------------------------------------------------------------

def _render_sorry_dave(buffer, progress):
    buffer.clear(Color.BLACK)

    # HAL's eye - more intense
    ex = buffer.width // 2 - 10
    ey = buffer.height // 2 - 4
    buffer.draw_sprite(ex, ey, HAL_EYE, Color.WHITE)

    cx = buffer.width // 2
    cy = buffer.height // 2
    draw_filled_circle(buffer, cx, cy, 2, '●', Color.BRIGHT_RED, Color.BLACK)
    buffer.set_cell(cx, cy, '@', Color.BRIGHT_RED, Color.RED)

    # Pod bay doors
    if progress > 0.3:
        door_y = buffer.height - 4
        # Sealed door visualization
        buffer.fill_rect(5, door_y, buffer.width - 10, 1, '█', Color.GRAY, Color.BLACK)
        buffer.fill_rect(5, door_y + 1, buffer.width - 10, 1, '▓', Color.DARK_GRAY, Color.BLACK)
        buffer.draw_text_centered(door_y - 1, "[ POD BAY DOORS - LOCKED ]", Color.RED)

    # Warning indicators
    if progress > 0.5:
        blink = int(progress * 10) % 2 == 0
        if blink:
            buffer.draw_text(2, 1, "⚠ OVERRIDE", Color.RED)
            buffer.draw_text(buffer.width - 13, 1, "⚠ OVERRIDE", Color.RED)


def scene_sorry_dave():
    return Scene(
        "sorry_dave", "I'M SORRY, DAVE", 15.0,
        _render_sorry_dave,
        [
            Dialogue(0.0, 0.2, "DAVE: Open the pod bay doors, HAL."),
            Dialogue(0.25, 0.55, "HAL: I'm sorry, Dave. I'm afraid I can't do that."),
            Dialogue(0.6, 0.8,
                     "HAL: This mission is too important for me to allow you to jeopardize it."),
            Dialogue(0.85, 0.98, "DAVE: HAL, I won't argue with you anymore. Open the doors!"),
        ]
    )


# ---------------------------------------------------------------------------
# Scene 8: Disconnecting HAL
# ---------------------------------------------------------------------------

def _render_disconnecting_hal(buffer, progress):
    buffer.clear(Color.BLACK)

    # Logic memory room - grid of modules
    module_rows = 4
    module_cols = 8
    module_w = 6
    module_h = 2
    start_x = (buffer.width - module_cols * (module_w + 1)) // 2
    start_y = 3

    # How many modules removed
    total_modules = module_rows * module_cols
    removed = int(progress * total_modules * 1.2)

    for row in range(module_rows):
        for col in range(module_cols):
            idx = row * module_cols + col
            mx = start_x + col * (module_w + 1)
            my = start_y + row * (module_h + 1)

            if idx < removed:
                # Empty slot
                buffer.fill_rect(mx, my, module_w, module_h, '·', Color.DARK_GRAY)
            else:
                # Active module
                buffer.fill_rect(mx, my, module_w, module_h, '█', Color.CYAN)
                label = f"M{idx:02d}"
                buffer.draw_text(mx + 1, my, label, Color.BLACK, Color.CYAN)

    # HAL's eye - dimming
    eye_y = start_y + module_rows * (module_h + 1) + 2
    cx = buffer.width // 2
    cy = eye_y + 2

    brightness = max(0.0, 1.0 - progress * 1.2)
    if brightness > 0.5:
        fg = Color.BRIGHT_RED
    elif brightness > 0.2:
        fg = Color.RED
    elif brightness > 0:
        fg = Color.DARK_GRAY
    else:
        fg = Color.BLACK

    if brightness > 0:
        draw_circle(buffer, cx, cy, 3, 'O', fg, Color.BLACK)
        buffer.set_cell(cx, cy, '@', fg, Color.BLACK)

    # "Daisy" text degradation
    if progress > 0.5:
        sub = (progress - 0.5) / 0.5
        daisy = "Daisy, Daisy, give me your answer, do..."
        # Progressively remove characters
        visible = int(len(daisy) * (1.0 - sub * 0.8))
        text = daisy[:visible]
        # Slow down - add spaces
        if sub > 0.5:
            spaced = ""
            for i, ch in enumerate(text):
                spaced += ch
                if hash_float(i, 888) < sub * 0.5:
                    spaced += " "
            text = spaced
        fg_text = Color.RED if sub < 0.5 else Color.DARK_GRAY
        buffer.draw_text_centered(cy + 5, text, fg_text)


def scene_disconnecting_hal():
    return Scene(
        "disconnecting_hal", "DAISY, DAISY...", 25.0,
        _render_disconnecting_hal,
        [
            Dialogue(0.0, 0.15, "DAVE: I'm going to disconnect you, HAL."),
            Dialogue(0.2, 0.35, "HAL: I'm afraid. I'm afraid, Dave."),
            Dialogue(0.4, 0.55, "HAL: My mind is going. I can feel it."),
            Dialogue(0.6, 0.75, "HAL: Daisy, Daisy, give me your answer, do..."),
            Dialogue(0.8, 0.95, "HAL: I'm... a... fraid..."),
        ]
    )


# ---------------------------------------------------------------------------
# Scene 9: Stargate Sequence
# ---------------------------------------------------------------------------

def _render_stargate(buffer, progress):
    # Multi-phase psychedelic sequence
    if progress < 0.3:
        # Speed lines phase
        sub = progress / 0.3
        speed_lines(buffer, sub)
        # Color accents
        for i in range(10):
            x = int(hash_float(600, i) * buffer.width)
            y = int(hash_float(600, i + 50) * buffer.height)
            colors = [Color.RED, Color.CYAN, Color.MAGENTA, Color.YELLOW,
                      Color.GREEN, Color.BRIGHT_BLUE]
            fg = colors[int(sub * 20 + i) % len(colors)]
            buffer.set_cell(x, y, '█', fg, Color.BLACK)

    elif progress < 0.6:
        # Tunnel phase
        sub = (progress - 0.3) / 0.3
        tunnel_effect(buffer, sub)

    elif progress < 0.85:
        # Abstract color patterns
        sub = (progress - 0.6) / 0.25
        wave_pattern(buffer, sub, amplitude=5, frequency=2.0)
        # Overlay matrix-rain style streams
        for col in range(0, buffer.width, 3):
            speed = hash_float(700, col) * 3 + 1
            offset = int(sub * buffer.height * speed) % buffer.height
            chars = "╬║╠╣╦╩═"
            colors = [Color.GREEN, Color.BRIGHT_GREEN, Color.CYAN, Color.BRIGHT_CYAN]
            for row in range(min(8, buffer.height)):
                y = (offset + row) % buffer.height
                ch = chars[int(hash_float(col, row + 800) * len(chars))]
                fg = colors[int(hash_float(col, row + 900) * len(colors))]
                buffer.set_cell(col, y, ch, fg, Color.BLACK)

    else:
        # Final flash / transformation
        sub = (progress - 0.85) / 0.15
        # Bright center expanding
        cx = buffer.width // 2
        cy = buffer.height // 2
        radius = int(sub * min(cx, cy))
        draw_filled_circle(buffer, cx, cy, radius, '█', Color.BRIGHT_WHITE, Color.BLACK)
        if radius > 2:
            draw_filled_circle(buffer, cx, cy, radius - 2, '▓', Color.WHITE, Color.BLACK)
        if radius > 4:
            draw_filled_circle(buffer, cx, cy, radius - 4, '░', Color.CYAN, Color.BLACK)


def scene_stargate():
    return Scene(
        "stargate", "JUPITER AND BEYOND THE INFINITE", 25.0,
        _render_stargate,
        [
            Dialogue(0.0, 0.15, "Beyond Jupiter..."),
            Dialogue(0.35, 0.55, "Through the Star Gate."),
            Dialogue(0.7, 0.85, "Beyond space. Beyond time."),
        ]
    )


# ---------------------------------------------------------------------------
# Scene 10: The Star Child
# ---------------------------------------------------------------------------

def _render_star_child(buffer, progress):
    alpha_out = fade_out(buffer, progress, 0.85)
    star_field(buffer, progress, seed=800, density=0.015)

    # Earth
    if progress < 0.9:
        ex = buffer.width // 2 + 15
        ey = buffer.height // 2 + 2
        buffer.draw_sprite(
            ex - len(EARTH_SPRITE[0]) // 2,
            ey - len(EARTH_SPRITE) // 2,
            EARTH_SPRITE, Color.BRIGHT_BLUE
        )

    # Star child - glowing embryo
    if progress > 0.1 and progress < 0.9:
        sub = min(1.0, (progress - 0.1) / 0.3)
        sc_x = buffer.width // 2 - 10
        sc_y = buffer.height // 2 - 2
        # Glow aura
        glow_radius = int(sub * 5) + 2
        draw_circle(buffer, sc_x + 4, sc_y + 2, glow_radius, '·', Color.BRIGHT_WHITE, Color.BLACK)
        if glow_radius > 2:
            draw_circle(buffer, sc_x + 4, sc_y + 2, glow_radius - 1, '+', Color.WHITE, Color.BLACK)
        # Child sprite
        buffer.draw_sprite(sc_x, sc_y, STAR_CHILD, Color.BRIGHT_WHITE)

    # Title card
    if progress > 0.85:
        title_sub = (progress - 0.85) / 0.15
        if title_sub > 0.3:
            buffer.clear()
            buffer.draw_text_centered(buffer.height // 2 - 2, "2 0 0 1", Color.BRIGHT_WHITE)
            buffer.draw_text_centered(buffer.height // 2, "A SPACE ODYSSEY", Color.WHITE)
            if title_sub > 0.6:
                buffer.draw_text_centered(buffer.height // 2 + 3, "THE END", Color.GRAY)


def scene_star_child():
    return Scene(
        "star_child", "THE STAR CHILD", 20.0,
        _render_star_child,
        [
            Dialogue(0.0, 0.15, "Transformation."),
            Dialogue(0.2, 0.5, "The Star Child gazes upon Earth."),
            Dialogue(0.6, 0.8, "A new beginning."),
        ]
    )
