import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'artist'))

from student import *
from stylus_format import Drawing
from renderer import render_drawing

all_strokes = []

# === Row 1: Pen (black) ===

# Horizontal lines at y=80
all_strokes.append(draw_line(50, 80, 250, 80, tool="pen", color="black", pressure=0.2))
all_strokes.append(draw_line(300, 80, 500, 80, tool="pen", color="black", pressure=0.5))
all_strokes.append(draw_line(550, 80, 750, 80, tool="pen", color="black", pressure=0.9))

# Vertical lines
all_strokes.append(draw_line(150, 100, 150, 180, tool="pen", color="black", pressure=0.2))
all_strokes.append(draw_line(400, 100, 400, 180, tool="pen", color="black", pressure=0.5))
all_strokes.append(draw_line(650, 100, 650, 180, tool="pen", color="black", pressure=0.9))

# === Row 2: Pencil (blue) ===

# Horizontal lines at y=280
all_strokes.append(draw_line(50, 280, 250, 280, tool="pencil", color="blue", pressure=0.2))
all_strokes.append(draw_line(300, 280, 500, 280, tool="pencil", color="blue", pressure=0.5))
all_strokes.append(draw_line(550, 280, 750, 280, tool="pencil", color="blue", pressure=0.9))

# Diagonal lines
all_strokes.append(draw_line(50, 300, 150, 380, tool="pencil", color="blue", pressure=0.2))
all_strokes.append(draw_line(300, 300, 400, 380, tool="pencil", color="blue", pressure=0.5))
all_strokes.append(draw_line(550, 300, 650, 380, tool="pencil", color="blue", pressure=0.9))

# === Row 3: Brush (red) ===

# Horizontal lines at y=480
all_strokes.append(draw_line(50, 480, 250, 480, tool="brush", color="red", pressure=0.2))
all_strokes.append(draw_line(300, 480, 500, 480, tool="brush", color="red", pressure=0.5))
all_strokes.append(draw_line(550, 480, 750, 480, tool="brush", color="red", pressure=0.9))

# Pressure ramp
all_strokes.append(draw_pressure_ramp(50, 540, 750, 540, tool="brush", color="red"))

# === Render and save ===
drawing = Drawing(strokes=all_strokes, width=800, height=600)
img = render_drawing(drawing, apply_paper=True)
output_path = os.path.join(os.path.dirname(__file__), "lesson_01.png")
img.convert("RGB").save(output_path)
print(f"Saved to {output_path}")
print(f"Total strokes: {len(all_strokes)}")
