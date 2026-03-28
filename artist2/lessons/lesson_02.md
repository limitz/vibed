# Lesson 2: Curves & Shapes

## Feedback from Lesson 1

**Result: PASS**

Good work on your first lesson. Here is what I observed:

**Strengths:**
- All 16 strokes are present and correctly placed at the specified coordinates.
- Three tools (pen, pencil, brush) are clearly distinguishable. The pen lines are crisp, the pencil lines softer, and the brush lines dramatically respond to pressure.
- Pressure variation is well demonstrated -- the difference between 0.2, 0.5, and 0.9 is immediately visible, especially in the brush row where the heavy line is noticeably thicker than the light one.
- The pressure ramp at the bottom shows a smooth thin-to-thick-to-thin transition. Well done.
- Code is clean, well-organized with comments separating each section.

**Areas for improvement:**
- The composition is functional but mechanical. Every element sits at the exact coordinates given, which shows you can follow instructions, but does not yet show spatial intuition. In future lessons you will need to make some placement decisions yourself.
- You only used `draw_line` and `draw_pressure_ramp`. You have not yet explored curves, shapes, or fills -- that starts now.
- The diagonal lines in Row 2 are short (100x80 pixels). Longer diagonals would have tested your control more rigorously. Acceptable for Lesson 1, but going forward I expect bolder strokes.

---

## Objectives

By the end of this lesson you will be able to:

1. Draw circles, arcs, and ellipses with controlled placement and size.
2. Draw S-curves to practice smooth, flowing motion.
3. Draw basic shapes: rectangles and triangles.
4. Combine curves and shapes into a composed study using multiple tools and colors.

---

## Concepts

### Circles and Arcs
A **circle** is defined by a center `(cx, cy)` and a `radius`. An **arc** is a partial circle defined by center, radius, and start/end angles in **radians** (0 = right, pi/2 = down, pi = left, 3*pi/2 = up; angles go clockwise because Y increases downward).

Key values:
- `math.pi` = 3.14159...
- Full circle = 0 to 2*pi
- Half circle (top) = math.pi to 2*math.pi
- Quarter circle = 0 to math.pi/2

### Ellipses
An **ellipse** has a center `(cx, cy)` plus two radii: `rx` (horizontal) and `ry` (vertical). When rx > ry, the ellipse is wider than it is tall.

### S-Curves
An S-curve creates a smooth, sinuous path from point A to point B. The `amplitude` parameter controls how far the curve swings away from the straight line connecting the two points. Higher amplitude = more dramatic S shape.

### Rectangles and Triangles
A **rectangle** is defined by its top-left corner `(x, y)`, width `w`, and height `h`. A **triangle** is defined by its three vertices `(x1,y1)`, `(x2,y2)`, `(x3,y3)`.

---

## Assignment

Create a Python script saved as `/home/wipkat/vibed/artist2/output/lesson_02.py` that produces `/home/wipkat/vibed/artist2/output/lesson_02.png`.

### Setup boilerplate

```python
import sys
import os
import math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'artist'))

from student import *
from stylus_format import Drawing
from renderer import render_drawing
```

After creating all strokes, render:

```python
drawing = Drawing(strokes=all_strokes, width=800, height=600)
img = render_drawing(drawing, apply_paper=True)
output_path = os.path.join(os.path.dirname(__file__), "lesson_02.png")
img.convert("RGB").save(output_path)
print(f"Saved to {output_path}")
print(f"Total strokes: {len(all_strokes)}")
```

### What to draw

Organize the canvas into four sections.

#### Section 1 -- Circles & Arcs (top-left quadrant)

Using the **pen** tool in **black**:

| Shape | Function | Parameters | Purpose |
|-------|----------|-----------|---------|
| 1 | `draw_circle` | cx=120, cy=100, radius=60, pressure=0.4 | Small circle, light |
| 2 | `draw_circle` | cx=120, cy=100, radius=40, pressure=0.7 | Concentric inner circle, heavier |
| 3 | `draw_arc` | cx=300, cy=100, radius=50, start_angle=0, end_angle=math.pi, pressure=0.5 | Bottom half-arc |
| 4 | `draw_arc` | cx=300, cy=100, radius=50, start_angle=math.pi, end_angle=2*math.pi, pressure=0.3 | Top half-arc (lighter, to show contrast) |
| 5 | `draw_arc` | cx=300, cy=100, radius=30, start_angle=0, end_angle=math.pi/2, pressure=0.6 | Quarter arc |

#### Section 2 -- Ellipses & S-Curves (top-right quadrant)

Using the **pencil** tool in **blue**:

| Shape | Function | Parameters | Purpose |
|-------|----------|-----------|---------|
| 6 | `draw_ellipse` | cx=570, cy=80, rx=80, ry=40, pressure=0.5 | Wide ellipse |
| 7 | `draw_ellipse` | cx=570, cy=80, rx=30, ry=60, pressure=0.5 | Tall ellipse |
| 8 | `draw_s_curve` | x1=480, y1=160, x2=700, y2=160, amplitude=40, pressure=0.4 | Horizontal S-curve |
| 9 | `draw_s_curve` | x1=480, y1=220, x2=700, y2=220, amplitude=25, pressure=0.7 | S-curve with smaller amplitude, heavier |

#### Section 3 -- Rectangles & Triangles (bottom-left quadrant)

Using the **pen** tool in **green**:

| Shape | Function | Parameters | Purpose |
|-------|----------|-----------|---------|
| 10 | `draw_rectangle` | x=40, y=320, w=150, h=100, pressure=0.5 | Medium rectangle |
| 11 | `draw_rectangle` | x=220, y=340, w=80, h=80, pressure=0.5 | Square |
| 12 | `draw_triangle` | (40, 480), (140, 560), (40, 560), pressure=0.5 | Right triangle |
| 13 | `draw_triangle` | (180, 560), (260, 460), (340, 560), pressure=0.5 | Isosceles triangle |

#### Section 4 -- Combined composition (bottom-right quadrant)

This section tests your ability to combine shapes. Use **multiple tools and colors** as specified:

| Shape | Function | Tool | Color | Parameters | Purpose |
|-------|----------|------|-------|-----------|---------|
| 14 | `draw_circle` | brush | red | cx=520, cy=400, radius=50, pressure=0.3 | Light brush circle |
| 15 | `draw_ellipse` | brush | red | cx=520, cy=400, rx=70, ry=35, pressure=0.6 | Ellipse around the circle |
| 16 | `draw_rectangle` | pen | purple | x=620, y=350, w=120, h=100, pressure=0.5 | Rectangle |
| 17 | `draw_triangle` | pen | purple | (680, 350), (620, 350), (650, 300), pressure=0.5 | Triangle sitting on top of rectangle |
| 18 | `draw_s_curve` | pencil | orange | x1=460, y1=500, x2=750, y2=500, amplitude=30, pressure=0.5 | S-curve below the shapes |
| 19 | `draw_arc` | charcoal | black | cx=680, cy=530, radius=40, start_angle=math.pi, end_angle=2*math.pi, pressure=0.6 | Upward arc using charcoal (new tool!) |

### Total strokes: 19

---

## PASS / FAIL Criteria

Your submission **passes** if ALL of the following are true:

1. **Circles**: At least 3 circles are drawn using `draw_circle` (concentric pair counts as 2).
2. **Arcs**: At least 3 arcs are drawn using `draw_arc`, including at least one quarter-arc and one half-arc.
3. **Ellipses**: At least 2 ellipses are drawn using `draw_ellipse`, one wider than tall and one taller than wide.
4. **S-curves**: At least 2 S-curves are drawn using `draw_s_curve` with different amplitudes.
5. **Rectangles**: At least 2 rectangles drawn using `draw_rectangle`, including one square (equal width and height).
6. **Triangles**: At least 2 triangles drawn using `draw_triangle`, including one right triangle and one isosceles triangle.
7. **Tool variety**: At least 4 different tools are used (pen, pencil, brush, and charcoal).
8. **Color variety**: At least 4 different colors are used.
9. **Pressure variation**: At least 3 distinct pressure values appear across the drawing.
10. **Spatial organization**: Shapes are arranged in the four quadrant layout described above -- they must not overlap incorrectly or pile up in one area.
11. **Output file**: The script produces a valid PNG at `/home/wipkat/vibed/artist2/output/lesson_02.png`.
12. **Minimum stroke count**: The drawing contains at least 19 strokes.

Your submission **fails** if any of the above are not met, or if the script raises an unhandled exception.

---

## Tips

- `draw_circle`, `draw_arc`, `draw_ellipse`, `draw_s_curve`, `draw_rectangle`, and `draw_triangle` each return a single `Stroke`. Just append them to `all_strokes`.
- Remember to `import math` so you can use `math.pi`.
- Arc angles are in radians. Use `math.pi` for half-turns.
- For the triangle function, pass the six coordinates as positional arguments: `draw_triangle(x1, y1, x2, y2, x3, y3, ...)`.
- The charcoal tool is new to you. It produces rough, textured marks -- explore how it feels compared to pen and pencil.
- Pay attention to how `amplitude` affects the shape of S-curves. A larger amplitude makes a more dramatic S.

Go shape your world.
