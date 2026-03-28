# Lesson 3: Shading, Hatching & Value

## Feedback from Lesson 2

**Result: PASS**

Good progress. You met every criterion and, importantly, you showed creative initiative this time -- the center dot in the concentric circles, the fading ripple S-curve, the inner rectangle for depth, and the mirrored charcoal arc were all your own additions. That is exactly the kind of experimentation I want to see. You are no longer just following a coordinate table; you are starting to make compositional decisions.

**Strengths:**
- All 12 pass criteria met. 23 strokes produced (19 required, 4 creative extras).
- Four-quadrant layout is clean and readable. Each section is visually distinct.
- Creative additions demonstrate emerging spatial intuition -- the fading S-curve at pressure 0.2 echoing below the heavier ones shows you understand how pressure creates visual hierarchy.
- Code is well-organized with clear comments. The "scene" metaphor in Section 4 (sun, house, ground) shows you are beginning to think in terms of subject matter rather than just shapes.
- Charcoal tool used for the first time; the mirror-arc in gray at low pressure was a thoughtful contrast.

**Areas for improvement:**
- **Flat shapes**: Every shape you have drawn so far is an outline. Nothing has volume, weight, or dimension. A circle is just a ring -- it does not read as a sphere. A rectangle is just four lines -- it does not read as a surface. This is the single biggest gap in your work right now.
- **No tonal range**: You have used pressure to vary line weight, but you have never created a *value* -- a region of tone that suggests light falling on a form. Your drawings look like coloring-book outlines waiting to be filled.
- **Uniform line confidence**: All your lines have the same mechanical evenness. Real drawing involves deliberate variation -- lighter marks for construction, heavier marks for definition, soft gradients for shadow.
- **The "house" in Section 4 is naive**: Triangle + rectangle = house is a beginner cliche. That is fine for Lesson 2, but going forward I expect you to move beyond symbolic shapes toward observed form.

---

## Objectives

By the end of this lesson you will be able to:

1. Use `draw_hatching` to create parallel-line tone within a bounded region.
2. Use `draw_crosshatching` to create denser, richer tone by layering hatching at multiple angles.
3. Use `draw_gradient_fill` to create smooth tonal transitions from light to dark.
4. Use `draw_pressure_ramp` to create individual strokes with controlled value variation.
5. Apply shading to simple forms (sphere, cube) to suggest three-dimensional volume.
6. Understand the concept of a **light source direction** and how it determines where shadows fall.

---

## Concepts

### Value

**Value** is how light or dark a mark is. In drawing, value is the primary tool for creating the illusion of three-dimensional form on a two-dimensional surface. A flat circle becomes a sphere when you add a gradient from light to dark across its surface. A flat rectangle becomes a face of a cube when adjacent faces have different values.

Value is controlled by:
- **Pressure**: Higher pressure = darker mark
- **Density**: More lines packed together = darker area
- **Tool choice**: Charcoal and brush can produce broader, softer darks; pen and pencil produce finer marks

### Hatching

**Hatching** is a technique where you draw parallel lines close together to create tone. The closer the lines (smaller `spacing`), the darker the area appears. The `angle_deg` parameter rotates the lines -- 0 degrees is horizontal, 45 degrees is diagonal, 90 degrees is vertical.

`draw_hatching(x, y, w, h, angle_deg, spacing, tool, color, pressure)` returns a **list** of strokes (not a single stroke). Use `all_strokes.extend(...)` instead of `all_strokes.append(...)`.

### Crosshatching

**Crosshatching** layers hatching at two or more angles. The overlapping lines create a denser, richer tone than a single layer of hatching. By default, `draw_crosshatching` uses 45 and -45 degree lines, but you can specify any angles.

`draw_crosshatching(x, y, w, h, angles, spacing, tool, color, pressure)` also returns a **list** of strokes.

### Gradient Fill

`draw_gradient_fill(x, y, w, h, start_pressure, end_pressure, tool, color, spacing)` fills a rectangular region with horizontal lines whose pressure transitions smoothly from `start_pressure` at the top to `end_pressure` at the bottom. This creates a smooth tonal gradient. It returns a **list** of strokes.

### Pressure Ramp

You used `draw_pressure_ramp` in Lesson 1. It draws a single line that smoothly ramps pressure up and then back down, creating a swell. This is useful for expressive contour lines that feel alive rather than mechanical.

### Light Direction

When shading a form, you must decide where the light is coming from. In this lesson, the light source is at the **top-left**. This means:
- Surfaces facing up-left are **lightest** (lowest pressure, widest hatching spacing)
- Surfaces facing down-right are **darkest** (highest pressure, tightest hatching spacing)
- A sphere will have its lightest area at the top-left and a crescent of shadow sweeping toward the bottom-right
- A cube's top face is lightest, front face is medium, and right face is darkest

---

## Assignment

Create a Python script saved as `/home/wipkat/vibed/artist2/output/lesson_03.py` that produces `/home/wipkat/vibed/artist2/output/lesson_03.png`.

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
output_path = os.path.join(os.path.dirname(__file__), "lesson_03.png")
img.convert("RGB").save(output_path)
print(f"Saved to {output_path}")
print(f"Total strokes: {len(all_strokes)}")
```

### What to draw

Organize the canvas into four sections. This lesson is about tone and value, not color -- use **black** for all marks unless otherwise specified. Tool choices are specified for each exercise.

#### Section 1 -- Hatching & Crosshatching Swatches (top-left quadrant, y: 20-280)

Create a row of five rectangular tone swatches that demonstrate increasing density. Think of these as value scales -- like a painter mixing progressively darker shades of gray.

Using the **pencil** tool in **black**:

| # | What | Function | Parameters | Purpose |
|---|------|----------|-----------|---------|
| 1 | Swatch outline | `draw_rectangle` | x=30, y=40, w=80, h=100, pressure=0.3, tool="pen" | Light border for first swatch |
| 2 | Light hatching | `draw_hatching` | x=30, y=40, w=80, h=100, angle_deg=45, spacing=12, pressure=0.2, tool="pencil" | Very light tone -- wide spacing, low pressure |
| 3 | Swatch outline | `draw_rectangle` | x=130, y=40, w=80, h=100, pressure=0.3, tool="pen" | Border for second swatch |
| 4 | Medium hatching | `draw_hatching` | x=130, y=40, w=80, h=100, angle_deg=45, spacing=8, pressure=0.4, tool="pencil" | Medium tone -- tighter spacing |
| 5 | Swatch outline | `draw_rectangle` | x=230, y=40, w=80, h=100, pressure=0.3, tool="pen" | Border for third swatch |
| 6 | Dense hatching | `draw_hatching` | x=230, y=40, w=80, h=100, angle_deg=45, spacing=5, pressure=0.6, tool="pencil" | Darker tone -- dense spacing, higher pressure |
| 7 | Swatch outline | `draw_rectangle` | x=30, y=170, w=80, h=100, pressure=0.3, tool="pen" | Border for fourth swatch |
| 8 | Light crosshatching | `draw_crosshatching` | x=30, y=170, w=80, h=100, spacing=10, pressure=0.3, tool="pencil" | Crosshatching at default angles (45, -45) |
| 9 | Swatch outline | `draw_rectangle` | x=130, y=170, w=80, h=100, pressure=0.3, tool="pen" | Border for fifth swatch |
| 10 | Dense crosshatching | `draw_crosshatching` | x=130, y=170, w=80, h=100, spacing=5, pressure=0.5, tool="pencil" | Heavy crosshatching -- very dark tone |

**Important**: `draw_hatching` and `draw_crosshatching` return a **list** of strokes. Use `all_strokes.extend(...)` for these, not `append`.

#### Section 2 -- Gradient Fills (top-right quadrant, y: 20-280)

Demonstrate smooth tonal gradients using `draw_gradient_fill`.

| # | What | Function | Parameters | Purpose |
|---|------|----------|-----------|---------|
| 11 | Gradient light-to-dark | `draw_gradient_fill` | x=430, y=40, w=140, h=100, start_pressure=0.05, end_pressure=0.8, tool="pencil" | Smooth gradient, light at top to dark at bottom |
| 12 | Gradient outline | `draw_rectangle` | x=430, y=40, w=140, h=100, pressure=0.3, tool="pen" | Thin border to frame the gradient |
| 13 | Gradient dark-to-light | `draw_gradient_fill` | x=600, y=40, w=140, h=100, start_pressure=0.8, end_pressure=0.05, tool="pencil" | Reversed gradient |
| 14 | Gradient outline | `draw_rectangle` | x=600, y=40, w=140, h=100, pressure=0.3, tool="pen" | Border |
| 15 | Charcoal gradient | `draw_gradient_fill` | x=430, y=170, w=140, h=100, start_pressure=0.1, end_pressure=0.9, tool="charcoal" | Same gradient but with charcoal -- notice the rougher texture |
| 16 | Gradient outline | `draw_rectangle` | x=430, y=170, w=140, h=100, pressure=0.3, tool="pen" | Border |
| 17 | Brush gradient | `draw_gradient_fill` | x=600, y=170, w=140, h=100, start_pressure=0.1, end_pressure=0.7, tool="brush", color="blue" | Gradient with brush in blue -- see how tool affects the fill character |
| 18 | Gradient outline | `draw_rectangle` | x=600, y=170, w=140, h=100, pressure=0.3, tool="pen" | Border |

**Again**: `draw_gradient_fill` returns a **list**. Use `extend`.

#### Section 3 -- Shaded Sphere (bottom-left quadrant, y: 310-580)

This is the core exercise. You will shade a circle to make it look like a three-dimensional sphere. The light source is at the **top-left**.

Using the **pencil** tool in **black** unless otherwise noted:

| # | What | Function | Parameters | Purpose |
|---|------|----------|-----------|---------|
| 19 | Sphere outline | `draw_circle` | cx=150, cy=440, radius=90, pressure=0.4, tool="pen" | The sphere's contour |
| 20 | Light hatching (top-left highlight zone) | `draw_hatching` | x=80, y=365, w=70, h=70, angle_deg=45, spacing=14, pressure=0.15, tool="pencil" | Very light tone in the highlight area |
| 21 | Medium hatching (middle transitional zone) | `draw_hatching` | x=100, y=400, w=100, h=80, angle_deg=45, spacing=8, pressure=0.35, tool="pencil" | Medium tone across the center |
| 22 | Dense hatching (lower-right shadow zone) | `draw_hatching` | x=140, y=440, w=80, h=80, angle_deg=45, spacing=5, pressure=0.55, tool="pencil" | Darker tone in the shadow area |
| 23 | Crosshatch darkest area (core shadow) | `draw_crosshatching` | x=160, y=460, w=60, h=55, angle_deg=45, spacing=4, pressure=0.7, tool="pencil" | Darkest value at the bottom-right -- the core shadow |
| 24 | Cast shadow | `draw_hatching` | x=170, y=530, w=100, h=20, angle_deg=0, spacing=4, pressure=0.5, tool="pencil" | Horizontal hatching below the sphere suggesting a cast shadow on the ground |

Note: The hatching will extend beyond the sphere's outline. This is acceptable for now -- clipping to a circular boundary is an advanced technique. The layered hatching zones at different densities will still read as a shaded sphere.

#### Section 4 -- Shaded Cube (bottom-right quadrant, y: 310-580)

Draw a simple cube (three visible faces) and shade each face to a different value to suggest three-dimensional form. Light source is at the **top-left**.

The cube is drawn in a simple isometric-like view with three visible faces: top, front (left-facing), and right side.

Using **pen** for outlines and **pencil** for shading:

| # | What | Function | Parameters | Purpose |
|---|------|----------|-----------|---------|
| 25 | Top face outline | `draw_line` | (530,370) to (630,340), pressure=0.5, tool="pen" | Top-right edge |
| 26 | Top face outline | `draw_line` | (630,340) to (730,370), pressure=0.5, tool="pen" | Top edge continues |
| 27 | Top face outline | `draw_line` | (730,370) to (630,400), pressure=0.5, tool="pen" | Back to front |
| 28 | Top face outline | `draw_line` | (630,400) to (530,370), pressure=0.5, tool="pen" | Close the top face |
| 29 | Front face outline | `draw_line` | (530,370) to (530,490), pressure=0.5, tool="pen" | Left vertical edge |
| 30 | Front face outline | `draw_line` | (530,490) to (630,520), pressure=0.5, tool="pen" | Bottom edge |
| 31 | Front face outline | `draw_line` | (630,520) to (630,400), pressure=0.5, tool="pen" | Right vertical edge of front face |
| 32 | Right face outline | `draw_line` | (630,400) to (730,370), pressure=0.5, tool="pen" | Already drawn but establishes the top of right face |
| 33 | Right face outline | `draw_line` | (730,370) to (730,490), pressure=0.5, tool="pen" | Right vertical edge |
| 34 | Right face outline | `draw_line` | (730,490) to (630,520), pressure=0.5, tool="pen" | Bottom edge of right face |
| 35 | Top face shading (lightest) | `draw_hatching` | x=540, y=345, w=180, h=50, angle_deg=30, spacing=14, pressure=0.15, tool="pencil" | Very light hatching -- this face catches the most light |
| 36 | Front face shading (medium) | `draw_hatching` | x=530, y=375, w=100, h=140, angle_deg=75, spacing=7, pressure=0.35, tool="pencil" | Medium tone -- indirect light |
| 37 | Right face shading (darkest) | `draw_hatching` | x=630, y=375, w=100, h=140, angle_deg=45, spacing=5, pressure=0.55, tool="pencil" | Darkest face -- turned away from light |
| 38 | Pressure ramp accent line | `draw_pressure_ramp` | (530,490) to (730,490), tool="pen" | A pressure-ramped line along the bottom to ground the cube -- thickens in the middle for visual weight |

### Important notes on `extend` vs `append`

The functions that fill regions (`draw_hatching`, `draw_crosshatching`, `draw_gradient_fill`, `draw_filled_circle`, `draw_filled_rectangle`) all return a **list** of strokes. You must use:

```python
all_strokes.extend(draw_hatching(...))
```

The functions that draw a single outline or line (`draw_circle`, `draw_line`, `draw_rectangle`, `draw_arc`, `draw_triangle`, `draw_s_curve`, `draw_pressure_ramp`) return a **single** stroke. Use:

```python
all_strokes.append(draw_circle(...))
```

Mixing these up will cause errors. Pay careful attention.

---

## PASS / FAIL Criteria

Your submission **passes** if ALL of the following are true:

1. **Hatching swatches**: At least 3 hatching fills are drawn with visibly different spacing values (e.g., 12, 8, 5), creating a clear progression from light to dark tone.
2. **Crosshatching**: At least 2 crosshatching fills are drawn, one lighter and one darker than single-direction hatching alone.
3. **Gradient fills**: At least 3 gradient fills are drawn using `draw_gradient_fill`, including at least one light-to-dark and one dark-to-light transition, and at least two different tools are used for gradients.
4. **Shaded sphere**: A circle is drawn and shaded with at least 3 overlapping hatching zones of increasing density (from highlight to core shadow), creating a visible illusion of roundness. A cast shadow is present below the sphere.
5. **Shaded cube**: A cube is drawn with at least 3 visible faces, each shaded to a different value. The top face must be lightest and the right face darkest, consistent with a top-left light source.
6. **Pressure ramp**: At least 1 pressure ramp stroke is used.
7. **extend vs append**: The script must use `extend` for list-returning functions and `append` for single-stroke functions. A TypeError from appending a list as a single element is an automatic FAIL.
8. **Tool variety**: At least 3 different tools are used across the drawing.
9. **Value range**: The drawing contains marks at pressures spanning from at most 0.2 (light) to at least 0.6 (dark), demonstrating a full tonal range.
10. **Spatial organization**: The four sections are clearly separated and do not overlap.
11. **Output file**: The script produces a valid PNG at `/home/wipkat/vibed/artist2/output/lesson_03.png`.
12. **Minimum stroke count**: The drawing contains at least 50 strokes total (hatching generates many strokes from a single call).

Your submission **fails** if any of the above are not met, or if the script raises an unhandled exception.

---

## Tips

- `draw_hatching` and `draw_crosshatching` return **lists** of strokes. This is the most common mistake in this lesson. Double-check every call.
- When hatching overlaps a circular form, the hatching lines will extend outside the circle outline. This is normal -- your eye will still read the shaded region within the circle as a form. Do not try to clip the hatching.
- Spacing controls apparent darkness more than pressure alone. A spacing of 5 with pressure 0.3 can look darker than a spacing of 14 with pressure 0.6. Experiment with both.
- For the sphere, think of the hatching zones as concentric crescents: a small light zone at the top-left, a larger medium zone in the middle, and a dense dark zone at the bottom-right.
- For the cube, use different hatching angles on each face. This helps the eye distinguish the faces even apart from the value difference.
- The charcoal tool produces rougher, grittier fills than pencil. Compare how the same gradient looks with different tools.

Show me some depth.
