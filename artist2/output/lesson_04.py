"""
Lesson 4: Color Theory & Composition
A color theory study strip and a still life composition with a red apple,
blue vase, and yellow lemon.
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
# PART 1 -- Color Theory Study Strip (y: 20-200)
# =============================================================================

# --- Exercise 1A: Warm vs. Cool Gradient Bars (x: 30-430, y: 30-100) ---

# 1. Warm gradient (red)
all_strokes.extend(draw_gradient_fill(x=30, y=30, w=190, h=70,
    start_pressure=0.1, end_pressure=0.7, tool="brush", color="red"))

# 2. Warm bar outline
all_strokes.append(draw_rectangle(x=30, y=30, w=190, h=70,
    pressure=0.3, tool="pen", color="red"))

# 3. Cool gradient (blue)
all_strokes.extend(draw_gradient_fill(x=240, y=30, w=190, h=70,
    start_pressure=0.1, end_pressure=0.7, tool="brush", color="blue"))

# 4. Cool bar outline
all_strokes.append(draw_rectangle(x=240, y=30, w=190, h=70,
    pressure=0.3, tool="pen", color="blue"))

# --- Exercise 1B: Complementary Color Hatching Swatches (x: 30-860, y: 120-190) ---

# 5. Red swatch
all_strokes.extend(draw_filled_rectangle(x=30, y=120, w=70, h=70,
    tool="brush", color="red", pressure=0.5))

# 6. Green swatch
all_strokes.extend(draw_filled_rectangle(x=120, y=120, w=70, h=70,
    tool="brush", color="green", pressure=0.5))

# 7. Red-green hatched (red layer)
all_strokes.extend(draw_crosshatching(x=210, y=120, w=70, h=70,
    spacing=6, pressure=0.4, tool="pencil", color="red"))

# 8. Red-green hatched (green layer overlaid)
all_strokes.extend(draw_crosshatching(x=210, y=120, w=70, h=70,
    spacing=8, pressure=0.3, tool="pencil", color="green"))

# 9. Blue swatch
all_strokes.extend(draw_filled_rectangle(x=340, y=120, w=70, h=70,
    tool="brush", color="blue", pressure=0.5))

# 10. Orange swatch
all_strokes.extend(draw_filled_rectangle(x=430, y=120, w=70, h=70,
    tool="brush", color="orange", pressure=0.5))

# 11. Blue-orange hatched (blue layer)
all_strokes.extend(draw_crosshatching(x=520, y=120, w=70, h=70,
    spacing=6, pressure=0.4, tool="pencil", color="blue"))

# 12. Blue-orange hatched (orange layer overlaid)
all_strokes.extend(draw_crosshatching(x=520, y=120, w=70, h=70,
    spacing=8, pressure=0.3, tool="pencil", color="orange"))

# 13. Yellow swatch
all_strokes.extend(draw_filled_rectangle(x=650, y=120, w=70, h=70,
    tool="brush", color="yellow", pressure=0.5))

# 14. Purple swatch
all_strokes.extend(draw_filled_rectangle(x=740, y=120, w=70, h=70,
    tool="brush", color="purple", pressure=0.5))

# --- Exercise 1C: Warm/Cool Color Strip Labels (x: 460-860, y: 30-100) ---

# 15. Orange hatching
all_strokes.extend(draw_hatching(x=460, y=30, w=70, h=70,
    angle_deg=45, spacing=7, pressure=0.5, tool="pencil", color="orange"))

# 16. Orange box outline
all_strokes.append(draw_rectangle(x=460, y=30, w=70, h=70,
    pressure=0.2, tool="pen", color="orange"))

# 17. Purple hatching
all_strokes.extend(draw_hatching(x=560, y=30, w=70, h=70,
    angle_deg=45, spacing=7, pressure=0.5, tool="pencil", color="purple"))

# 18. Purple box outline
all_strokes.append(draw_rectangle(x=560, y=30, w=70, h=70,
    pressure=0.2, tool="pen", color="purple"))

# =============================================================================
# PART 2 -- Still Life Composition (y: 220-680)
# =============================================================================

# --- The Table Surface (background) ---

# 19. Table surface
all_strokes.extend(draw_filled_rectangle(x=30, y=450, w=840, h=230,
    tool="brush", color=(180, 150, 110), pressure=0.3))

# 20. Table top edge
all_strokes.append(draw_line(30, 450, 870, 450,
    tool="pen", color="brown", pressure=0.5))

# 21. Background wash
all_strokes.extend(draw_gradient_fill(x=30, y=220, w=840, h=230,
    start_pressure=0.15, end_pressure=0.05, tool="brush", color=(150, 160, 180)))

# 22. Table shadow gradient
all_strokes.extend(draw_gradient_fill(x=30, y=450, w=840, h=230,
    start_pressure=0.05, end_pressure=0.2, tool="brush", color="brown"))

# --- The Red Apple (focal point, near x=280, cy=500) ---

# 23. Apple base fill
all_strokes.extend(draw_filled_circle(cx=280, cy=500, radius=55,
    tool="brush", color="red", pressure=0.45))

# 24. Apple highlight zone
all_strokes.extend(draw_hatching(x=240, y=455, w=40, h=40,
    angle_deg=30, spacing=10, pressure=0.15, tool="pencil", color=(255, 180, 180)))

# 25. Apple midtone
all_strokes.extend(draw_hatching(x=250, y=475, w=60, h=50,
    angle_deg=45, spacing=7, pressure=0.35, tool="pencil", color=(180, 30, 30)))

# 26. Apple shadow
all_strokes.extend(draw_crosshatching(x=280, y=495, w=50, h=50,
    spacing=5, pressure=0.6, tool="pencil", color=(120, 20, 20)))

# 27. Apple outline
all_strokes.append(draw_circle(cx=280, cy=500, radius=55,
    tool="pen", color=(130, 20, 20), pressure=0.4))

# 28. Apple cast shadow
all_strokes.extend(draw_hatching(x=260, y=555, w=80, h=15,
    angle_deg=0, spacing=4, pressure=0.35, tool="pencil", color=(100, 80, 60)))

# 29. Apple stem
all_strokes.append(draw_line(280, 447, 285, 435,
    tool="pen", color="brown", pressure=0.4))

# --- The Blue Vase (x=560, cy=460, tall form) ---

# 30. Vase body fill
all_strokes.extend(draw_filled_rectangle(x=525, y=380, w=70, h=150,
    tool="brush", color="blue", pressure=0.4))

# 31. Vase top ellipse
all_strokes.append(draw_ellipse(cx=560, cy=380, rx=35, ry=10,
    tool="pen", color=(30, 30, 150), pressure=0.4))

# 32. Vase bottom ellipse
all_strokes.append(draw_ellipse(cx=560, cy=530, rx=35, ry=8,
    tool="pen", color=(30, 30, 150), pressure=0.4))

# 33. Vase left edge
all_strokes.append(draw_line(525, 380, 525, 530,
    tool="pen", color=(30, 30, 150), pressure=0.45))

# 34. Vase right edge
all_strokes.append(draw_line(595, 380, 595, 530,
    tool="pen", color=(30, 30, 150), pressure=0.45))

# 35. Vase highlight
all_strokes.extend(draw_hatching(x=530, y=390, w=25, h=120,
    angle_deg=90, spacing=10, pressure=0.15, tool="pencil", color=(140, 140, 255)))

# 36. Vase shadow
all_strokes.extend(draw_crosshatching(x=565, y=390, w=25, h=120,
    spacing=5, pressure=0.55, tool="pencil", color=(20, 20, 100)))

# 37. Vase cast shadow
all_strokes.extend(draw_hatching(x=555, y=530, w=70, h=15,
    angle_deg=0, spacing=4, pressure=0.3, tool="pencil", color=(80, 70, 60)))

# --- The Yellow Lemon (x=420, cy=530, small foreground object) ---

# 38. Lemon base fill
all_strokes.extend(draw_filled_circle(cx=420, cy=530, radius=30,
    tool="brush", color="yellow", pressure=0.4))

# 39. Lemon highlight
all_strokes.extend(draw_hatching(x=395, y=508, w=25, h=20,
    angle_deg=30, spacing=9, pressure=0.1, tool="pencil", color=(255, 255, 200)))

# 40. Lemon shadow
all_strokes.extend(draw_hatching(x=420, y=525, w=30, h=30,
    angle_deg=45, spacing=6, pressure=0.45, tool="pencil", color=(180, 160, 0)))

# 41. Lemon outline
all_strokes.append(draw_ellipse(cx=420, cy=530, rx=35, ry=22,
    tool="pen", color=(160, 140, 0), pressure=0.35))

# 42. Lemon cast shadow
all_strokes.extend(draw_hatching(x=415, y=553, w=40, h=10,
    angle_deg=0, spacing=4, pressure=0.3, tool="pencil", color=(100, 80, 50)))

# --- Final Touches ---

# 43. Table front edge
all_strokes.append(draw_pressure_ramp(30, 680, 870, 680,
    tool="pen", color="brown"))

# =============================================================================
# Render and save
# =============================================================================
drawing = Drawing(strokes=all_strokes, width=900, height=700)
img = render_drawing(drawing, apply_paper=True)
output_path = os.path.join(os.path.dirname(__file__), "lesson_04.png")
img.convert("RGB").save(output_path)
print(f"Saved to {output_path}")
print(f"Total strokes: {len(all_strokes)}")
