"""Lesson 6: Portrait & Expression - Three portrait studies with different expressions."""
import sys
import os
import math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'artist'))

from student import *
from stylus_format import Drawing
from renderer import render_drawing

all_strokes = []

# ============================================================
# Background - subtle warm paper tone with dividers
# ============================================================

# Subtle background wash
all_strokes.extend(draw_filled_rectangle(0, 0, 900, 700, tool="brush",
                                          color=(245, 235, 220), pressure=0.15, fill_spacing=2.0))

# Dividing lines between portraits
all_strokes.append(draw_line(300, 30, 300, 670, tool="pencil", color=(200, 185, 165), pressure=0.2))
all_strokes.append(draw_line(600, 30, 600, 670, tool="pencil", color=(200, 185, 165), pressure=0.2))

# ============================================================
# Color palette
# ============================================================
SKIN_BASE = (225, 190, 155)
SKIN_SHADOW = (195, 155, 120)
SKIN_DEEP_SHADOW = (165, 125, 95)
HAIR_BROWN = (80, 55, 35)
HAIR_BROWN_LIGHT = (120, 85, 55)
HAIR_RED = (160, 55, 30)
HAIR_RED_LIGHT = (200, 90, 50)
HAIR_BLACK = (40, 35, 30)
HAIR_BLACK_HIGHLIGHT = (75, 65, 55)
LIP_COLOR = (185, 95, 85)
LIP_DARK = (150, 70, 65)
EYE_BROWN = (85, 55, 30)
EYE_BLUE = (60, 100, 150)
EYE_GREEN = (55, 110, 70)
WHITE = (255, 255, 255)
EYEBROW_DARK = (65, 45, 30)
BLUSH = (215, 155, 140)
NOSE_COLOR = (185, 145, 115)


def draw_portrait(cx, cy, expression, hair_style, eye_color, hair_color, hair_highlight):
    """Draw a single portrait centered at (cx, cy).

    expression: 'happy', 'sad', 'contemplative'
    hair_style: 'wavy', 'straight_long', 'curly_short'
    """
    strokes = []

    # Head dimensions
    head_rx = 70   # horizontal radius
    head_ry = 95   # vertical radius

    # Key landmark positions
    eye_y = cy - 5          # eyes at vertical midpoint (slightly above center)
    nose_y = cy + 42        # nose halfway between eyes and chin
    mouth_y = cy + 62       # mouth 1/3 from nose to chin
    chin_y = cy + head_ry
    forehead_y = cy - head_ry

    # === NECK AND SHOULDERS (back layer) ===
    neck_w = 22
    shoulder_y = chin_y + 45
    # Neck
    strokes.append(draw_line(cx - neck_w, chin_y - 5, cx - neck_w, shoulder_y,
                             tool="pencil", color=SKIN_SHADOW, pressure=0.3))
    strokes.append(draw_line(cx + neck_w, chin_y - 5, cx + neck_w, shoulder_y,
                             tool="pencil", color=SKIN_SHADOW, pressure=0.3))
    # Neck fill
    strokes.extend(draw_filled_rectangle(cx - neck_w, chin_y - 5, neck_w * 2, 50,
                                          tool="brush", color=SKIN_BASE, pressure=0.3, fill_spacing=2.0))
    # Neck shadow
    strokes.extend(draw_hatching(cx - neck_w, chin_y - 2, neck_w * 2, 15,
                                  angle_deg=0, spacing=5, tool="pencil",
                                  color=SKIN_DEEP_SHADOW, pressure=0.25))
    # Shoulders
    strokes.append(draw_curve([(cx - neck_w, shoulder_y), (cx - 55, shoulder_y + 10),
                                (cx - 90, shoulder_y + 30)],
                               tool="pencil", color=SKIN_SHADOW, pressure=0.35))
    strokes.append(draw_curve([(cx + neck_w, shoulder_y), (cx + 55, shoulder_y + 10),
                                (cx + 90, shoulder_y + 30)],
                               tool="pencil", color=SKIN_SHADOW, pressure=0.35))
    # Shoulder fill hint
    strokes.append(draw_curve([(cx - 85, shoulder_y + 28), (cx - 50, shoulder_y + 18),
                                (cx, shoulder_y + 5), (cx + 50, shoulder_y + 18),
                                (cx + 85, shoulder_y + 28)],
                               tool="brush", color=(200, 180, 160), pressure=0.2))

    # === SKIN BASE FILL ===
    strokes.extend(draw_filled_circle(cx, cy, head_ry - 5, tool="brush",
                                       color=SKIN_BASE, pressure=0.3, fill_spacing=2.0))
    # Second pass for better coverage, slightly smaller
    strokes.extend(draw_filled_circle(cx, cy, head_ry - 12, tool="brush",
                                       color=SKIN_BASE, pressure=0.25, fill_spacing=2.5))

    # === FACE SHADING (light from upper-left) ===
    # Shadow side (right side of face)
    strokes.extend(draw_hatching(cx + 10, cy - 60, 55, 130,
                                  angle_deg=75, spacing=7, tool="pencil",
                                  color=SKIN_SHADOW, pressure=0.2))
    # Deeper shadow on right cheek
    strokes.extend(draw_hatching(cx + 25, cy - 20, 35, 70,
                                  angle_deg=60, spacing=8, tool="pencil",
                                  color=SKIN_DEEP_SHADOW, pressure=0.18))

    # Under nose shadow
    strokes.extend(draw_hatching(cx - 15, nose_y + 2, 30, 8,
                                  angle_deg=0, spacing=4, tool="pencil",
                                  color=SKIN_SHADOW, pressure=0.2))

    # Jaw shadow
    strokes.extend(draw_hatching(cx - 40, chin_y - 20, 80, 15,
                                  angle_deg=0, spacing=5, tool="brush",
                                  color=SKIN_DEEP_SHADOW, pressure=0.15))

    # Under lower lip shadow
    strokes.extend(draw_hatching(cx - 12, mouth_y + 10, 24, 6,
                                  angle_deg=0, spacing=4, tool="pencil",
                                  color=SKIN_SHADOW, pressure=0.18))

    # Eye socket shadows
    strokes.extend(draw_hatching(cx - 38, eye_y - 12, 25, 10,
                                  angle_deg=30, spacing=5, tool="pencil",
                                  color=SKIN_SHADOW, pressure=0.15))
    strokes.extend(draw_hatching(cx + 13, eye_y - 12, 25, 10,
                                  angle_deg=30, spacing=5, tool="pencil",
                                  color=SKIN_SHADOW, pressure=0.15))

    # Cheek blush (subtle, light side)
    strokes.extend(draw_hatching(cx - 45, cy + 10, 20, 15,
                                  angle_deg=45, spacing=6, tool="brush",
                                  color=BLUSH, pressure=0.12))

    # === HEAD OUTLINE ===
    strokes.append(draw_ellipse(cx, cy, head_rx, head_ry, tool="pen",
                                 color=(100, 75, 55), pressure=0.35))

    # === EARS ===
    # Left ear
    strokes.append(draw_arc(cx - head_rx + 3, eye_y + 15, 12,
                             math.pi * 0.8, math.pi * 1.8,
                             tool="pen", color=(100, 75, 55), pressure=0.25))
    # Right ear
    strokes.append(draw_arc(cx + head_rx - 3, eye_y + 15, 12,
                             -math.pi * 0.8, math.pi * 0.8,
                             tool="pen", color=(100, 75, 55), pressure=0.25))

    # === EYES ===
    eye_spacing = 22
    eye_rx = 12
    eye_ry = 6

    if expression == 'happy':
        # Slightly squinted happy eyes
        eye_ry = 5
        # Left eye
        strokes.append(draw_ellipse(cx - eye_spacing, eye_y, eye_rx, eye_ry,
                                     tool="pen", color=(80, 60, 45), pressure=0.35))
        # Right eye
        strokes.append(draw_ellipse(cx + eye_spacing, eye_y, eye_rx, eye_ry,
                                     tool="pen", color=(80, 60, 45), pressure=0.35))
        # Iris - looking forward
        strokes.extend(draw_filled_circle(cx - eye_spacing, eye_y + 1, 4,
                                           tool="pen", color=eye_color, pressure=0.5, fill_spacing=1.5))
        strokes.extend(draw_filled_circle(cx + eye_spacing, eye_y + 1, 4,
                                           tool="pen", color=eye_color, pressure=0.5, fill_spacing=1.5))
        # Pupils
        strokes.extend(draw_filled_circle(cx - eye_spacing, eye_y + 1, 2,
                                           tool="pen", color=(20, 15, 10), pressure=0.6, fill_spacing=1.0))
        strokes.extend(draw_filled_circle(cx + eye_spacing, eye_y + 1, 2,
                                           tool="pen", color=(20, 15, 10), pressure=0.6, fill_spacing=1.0))
        # Eye highlights (tiny white dots)
        strokes.extend(draw_filled_circle(cx - eye_spacing - 2, eye_y - 1, 1.2,
                                           tool="pen", color=WHITE, pressure=0.7, fill_spacing=0.8))
        strokes.extend(draw_filled_circle(cx + eye_spacing - 2, eye_y - 1, 1.2,
                                           tool="pen", color=WHITE, pressure=0.7, fill_spacing=0.8))
        # Crow's feet wrinkles from smiling
        strokes.append(draw_line(cx - eye_spacing - eye_rx - 2, eye_y - 2,
                                  cx - eye_spacing - eye_rx - 8, eye_y - 5,
                                  tool="pencil", color=SKIN_SHADOW, pressure=0.15))
        strokes.append(draw_line(cx + eye_spacing + eye_rx + 2, eye_y - 2,
                                  cx + eye_spacing + eye_rx + 8, eye_y - 5,
                                  tool="pencil", color=SKIN_SHADOW, pressure=0.15))

    elif expression == 'sad':
        # Droopy, slightly closed eyes
        eye_ry = 5
        # Left eye - slightly drooped
        strokes.append(draw_ellipse(cx - eye_spacing, eye_y + 2, eye_rx, eye_ry,
                                     tool="pen", color=(80, 60, 45), pressure=0.35))
        # Right eye
        strokes.append(draw_ellipse(cx + eye_spacing, eye_y + 2, eye_rx, eye_ry,
                                     tool="pen", color=(80, 60, 45), pressure=0.35))
        # Iris - looking down
        strokes.extend(draw_filled_circle(cx - eye_spacing, eye_y + 4, 4,
                                           tool="pen", color=eye_color, pressure=0.5, fill_spacing=1.5))
        strokes.extend(draw_filled_circle(cx + eye_spacing, eye_y + 4, 4,
                                           tool="pen", color=eye_color, pressure=0.5, fill_spacing=1.5))
        # Pupils
        strokes.extend(draw_filled_circle(cx - eye_spacing, eye_y + 4, 2,
                                           tool="pen", color=(20, 15, 10), pressure=0.6, fill_spacing=1.0))
        strokes.extend(draw_filled_circle(cx + eye_spacing, eye_y + 4, 2,
                                           tool="pen", color=(20, 15, 10), pressure=0.6, fill_spacing=1.0))
        # Eye highlights
        strokes.extend(draw_filled_circle(cx - eye_spacing - 2, eye_y + 2, 1.2,
                                           tool="pen", color=WHITE, pressure=0.7, fill_spacing=0.8))
        strokes.extend(draw_filled_circle(cx + eye_spacing - 2, eye_y + 2, 1.2,
                                           tool="pen", color=WHITE, pressure=0.7, fill_spacing=0.8))
        # Heavy upper eyelid lines (droopy)
        strokes.append(draw_arc(cx - eye_spacing, eye_y + 2, eye_rx,
                                 math.pi, 2 * math.pi,
                                 tool="pen", color=(70, 50, 35), pressure=0.4))
        strokes.append(draw_arc(cx + eye_spacing, eye_y + 2, eye_rx,
                                 math.pi, 2 * math.pi,
                                 tool="pen", color=(70, 50, 35), pressure=0.4))

    elif expression == 'contemplative':
        # Steady, focused eyes
        eye_ry = 6
        # Left eye
        strokes.append(draw_ellipse(cx - eye_spacing, eye_y, eye_rx, eye_ry,
                                     tool="pen", color=(80, 60, 45), pressure=0.3))
        # Right eye
        strokes.append(draw_ellipse(cx + eye_spacing, eye_y, eye_rx, eye_ry,
                                     tool="pen", color=(80, 60, 45), pressure=0.3))
        # Iris - looking slightly to the side (thoughtful gaze)
        strokes.extend(draw_filled_circle(cx - eye_spacing + 2, eye_y, 4.5,
                                           tool="pen", color=eye_color, pressure=0.5, fill_spacing=1.5))
        strokes.extend(draw_filled_circle(cx + eye_spacing + 2, eye_y, 4.5,
                                           tool="pen", color=eye_color, pressure=0.5, fill_spacing=1.5))
        # Pupils
        strokes.extend(draw_filled_circle(cx - eye_spacing + 2, eye_y, 2,
                                           tool="pen", color=(20, 15, 10), pressure=0.6, fill_spacing=1.0))
        strokes.extend(draw_filled_circle(cx + eye_spacing + 2, eye_y, 2,
                                           tool="pen", color=(20, 15, 10), pressure=0.6, fill_spacing=1.0))
        # Eye highlights
        strokes.extend(draw_filled_circle(cx - eye_spacing, eye_y - 2, 1.2,
                                           tool="pen", color=WHITE, pressure=0.7, fill_spacing=0.8))
        strokes.extend(draw_filled_circle(cx + eye_spacing, eye_y - 2, 1.2,
                                           tool="pen", color=WHITE, pressure=0.7, fill_spacing=0.8))
        # Subtle eyelid crease
        strokes.append(draw_arc(cx - eye_spacing, eye_y - 3, eye_rx + 2,
                                 math.pi * 1.1, math.pi * 1.9,
                                 tool="pencil", color=SKIN_SHADOW, pressure=0.2))
        strokes.append(draw_arc(cx + eye_spacing, eye_y - 3, eye_rx + 2,
                                 math.pi * 1.1, math.pi * 1.9,
                                 tool="pencil", color=SKIN_SHADOW, pressure=0.2))

    # === EYEBROWS ===
    if expression == 'happy':
        # Gently arched, slightly raised
        strokes.append(draw_curve([(cx - eye_spacing - 12, eye_y - 18),
                                    (cx - eye_spacing, eye_y - 23),
                                    (cx - eye_spacing + 10, eye_y - 17)],
                                   tool="marker", color=EYEBROW_DARK, pressure=0.4))
        strokes.append(draw_curve([(cx + eye_spacing - 10, eye_y - 17),
                                    (cx + eye_spacing, eye_y - 23),
                                    (cx + eye_spacing + 12, eye_y - 18)],
                                   tool="marker", color=EYEBROW_DARK, pressure=0.4))
    elif expression == 'sad':
        # Inner ends angled upward (worried brow)
        strokes.append(draw_curve([(cx - eye_spacing - 12, eye_y - 15),
                                    (cx - eye_spacing - 4, eye_y - 18),
                                    (cx - eye_spacing + 8, eye_y - 22)],
                                   tool="charcoal", color=EYEBROW_DARK, pressure=0.45))
        strokes.append(draw_curve([(cx + eye_spacing - 8, eye_y - 22),
                                    (cx + eye_spacing + 4, eye_y - 18),
                                    (cx + eye_spacing + 12, eye_y - 15)],
                                   tool="charcoal", color=EYEBROW_DARK, pressure=0.45))
    elif expression == 'contemplative':
        # Level, relaxed, slightly thick
        strokes.append(draw_curve([(cx - eye_spacing - 12, eye_y - 18),
                                    (cx - eye_spacing, eye_y - 20),
                                    (cx - eye_spacing + 10, eye_y - 18)],
                                   tool="pencil", color=EYEBROW_DARK, pressure=0.4))
        strokes.append(draw_curve([(cx + eye_spacing - 10, eye_y - 18),
                                    (cx + eye_spacing, eye_y - 20),
                                    (cx + eye_spacing + 10, eye_y - 18)],
                                   tool="pencil", color=EYEBROW_DARK, pressure=0.4))

    # === NOSE ===
    # Nose bridge - subtle vertical line
    strokes.append(draw_line(cx, eye_y + 12, cx, nose_y - 5,
                              tool="pencil", color=NOSE_COLOR, pressure=0.2))
    # Nose tip arc
    strokes.append(draw_arc(cx, nose_y - 2, 6,
                             math.pi * 0.3, math.pi * 0.7,
                             tool="pencil", color=NOSE_COLOR, pressure=0.25))
    # Nostrils (small arcs)
    strokes.append(draw_arc(cx - 7, nose_y, 4,
                             math.pi * 0.2, math.pi * 0.9,
                             tool="pen", color=SKIN_DEEP_SHADOW, pressure=0.2))
    strokes.append(draw_arc(cx + 7, nose_y, 4,
                             math.pi * 0.1, math.pi * 0.8,
                             tool="pen", color=SKIN_DEEP_SHADOW, pressure=0.2))

    # === MOUTH ===
    if expression == 'happy':
        # Wide smile - upward curve with lifted corners
        # Upper lip (M-shape)
        strokes.append(draw_curve([(cx - 18, mouth_y),
                                    (cx - 8, mouth_y - 4),
                                    (cx, mouth_y - 2),
                                    (cx + 8, mouth_y - 4),
                                    (cx + 18, mouth_y)],
                                   tool="pen", color=LIP_COLOR, pressure=0.35))
        # Smile line (main expression)
        strokes.append(draw_curve([(cx - 20, mouth_y - 2),
                                    (cx - 10, mouth_y + 4),
                                    (cx, mouth_y + 6),
                                    (cx + 10, mouth_y + 4),
                                    (cx + 20, mouth_y - 2)],
                                   tool="pen", color=LIP_DARK, pressure=0.4))
        # Lower lip
        strokes.append(draw_curve([(cx - 16, mouth_y + 2),
                                    (cx - 6, mouth_y + 10),
                                    (cx, mouth_y + 11),
                                    (cx + 6, mouth_y + 10),
                                    (cx + 16, mouth_y + 2)],
                                   tool="pen", color=LIP_COLOR, pressure=0.3))
        # Lip fill
        strokes.extend(draw_hatching(cx - 15, mouth_y - 2, 30, 12,
                                      angle_deg=0, spacing=3, tool="brush",
                                      color=LIP_COLOR, pressure=0.15))
        # Smile creases
        strokes.append(draw_curve([(cx - 22, mouth_y - 5),
                                    (cx - 25, mouth_y + 5),
                                    (cx - 22, mouth_y + 10)],
                                   tool="pencil", color=SKIN_SHADOW, pressure=0.15))
        strokes.append(draw_curve([(cx + 22, mouth_y - 5),
                                    (cx + 25, mouth_y + 5),
                                    (cx + 22, mouth_y + 10)],
                                   tool="pencil", color=SKIN_SHADOW, pressure=0.15))

    elif expression == 'sad':
        # Downturned mouth
        # Upper lip
        strokes.append(draw_curve([(cx - 14, mouth_y + 3),
                                    (cx - 6, mouth_y - 1),
                                    (cx, mouth_y),
                                    (cx + 6, mouth_y - 1),
                                    (cx + 14, mouth_y + 3)],
                                   tool="pen", color=LIP_DARK, pressure=0.4))
        # Lower lip - downward curve (frown)
        strokes.append(draw_curve([(cx - 14, mouth_y + 4),
                                    (cx - 5, mouth_y + 12),
                                    (cx, mouth_y + 13),
                                    (cx + 5, mouth_y + 12),
                                    (cx + 14, mouth_y + 4)],
                                   tool="pen", color=LIP_COLOR, pressure=0.35))
        # Lip line - the key expression element: corners turned down
        strokes.append(draw_curve([(cx - 16, mouth_y),
                                    (cx - 8, mouth_y + 5),
                                    (cx, mouth_y + 6),
                                    (cx + 8, mouth_y + 5),
                                    (cx + 16, mouth_y)],
                                   tool="pen", color=LIP_DARK, pressure=0.35))
        # Lip fill
        strokes.extend(draw_hatching(cx - 12, mouth_y + 1, 24, 10,
                                      angle_deg=0, spacing=3, tool="brush",
                                      color=(175, 100, 90), pressure=0.12))

    elif expression == 'contemplative':
        # Neutral, nearly straight lips pressed together
        # Upper lip
        strokes.append(draw_curve([(cx - 14, mouth_y + 1),
                                    (cx - 5, mouth_y - 2),
                                    (cx, mouth_y - 1),
                                    (cx + 5, mouth_y - 2),
                                    (cx + 14, mouth_y + 1)],
                                   tool="pen", color=LIP_COLOR, pressure=0.3))
        # Lip line - neutral, very slightly downturned
        strokes.append(draw_line(cx - 15, mouth_y + 1, cx + 15, mouth_y + 1,
                                  tool="pen", color=LIP_DARK, pressure=0.35))
        # Lower lip
        strokes.append(draw_curve([(cx - 12, mouth_y + 2),
                                    (cx - 4, mouth_y + 8),
                                    (cx, mouth_y + 9),
                                    (cx + 4, mouth_y + 8),
                                    (cx + 12, mouth_y + 2)],
                                   tool="pen", color=LIP_COLOR, pressure=0.3))
        # Lip fill
        strokes.extend(draw_hatching(cx - 11, mouth_y - 1, 22, 9,
                                      angle_deg=0, spacing=3, tool="brush",
                                      color=LIP_COLOR, pressure=0.1))

    # === HAIR ===
    if hair_style == 'wavy':
        # Wavy medium-length hair - flows from crown
        crown_x, crown_y = cx - 10, forehead_y - 5

        # Hair mass fill (background)
        for offset_y in range(-15, 5, 3):
            strokes.append(draw_arc(cx, forehead_y + offset_y, head_rx + 8,
                                     math.pi, 2 * math.pi,
                                     tool="charcoal", color=hair_color, pressure=0.35))

        # Flowing wavy strands - left side
        for i in range(12):
            start_x = crown_x - 5 + i * 5
            start_y = forehead_y - 8 + abs(i - 6) * 2
            end_x = cx - head_rx - 15 + i * 3
            end_y = eye_y + 40 + i * 8
            amp = 8 + (i % 3) * 4
            strokes.append(draw_s_curve(start_x, start_y, end_x, end_y,
                                         amplitude=amp, tool="charcoal",
                                         color=hair_color,
                                         pressure=0.25 + (i % 4) * 0.05))

        # Right side hair
        for i in range(10):
            start_x = cx + i * 5
            start_y = forehead_y - 5 + abs(i - 5) * 2
            end_x = cx + head_rx + 5 + i * 2
            end_y = eye_y + 35 + i * 9
            amp = 7 + (i % 3) * 5
            strokes.append(draw_s_curve(start_x, start_y, end_x, end_y,
                                         amplitude=amp, tool="charcoal",
                                         color=hair_color,
                                         pressure=0.22 + (i % 3) * 0.06))

        # Highlight strands
        for i in range(6):
            start_x = crown_x + i * 8
            start_y = forehead_y - 3
            end_x = cx - 30 + i * 12
            end_y = eye_y + 20 + i * 10
            strokes.append(draw_s_curve(start_x, start_y, end_x, end_y,
                                         amplitude=6, tool="pencil",
                                         color=hair_highlight, pressure=0.2))

        # Hairline definition
        strokes.append(draw_arc(cx, forehead_y + 8, head_rx - 5,
                                 math.pi * 1.05, math.pi * 1.95,
                                 tool="pen", color=hair_color, pressure=0.3))

    elif hair_style == 'straight_long':
        # Long straight dark hair
        crown_x, crown_y = cx, forehead_y - 8

        # Hair mass on top
        for offset_y in range(-12, 8, 3):
            strokes.append(draw_arc(cx, forehead_y + offset_y, head_rx + 10,
                                     math.pi, 2 * math.pi,
                                     tool="charcoal", color=hair_color, pressure=0.4))

        # Straight strands falling down - left side
        for i in range(14):
            x_start = cx - head_rx + i * 4 - 10
            x_end = x_start - 5
            y_start = forehead_y - 5
            y_end = mouth_y + 30 + (i % 3) * 10
            strokes.append(draw_line(x_start, y_start, x_end, y_end,
                                      tool="charcoal", color=hair_color,
                                      pressure=0.3 + (i % 3) * 0.05))

        # Right side
        for i in range(14):
            x_start = cx + i * 4
            x_end = x_start + 5
            y_start = forehead_y - 5
            y_end = mouth_y + 25 + (i % 3) * 12
            strokes.append(draw_line(x_start, y_start, x_end, y_end,
                                      tool="charcoal", color=hair_color,
                                      pressure=0.3 + (i % 3) * 0.05))

        # Highlight strands (pencil, lighter)
        for i in range(5):
            x_pos = cx - 30 + i * 15
            strokes.append(draw_line(x_pos, forehead_y, x_pos - 2, mouth_y + 20,
                                      tool="pencil", color=hair_highlight,
                                      pressure=0.18))

        # Hair parting line
        strokes.append(draw_line(cx - 5, forehead_y - 5, cx - 5, forehead_y + 12,
                                  tool="pen", color=hair_color, pressure=0.3))

    elif hair_style == 'curly_short':
        # Short curly/textured hair
        crown_y = forehead_y - 10

        # Curly mass using overlapping small arcs and circles
        for row in range(5):
            for col in range(7):
                curl_x = cx - 45 + col * 15 + (row % 2) * 7
                curl_y = crown_y + row * 12
                # Check if within head boundary (roughly)
                dist_from_center = math.sqrt((curl_x - cx) ** 2 + (curl_y - (cy - 30)) ** 2)
                if dist_from_center < head_rx + 20:
                    radius = 6 + (col + row) % 3 * 2
                    strokes.append(draw_circle(curl_x, curl_y, radius,
                                               tool="charcoal", color=hair_color,
                                               pressure=0.3 + (row * col % 4) * 0.05))

        # More curls at the sides
        for i in range(6):
            curl_x = cx - head_rx - 5 + (i % 2) * 5
            curl_y = forehead_y - 5 + i * 12
            strokes.append(draw_circle(curl_x, curl_y, 5 + i % 3,
                                        tool="charcoal", color=hair_color,
                                        pressure=0.28))
        for i in range(6):
            curl_x = cx + head_rx + 5 - (i % 2) * 5
            curl_y = forehead_y - 5 + i * 12
            strokes.append(draw_circle(curl_x, curl_y, 5 + i % 3,
                                        tool="charcoal", color=hair_color,
                                        pressure=0.28))

        # Highlight curls
        for i in range(4):
            curl_x = cx - 20 + i * 14
            curl_y = crown_y + 5 + (i % 2) * 10
            strokes.append(draw_circle(curl_x, curl_y, 5,
                                        tool="pencil", color=hair_highlight,
                                        pressure=0.18))

        # Top mass fill
        strokes.extend(draw_filled_circle(cx, crown_y + 10, 50,
                                           tool="charcoal", color=hair_color,
                                           pressure=0.2, fill_spacing=4.0))

    return strokes


# ============================================================
# Portrait 1: HAPPY (left) - wavy brown hair, brown eyes
# ============================================================
portrait1 = draw_portrait(150, 310, 'happy', 'wavy', EYE_BROWN, HAIR_BROWN, HAIR_BROWN_LIGHT)
all_strokes.extend(portrait1)

# ============================================================
# Portrait 2: SAD (center) - straight long dark hair, blue eyes
# ============================================================
portrait2 = draw_portrait(450, 310, 'sad', 'straight_long', EYE_BLUE, HAIR_BLACK, HAIR_BLACK_HIGHLIGHT)
all_strokes.extend(portrait2)

# ============================================================
# Portrait 3: CONTEMPLATIVE (right) - curly short red hair, green eyes
# ============================================================
portrait3 = draw_portrait(750, 310, 'contemplative', 'curly_short', EYE_GREEN, HAIR_RED, HAIR_RED_LIGHT)
all_strokes.extend(portrait3)

# ============================================================
# Title area - subtle decorative frame
# ============================================================
# Top border line
all_strokes.append(draw_line(30, 25, 870, 25, tool="pen", color=(180, 160, 140), pressure=0.2))
# Bottom border line
all_strokes.append(draw_line(30, 675, 870, 675, tool="pen", color=(180, 160, 140), pressure=0.2))

# ============================================================
# Render
# ============================================================
drawing = Drawing(strokes=all_strokes, width=900, height=700)
img = render_drawing(drawing, apply_paper=True)
output_path = os.path.join(os.path.dirname(__file__), "lesson_06.png")
img.convert("RGB").save(output_path)
print(f"Saved to {output_path}")
print(f"Total strokes: {len(all_strokes)}")
