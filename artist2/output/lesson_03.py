#!/usr/bin/env python3
"""
Lesson 3: Shading, Hatching & Value
Student assignment - creating tonal value and 3D form through shading.
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
# Section 1 -- Hatching & Crosshatching Swatches (top-left quadrant, y: 20-280)
# =============================================================================

# Swatch 1: Light hatching
all_strokes.append(draw_rectangle(x=30, y=40, w=80, h=100, pressure=0.3, tool="pen"))
all_strokes.extend(draw_hatching(x=30, y=40, w=80, h=100, angle_deg=45, spacing=12, pressure=0.2, tool="pencil"))

# Swatch 2: Medium hatching
all_strokes.append(draw_rectangle(x=130, y=40, w=80, h=100, pressure=0.3, tool="pen"))
all_strokes.extend(draw_hatching(x=130, y=40, w=80, h=100, angle_deg=45, spacing=8, pressure=0.4, tool="pencil"))

# Swatch 3: Dense hatching
all_strokes.append(draw_rectangle(x=230, y=40, w=80, h=100, pressure=0.3, tool="pen"))
all_strokes.extend(draw_hatching(x=230, y=40, w=80, h=100, angle_deg=45, spacing=5, pressure=0.6, tool="pencil"))

# Swatch 4: Light crosshatching
all_strokes.append(draw_rectangle(x=30, y=170, w=80, h=100, pressure=0.3, tool="pen"))
all_strokes.extend(draw_crosshatching(x=30, y=170, w=80, h=100, spacing=10, pressure=0.3, tool="pencil"))

# Swatch 5: Dense crosshatching
all_strokes.append(draw_rectangle(x=130, y=170, w=80, h=100, pressure=0.3, tool="pen"))
all_strokes.extend(draw_crosshatching(x=130, y=170, w=80, h=100, spacing=5, pressure=0.5, tool="pencil"))

# =============================================================================
# Section 2 -- Gradient Fills (top-right quadrant, y: 20-280)
# =============================================================================

# Gradient light-to-dark (pencil)
all_strokes.extend(draw_gradient_fill(x=430, y=40, w=140, h=100, start_pressure=0.05, end_pressure=0.8, tool="pencil"))
all_strokes.append(draw_rectangle(x=430, y=40, w=140, h=100, pressure=0.3, tool="pen"))

# Gradient dark-to-light (pencil)
all_strokes.extend(draw_gradient_fill(x=600, y=40, w=140, h=100, start_pressure=0.8, end_pressure=0.05, tool="pencil"))
all_strokes.append(draw_rectangle(x=600, y=40, w=140, h=100, pressure=0.3, tool="pen"))

# Charcoal gradient
all_strokes.extend(draw_gradient_fill(x=430, y=170, w=140, h=100, start_pressure=0.1, end_pressure=0.9, tool="charcoal"))
all_strokes.append(draw_rectangle(x=430, y=170, w=140, h=100, pressure=0.3, tool="pen"))

# Brush gradient in blue
all_strokes.extend(draw_gradient_fill(x=600, y=170, w=140, h=100, start_pressure=0.1, end_pressure=0.7, tool="brush", color="blue"))
all_strokes.append(draw_rectangle(x=600, y=170, w=140, h=100, pressure=0.3, tool="pen"))

# =============================================================================
# Section 3 -- Shaded Sphere (bottom-left quadrant, y: 310-580)
# =============================================================================

# Sphere outline
all_strokes.append(draw_circle(cx=150, cy=440, radius=90, pressure=0.4, tool="pen"))

# Light hatching (top-left highlight zone)
all_strokes.extend(draw_hatching(x=80, y=365, w=70, h=70, angle_deg=45, spacing=14, pressure=0.15, tool="pencil"))

# Medium hatching (middle transitional zone)
all_strokes.extend(draw_hatching(x=100, y=400, w=100, h=80, angle_deg=45, spacing=8, pressure=0.35, tool="pencil"))

# Dense hatching (lower-right shadow zone)
all_strokes.extend(draw_hatching(x=140, y=440, w=80, h=80, angle_deg=45, spacing=5, pressure=0.55, tool="pencil"))

# Crosshatch darkest area (core shadow)
all_strokes.extend(draw_crosshatching(x=160, y=460, w=60, h=55, spacing=4, pressure=0.7, tool="pencil"))

# Cast shadow
all_strokes.extend(draw_hatching(x=170, y=530, w=100, h=20, angle_deg=0, spacing=4, pressure=0.5, tool="pencil"))

# =============================================================================
# Section 4 -- Shaded Cube (bottom-right quadrant, y: 310-580)
# =============================================================================

# Top face outline
all_strokes.append(draw_line(530, 370, 630, 340, pressure=0.5, tool="pen"))
all_strokes.append(draw_line(630, 340, 730, 370, pressure=0.5, tool="pen"))
all_strokes.append(draw_line(730, 370, 630, 400, pressure=0.5, tool="pen"))
all_strokes.append(draw_line(630, 400, 530, 370, pressure=0.5, tool="pen"))

# Front face outline
all_strokes.append(draw_line(530, 370, 530, 490, pressure=0.5, tool="pen"))
all_strokes.append(draw_line(530, 490, 630, 520, pressure=0.5, tool="pen"))
all_strokes.append(draw_line(630, 520, 630, 400, pressure=0.5, tool="pen"))

# Right face outline
all_strokes.append(draw_line(630, 400, 730, 370, pressure=0.5, tool="pen"))
all_strokes.append(draw_line(730, 370, 730, 490, pressure=0.5, tool="pen"))
all_strokes.append(draw_line(730, 490, 630, 520, pressure=0.5, tool="pen"))

# Top face shading (lightest)
all_strokes.extend(draw_hatching(x=540, y=345, w=180, h=50, angle_deg=30, spacing=14, pressure=0.15, tool="pencil"))

# Front face shading (medium)
all_strokes.extend(draw_hatching(x=530, y=375, w=100, h=140, angle_deg=75, spacing=7, pressure=0.35, tool="pencil"))

# Right face shading (darkest)
all_strokes.extend(draw_hatching(x=630, y=375, w=100, h=140, angle_deg=45, spacing=5, pressure=0.55, tool="pencil"))

# Pressure ramp accent line along the bottom
all_strokes.append(draw_pressure_ramp(530, 490, 730, 490, tool="pen"))

# =============================================================================
# Render and save
# =============================================================================

drawing = Drawing(strokes=all_strokes, width=800, height=600)
img = render_drawing(drawing, apply_paper=True)
output_path = os.path.join(os.path.dirname(__file__), "lesson_03.png")
img.convert("RGB").save(output_path)
print(f"Saved to {output_path}")
print(f"Total strokes: {len(all_strokes)}")
