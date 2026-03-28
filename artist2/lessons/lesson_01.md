# Lesson 1: Line Control & Tool Exploration

## Objectives

By the end of this lesson you will be able to:

1. Draw straight lines in horizontal, vertical, and diagonal directions with precise placement.
2. Understand how three fundamental tools -- **pen**, **pencil**, and **brush** -- produce visually distinct strokes.
3. Control stroke **pressure** to create thin, medium, and heavy lines.
4. Combine tools and pressures into a structured composition.

---

## Concepts

### Tools
Every drawing tool leaves a different mark:

- **Pen** produces clean, sharp lines with consistent edges. Good for outlines and precise work.
- **Pencil** produces softer, slightly textured lines. The lighter feel is ideal for sketching.
- **Brush** produces broad, expressive strokes whose width responds strongly to pressure changes.

### Pressure
Pressure ranges from `0.0` (feather-light) to `1.0` (full force). Low pressure creates thin, faint marks; high pressure creates thick, bold marks. The effect is most dramatic with the brush tool.

### Coordinates
The canvas is 800 pixels wide and 600 pixels tall. The origin `(0, 0)` is the top-left corner. X increases to the right; Y increases downward.

---

## Assignment

Create a Python script that produces an image demonstrating your control of lines, tools, and pressure. The image should be saved to `/home/wipkat/vibed/artist2/output/lesson_01.png`.

Your script must be saved as: `/home/wipkat/vibed/artist2/output/lesson_01.py`

### Setup boilerplate

Your script should start with:

```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'artist'))

from student import *
from stylus_format import Drawing
from renderer import render_drawing
```

After creating all your strokes, combine them into a `Drawing` and render:

```python
drawing = Drawing(strokes=all_strokes, width=800, height=600)
render_drawing(drawing, "lesson_01.png")
```

### What to draw

Organize your canvas into three horizontal rows, one per tool. Each row demonstrates that tool at three different pressures.

#### Row 1 -- Pen (y = 100)

Draw three horizontal lines using the **pen** tool in **black**:

| Line | Start | End | Pressure | Label purpose |
|------|-------|-----|----------|---------------|
| 1 | (50, 80) | (250, 80) | 0.2 | Light |
| 2 | (300, 80) | (500, 80) | 0.5 | Medium |
| 3 | (550, 80) | (750, 80) | 0.9 | Heavy |

Then draw one vertical line per pressure to show you can handle both orientations:

| Line | Start | End | Pressure |
|------|-------|-----|----------|
| 4 | (150, 100) | (150, 180) | 0.2 |
| 5 | (400, 100) | (400, 180) | 0.5 |
| 6 | (650, 100) | (650, 180) | 0.9 |

#### Row 2 -- Pencil (y = 300)

Draw three horizontal lines using the **pencil** tool in **blue**:

| Line | Start | End | Pressure |
|------|-------|-----|----------|
| 7 | (50, 280) | (250, 280) | 0.2 |
| 8 | (300, 280) | (500, 280) | 0.5 |
| 9 | (550, 280) | (750, 280) | 0.9 |

Then draw three diagonal lines (top-left to bottom-right) to practice angled control:

| Line | Start | End | Pressure |
|------|-------|-----|----------|
| 10 | (50, 300) | (150, 380) | 0.2 |
| 11 | (300, 300) | (400, 380) | 0.5 |
| 12 | (550, 300) | (650, 380) | 0.9 |

#### Row 3 -- Brush (y = 500)

Draw three horizontal lines using the **brush** tool in **red**:

| Line | Start | End | Pressure |
|------|-------|-----|----------|
| 13 | (50, 480) | (250, 480) | 0.2 |
| 14 | (300, 480) | (500, 480) | 0.5 |
| 15 | (550, 480) | (750, 480) | 0.9 |

Then draw one **pressure ramp** line to show a smooth transition from light to heavy:

| Line | Start | End | Function |
|------|-------|-----|----------|
| 16 | (50, 540) | (750, 540) | `draw_pressure_ramp` |

Use the **brush** tool in **red** for the pressure ramp.

### Total strokes: 16

---

## PASS / FAIL Criteria

Your submission **passes** if ALL of the following are true:

1. **Three tools used**: The drawing contains strokes made with `pen`, `pencil`, and `brush`.
2. **Horizontal lines present**: At least 9 horizontal lines (3 per tool row).
3. **Non-horizontal lines present**: At least 3 vertical lines AND at least 3 diagonal lines.
4. **Pressure variation**: At least three distinct pressure levels are used (e.g., 0.2, 0.5, 0.9).
5. **Pressure ramp**: At least one stroke uses `draw_pressure_ramp`.
6. **Multiple colors**: At least 2 different colors are used.
7. **Output file**: The script produces a valid PNG image at `/home/wipkat/vibed/artist2/output/lesson_01.png`.
8. **Minimum stroke count**: The drawing contains at least 16 strokes.

Your submission **fails** if any of the above are not met, or if the script raises an unhandled exception.

---

## Tips

- Keep your code organized. Build a list called `all_strokes` and append each stroke to it as you go.
- Remember that `draw_line` returns a single `Stroke` object -- just append it.
- `draw_pressure_ramp` also returns a single `Stroke`.
- Double-check that you pass the correct `tool=` keyword for each row.
- Run your script and visually inspect the output. You should be able to clearly see the difference between light and heavy pressure, and between the three tools.

Good luck -- steady hands make great artists!
