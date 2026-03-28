# Lesson 4: Color Theory & Composition

## Feedback from Lesson 3

**Result: PASS**

You met all 12 criteria. The hatching swatches show clear value progression, the gradient fills work, the cube is your strongest piece -- three distinct face values with different hatching angles make it read as a solid form. The pressure ramp grounding line was a good touch. You used extend/append correctly throughout. 443 strokes is a serious amount of drawing.

**Strengths:**
- The cube is convincing. The top face reads as lightest, the right face as darkest, and the different hatching angles help the eye separate the planes. This is the first object you have drawn that genuinely looks three-dimensional.
- Gradient fills are competently executed. The charcoal gradient has a distinctly grittier texture than the pencil one, and the blue brush gradient shows you can differentiate tools by character, not just by name.
- Your code organization continues to be clean and well-commented.
- The value scale swatches in Section 1 demonstrate you understand how spacing and pressure combine to control tone.

**Weaknesses -- and I need to be direct about the sphere:**
- **The sphere does not look 3D.** It looks like a circle drawn on top of a hatched rectangle. The hatching zones extend well beyond the circle boundary, so the eye does not associate the shading with the spherical form. The core shadow reads as a dark square in the corner, not as a crescent wrapping around a curved surface. The cast shadow is a disconnected horizontal bar rather than an elliptical shape anchored to the sphere's base. The overall result is a flat diagram rather than an illusion of volume.
- **The value jumps in the hatching swatches are uneven.** Swatch 1 to swatch 2 is a gentle step, but swatch 2 to swatch 3 is an abrupt leap to much darker tone. A good value scale should have perceptually even steps.
- **Everything is still monochrome.** You have used black for all marks (except the single blue gradient). You have not yet explored how color interacts with value, or how warm and cool colors create visual contrast.
- **No compositional decision-making.** You placed objects where the lesson told you to place them. The four-quadrant layout is an instructional scaffold, not a composition. You have not yet had to decide where to place objects to create visual interest, balance, or a focal point.

These weaknesses are normal at this stage. The sphere problem in particular is a common struggle -- shading a round form with rectilinear hatching zones is genuinely difficult. But you need to understand that the technique is not yet working for that shape. The cube works because rectilinear hatching aligns naturally with flat planes. For round forms, you would need curved hatching that follows the form's contour, or much more carefully bounded hatching zones. We will not fix the sphere in this lesson -- instead, we move forward to color and composition.

---

## Objectives

By the end of this lesson you will be able to:

1. Use **color deliberately** -- choosing colors for contrast and harmony, not arbitrarily.
2. Understand **warm vs. cool colors** and how their contrast creates visual depth.
3. Apply **complementary color relationships** (red/green, blue/orange, yellow/purple) to create vibrant compositions.
4. Use **hatching, crosshatching, and gradient fills in color** -- not just black.
5. Compose a scene using the **rule of thirds** and a clear **focal point**.
6. Shade colored objects to show form, combining what you learned in Lesson 3 with deliberate color choices.

---

## Concepts

### Warm and Cool Colors

Colors divide into two families:
- **Warm colors**: red, orange, yellow, brown, pink. These advance -- they appear to come toward the viewer.
- **Cool colors**: blue, green, purple, cyan. These recede -- they appear to sit further back.

Placing a warm object against a cool background creates natural depth. A red apple on a blue cloth will pop forward. A blue vase next to a yellow lemon will create a vibrant push-pull tension.

### Complementary Colors

Complementary colors sit opposite each other on the color wheel:
- **Red and Green**
- **Blue and Orange**
- **Yellow and Purple**

When placed side by side, complementary colors intensify each other. A red apple looks *redder* against a green background. This is one of the most powerful tools in color composition.

### Value Still Matters

Color does not replace value. A red apple still needs to be shaded from light red (highlight) to dark red (shadow). You create darker versions of a color by:
- Using lower pressure (lighter/thinner marks)
- Using tighter hatching spacing (denser marks)
- Mixing in a darker version of the color or using the color's natural dark range
- For shadows on colored objects, use a darker or cooler version of the object's color, or use the complement at low pressure

In this drawing system, you control value primarily through **pressure** and **hatching density**. A red apple's shadow side uses red at higher pressure and tighter spacing. Its cast shadow might use a dark purple or brown.

### Composition: Rule of Thirds

Divide the canvas into a 3x3 grid. The four intersection points of the grid lines are called **power points** -- the eye is naturally drawn to objects placed at or near these locations. On a 900x700 canvas, the power points are approximately at:
- (300, 233) -- left-upper
- (600, 233) -- right-upper
- (300, 467) -- left-lower
- (600, 467) -- right-lower

A strong composition places the main subject near one of these points, not dead center. The remaining objects provide balance and context.

### Focal Point

Every composition needs a **focal point** -- the single area where you want the viewer's eye to go first. You create a focal point through:
- **Contrast**: The area with the strongest value or color contrast draws the eye.
- **Detail**: More detailed/dense areas attract attention over sparse areas.
- **Isolation**: An object with space around it stands out more than one crowded by neighbors.
- **Warm color**: A warm-colored object amid cool surroundings naturally becomes the focal point.

---

## Assignment

Create a Python script saved as `/home/wipkat/vibed/artist2/output/lesson_04.py` that produces `/home/wipkat/vibed/artist2/output/lesson_04.png`.

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
drawing = Drawing(strokes=all_strokes, width=900, height=700)
img = render_drawing(drawing, apply_paper=True)
output_path = os.path.join(os.path.dirname(__file__), "lesson_04.png")
img.convert("RGB").save(output_path)
print(f"Saved to {output_path}")
print(f"Total strokes: {len(all_strokes)}")
```

### What to draw

This lesson has **two parts**: a color theory study strip across the top, and a composed still life below.

---

#### Part 1 -- Color Theory Study Strip (y: 20-200)

This is your reference strip. It demonstrates warm/cool contrast and complementary pairs.

##### Exercise 1A: Warm vs. Cool Gradient Bars (x: 30-430, y: 30-100)

Draw two adjacent gradient-filled rectangles that show warm and cool gradients side by side.

| # | What | Function | Parameters | Purpose |
|---|------|----------|-----------|---------|
| 1 | Warm gradient | `draw_gradient_fill` | x=30, y=30, w=190, h=70, start_pressure=0.1, end_pressure=0.7, tool="brush", color="red" | Warm gradient from light to dark red |
| 2 | Warm bar outline | `draw_rectangle` | x=30, y=30, w=190, h=70, pressure=0.3, tool="pen", color="red" | Frame |
| 3 | Cool gradient | `draw_gradient_fill` | x=240, y=30, w=190, h=70, start_pressure=0.1, end_pressure=0.7, tool="brush", color="blue" | Cool gradient from light to dark blue |
| 4 | Cool bar outline | `draw_rectangle` | x=240, y=30, w=190, h=70, pressure=0.3, tool="pen", color="blue" | Frame |

##### Exercise 1B: Complementary Color Hatching Swatches (x: 30-860, y: 120-190)

Draw six square swatches showing three complementary pairs. Each pair uses crosshatching in both colors overlaid, creating a vibrant optical mix.

| # | What | Function | Parameters | Purpose |
|---|------|----------|-----------|---------|
| 5 | Red swatch | `draw_filled_rectangle` | x=30, y=120, w=70, h=70, tool="brush", color="red", pressure=0.5 | Solid red |
| 6 | Green swatch | `draw_filled_rectangle` | x=120, y=120, w=70, h=70, tool="brush", color="green", pressure=0.5 | Solid green -- complement of red |
| 7 | Red-green hatched | `draw_crosshatching` | x=210, y=120, w=70, h=70, spacing=6, pressure=0.4, tool="pencil", color="red" | Red layer |
| 8 | Red-green hatched | `draw_crosshatching` | x=210, y=120, w=70, h=70, spacing=8, pressure=0.3, tool="pencil", color="green" | Green layer overlaid -- observe the optical mixing |
| 9 | Blue swatch | `draw_filled_rectangle` | x=340, y=120, w=70, h=70, tool="brush", color="blue", pressure=0.5 | Solid blue |
| 10 | Orange swatch | `draw_filled_rectangle` | x=430, y=120, w=70, h=70, tool="brush", color="orange", pressure=0.5 | Solid orange -- complement of blue |
| 11 | Blue-orange hatched | `draw_crosshatching` | x=520, y=120, w=70, h=70, spacing=6, pressure=0.4, tool="pencil", color="blue" | Blue layer |
| 12 | Blue-orange hatched | `draw_crosshatching` | x=520, y=120, w=70, h=70, spacing=8, pressure=0.3, tool="pencil", color="orange" | Orange layer overlaid |
| 13 | Yellow swatch | `draw_filled_rectangle` | x=650, y=120, w=70, h=70, tool="brush", color="yellow", pressure=0.5 | Solid yellow |
| 14 | Purple swatch | `draw_filled_rectangle` | x=740, y=120, w=70, h=70, tool="brush", color="purple", pressure=0.5 | Solid purple -- complement of yellow |

Remember: `draw_filled_rectangle`, `draw_crosshatching` return **lists** -- use `extend`. `draw_rectangle` returns a single stroke -- use `append`.

##### Exercise 1C: Warm/Cool Color Strip Labels (x: 460-860, y: 30-100)

Draw two small hatched squares demonstrating colored hatching (not black).

| # | What | Function | Parameters | Purpose |
|---|------|----------|-----------|---------|
| 15 | Orange hatching | `draw_hatching` | x=460, y=30, w=70, h=70, angle_deg=45, spacing=7, pressure=0.5, tool="pencil", color="orange" | Warm-colored hatching |
| 16 | Orange box outline | `draw_rectangle` | x=460, y=30, w=70, h=70, pressure=0.2, tool="pen", color="orange" | Frame |
| 17 | Purple hatching | `draw_hatching` | x=560, y=30, w=70, h=70, angle_deg=45, spacing=7, pressure=0.5, tool="pencil", color="purple" | Cool-colored hatching -- compare visual weight to the warm orange |
| 18 | Purple box outline | `draw_rectangle` | x=560, y=30, w=70, h=70, pressure=0.2, tool="pen", color="purple" | Frame |

---

#### Part 2 -- Still Life Composition (y: 220-680)

This is the main exercise. You will compose a simple still life on a table: **a red apple, a blue vase, and a yellow lemon**. The light source is at the **top-left**, as in Lesson 3.

The composition uses the rule of thirds. The canvas area for the still life is x: 30-870, y: 220-680. The apple (the focal point) should be placed near the left-lower power point area. The vase sits to the right and slightly behind. The lemon sits between them in the foreground.

##### The Table Surface (background)

| # | What | Function | Parameters | Purpose |
|---|------|----------|-----------|---------|
| 19 | Table surface | `draw_filled_rectangle` | x=30, y=450, w=840, h=230, tool="brush", color=(180, 150, 110), pressure=0.3 | Warm beige/tan table surface |
| 20 | Table top edge | `draw_line` | (30, 450) to (870, 450), tool="pen", color="brown", pressure=0.5 | Table edge line -- the horizon of the tabletop |
| 21 | Background wash | `draw_gradient_fill` | x=30, y=220, w=840, h=230, start_pressure=0.15, end_pressure=0.05, tool="brush", color=(150, 160, 180) | Cool gray-blue background wall -- recedes behind the objects |
| 22 | Table shadow gradient | `draw_gradient_fill` | x=30, y=450, w=840, h=230, start_pressure=0.05, end_pressure=0.2, tool="brush", color="brown" | Subtle darkening toward the front of the table |

##### The Red Apple (focal point, near x=280, cy=500)

The apple is a filled circle with shading. It is the warmest, most saturated object -- the focal point.

| # | What | Function | Parameters | Purpose |
|---|------|----------|-----------|---------|
| 23 | Apple base fill | `draw_filled_circle` | cx=280, cy=500, radius=55, tool="brush", color="red", pressure=0.45 | Base red fill |
| 24 | Apple highlight zone | `draw_hatching` | x=240, y=455, w=40, h=40, angle_deg=30, spacing=10, pressure=0.15, tool="pencil", color=(255, 180, 180) | Light pink hatching on the highlight side (top-left) |
| 25 | Apple midtone | `draw_hatching` | x=250, y=475, w=60, h=50, angle_deg=45, spacing=7, pressure=0.35, tool="pencil", color=(180, 30, 30) | Deeper red for the middle zone |
| 26 | Apple shadow | `draw_crosshatching` | x=280, y=495, w=50, h=50, spacing=5, pressure=0.6, tool="pencil", color=(120, 20, 20) | Dark red crosshatching for the shadow side |
| 27 | Apple outline | `draw_circle` | cx=280, cy=500, radius=55, tool="pen", color=(130, 20, 20), pressure=0.4 | Contour line in dark red |
| 28 | Apple cast shadow | `draw_hatching` | x=260, y=555, w=80, h=15, angle_deg=0, spacing=4, pressure=0.35, tool="pencil", color=(100, 80, 60) | Horizontal cast shadow on the table |
| 29 | Apple stem | `draw_line` | (280, 447) to (285, 435), tool="pen", color="brown", pressure=0.4 | Small stem at the top |

##### The Blue Vase (x=560, cy=460, tall form)

The vase is a tall, cool-colored form. It contrasts with the warm apple and sits further right, providing balance.

| # | What | Function | Parameters | Purpose |
|---|------|----------|-----------|---------|
| 30 | Vase body fill | `draw_filled_rectangle` | x=525, y=380, w=70, h=150, tool="brush", color="blue", pressure=0.4 | Base blue fill for the vase body |
| 31 | Vase top ellipse | `draw_ellipse` | cx=560, cy=380, rx=35, ry=10, tool="pen", color=(30, 30, 150), pressure=0.4 | Elliptical opening at top |
| 32 | Vase bottom ellipse | `draw_ellipse` | cx=560, cy=530, rx=35, ry=8, tool="pen", color=(30, 30, 150), pressure=0.4 | Base of the vase |
| 33 | Vase left edge | `draw_line` | (525, 380) to (525, 530), tool="pen", color=(30, 30, 150), pressure=0.45 | Left contour |
| 34 | Vase right edge | `draw_line` | (595, 380) to (595, 530), tool="pen", color=(30, 30, 150), pressure=0.45 | Right contour |
| 35 | Vase highlight | `draw_hatching` | x=530, y=390, w=25, h=120, angle_deg=90, spacing=10, pressure=0.15, tool="pencil", color=(140, 140, 255) | Light blue vertical hatching on the left (highlight side) |
| 36 | Vase shadow | `draw_crosshatching` | x=565, y=390, w=25, h=120, spacing=5, pressure=0.55, tool="pencil", color=(20, 20, 100) | Dark blue crosshatching on the right (shadow side) |
| 37 | Vase cast shadow | `draw_hatching` | x=555, y=530, w=70, h=15, angle_deg=0, spacing=4, pressure=0.3, tool="pencil", color=(80, 70, 60) | Cast shadow on table, pushed to the right |

##### The Yellow Lemon (x=420, cy=530, small foreground object)

The lemon is a small, warm-colored ellipse sitting between the apple and vase in the foreground.

| # | What | Function | Parameters | Purpose |
|---|------|----------|-----------|---------|
| 38 | Lemon base fill | `draw_filled_circle` | cx=420, cy=530, radius=30, tool="brush", color="yellow", pressure=0.4 | Base yellow fill |
| 39 | Lemon highlight | `draw_hatching` | x=395, y=508, w=25, h=20, angle_deg=30, spacing=9, pressure=0.1, tool="pencil", color=(255, 255, 200) | Pale yellow highlight top-left |
| 40 | Lemon shadow | `draw_hatching` | x=420, y=525, w=30, h=30, angle_deg=45, spacing=6, pressure=0.45, tool="pencil", color=(180, 160, 0) | Darker yellow-ochre shadow |
| 41 | Lemon outline | `draw_ellipse` | cx=420, cy=530, rx=35, ry=22, tool="pen", color=(160, 140, 0), pressure=0.35 | Lemon is slightly wider than tall -- a lemon shape |
| 42 | Lemon cast shadow | `draw_hatching` | x=415, y=553, w=40, h=10, angle_deg=0, spacing=4, pressure=0.3, tool="pencil", color=(100, 80, 50) | Small cast shadow |

##### Final Touches

| # | What | Function | Parameters | Purpose |
|---|------|----------|-----------|---------|
| 43 | Table front edge | `draw_pressure_ramp` | (30, 680) to (870, 680), tool="pen", color="brown" | Grounding line along the bottom with pressure variation |

---

## Important Reminders

- `draw_filled_rectangle`, `draw_filled_circle`, `draw_hatching`, `draw_crosshatching`, `draw_gradient_fill` all return **lists** of strokes. Use `all_strokes.extend(...)`.
- `draw_line`, `draw_circle`, `draw_ellipse`, `draw_rectangle`, `draw_pressure_ramp` return a **single** stroke. Use `all_strokes.append(...)`.
- **RGB tuples** like `(180, 150, 110)` can be used as the `color` parameter alongside named colors like `"red"`.
- The canvas is **900 wide by 700 tall** -- larger than previous lessons.
- Think about **layer order**: draw backgrounds first, then objects, then outlines and shadows last so they sit on top.

---

## PASS / FAIL Criteria

Your submission **passes** if ALL of the following are true:

1. **Warm/cool gradients**: At least 2 gradient fills are drawn in different colors (one warm, one cool), showing smooth tonal transitions.
2. **Complementary color swatches**: At least 3 complementary pairs are shown as filled rectangles (6 swatches total), with at least one pair demonstrating overlaid colored crosshatching.
3. **Colored hatching**: At least 2 hatching or crosshatching fills use a non-black color (e.g., red, blue, orange, purple), demonstrating that hatching can create tone in color, not just in grayscale.
4. **Still life present**: The composition includes at least 3 distinct objects (apple, vase, lemon or equivalent) placed on a table surface, each drawn in a different color.
5. **Warm focal point**: The warmest/most saturated object (the apple) is positioned as the visual focal point -- not dead center on the canvas, but offset according to rule-of-thirds placement.
6. **Shading on each object**: Every object in the still life has at least a highlight zone and a shadow zone, created through hatching/crosshatching at different pressures and/or spacings. No object is a flat, uniform fill.
7. **Cast shadows**: At least 2 objects have visible cast shadows on the table surface.
8. **Background/foreground separation**: There is a visible background (wall) and foreground (table) that differ in color temperature or value, creating spatial depth.
9. **Tool variety**: At least 3 different tools are used across the entire drawing.
10. **Color variety**: At least 6 distinct colors or RGB tuples are used across the drawing.
11. **extend vs append**: The script uses `extend` for list-returning functions and `append` for single-stroke functions. A TypeError is an automatic FAIL.
12. **Output file**: The script produces a valid PNG at `/home/wipkat/vibed/artist2/output/lesson_04.png` at 900x700 canvas size.
13. **Minimum stroke count**: The drawing contains at least 80 strokes total.

Your submission **fails** if any of the above are not met, or if the script raises an unhandled exception.

---

## Tips

- **Layer order matters.** Draw the background and table first, then the objects, then outlines and shadows. If you draw the background last, it will cover your objects.
- **Color value is not the same as brightness.** Yellow is inherently a light-valued color. Red is mid-value. Blue is dark-value. This means yellow objects need less shadow hatching to look right, while blue objects can tolerate denser hatching without looking overworked.
- **Use the object's own color for shading, not black.** A red apple's shadow should be dark red, not black hatching over red. Black hatching on top of color looks muddy and dead. Use RGB tuples to create darker versions of each color.
- **Complementary shadows**: A subtle technique is to add a hint of an object's complementary color into its shadow. A red apple might have a tiny bit of green in its deepest shadow. This makes shadows feel more alive. This is optional but encouraged.
- **The table surface is not just "brown."** Use a warm neutral like `(180, 150, 110)` and add subtle color variation with the gradient fill.
- **Remember extend vs append.** This is still the most common error. Every `draw_filled_*`, `draw_hatching`, `draw_crosshatching`, and `draw_gradient_fill` call needs `extend`.

Show me some color.
