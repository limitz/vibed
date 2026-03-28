"""
Lesson 02: Curves & Shapes
A study in circles, arcs, ellipses, S-curves, rectangles, and triangles,
arranged across four quadrants with multiple tools and colors.
"""

import sys
import os
import math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'artist'))

from student import *
from stylus_format import Drawing
from renderer import render_drawing

all_strokes = []

# =============================================================================
# Section 1 -- Circles & Arcs (top-left quadrant)
# Pen tool, black ink
# =============================================================================

# Shape 1: Outer concentric circle, light pressure
all_strokes.append(draw_circle(cx=120, cy=100, radius=60, tool="pen", color="black", pressure=0.4))

# Shape 2: Inner concentric circle, heavier pressure
all_strokes.append(draw_circle(cx=120, cy=100, radius=40, tool="pen", color="black", pressure=0.7))

# Shape 3: Bottom half-arc
all_strokes.append(draw_arc(cx=300, cy=100, radius=50, start_angle=0, end_angle=math.pi, tool="pen", color="black", pressure=0.5))

# Shape 4: Top half-arc, lighter to show contrast
all_strokes.append(draw_arc(cx=300, cy=100, radius=50, start_angle=math.pi, end_angle=2*math.pi, tool="pen", color="black", pressure=0.3))

# Shape 5: Quarter arc
all_strokes.append(draw_arc(cx=300, cy=100, radius=30, start_angle=0, end_angle=math.pi/2, tool="pen", color="black", pressure=0.6))

# Creative touch: a tiny dot-circle at the center of the concentric pair
all_strokes.append(draw_circle(cx=120, cy=100, radius=5, tool="pen", color="black", pressure=0.9))

# =============================================================================
# Section 2 -- Ellipses & S-Curves (top-right quadrant)
# Pencil tool, blue
# =============================================================================

# Shape 6: Wide ellipse
all_strokes.append(draw_ellipse(cx=570, cy=80, rx=80, ry=40, tool="pencil", color="blue", pressure=0.5))

# Shape 7: Tall ellipse (overlapping the wide one -- like a compass rose shape)
all_strokes.append(draw_ellipse(cx=570, cy=80, rx=30, ry=60, tool="pencil", color="blue", pressure=0.5))

# Shape 8: Horizontal S-curve, moderate amplitude
all_strokes.append(draw_s_curve(x1=480, y1=160, x2=700, y2=160, amplitude=40, tool="pencil", color="blue", pressure=0.4))

# Shape 9: S-curve with smaller amplitude but heavier pressure
all_strokes.append(draw_s_curve(x1=480, y1=220, x2=700, y2=220, amplitude=25, tool="pencil", color="blue", pressure=0.7))

# Creative touch: a gentle third S-curve echoing below, very light, like a fading ripple
all_strokes.append(draw_s_curve(x1=490, y1=260, x2=690, y2=260, amplitude=15, tool="pencil", color="blue", pressure=0.2))

# =============================================================================
# Section 3 -- Rectangles & Triangles (bottom-left quadrant)
# Pen tool, green
# =============================================================================

# Shape 10: Medium rectangle
all_strokes.append(draw_rectangle(x=40, y=320, w=150, h=100, tool="pen", color="green", pressure=0.5))

# Shape 11: Square
all_strokes.append(draw_rectangle(x=220, y=340, w=80, h=80, tool="pen", color="green", pressure=0.5))

# Shape 12: Right triangle
all_strokes.append(draw_triangle(40, 480, 140, 560, 40, 560, tool="pen", color="green", pressure=0.5))

# Shape 13: Isosceles triangle
all_strokes.append(draw_triangle(180, 560, 260, 460, 340, 560, tool="pen", color="green", pressure=0.5))

# Creative touch: small diamond (rotated square) inside the square, using hatching would be
# too much -- instead a subtle inner rectangle to give the square some depth
all_strokes.append(draw_rectangle(x=235, y=355, w=50, h=50, tool="pen", color="green", pressure=0.3))

# =============================================================================
# Section 4 -- Combined composition (bottom-right quadrant)
# Multiple tools and colors -- a little scene: sun-like shape, house, and ground
# =============================================================================

# Shape 14: Light brush circle (the "sun" body)
all_strokes.append(draw_circle(cx=520, cy=400, radius=50, tool="brush", color="red", pressure=0.3))

# Shape 15: Ellipse orbit around the circle
all_strokes.append(draw_ellipse(cx=520, cy=400, rx=70, ry=35, tool="brush", color="red", pressure=0.6))

# Shape 16: Rectangle (the "house" body)
all_strokes.append(draw_rectangle(x=620, y=350, w=120, h=100, tool="pen", color="purple", pressure=0.5))

# Shape 17: Triangle roof on top of the house
all_strokes.append(draw_triangle(680, 350, 620, 350, 650, 300, tool="pen", color="purple", pressure=0.5))

# Shape 18: S-curve below the shapes (the "ground")
all_strokes.append(draw_s_curve(x1=460, y1=500, x2=750, y2=500, amplitude=30, tool="pencil", color="orange", pressure=0.5))

# Shape 19: Upward arc in charcoal -- new tool!
all_strokes.append(draw_arc(cx=680, cy=530, radius=40, start_angle=math.pi, end_angle=2*math.pi, tool="charcoal", color="black", pressure=0.6))

# Creative touch: a second charcoal arc mirroring below, like a reflection
all_strokes.append(draw_arc(cx=680, cy=570, radius=25, start_angle=0, end_angle=math.pi, tool="charcoal", color="gray", pressure=0.3))

# =============================================================================
# Render and save
# =============================================================================

drawing = Drawing(strokes=all_strokes, width=800, height=600)
img = render_drawing(drawing, apply_paper=True)
output_path = os.path.join(os.path.dirname(__file__), "lesson_02.png")
img.convert("RGB").save(output_path)
print(f"Saved to {output_path}")
print(f"Total strokes: {len(all_strokes)}")
