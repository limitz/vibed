"""
Lesson 05: Landscape & Atmospheric Perspective
Scene: Golden hour sunset over a lake, with layered hills and a foreground oak tree.

Mood: Warm, contemplative late afternoon. The sun is low on the right,
casting amber light across the scene. Distant hills dissolve into blue-violet haze.
A still lake mirrors the sky. A large oak tree anchors the left foreground.
"""

import sys
import os
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'artist'))

from student import (
    draw_line, draw_circle, draw_curve, draw_pressure_ramp,
    draw_hatching, draw_filled_circle, draw_rectangle, draw_triangle,
    draw_s_curve, draw_arc, draw_ellipse, draw_crosshatching,
    draw_filled_rectangle, draw_gradient_fill,
)
from stylus_format import Drawing
from renderer import render_drawing

import numpy as np
np.random.seed(2026)

all_strokes = []

W, H = 1000, 600

# ===========================================================================
# Color palette -- golden hour sunset
# ===========================================================================
SKY_TOP = (70, 100, 160)        # deep blue at zenith
SKY_MID = (180, 140, 100)       # warm amber at mid-sky
SKY_HORIZON = (240, 190, 120)   # pale gold near horizon
SUN_COLOR = (255, 220, 140)     # warm sun
SUN_GLOW = (255, 200, 120)      # glow around sun

HILL_FAR = (160, 150, 190)      # pale blue-violet, most distant
HILL_MID = (130, 130, 160)      # blue-purple, middle distance
HILL_NEAR = (100, 115, 130)     # darker blue-gray

LAKE_BASE = (120, 140, 170)     # steel-blue water
LAKE_DARK = (80, 100, 130)      # darker ripple tones
LAKE_HIGHLIGHT = (200, 180, 150)  # warm reflected sky

FIELD_GREEN = (90, 120, 70)     # middle-ground green field
FIELD_DARK = (60, 90, 50)       # shadow in field

FG_EARTH = (100, 75, 50)        # warm brown foreground earth
FG_DARK = (60, 45, 30)          # dark earth shadow
FG_GRASS = (70, 100, 40)        # foreground grass green
FG_GRASS_DARK = (40, 65, 25)    # dark grass

TRUNK_BROWN = (55, 35, 20)      # dark oak trunk
CANOPY_GREEN = (50, 80, 35)     # dark foliage
CANOPY_LIGHT = (80, 110, 50)    # sunlit foliage highlights

ROCK_GRAY = (90, 85, 75)        # warm gray rocks
ROCK_SHADOW = (55, 50, 45)      # rock shadow

FLOWER_RED = (190, 60, 50)      # wildflower accents
FLOWER_YELLOW = (220, 190, 60)  # yellow wildflowers
FLOWER_WHITE = (230, 225, 210)  # white wildflowers

# ===========================================================================
# LAYER 1: SKY -- brush tool, gradient from deep blue top to golden horizon
# ===========================================================================

# Upper sky: deep blue
all_strokes.extend(draw_gradient_fill(
    0, 0, W, 120,
    start_pressure=0.5, end_pressure=0.35,
    tool="brush", color=SKY_TOP, spacing=2.5
))

# Mid sky: transition zone -- warmer
all_strokes.extend(draw_gradient_fill(
    0, 118, W, 80,
    start_pressure=0.35, end_pressure=0.3,
    tool="brush", color=SKY_MID, spacing=2.5
))

# Lower sky near horizon: warm gold
all_strokes.extend(draw_gradient_fill(
    0, 196, W, 70,
    start_pressure=0.3, end_pressure=0.4,
    tool="brush", color=SKY_HORIZON, spacing=2.5
))

# Sun -- a warm filled circle on the right side, low in the sky
all_strokes.extend(draw_filled_circle(
    780, 210, 28,
    tool="brush", color=SUN_COLOR, pressure=0.45, fill_spacing=2.0
))

# Sun glow -- larger, very light circle behind the sun
all_strokes.extend(draw_filled_circle(
    780, 210, 55,
    tool="brush", color=SUN_GLOW, pressure=0.12, fill_spacing=3.0
))

# A few soft cloud wisps in the upper sky using charcoal at low pressure
for cy, cx1, cx2, amp in [(80, 200, 400, 8), (60, 500, 700, 6), (100, 650, 850, 10)]:
    all_strokes.append(draw_s_curve(
        cx1, cy, cx2, cy, amplitude=amp,
        tool="charcoal", color=(200, 210, 230), pressure=0.12
    ))

# ===========================================================================
# LAYER 2: DISTANT HILLS -- charcoal and brush, cool pale colors
# ===========================================================================

# Farthest hill (Layer A) -- very pale blue-violet, gentle undulation
# Filled rectangle as base, then a curved top edge
all_strokes.extend(draw_filled_rectangle(
    0, 210, W, 50,
    tool="brush", color=HILL_FAR, pressure=0.18, fill_spacing=2.5
))
# Curved ridgeline
hill_far_pts = [(0, 225), (150, 212), (300, 218), (450, 208), (600, 215),
                (750, 205), (900, 218), (1000, 222)]
all_strokes.append(draw_curve(
    hill_far_pts, tool="charcoal", color=HILL_FAR, pressure=0.15
))

# Second distant hill (Layer B) -- slightly darker blue-purple
all_strokes.extend(draw_filled_rectangle(
    0, 230, W, 50,
    tool="brush", color=HILL_MID, pressure=0.22, fill_spacing=2.5
))
# Ridgeline with more variation
hill_mid_pts = [(0, 248), (120, 235), (250, 245), (380, 230), (500, 242),
                (620, 228), (750, 240), (880, 232), (1000, 245)]
all_strokes.append(draw_curve(
    hill_mid_pts, tool="charcoal", color=HILL_MID, pressure=0.2
))

# Subtle hatching on the nearer distant hill -- very light, wide spacing
all_strokes.extend(draw_hatching(
    0, 235, W, 40,
    angle_deg=10, spacing=14, tool="charcoal", color=HILL_MID, pressure=0.1
))

# Near distant hill -- darker, transitioning to middle ground
all_strokes.extend(draw_filled_rectangle(
    0, 260, W, 40,
    tool="brush", color=HILL_NEAR, pressure=0.25, fill_spacing=2.5
))
hill_near_pts = [(0, 272), (100, 265), (200, 275), (350, 260), (500, 270),
                 (650, 258), (800, 268), (950, 262), (1000, 270)]
all_strokes.append(draw_curve(
    hill_near_pts, tool="charcoal", color=HILL_NEAR, pressure=0.22
))

# Tiny distant trees on the middle hill -- small pale dots (atmospheric perspective demo)
for tx in [180, 210, 235, 400, 420, 625, 650, 670]:
    all_strokes.extend(draw_filled_circle(
        tx, 240 + np.random.randint(-5, 5), 4,
        tool="brush", color=(120, 135, 120), pressure=0.15, fill_spacing=2.0
    ))
    all_strokes.append(draw_line(
        tx, 244 + np.random.randint(-3, 3), tx, 250 + np.random.randint(-2, 2),
        tool="pencil", color=(120, 120, 110), pressure=0.12, num_events=6
    ))

# ===========================================================================
# LAYER 3: MIDDLE GROUND -- green field + lake
# ===========================================================================

# Green rolling field on the left and right sides
all_strokes.extend(draw_filled_rectangle(
    0, 290, 380, 90,
    tool="brush", color=FIELD_GREEN, pressure=0.3, fill_spacing=2.5
))
all_strokes.extend(draw_filled_rectangle(
    680, 290, 320, 90,
    tool="brush", color=FIELD_GREEN, pressure=0.3, fill_spacing=2.5
))

# Field texture -- gentle hatching with pencil
all_strokes.extend(draw_hatching(
    0, 295, 370, 80,
    angle_deg=15, spacing=10, tool="pencil", color=FIELD_DARK, pressure=0.2
))
all_strokes.extend(draw_hatching(
    690, 295, 310, 80,
    angle_deg=-10, spacing=10, tool="pencil", color=FIELD_DARK, pressure=0.2
))

# Rolling hill contours in the middle ground
mg_curve_pts = [(0, 295), (100, 290), (200, 300), (320, 285), (380, 295)]
all_strokes.append(draw_curve(
    mg_curve_pts, tool="pencil", color=FIELD_DARK, pressure=0.25
))
mg_curve_pts2 = [(680, 295), (750, 288), (850, 298), (950, 290), (1000, 295)]
all_strokes.append(draw_curve(
    mg_curve_pts2, tool="pencil", color=FIELD_DARK, pressure=0.25
))

# --- Lake in the center ---
# Lake base -- steel blue
all_strokes.extend(draw_filled_rectangle(
    350, 300, 360, 80,
    tool="brush", color=LAKE_BASE, pressure=0.3, fill_spacing=2.0
))

# Lake reflects the warm sky -- lighter warm strokes near center
all_strokes.extend(draw_gradient_fill(
    380, 310, 300, 30,
    start_pressure=0.12, end_pressure=0.08,
    tool="brush", color=LAKE_HIGHLIGHT, spacing=3.5
))

# Ripple texture -- horizontal lines at varying tones
for ry in range(305, 378, 6):
    ripple_color = LAKE_DARK if (ry // 6) % 2 == 0 else LAKE_BASE
    all_strokes.append(draw_line(
        355, ry, 705, ry,
        tool="pencil", color=ripple_color, pressure=0.15, num_events=20
    ))

# Lake shore curves
all_strokes.append(draw_curve(
    [(350, 300), (420, 295), (530, 298), (620, 294), (710, 300)],
    tool="pencil", color=(80, 95, 70), pressure=0.25
))
all_strokes.append(draw_curve(
    [(350, 380), (430, 383), (530, 378), (640, 385), (710, 380)],
    tool="pencil", color=(75, 85, 60), pressure=0.3
))

# A small wooden dock/pier extending into the lake from the right bank
# -- a creative detail to lead the eye into the scene
for plank_y in range(310, 355, 5):
    all_strokes.append(draw_line(
        690, plank_y, 715, plank_y,
        tool="pen", color=(90, 65, 40), pressure=0.35, num_events=8
    ))
# Dock posts
all_strokes.append(draw_line(695, 305, 695, 358, tool="pen", color=TRUNK_BROWN, pressure=0.4, num_events=10))
all_strokes.append(draw_line(710, 305, 710, 358, tool="pen", color=TRUNK_BROWN, pressure=0.4, num_events=10))

# ===========================================================================
# LAYER 4: FOREGROUND -- warm earth, detailed texture
# ===========================================================================

# Foreground earth base
all_strokes.extend(draw_filled_rectangle(
    0, 385, W, 215,
    tool="brush", color=FG_EARTH, pressure=0.45, fill_spacing=2.5
))

# Gradient -- darker at the very bottom (closer to viewer)
all_strokes.extend(draw_gradient_fill(
    0, 480, W, 120,
    start_pressure=0.2, end_pressure=0.45,
    tool="brush", color=FG_DARK, spacing=3.0
))

# Foreground grass -- green overlay on top of earth
all_strokes.extend(draw_filled_rectangle(
    0, 385, W, 60,
    tool="brush", color=FG_GRASS, pressure=0.35, fill_spacing=3.0
))

# Grass texture -- diagonal hatching with marker (bold foreground detail)
all_strokes.extend(draw_hatching(
    0, 388, W, 55,
    angle_deg=70, spacing=6, tool="marker", color=FG_GRASS_DARK, pressure=0.4
))

# Additional crosshatching on the ground for richness -- pencil
all_strokes.extend(draw_crosshatching(
    0, 440, W, 160,
    angles=[30, -45], spacing=7,
    tool="pencil", color=FG_DARK, pressure=0.3
))

# Individual grass tufts in the foreground -- short diagonal lines with pen
for gx in range(30, 980, 25):
    gy = 400 + np.random.randint(-5, 15)
    length = np.random.randint(8, 18)
    angle = np.random.randint(60, 100)
    rad = math.radians(angle)
    gx2 = gx + length * math.cos(rad)
    gy2 = gy - length * math.sin(rad)  # upward
    color = FG_GRASS if np.random.random() > 0.4 else FG_GRASS_DARK
    all_strokes.append(draw_line(
        gx, gy, gx2, gy2,
        tool="pen", color=color, pressure=0.45, num_events=6
    ))

# ===========================================================================
# LAYER 5: FOREGROUND OAK TREE (left side, large, detailed)
# ===========================================================================

# Trunk -- thick, drawn with marker for bold graphic presence
trunk_x = 150
trunk_top = 280
trunk_bot = 470

# Main trunk with marker
for offset in range(-8, 9, 3):
    all_strokes.append(draw_line(
        trunk_x + offset, trunk_top + 40, trunk_x + offset + 3, trunk_bot,
        tool="marker", color=TRUNK_BROWN, pressure=0.65, num_events=15
    ))

# Trunk bark texture -- crosshatching with pen
all_strokes.extend(draw_crosshatching(
    trunk_x - 8, trunk_top + 50, 20, 130,
    angles=[80, -80], spacing=5,
    tool="pen", color=(35, 22, 12), pressure=0.5
))

# Main branches -- pen for sharp detail
branches = [
    (trunk_x, trunk_top + 40, trunk_x - 70, trunk_top - 10, 0.5),
    (trunk_x, trunk_top + 30, trunk_x + 80, trunk_top - 20, 0.45),
    (trunk_x - 3, trunk_top + 60, trunk_x - 90, trunk_top + 20, 0.4),
    (trunk_x + 3, trunk_top + 55, trunk_x + 60, trunk_top + 10, 0.4),
    (trunk_x, trunk_top + 80, trunk_x - 50, trunk_top + 40, 0.35),
    (trunk_x + 2, trunk_top + 75, trunk_x + 70, trunk_top + 50, 0.35),
]
for bx1, by1, bx2, by2, bp in branches:
    all_strokes.append(draw_pressure_ramp(
        bx1, by1, bx2, by2,
        tool="pen", color=TRUNK_BROWN, num_events=20
    ))

# Canopy -- large irregular mass of foliage using charcoal filled circles
# Multiple overlapping circles to create organic shape
canopy_circles = [
    (trunk_x - 50, trunk_top - 10, 40),
    (trunk_x + 10, trunk_top - 25, 45),
    (trunk_x - 20, trunk_top + 10, 35),
    (trunk_x + 50, trunk_top - 5, 38),
    (trunk_x - 70, trunk_top + 15, 32),
    (trunk_x - 30, trunk_top - 35, 35),
    (trunk_x + 30, trunk_top - 40, 30),
    (trunk_x + 65, trunk_top + 20, 28),
    (trunk_x - 80, trunk_top + 30, 25),
]
for ccx, ccy, cr in canopy_circles:
    all_strokes.extend(draw_filled_circle(
        ccx, ccy, cr,
        tool="charcoal", color=CANOPY_GREEN, pressure=0.4, fill_spacing=2.5
    ))

# Canopy highlights -- sunlit side (right side, facing the sun)
highlight_circles = [
    (trunk_x + 30, trunk_top - 30, 22),
    (trunk_x + 55, trunk_top - 5, 20),
    (trunk_x + 15, trunk_top - 15, 18),
    (trunk_x + 45, trunk_top + 10, 15),
]
for hcx, hcy, hr in highlight_circles:
    all_strokes.extend(draw_filled_circle(
        hcx, hcy, hr,
        tool="charcoal", color=CANOPY_LIGHT, pressure=0.25, fill_spacing=3.0
    ))

# Canopy texture -- hatching to give depth
all_strokes.extend(draw_hatching(
    trunk_x - 85, trunk_top - 40, 170, 90,
    angle_deg=45, spacing=5, tool="charcoal", color=(35, 55, 25), pressure=0.35
))

# Tree shadow on the ground -- cast to the left (sun on the right)
all_strokes.extend(draw_filled_rectangle(
    trunk_x - 100, 420, 120, 30,
    tool="brush", color=(50, 40, 30), pressure=0.2, fill_spacing=3.0
))

# ===========================================================================
# LAYER 5b: FOREGROUND DETAILS -- rocks, wildflowers, a path
# ===========================================================================

# Rocks in the right foreground
rock_positions = [(750, 460, 18), (790, 475, 14), (830, 455, 20), (770, 490, 12)]
for rx, ry, rr in rock_positions:
    all_strokes.extend(draw_filled_circle(
        rx, ry, rr,
        tool="brush", color=ROCK_GRAY, pressure=0.45, fill_spacing=2.0
    ))
    # Shadow on the rock
    all_strokes.extend(draw_crosshatching(
        rx - rr, ry - rr // 2, rr * 2, rr,
        angles=[45, -30], spacing=4,
        tool="pen", color=ROCK_SHADOW, pressure=0.45
    ))

# A winding dirt path from middle ground to foreground
# -- draws the eye from the dock area toward the viewer
path_pts_left = [(680, 385), (650, 420), (620, 460), (600, 510), (590, 570), (585, 600)]
path_pts_right = [(720, 385), (700, 420), (680, 465), (670, 515), (665, 575), (665, 600)]
all_strokes.append(draw_curve(
    path_pts_left, tool="pencil", color=FG_DARK, pressure=0.35
))
all_strokes.append(draw_curve(
    path_pts_right, tool="pencil", color=FG_DARK, pressure=0.35
))
# Fill path with earth tone
all_strokes.extend(draw_filled_rectangle(
    610, 440, 60, 160,
    tool="brush", color=(115, 90, 65), pressure=0.3, fill_spacing=3.0
))

# Wildflowers scattered in the foreground grass
flower_data = [
    # (x, y, color)
    (280, 410, FLOWER_RED), (310, 418, FLOWER_YELLOW), (350, 405, FLOWER_WHITE),
    (380, 425, FLOWER_RED), (420, 412, FLOWER_YELLOW), (460, 420, FLOWER_WHITE),
    (500, 408, FLOWER_RED), (540, 430, FLOWER_YELLOW), (250, 422, FLOWER_WHITE),
    (320, 435, FLOWER_RED), (440, 432, FLOWER_YELLOW), (560, 415, FLOWER_RED),
    (270, 440, FLOWER_YELLOW), (490, 442, FLOWER_WHITE), (520, 438, FLOWER_RED),
]
for fx, fy, fc in flower_data:
    all_strokes.extend(draw_filled_circle(
        fx, fy, 3,
        tool="pen", color=fc, pressure=0.5, fill_spacing=1.5
    ))

# A few birds in the distant sky -- simple V shapes with pen
for bx, by in [(350, 100), (380, 85), (420, 95), (620, 70), (650, 80)]:
    all_strokes.append(draw_line(bx - 6, by + 3, bx, by, tool="pen", color=(60, 70, 90), pressure=0.2, num_events=5))
    all_strokes.append(draw_line(bx, by, bx + 6, by + 3, tool="pen", color=(60, 70, 90), pressure=0.2, num_events=5))

# A second smaller tree on the right middle ground (atmospheric perspective contrast)
# -- smaller, lighter, less detailed than the foreground oak
small_tree_x = 870
small_tree_top = 340
# Small trunk -- pencil, lighter
all_strokes.append(draw_line(
    small_tree_x, small_tree_top + 15, small_tree_x, small_tree_top + 50,
    tool="pencil", color=(85, 70, 55), pressure=0.3, num_events=10
))
# Small canopy -- one filled circle, charcoal, lighter color
all_strokes.extend(draw_filled_circle(
    small_tree_x, small_tree_top + 5, 18,
    tool="charcoal", color=(80, 105, 65), pressure=0.25, fill_spacing=2.5
))

# Another distant tree even further back
dt_x = 920
all_strokes.append(draw_line(
    dt_x, 305, dt_x, 318,
    tool="pencil", color=(110, 110, 100), pressure=0.18, num_events=6
))
all_strokes.extend(draw_filled_circle(
    dt_x, 300, 10,
    tool="brush", color=(110, 125, 105), pressure=0.15, fill_spacing=3.0
))

# ===========================================================================
# FINISHING TOUCHES
# ===========================================================================

# Soft edge along the bottom to ground the scene
all_strokes.append(draw_line(
    0, 598, W, 598,
    tool="marker", color=FG_DARK, pressure=0.6, num_events=25
))

# A subtle warm glow line at the horizon (where sky meets hills)
all_strokes.append(draw_line(
    0, 210, W, 210,
    tool="brush", color=(220, 180, 130), pressure=0.1, num_events=30
))

# ===========================================================================
# RENDER
# ===========================================================================

drawing = Drawing(strokes=all_strokes, width=W, height=H)
img = render_drawing(drawing, apply_paper=True)
output_path = os.path.join(os.path.dirname(__file__), "lesson_05.png")
img.convert("RGB").save(output_path)
print(f"Saved to {output_path}")
print(f"Total strokes: {len(all_strokes)}")

# Verify all 5 tools used
tools_used = set()
for s in all_strokes:
    for e in s.events:
        tools_used.add(e.tool)
print(f"Tools used: {sorted(tools_used)}")

# Count unique colors
colors_used = set()
for s in all_strokes:
    for e in s.events:
        colors_used.add(str(e.color))
print(f"Unique colors: {len(colors_used)}")
