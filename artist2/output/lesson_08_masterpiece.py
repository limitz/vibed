import sys
import os
import math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'artist'))

from student import *
from stylus_format import Drawing
from renderer import render_drawing

all_strokes = []

# ============================================================
# "The Dreamer's Horizon"
#
# A solitary figure stands on a warm foreground hill at twilight,
# gazing toward distant atmospheric mountains. From their head,
# abstract swirls of color and energy rise and dissolve into
# the sky -- imagination made visible, blurring the line between
# the inner world and the outer landscape.
#
# Composition plan (1200x800):
#   Sky:        y=0 to y=350   (gradient from deep indigo top to warm amber horizon)
#   Mountains:  y=250 to y=400 (3 layers, atmospheric perspective)
#   Lake:       y=380 to y=480 (still water with reflections)
#   Meadow:     y=450 to y=650 (rolling green hills)
#   Foreground: y=600 to y=800 (warm earth, wildflowers, texture)
#   Figure:     centered-right around x=750, standing on hill at y~580
#   Abstract:   emanating from figure's head upward and leftward into sky
# ============================================================

W, H = 1200, 800

# --- COLOR PALETTE (30+ colors) ---
# Sky
SKY_DEEP       = (20, 15, 55)
SKY_MID        = (45, 30, 90)
SKY_LOWER      = (80, 50, 120)
SKY_HORIZON    = (180, 120, 80)
SKY_AMBER      = (220, 160, 70)
SKY_GOLD       = (240, 200, 100)
STAR_WHITE     = (240, 235, 220)

# Mountains (atmospheric perspective: far=cool/light, near=warm/dark)
MTN_FAR        = (120, 110, 150)
MTN_MID        = (90, 80, 120)
MTN_NEAR       = (60, 55, 85)
MTN_FAR_SHADOW = (100, 90, 130)

# Lake
LAKE_DEEP      = (40, 50, 80)
LAKE_SURFACE   = (70, 80, 120)
LAKE_REFLECT   = (100, 90, 140)
LAKE_SHIMMER   = (150, 140, 180)

# Meadow
MEADOW_FAR     = (80, 120, 70)
MEADOW_MID     = (60, 100, 50)
MEADOW_NEAR    = (45, 85, 35)
MEADOW_DARK    = (30, 60, 25)
MEADOW_WARM    = (90, 110, 40)

# Foreground earth
EARTH_WARM     = (140, 100, 60)
EARTH_DARK     = (100, 70, 40)
EARTH_LIGHT    = (170, 130, 80)
EARTH_SHADOW   = (80, 55, 30)

# Figure
SKIN_BASE      = (200, 165, 130)
SKIN_SHADOW    = (165, 130, 100)
SKIN_DEEP      = (130, 100, 75)
HAIR_DARK      = (40, 30, 25)
HAIR_HIGHLIGHT = (70, 55, 45)
COAT_BLUE      = (50, 60, 100)
COAT_DARK      = (30, 35, 65)
COAT_LIGHT     = (70, 80, 130)
PANTS_GRAY     = (70, 65, 60)
BOOTS_BROWN    = (60, 40, 25)

# Abstract/imagination swirls
ABS_MAGENTA    = (180, 50, 120)
ABS_CYAN       = (50, 180, 200)
ABS_VIOLET     = (120, 50, 180)
ABS_ORANGE     = (230, 130, 40)
ABS_PINK       = (220, 120, 160)
ABS_TEAL       = (40, 160, 150)
ABS_YELLOW     = (240, 220, 80)
ABS_ROSE       = (200, 80, 100)
ABS_LIME       = (160, 220, 60)
ABS_LAVENDER   = (170, 140, 220)

# Flowers
FLOWER_RED     = (200, 50, 40)
FLOWER_YELLOW  = (240, 210, 50)
FLOWER_WHITE   = (230, 230, 220)
FLOWER_PURPLE  = (150, 60, 160)

# Tree
TRUNK_BROWN    = (70, 50, 30)
LEAF_GREEN     = (50, 90, 40)
LEAF_DARK      = (30, 60, 25)
LEAF_LIGHT     = (80, 130, 60)

# ============================================================
# LAYER 1: SKY (deep indigo top fading to amber horizon)
# ============================================================

# Deep sky gradient fills - layered for richness
all_strokes.extend(draw_gradient_fill(0, 0, W, 120, 0.6, 0.3, "brush", SKY_DEEP, spacing=3))
all_strokes.extend(draw_gradient_fill(0, 80, W, 120, 0.5, 0.25, "brush", SKY_MID, spacing=4))
all_strokes.extend(draw_gradient_fill(0, 160, W, 120, 0.4, 0.2, "brush", SKY_LOWER, spacing=4))
all_strokes.extend(draw_gradient_fill(0, 240, W, 100, 0.3, 0.15, "brush", SKY_HORIZON, spacing=5))
all_strokes.extend(draw_gradient_fill(0, 300, W, 80, 0.35, 0.15, "brush", SKY_AMBER, spacing=5))
all_strokes.extend(draw_gradient_fill(0, 340, W, 50, 0.3, 0.1, "brush", SKY_GOLD, spacing=6))

# Stars in the upper sky (tiny dots - deliberate artistic choice: stars that echo
# the abstract swirl colors below, connecting cosmos to imagination)
import random
random.seed(42)
for _ in range(25):
    sx = random.randint(20, 1180)
    sy = random.randint(10, 180)
    star_color = random.choice([STAR_WHITE, ABS_CYAN, ABS_LAVENDER, ABS_PINK])
    all_strokes.extend(draw_filled_circle(sx, sy, 1, "pen", star_color, pressure=0.5))

# Crescent moon (upper right) - pen for crisp edges
all_strokes.extend(draw_filled_circle(950, 80, 18, "pen", (220, 215, 200), pressure=0.4))
all_strokes.extend(draw_filled_circle(958, 74, 15, "pen", SKY_DEEP, pressure=0.6))

# ============================================================
# LAYER 2: DISTANT MOUNTAINS (3 layers, atmospheric perspective)
# ============================================================

# Farthest mountains - charcoal at low pressure for hazy quality
# Ridge line using curves
far_ridge_pts = [(0, 310), (100, 290), (200, 280), (350, 295),
                 (500, 270), (600, 285), (750, 260), (900, 275),
                 (1050, 290), (1200, 300)]
# Fill below the ridge with gradient
all_strokes.extend(draw_gradient_fill(0, 260, W, 100, 0.15, 0.08, "charcoal", MTN_FAR, spacing=5))
# Ridge outline
all_strokes.append(draw_curve(far_ridge_pts, "charcoal", MTN_FAR, pressure=0.2))

# Middle mountains - slightly darker/more detailed
mid_ridge_pts = [(0, 340), (150, 310), (300, 325), (450, 300),
                 (550, 315), (700, 295), (850, 320), (1000, 305),
                 (1100, 330), (1200, 340)]
all_strokes.extend(draw_gradient_fill(0, 295, W, 80, 0.2, 0.1, "charcoal", MTN_MID, spacing=5))
all_strokes.append(draw_curve(mid_ridge_pts, "charcoal", MTN_MID, pressure=0.25))
# Light shadow hatching on middle mountains
all_strokes.extend(draw_hatching(200, 310, 300, 40, spacing=12, angle_deg=60,
                                  tool="pencil", color=MTN_MID_SHADOW if False else MTN_FAR_SHADOW, pressure=0.15))

# Near mountains - darkest, most detailed, warmer
near_ridge_pts = [(0, 380), (100, 355), (200, 365), (350, 345),
                  (450, 360), (600, 340), (700, 355), (850, 350),
                  (950, 365), (1100, 355), (1200, 375)]
all_strokes.extend(draw_gradient_fill(0, 340, W, 70, 0.3, 0.15, "charcoal", MTN_NEAR, spacing=4))
all_strokes.append(draw_curve(near_ridge_pts, "pencil", MTN_NEAR, pressure=0.35))
# Crosshatching for shadow on near mountains
all_strokes.extend(draw_crosshatching(500, 345, 250, 35, spacing=10, angles=[45, -30],
                                       tool="pencil", color=MTN_NEAR, pressure=0.2))

# ============================================================
# LAYER 3: LAKE (still water, center middle ground)
# ============================================================

# Lake base fill
all_strokes.extend(draw_filled_rectangle(0, 375, W, 110, "brush", LAKE_DEEP, pressure=0.35))
# Surface color layer
all_strokes.extend(draw_gradient_fill(0, 375, W, 110, 0.15, 0.25, "brush", LAKE_SURFACE, spacing=5))

# Horizontal ripple lines across the lake
for ry in range(385, 480, 8):
    ripple_pressure = 0.08 + 0.1 * ((ry - 385) / 95)
    all_strokes.append(draw_line(20, ry, W - 20, ry, "pencil", LAKE_SHIMMER, pressure=ripple_pressure))

# Mountain reflections in water (inverted, faded)
for ry in range(390, 460, 12):
    rx_start = random.randint(100, 400)
    rx_end = rx_start + random.randint(100, 300)
    all_strokes.append(draw_line(rx_start, ry, rx_end, ry, "brush", LAKE_REFLECT, pressure=0.1))

# ============================================================
# LAYER 4: MEADOW / ROLLING HILLS
# ============================================================

# Far meadow (lighter green, less detail)
meadow_far_pts = [(0, 470), (150, 455), (300, 465), (500, 450),
                  (700, 460), (900, 448), (1100, 458), (1200, 465)]
all_strokes.extend(draw_gradient_fill(0, 445, W, 80, 0.25, 0.15, "brush", MEADOW_FAR, spacing=5))
all_strokes.append(draw_curve(meadow_far_pts, "pencil", MEADOW_FAR, pressure=0.25))

# Mid meadow
meadow_mid_pts = [(0, 530), (200, 510), (400, 520), (600, 505),
                  (800, 515), (1000, 500), (1200, 520)]
all_strokes.extend(draw_gradient_fill(0, 500, W, 80, 0.3, 0.15, "brush", MEADOW_MID, spacing=4))
all_strokes.append(draw_curve(meadow_mid_pts, "pencil", MEADOW_MID, pressure=0.3))
# Gentle hatching for grass texture
all_strokes.extend(draw_hatching(0, 510, 600, 50, spacing=10, angle_deg=80,
                                  tool="pencil", color=MEADOW_DARK, pressure=0.15))

# Near meadow hill where figure stands
meadow_near_pts = [(0, 600), (200, 580), (500, 570), (700, 560),
                   (900, 565), (1100, 575), (1200, 590)]
all_strokes.extend(draw_gradient_fill(0, 555, W, 80, 0.35, 0.2, "brush", MEADOW_NEAR, spacing=4))
all_strokes.append(draw_curve(meadow_near_pts, "pencil", MEADOW_NEAR, pressure=0.35))
# Grass hatching - marker for bold foreground texture
all_strokes.extend(draw_hatching(0, 560, 650, 50, spacing=7, angle_deg=85,
                                  tool="marker", color=MEADOW_DARK, pressure=0.25))
all_strokes.extend(draw_hatching(700, 555, 500, 55, spacing=8, angle_deg=75,
                                  tool="marker", color=MEADOW_DARK, pressure=0.2))

# ============================================================
# LAYER 5: FOREGROUND EARTH
# ============================================================

all_strokes.extend(draw_filled_rectangle(0, 620, W, 180, "brush", EARTH_WARM, pressure=0.35))
all_strokes.extend(draw_gradient_fill(0, 650, W, 150, 0.2, 0.4, "brush", EARTH_DARK, spacing=4))
# Foreground texture - crosshatching with charcoal for gritty earth
all_strokes.extend(draw_crosshatching(0, 660, 500, 140, spacing=8, angles=[30, -45],
                                       tool="charcoal", color=EARTH_SHADOW, pressure=0.25))
all_strokes.extend(draw_crosshatching(600, 670, 600, 130, spacing=9, angles=[40, -30],
                                       tool="charcoal", color=EARTH_SHADOW, pressure=0.2))
# Warm light patches on foreground earth
all_strokes.extend(draw_hatching(100, 640, 300, 60, spacing=10, angle_deg=0,
                                  tool="brush", color=EARTH_LIGHT, pressure=0.15))

# ============================================================
# LAYER 5b: TREE (left foreground, compositional anchor)
# ============================================================

# Tree trunk - marker for bold foreground presence
tree_x = 120
tree_base_y = 610
all_strokes.append(draw_line(tree_x, tree_base_y, tree_x - 5, tree_base_y - 160, "marker", TRUNK_BROWN, pressure=0.6))
all_strokes.append(draw_line(tree_x + 8, tree_base_y, tree_x + 3, tree_base_y - 160, "marker", TRUNK_BROWN, pressure=0.55))
# Trunk texture
all_strokes.extend(draw_hatching(tree_x - 5, tree_base_y - 150, 15, 140, spacing=6, angle_deg=5,
                                  tool="pen", color=TRUNK_BROWN, pressure=0.3))

# Branches
branches = [
    (tree_x - 2, tree_base_y - 140, tree_x - 60, tree_base_y - 200),
    (tree_x + 2, tree_base_y - 130, tree_x + 70, tree_base_y - 190),
    (tree_x - 3, tree_base_y - 110, tree_x - 45, tree_base_y - 170),
    (tree_x + 5, tree_base_y - 100, tree_x + 50, tree_base_y - 155),
    (tree_x, tree_base_y - 155, tree_x - 15, tree_base_y - 220),
    (tree_x, tree_base_y - 155, tree_x + 20, tree_base_y - 225),
]
for bx1, by1, bx2, by2 in branches:
    all_strokes.append(draw_line(bx1, by1, bx2, by2, "pen", TRUNK_BROWN, pressure=0.35))

# Canopy - overlapping filled circles for organic mass
canopy_centers = [
    (tree_x - 50, tree_base_y - 200, 30), (tree_x - 20, tree_base_y - 220, 35),
    (tree_x + 15, tree_base_y - 215, 32), (tree_x + 50, tree_base_y - 195, 28),
    (tree_x - 35, tree_base_y - 175, 25), (tree_x + 35, tree_base_y - 170, 22),
    (tree_x, tree_base_y - 235, 28), (tree_x - 10, tree_base_y - 190, 30),
    (tree_x + 25, tree_base_y - 210, 26),
]
for cx, cy, r in canopy_centers:
    all_strokes.extend(draw_filled_circle(cx, cy, r, "charcoal", LEAF_DARK, pressure=0.3))
for cx, cy, r in canopy_centers:
    all_strokes.extend(draw_filled_circle(cx - 3, cy - 3, r - 5, "brush", LEAF_GREEN, pressure=0.2))
# Leaf highlights
for cx, cy, r in canopy_centers[::2]:
    all_strokes.extend(draw_filled_circle(cx - 5, cy - 5, r // 3, "pencil", LEAF_LIGHT, pressure=0.15))

# Tree shadow on ground
all_strokes.extend(draw_hatching(tree_x - 10, tree_base_y + 5, 80, 25, spacing=5, angle_deg=0,
                                  tool="charcoal", color=EARTH_SHADOW, pressure=0.2))

# ============================================================
# LAYER 5c: PATH leading from foreground toward figure
# ============================================================

# A winding dirt path (leading line to guide eye to figure)
path_pts = [(200, 790), (250, 750), (320, 700), (420, 660),
            (530, 630), (640, 600), (720, 580)]
all_strokes.append(draw_curve(path_pts, "pencil", EARTH_LIGHT, pressure=0.3))
# Path edge
path_pts_r = [(220, 790), (270, 745), (345, 695), (445, 655),
              (555, 625), (660, 598), (735, 577)]
all_strokes.append(draw_curve(path_pts_r, "pencil", EARTH_DARK, pressure=0.25))

# ============================================================
# LAYER 5d: WILDFLOWERS scattered in meadow
# ============================================================

flower_positions = [
    (300, 590, FLOWER_RED), (350, 585, FLOWER_YELLOW), (420, 575, FLOWER_WHITE),
    (500, 570, FLOWER_PURPLE), (550, 580, FLOWER_RED), (620, 565, FLOWER_YELLOW),
    (680, 568, FLOWER_WHITE), (200, 600, FLOWER_PURPLE), (260, 595, FLOWER_YELLOW),
    (830, 570, FLOWER_RED), (880, 575, FLOWER_WHITE), (950, 580, FLOWER_YELLOW),
    (160, 620, FLOWER_RED), (380, 610, FLOWER_PURPLE), (580, 605, FLOWER_YELLOW),
    (1050, 578, FLOWER_WHITE), (1100, 585, FLOWER_RED),
]
for fx, fy, fc in flower_positions:
    all_strokes.extend(draw_filled_circle(fx, fy, 3, "pen", fc, pressure=0.4))
    # Tiny stem
    all_strokes.append(draw_line(fx, fy + 3, fx, fy + 10, "pen", MEADOW_DARK, pressure=0.2))

# ============================================================
# LAYER 5e: ROCKS in foreground
# ============================================================

# A few rocks near the path
rocks = [(450, 650, 15, 10), (500, 665, 12, 8), (180, 680, 18, 12)]
for rx, ry, rw, rh in rocks:
    all_strokes.extend(draw_filled_circle(rx, ry, rw, "brush", (120, 110, 100), pressure=0.3))
    # Rock shadow/shading
    all_strokes.extend(draw_hatching(rx - rw//2, ry, rw, rh, spacing=4, angle_deg=45,
                                      tool="pen", color=(80, 70, 60), pressure=0.25))
    # Cast shadow
    all_strokes.extend(draw_hatching(rx + 5, ry + rh, rw + 5, 6, spacing=4, angle_deg=0,
                                      tool="charcoal", color=EARTH_SHADOW, pressure=0.15))

# ============================================================
# LAYER 6: THE FIGURE (standing on hill, gazing at horizon)
# ============================================================

fig_x = 750  # center x of figure
fig_base = 558  # feet position (on the near meadow hill)

# --- Body (coat/torso) ---
# The figure is seen from slightly behind/side, looking left toward the horizon
# Coat body - filled rectangle for torso, slightly angled
coat_top = fig_base - 85
coat_bottom = fig_base - 25
all_strokes.extend(draw_filled_rectangle(fig_x - 18, coat_top, 36, 60, "brush", COAT_BLUE, pressure=0.4))
# Coat shading (right side darker - light from left/horizon)
all_strokes.extend(draw_hatching(fig_x + 2, coat_top, 16, 60, spacing=5, angle_deg=90,
                                  tool="pencil", color=COAT_DARK, pressure=0.25))
# Coat highlight (left side catches horizon light)
all_strokes.extend(draw_hatching(fig_x - 16, coat_top + 10, 12, 40, spacing=7, angle_deg=90,
                                  tool="pencil", color=COAT_LIGHT, pressure=0.15))

# Coat outline
all_strokes.append(draw_line(fig_x - 18, coat_top, fig_x - 18, coat_bottom, "pen", COAT_DARK, pressure=0.4))
all_strokes.append(draw_line(fig_x + 18, coat_top, fig_x + 18, coat_bottom, "pen", COAT_DARK, pressure=0.4))
all_strokes.append(draw_line(fig_x - 18, coat_top, fig_x + 18, coat_top, "pen", COAT_DARK, pressure=0.35))

# --- Legs ---
all_strokes.append(draw_line(fig_x - 8, coat_bottom, fig_x - 10, fig_base, "pen", PANTS_GRAY, pressure=0.4))
all_strokes.append(draw_line(fig_x + 8, coat_bottom, fig_x + 6, fig_base, "pen", PANTS_GRAY, pressure=0.4))
# Fill legs
all_strokes.extend(draw_filled_rectangle(fig_x - 12, coat_bottom, 10, 25, "brush", PANTS_GRAY, pressure=0.35))
all_strokes.extend(draw_filled_rectangle(fig_x + 2, coat_bottom, 10, 25, "brush", PANTS_GRAY, pressure=0.35))

# --- Boots ---
all_strokes.extend(draw_filled_rectangle(fig_x - 14, fig_base - 5, 12, 7, "marker", BOOTS_BROWN, pressure=0.45))
all_strokes.extend(draw_filled_rectangle(fig_x + 1, fig_base - 5, 12, 7, "marker", BOOTS_BROWN, pressure=0.45))

# --- Neck ---
all_strokes.append(draw_line(fig_x - 3, coat_top, fig_x - 3, coat_top - 12, "pen", SKIN_BASE, pressure=0.35))
all_strokes.append(draw_line(fig_x + 3, coat_top, fig_x + 3, coat_top - 12, "pen", SKIN_BASE, pressure=0.35))

# --- Head (slightly turned left, looking toward horizon) ---
head_cx = fig_x - 2  # slightly left-shifted to suggest looking left
head_cy = coat_top - 28
head_rx = 14
head_ry = 17

# Head fill
all_strokes.extend(draw_filled_circle(head_cx, head_cy, head_ry, "brush", SKIN_BASE, pressure=0.35))
# Head outline
all_strokes.append(draw_ellipse(head_cx, head_cy, head_rx, head_ry, "pen", SKIN_BASE, pressure=0.35))

# Face shading (right side shadow)
all_strokes.extend(draw_hatching(head_cx + 2, head_cy - 10, 12, 22, spacing=4, angle_deg=80,
                                  tool="pencil", color=SKIN_SHADOW, pressure=0.2))
# Deeper shadow near jaw
all_strokes.extend(draw_hatching(head_cx + 5, head_cy + 3, 8, 12, spacing=3, angle_deg=70,
                                  tool="pencil", color=SKIN_DEEP, pressure=0.2))

# --- Facial features (small, figure is not huge) ---
# Eye (just the left eye visible from this angle - simple but expressive)
eye_x = head_cx - 5
eye_y = head_cy - 2
all_strokes.append(draw_ellipse(eye_x, eye_y, 3, 2, "pen", (60, 50, 40), pressure=0.4))
# Iris
all_strokes.extend(draw_filled_circle(eye_x - 1, eye_y, 1.5, "pen", (80, 100, 60), pressure=0.5))
# Highlight
all_strokes.extend(draw_filled_circle(eye_x - 1, eye_y - 1, 0.8, "pen", STAR_WHITE, pressure=0.5))

# Second eye (partially visible, further away)
eye2_x = head_cx - 12
eye2_y = head_cy - 1
all_strokes.append(draw_arc(eye2_x, eye2_y, 2, 0, math.pi, "pen", (60, 50, 40), pressure=0.3))

# Nose (understated - small line and tip)
all_strokes.append(draw_line(head_cx - 8, head_cy - 1, head_cx - 10, head_cy + 4, "pen", SKIN_SHADOW, pressure=0.25))
all_strokes.append(draw_arc(head_cx - 9, head_cy + 5, 2, math.pi * 0.8, math.pi * 1.5, "pen", SKIN_SHADOW, pressure=0.2))

# Mouth (slight contemplative/wistful expression - gently parted)
all_strokes.append(draw_line(head_cx - 8, head_cy + 8, head_cx - 2, head_cy + 7, "pen", (160, 100, 90), pressure=0.3))
# Very slight upward curve at the left - not quite a smile, but hopeful
all_strokes.append(draw_arc(head_cx - 9, head_cy + 7, 3, math.pi * 1.2, math.pi * 1.8, "pen", (160, 100, 90), pressure=0.2))

# Eyebrow (calm, slightly raised - wonder/contemplation)
all_strokes.append(draw_line(eye_x - 4, eye_y - 5, eye_x + 4, eye_y - 6, "pencil", HAIR_DARK, pressure=0.3))

# Cheek blush
all_strokes.extend(draw_hatching(head_cx - 8, head_cy + 1, 6, 5, spacing=3, angle_deg=30,
                                  tool="brush", color=(210, 160, 140), pressure=0.1))

# --- Hair (wind-blown, flowing to the right - connects to abstract swirls) ---
# Hair mass
all_strokes.extend(draw_filled_circle(head_cx + 2, head_cy - 8, 14, "charcoal", HAIR_DARK, pressure=0.35))
all_strokes.extend(draw_filled_circle(head_cx + 8, head_cy - 5, 10, "charcoal", HAIR_DARK, pressure=0.3))

# Wind-blown hair strands that will transition into abstract swirls
# This is the KEY TRANSITION POINT - hair becomes abstract art
hair_strand_starts = [
    (head_cx + 12, head_cy - 12),
    (head_cx + 14, head_cy - 8),
    (head_cx + 15, head_cy - 4),
    (head_cx + 10, head_cy - 15),
]
# These strands get progressively more abstract
for i, (hx, hy) in enumerate(hair_strand_starts):
    # Start as hair-colored pencil strands
    end_x = hx + 30 + i * 15
    end_y = hy - 10 - i * 8
    all_strokes.append(draw_s_curve(hx, hy, end_x, end_y, amplitude=8 + i * 4,
                                     tool="pencil", color=HAIR_DARK, pressure=0.25 - i * 0.03))

# --- Arms (one slightly extended, reaching toward horizon) ---
# Left arm extended forward
all_strokes.append(draw_line(fig_x - 18, coat_top + 10, fig_x - 35, coat_top + 5,
                              "pen", COAT_BLUE, pressure=0.35))
all_strokes.append(draw_line(fig_x - 35, coat_top + 5, fig_x - 45, coat_top - 2,
                              "pen", COAT_BLUE, pressure=0.3))
# Hand
all_strokes.extend(draw_filled_circle(fig_x - 46, coat_top - 3, 4, "brush", SKIN_BASE, pressure=0.3))

# Right arm at side
all_strokes.append(draw_line(fig_x + 18, coat_top + 10, fig_x + 22, coat_top + 40,
                              "pen", COAT_BLUE, pressure=0.35))

# Figure shadow on ground
all_strokes.extend(draw_hatching(fig_x - 20, fig_base + 2, 55, 12, spacing=4, angle_deg=10,
                                  tool="charcoal", color=MEADOW_DARK, pressure=0.2))

# ============================================================
# LAYER 7: ABSTRACT EXPRESSIVE ELEMENTS
# Emanating from the figure's head/imagination, swirling upward
# into the sky. The abstract marks start as semi-representational
# (hair-like, wind-like) and become pure abstract expression
# as they rise, representing thoughts/dreams dissolving into sky.
# ============================================================

# --- Phase 1: Semi-abstract swirls near the figure (hair-to-imagination transition) ---
swirl_origin_x = head_cx + 15
swirl_origin_y = head_cy - 15

# S-curves radiating upward and outward from the figure's head
abstract_curves = [
    # (start_x, start_y, end_x, end_y, amplitude, tool, color, pressure)
    (swirl_origin_x, swirl_origin_y, swirl_origin_x - 80, swirl_origin_y - 100, 25, "pencil", ABS_VIOLET, 0.25),
    (swirl_origin_x, swirl_origin_y, swirl_origin_x - 40, swirl_origin_y - 130, 30, "brush", ABS_MAGENTA, 0.2),
    (swirl_origin_x, swirl_origin_y, swirl_origin_x + 50, swirl_origin_y - 120, 20, "brush", ABS_CYAN, 0.2),
    (swirl_origin_x, swirl_origin_y, swirl_origin_x - 120, swirl_origin_y - 80, 35, "charcoal", ABS_PINK, 0.18),
    (swirl_origin_x, swirl_origin_y, swirl_origin_x + 100, swirl_origin_y - 90, 28, "pencil", ABS_TEAL, 0.2),
    (swirl_origin_x, swirl_origin_y - 30, swirl_origin_x - 150, swirl_origin_y - 150, 40, "brush", ABS_ORANGE, 0.15),
    (swirl_origin_x, swirl_origin_y - 20, swirl_origin_x + 80, swirl_origin_y - 170, 22, "charcoal", ABS_LAVENDER, 0.18),
]
for sx1, sy1, sx2, sy2, amp, tool, color, press in abstract_curves:
    all_strokes.append(draw_s_curve(sx1, sy1, sx2, sy2, amplitude=amp, tool=tool, color=color, pressure=press))

# --- Phase 2: Abstract energy dispersing across the sky ---
# Pressure ramps radiating outward (like thoughts shooting into the cosmos)
ramp_targets = [
    (650, 120, ABS_VIOLET), (700, 80, ABS_MAGENTA), (600, 150, ABS_CYAN),
    (800, 100, ABS_PINK), (550, 180, ABS_TEAL), (750, 50, ABS_ORANGE),
    (500, 100, ABS_LAVENDER), (850, 140, ABS_ROSE), (450, 200, ABS_YELLOW),
    (900, 80, ABS_VIOLET), (400, 150, ABS_LIME), (680, 40, ABS_CYAN),
    (520, 60, ABS_MAGENTA), (780, 170, ABS_TEAL), (620, 200, ABS_PINK),
]
for tx, ty, tc in ramp_targets:
    all_strokes.append(draw_pressure_ramp(swirl_origin_x, swirl_origin_y - 50, tx, ty,
                                           tool="brush", color=tc))

# --- Phase 3: Abstract circles/ellipses floating in the sky (dream bubbles) ---
dream_bubbles = [
    (580, 130, 20, 15, ABS_VIOLET, "brush", 0.12),
    (700, 90, 25, 18, ABS_CYAN, "brush", 0.1),
    (500, 180, 15, 12, ABS_MAGENTA, "pencil", 0.15),
    (820, 120, 18, 22, ABS_PINK, "brush", 0.1),
    (450, 140, 12, 10, ABS_TEAL, "pencil", 0.12),
    (750, 60, 22, 16, ABS_ORANGE, "brush", 0.08),
    (600, 200, 16, 14, ABS_LAVENDER, "pencil", 0.12),
    (680, 160, 10, 8, ABS_ROSE, "pencil", 0.15),
]
for bx, by, brx, bry, bc, bt, bp in dream_bubbles:
    all_strokes.append(draw_ellipse(bx, by, brx, bry, bt, bc, pressure=bp))
    # Faint fill inside some bubbles
    all_strokes.extend(draw_filled_circle(bx, by, min(brx, bry) - 3, bt, bc, pressure=bp * 0.5))

# --- Phase 4: Dense abstract mark-making zone (upper-right quadrant) ---
# This is where imagination fully dissolves into pure abstract expression
# Crosshatching in various abstract colors
all_strokes.extend(draw_crosshatching(550, 30, 250, 150, spacing=12, angles=[30, -60],
                                       tool="charcoal", color=ABS_VIOLET, pressure=0.12))
all_strokes.extend(draw_crosshatching(650, 60, 200, 120, spacing=14, angles=[45, -20],
                                       tool="pencil", color=ABS_CYAN, pressure=0.1))
all_strokes.extend(draw_crosshatching(500, 80, 180, 100, spacing=16, angles=[60, -45],
                                       tool="brush", color=ABS_MAGENTA, pressure=0.08))

# Scattered triangles (sharp, energetic marks in the abstract zone)
triangles_abstract = [
    (620, 100, 640, 130, 610, 125, ABS_ORANGE, "pen"),
    (720, 70, 745, 95, 710, 100, ABS_YELLOW, "pen"),
    (560, 160, 585, 180, 550, 185, ABS_ROSE, "pen"),
    (800, 110, 815, 135, 790, 130, ABS_LIME, "pen"),
    (480, 120, 500, 145, 470, 140, ABS_TEAL, "pen"),
]
for tx1, ty1, tx2, ty2, tx3, ty3, tc, tt in triangles_abstract:
    all_strokes.append(draw_triangle(tx1, ty1, tx2, ty2, tx3, ty3, tt, tc, pressure=0.3))

# Abstract arcs (flowing, organic shapes)
abstract_arcs = [
    (650, 120, 40, 0, math.pi * 0.8, ABS_VIOLET, "brush", 0.15),
    (550, 180, 35, math.pi * 0.5, math.pi * 1.5, ABS_CYAN, "charcoal", 0.12),
    (780, 90, 30, math.pi, math.pi * 2, ABS_MAGENTA, "pencil", 0.18),
    (700, 150, 45, math.pi * 0.3, math.pi * 1.2, ABS_ORANGE, "brush", 0.1),
    (500, 100, 50, math.pi * 1.5, math.pi * 2.5, ABS_PINK, "charcoal", 0.1),
    (620, 60, 35, 0, math.pi * 0.7, ABS_TEAL, "brush", 0.12),
]
for acx, acy, ar, a1, a2, ac, at, ap in abstract_arcs:
    all_strokes.append(draw_arc(acx, acy, ar, a1, a2, at, ac, pressure=ap))

# --- Phase 5: Abstract marks that OVERLAP the landscape below ---
# (ensuring compositional unity - abstract elements interact with representational)
# Faint colored S-curves drifting down from the abstract zone into the mountains
overlay_curves = [
    (500, 200, 350, 320, 30, "brush", ABS_LAVENDER, 0.08),
    (600, 180, 450, 350, 25, "brush", ABS_VIOLET, 0.06),
    (700, 150, 550, 300, 35, "brush", ABS_CYAN, 0.07),
    (800, 130, 650, 280, 20, "brush", ABS_PINK, 0.06),
    (750, 200, 900, 350, 28, "brush", ABS_TEAL, 0.05),
]
for ox1, oy1, ox2, oy2, oamp, ot, oc, op in overlay_curves:
    all_strokes.append(draw_s_curve(ox1, oy1, ox2, oy2, amplitude=oamp, tool=ot, color=oc, pressure=op))

# Abstract dots scattered across the sky-landscape boundary (like dream particles)
for _ in range(30):
    dx = random.randint(350, 900)
    dy = random.randint(50, 350)
    dc = random.choice([ABS_VIOLET, ABS_CYAN, ABS_MAGENTA, ABS_PINK, ABS_TEAL,
                        ABS_ORANGE, ABS_YELLOW, ABS_LAVENDER, ABS_ROSE, ABS_LIME])
    dr = random.uniform(1, 4)
    all_strokes.extend(draw_filled_circle(dx, dy, dr, "pen", dc, pressure=0.3))

# ============================================================
# LAYER 8: FINAL DETAILS AND ATMOSPHERIC TOUCHES
# ============================================================

# Distant birds (V-shapes near mountains)
bird_positions = [(300, 280), (330, 275), (370, 285), (900, 260), (930, 255)]
for bx, by in bird_positions:
    all_strokes.append(draw_line(bx - 5, by, bx, by - 3, "pen", MTN_NEAR, pressure=0.2))
    all_strokes.append(draw_line(bx, by - 3, bx + 5, by, "pen", MTN_NEAR, pressure=0.2))

# Mist/fog wisps over the lake (charcoal at very low pressure)
for my in range(390, 470, 20):
    mx_start = random.randint(200, 600)
    mx_end = mx_start + random.randint(100, 300)
    all_strokes.append(draw_s_curve(mx_start, my, mx_end, my + 3, amplitude=5,
                                     tool="charcoal", color=LAKE_SHIMMER, pressure=0.06))

# Subtle light rays from the horizon (deliberate artistic choice:
# diagonal light beams connecting the sky to the ground, symbolizing
# the connection between the dreamer's inner world and outer reality)
for angle_offset in range(-3, 4):
    ray_x_top = 600 + angle_offset * 60
    ray_x_bottom = 600 + angle_offset * 40
    all_strokes.append(draw_line(ray_x_top, 250, ray_x_bottom, 380,
                                  "brush", SKY_GOLD, pressure=0.04))

# Ground-level glow near figure's feet (warm light pooling)
all_strokes.extend(draw_gradient_fill(fig_x - 50, fig_base - 10, 100, 20,
                                       0.08, 0.02, "brush", SKY_AMBER, spacing=8))

# ============================================================
# DELIBERATE ARTISTIC CHOICE: "Constellation of memories"
# Tiny connected dots in the upper sky forming an abstract
# constellation pattern unique to this figure's imagination.
# Not a real constellation - a personal one. Points connected
# by faint pencil lines, with each star a different abstract color.
# This represents the dreamer's personal mythology projected
# onto the night sky.
# ============================================================

constellation_points = [
    (350, 50, ABS_CYAN), (380, 80, ABS_VIOLET), (420, 45, ABS_MAGENTA),
    (410, 100, ABS_PINK), (460, 70, ABS_TEAL), (440, 120, ABS_LAVENDER),
    (490, 55, ABS_ORANGE),
]
# Draw stars
for cpx, cpy, cpc in constellation_points:
    all_strokes.extend(draw_filled_circle(cpx, cpy, 2.5, "pen", cpc, pressure=0.6))
# Connect them with faint lines
for i in range(len(constellation_points) - 1):
    x1, y1, _ = constellation_points[i]
    x2, y2, _ = constellation_points[i + 1]
    all_strokes.append(draw_line(x1, y1, x2, y2, "pencil", (150, 145, 170), pressure=0.1))
# Close the constellation loop
x1, y1, _ = constellation_points[-1]
x2, y2, _ = constellation_points[0]
all_strokes.append(draw_line(x1, y1, x2, y2, "pencil", (150, 145, 170), pressure=0.08))

# A second smaller constellation near the first
constellation2 = [
    (200, 60, ABS_YELLOW), (230, 40, ABS_ROSE), (260, 75, ABS_LIME),
    (240, 100, ABS_CYAN),
]
for cpx, cpy, cpc in constellation2:
    all_strokes.extend(draw_filled_circle(cpx, cpy, 2, "pen", cpc, pressure=0.5))
for i in range(len(constellation2) - 1):
    x1, y1, _ = constellation2[i]
    x2, y2, _ = constellation2[i + 1]
    all_strokes.append(draw_line(x1, y1, x2, y2, "pencil", (140, 135, 160), pressure=0.08))
x1, y1, _ = constellation2[-1]
x2, y2, _ = constellation2[0]
all_strokes.append(draw_line(x1, y1, x2, y2, "pencil", (140, 135, 160), pressure=0.08))

# ============================================================
# RENDER
# ============================================================

title = "The Dreamer's Horizon"

drawing = Drawing(strokes=all_strokes, width=1200, height=800)
img = render_drawing(drawing, apply_paper=True)
output_path = os.path.join(os.path.dirname(__file__), "lesson_08_masterpiece.png")
img.convert("RGB").save(output_path)
print(f"Title: {title}")
print(f"Saved to {output_path}")
print(f"Total strokes: {len(all_strokes)}")

# Print tool usage summary
tool_counts = {}
for s in all_strokes:
    if s.events:
        t = s.events[0].tool
        tool_counts[t] = tool_counts.get(t, 0) + 1
print(f"Tool breakdown: {tool_counts}")

# Print unique color count
unique_colors = set()
for s in all_strokes:
    for e in s.events:
        unique_colors.add(e.resolved_color())
print(f"Unique colors: {len(unique_colors)}")
