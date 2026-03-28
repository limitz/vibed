"""
Lesson 7: Abstract & Expressive Art
Two panels: Energy/Chaos (left) and Calm/Serenity (right)
"""
import sys
import os
import math
import random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'artist'))

from student import (draw_line, draw_circle, draw_curve, draw_pressure_ramp,
                      draw_hatching, draw_filled_circle, draw_rectangle,
                      draw_triangle, draw_s_curve, draw_arc, draw_ellipse,
                      draw_crosshatching, draw_filled_rectangle, draw_gradient_fill)
from stylus_format import Drawing
from renderer import render_drawing

random.seed(42)
all_strokes = []

# ============================================================
# COLOR PALETTES
# ============================================================

# Warm colors for chaos panel (left) - 5+ distinct warm hues
WARM_REDS = [(220, 40, 30), (180, 20, 15), (255, 80, 50), (200, 50, 40), (160, 25, 20)]
WARM_ORANGES = [(240, 130, 30), (200, 100, 20), (255, 160, 60), (220, 110, 25)]
WARM_YELLOWS = [(250, 220, 40), (240, 200, 20), (255, 240, 100), (230, 190, 30)]
WARM_DARKS = [(40, 20, 15), (60, 30, 20), (80, 30, 15), (50, 15, 10)]
ALL_WARM = WARM_REDS + WARM_ORANGES + WARM_YELLOWS + WARM_DARKS

# Cool colors for calm panel (right) - 5+ distinct cool hues
COOL_BLUES = [(70, 120, 180), (40, 80, 140), (100, 150, 200), (30, 60, 110), (80, 130, 190)]
COOL_BLUE_GREENS = [(50, 140, 130), (70, 160, 150), (90, 180, 170)]
COOL_PURPLES = [(120, 100, 160), (140, 120, 180), (100, 80, 140)]
COOL_PALES = [(220, 230, 240), (200, 215, 230), (240, 240, 250), (190, 210, 230)]
COOL_GRAYS = [(160, 150, 145), (140, 135, 130)]
ALL_COOL = COOL_BLUES + COOL_BLUE_GREENS + COOL_PURPLES + COOL_PALES + COOL_GRAYS

# ============================================================
# PANEL 1: ENERGY / CHAOS (Left half, x: 0-490)
# ============================================================

# --- Background: layered warm gradient fills ---
# Base layer - deep red wash (vertical pressure gradient)
all_strokes.extend(draw_gradient_fill(
    10, 10, 470, 480,
    start_pressure=0.2, end_pressure=0.5,
    tool="brush", color=(180, 20, 15), spacing=8
))

# Second warm layer - orange charcoal texture
all_strokes.extend(draw_gradient_fill(
    30, 50, 430, 400,
    start_pressure=0.15, end_pressure=0.35,
    tool="charcoal", color=(255, 160, 60), spacing=10
))

# Yellow heat layer - lighter on top
all_strokes.extend(draw_gradient_fill(
    60, 20, 380, 200,
    start_pressure=0.25, end_pressure=0.1,
    tool="brush", color=(250, 220, 40), spacing=12
))

# --- Explosive focal point: upper-left-of-center ---
focal_x, focal_y = 240, 200

# Dense crosshatching at the core - charcoal, tight spacing, HOT
all_strokes.extend(draw_crosshatching(
    focal_x - 60, focal_y - 50, 120, 100,
    tool="charcoal", color=(40, 20, 15), pressure=0.8,
    spacing=4, angles=[30, -45, 70]
))

# Bright yellow burst behind the core
for r in [45, 55, 65]:
    all_strokes.extend(draw_filled_circle(
        focal_x, focal_y, r,
        tool="marker", color=(250, 220, 40), pressure=0.4
    ))

# Red-orange radiating filled circles - fragmented, overlapping
burst_positions = [
    (focal_x - 50, focal_y - 40, 25), (focal_x + 60, focal_y - 30, 20),
    (focal_x - 30, focal_y + 50, 22), (focal_x + 40, focal_y + 45, 18),
    (focal_x - 70, focal_y + 10, 15), (focal_x + 80, focal_y - 10, 17),
]
for bx, by, br in burst_positions:
    color = random.choice(WARM_REDS + WARM_ORANGES)
    all_strokes.extend(draw_filled_circle(bx, by, br, tool="charcoal", color=color, pressure=0.6))

# --- Radiating lines from focal point - explosive energy ---
for angle_deg in range(0, 360, 15):
    angle = math.radians(angle_deg)
    length = random.randint(80, 200)
    end_x = focal_x + math.cos(angle) * length
    end_y = focal_y + math.sin(angle) * length
    # Keep within left panel
    end_x = max(5, min(485, end_x))
    end_y = max(5, min(495, end_y))
    color = random.choice(WARM_REDS + WARM_ORANGES + WARM_YELLOWS)
    tool = random.choice(["charcoal", "marker", "charcoal", "marker", "pen"])
    all_strokes.append(draw_pressure_ramp(
        focal_x, focal_y, end_x, end_y,
        tool=tool, color=color
    ))

# --- Jagged S-curves cutting across the panel - tension lines ---
for i in range(8):
    y_start = random.randint(30, 470)
    x_start = random.randint(10, 100)
    y_end = y_start + random.randint(-80, 80)
    y_end = max(10, min(490, y_end))
    amplitude = random.randint(25, 50)
    color = random.choice(WARM_DARKS + WARM_REDS)
    all_strokes.append(draw_s_curve(
        x_start, y_start, random.randint(350, 480), y_end,
        amplitude=amplitude, tool="marker", color=color,
        pressure=random.uniform(0.5, 0.8)
    ))

# --- Sharp triangles - collision fragments ---
for i in range(6):
    tx = random.randint(50, 430)
    ty = random.randint(50, 430)
    size = random.randint(20, 50)
    color = random.choice(WARM_YELLOWS + WARM_ORANGES)
    all_strokes.append(draw_triangle(
        tx, ty, tx + size, ty + random.randint(-size, size),
        tx + random.randint(-size // 2, size // 2), ty - size,
        tool="pen", color=color, pressure=random.uniform(0.5, 0.8)
    ))

# --- Heavy hatching zones - dark aggressive texture ---
# Bottom-left dense area
all_strokes.extend(draw_hatching(
    20, 350, 180, 130,
    tool="charcoal", color=(60, 30, 20),
    pressure=0.7, spacing=4, angle_deg=60
))
# Upper-right secondary cluster
all_strokes.extend(draw_hatching(
    300, 30, 170, 120,
    tool="marker", color=(200, 50, 40),
    pressure=0.6, spacing=5, angle_deg=-30
))

# --- Arcs - spinning, chaotic motion ---
for i in range(10):
    cx = random.randint(50, 440)
    cy = random.randint(50, 450)
    r = random.randint(20, 70)
    start_angle = random.uniform(0, math.pi * 2)
    end_angle = start_angle + random.uniform(math.pi * 0.5, math.pi * 1.5)
    color = random.choice(ALL_WARM)
    tool = random.choice(["charcoal", "marker", "pen"])
    all_strokes.append(draw_arc(
        cx, cy, r, start_angle, end_angle,
        tool=tool, color=color, pressure=random.uniform(0.4, 0.8)
    ))

# --- Foreground slashes - pen and marker, dark, sharp ---
for i in range(12):
    x1 = random.randint(10, 470)
    y1 = random.randint(10, 490)
    angle = random.uniform(-math.pi, math.pi)
    length = random.randint(40, 120)
    x2 = x1 + math.cos(angle) * length
    y2 = y1 + math.sin(angle) * length
    x2 = max(5, min(485, x2))
    y2 = max(5, min(495, y2))
    color = random.choice(WARM_DARKS + [(220, 40, 30)])
    tool = random.choice(["pen", "marker"])
    all_strokes.append(draw_line(x1, y1, x2, y2,
                                  tool=tool, color=color, pressure=random.uniform(0.6, 0.9)))

# --- Small hot circles scattered - like sparks ---
for i in range(8):
    cx = random.randint(30, 460)
    cy = random.randint(30, 470)
    r = random.randint(3, 10)
    color = random.choice(WARM_YELLOWS + [(255, 255, 180)])
    all_strokes.extend(draw_filled_circle(cx, cy, r, tool="pen", color=color, pressure=0.7))

# --- More crosshatching overlays for visual density ---
all_strokes.extend(draw_crosshatching(
    100, 280, 150, 120,
    tool="charcoal", color=(200, 100, 20), pressure=0.5,
    spacing=5, angles=[20, -60]
))

# ============================================================
# PANEL 2: CALM / SERENITY (Right half, x: 510-1000)
# ============================================================

# --- Background: soft cool gradient fills ---
# Base - deep blue vertical wash (dark at top, lighter at bottom)
all_strokes.extend(draw_gradient_fill(
    520, 10, 470, 480,
    start_pressure=0.3, end_pressure=0.12,
    tool="brush", color=(30, 60, 110), spacing=7
))

# Second layer - blue-green mist
all_strokes.extend(draw_gradient_fill(
    530, 100, 440, 300,
    start_pressure=0.1, end_pressure=0.18,
    tool="pencil", color=(90, 180, 170), spacing=12
))

# Pale top wash - like dawn sky
all_strokes.extend(draw_gradient_fill(
    540, 20, 440, 180,
    start_pressure=0.15, end_pressure=0.05,
    tool="brush", color=(200, 215, 230), spacing=9
))

# --- Gentle horizontal flow lines - like still water or breath ---
for i in range(10):
    y = 80 + i * 38
    x_start = 530
    x_end = 970
    color = random.choice(COOL_BLUES + COOL_BLUE_GREENS)
    # Very gentle S-curves with low amplitude
    all_strokes.append(draw_s_curve(
        x_start, y, x_end, y + random.randint(-5, 5),
        amplitude=random.randint(5, 12), tool="brush",
        color=color, pressure=random.uniform(0.15, 0.3)
    ))

# --- Floating ellipses - like stones in a zen garden ---
ellipse_positions = [
    (620, 150, 35, 20), (780, 200, 40, 22), (700, 320, 30, 18),
    (870, 280, 45, 25), (650, 400, 28, 16), (830, 380, 32, 19),
    (920, 130, 25, 15), (750, 100, 20, 12),
]
for ex, ey, erx, ery in ellipse_positions:
    color = random.choice(COOL_PURPLES + COOL_BLUES)
    all_strokes.append(draw_ellipse(
        ex, ey, erx, ery,
        tool="pencil", color=color, pressure=random.uniform(0.2, 0.35)
    ))

# --- Soft concentric circles - meditation ripples ---
ripple_cx, ripple_cy = 760, 250
for r in range(15, 90, 12):
    alpha = max(0.1, 0.35 - r * 0.003)
    color = random.choice(COOL_BLUES + COOL_PALES)
    all_strokes.append(draw_circle(
        ripple_cx, ripple_cy, r,
        tool="brush", color=color, pressure=alpha
    ))

# --- Widely spaced hatching - soft texture like mist ---
all_strokes.extend(draw_hatching(
    540, 50, 210, 150,
    tool="pencil", color=(140, 135, 130),
    pressure=0.15, spacing=14, angle_deg=0
))
all_strokes.extend(draw_hatching(
    800, 300, 180, 170,
    tool="pencil", color=(160, 150, 145),
    pressure=0.12, spacing=16, angle_deg=10
))

# --- Gentle gradient fill patches - like fog ---
all_strokes.extend(draw_gradient_fill(
    600, 280, 180, 120,
    start_pressure=0.08, end_pressure=0.2,
    tool="brush", color=(100, 150, 200), spacing=10
))

# --- Soft curves flowing horizontally - like wisps ---
for i in range(6):
    y_center = 100 + i * 65
    points = []
    for j in range(6):
        px = 530 + j * 90
        py = y_center + random.randint(-8, 8)
        points.append((px, py))
    color = random.choice(COOL_PALES + COOL_BLUE_GREENS)
    all_strokes.append(draw_curve(
        points, tool="brush", color=color,
        pressure=random.uniform(0.12, 0.25)
    ))

# --- Small pale circles floating - like bubbles or stars ---
for i in range(10):
    cx = random.randint(540, 970)
    cy = random.randint(30, 470)
    r = random.randint(4, 12)
    color = random.choice(COOL_PALES + [(230, 240, 250)])
    all_strokes.extend(draw_filled_circle(cx, cy, r, tool="brush", color=color, pressure=0.2))

# --- A few pen accents - subtle structural lines ---
for i in range(4):
    x1 = random.randint(560, 900)
    y1 = random.randint(100, 400)
    x2 = x1 + random.randint(40, 100)
    y2 = y1 + random.randint(-10, 10)
    all_strokes.append(draw_line(
        x1, y1, x2, y2,
        tool="pen", color=(100, 80, 140), pressure=0.2
    ))

# --- Charcoal whisper marks in the calm panel (tool variety) ---
for i in range(3):
    x1 = random.randint(550, 950)
    y1 = random.randint(50, 450)
    x2 = x1 + random.randint(30, 80)
    y2 = y1 + random.randint(-15, 15)
    all_strokes.append(draw_line(
        x1, y1, x2, y2,
        tool="charcoal", color=(140, 135, 130), pressure=0.12
    ))

# --- Marker accent in calm panel (tool variety, very subtle) ---
all_strokes.append(draw_line(
    760, 440, 810, 442,
    tool="marker", color=(120, 100, 160), pressure=0.15
))

# --- Gentle arcs - like slow breath ---
for i in range(5):
    cx = random.randint(580, 920)
    cy = random.randint(80, 420)
    r = random.randint(25, 55)
    start = random.uniform(0, math.pi)
    end = start + random.uniform(math.pi * 0.3, math.pi * 0.7)
    color = random.choice(COOL_BLUES + COOL_PURPLES)
    all_strokes.append(draw_arc(
        cx, cy, r, start, end,
        tool="pencil", color=color, pressure=random.uniform(0.15, 0.25)
    ))

# --- Second ripple center, lower right ---
ripple2_cx, ripple2_cy = 890, 380
for r in range(10, 60, 10):
    color = random.choice(COOL_BLUE_GREENS + COOL_PALES)
    all_strokes.append(draw_circle(
        ripple2_cx, ripple2_cy, r,
        tool="pencil", color=color, pressure=max(0.1, 0.25 - r * 0.003)
    ))


# ============================================================
# TRANSITION ZONE (x: 485-515)
# ============================================================

# Warm side fading out - charcoal vertical lines losing pressure
for i in range(6):
    x = 475 + i * 4
    color_warm = random.choice(WARM_ORANGES + WARM_REDS)
    p = max(0.1, 0.5 - i * 0.07)
    all_strokes.append(draw_line(
        x, 20, x, 480,
        tool="charcoal", color=color_warm, pressure=p
    ))

# Cool side fading in - brush vertical lines gaining pressure
for i in range(6):
    x = 500 + i * 4
    color_cool = random.choice(COOL_BLUES + COOL_BLUE_GREENS)
    p = max(0.1, 0.1 + i * 0.06)
    all_strokes.append(draw_line(
        x, 20, x, 480,
        tool="brush", color=color_cool, pressure=p
    ))

# A decisive vertical line at the boundary - pen
all_strokes.append(draw_line(
    497, 5, 497, 495,
    tool="pen", color=(80, 50, 40), pressure=0.4
))

# A second softer line just right of center
all_strokes.append(draw_line(
    503, 5, 503, 495,
    tool="pencil", color=(100, 120, 160), pressure=0.25
))

# Intermingling curves that cross the boundary
# Warm curve reaching into cool
all_strokes.append(draw_s_curve(
    460, 200, 540, 210, amplitude=15,
    tool="charcoal", color=(200, 100, 20), pressure=0.35
))
# Cool curve reaching into warm
all_strokes.append(draw_s_curve(
    460, 300, 540, 295, amplitude=12,
    tool="brush", color=(70, 120, 180), pressure=0.25
))

# ============================================================
# RENDER
# ============================================================

drawing = Drawing(strokes=all_strokes, width=1000, height=500)
img = render_drawing(drawing, apply_paper=True)
output_path = os.path.join(os.path.dirname(__file__), "lesson_07.png")
img.convert("RGB").save(output_path)
print(f"Saved to {output_path}")
print(f"Total strokes: {len(all_strokes)}")
