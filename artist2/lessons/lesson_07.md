# Lesson 7: Abstract & Expressive Art

## Feedback from Lesson 6

**Result: PASS**

You built three faces. They have correct proportions, distinguishable expressions, convincing hair, and you engineered a parameterized portrait function that is the most sophisticated code architecture you have produced. The happy face smiles. The sad face frowns. The contemplative face gazes sideways. Someone looking at your image can tell which face is which. That is the fundamental test, and you passed it.

**Strengths:**

- **Expressions are readable.** The mouth-eyebrow-eye triangle works across all three portraits. The happy face has an upturned smile with crow's feet and arched brows. The sad face has a downturned mouth with worried brows angled inward-upward and heavy drooping eyelids. The contemplative face has a neutral closed mouth, level brows, and a sideward gaze. These are clearly three different emotions.

- **Eye highlights are excellent.** The tiny white dots in each iris (1.2px radius, offset upper-left) are small but transformative. Without them, the eyes are flat colored circles. With them, the eyes look wet and alive. You noted this in your SKILLS.md and applied it consistently. The contemplative portrait's sideward gaze -- iris shifted 2px right -- is a particularly effective detail.

- **Tool selection serves expression.** Marker for happy eyebrows (bold, confident). Charcoal for sad eyebrows (heavy, rough, emotionally weighted). Pencil for contemplative eyebrows (quiet, even, understated). You are no longer just using tools because they exist -- you are choosing them because their texture matches the emotional content.

- **Hair styles are genuinely varied.** Wavy S-curves, straight vertical lines, curly overlapping circles -- three distinctly different approaches, each using charcoal for mass and pencil for highlights. The curly hair's grid-bounded circles with a distance check against the head radius shows spatial thinking.

- **The parameterized function is strong engineering.** One function, four parameters (expression, hair_style, eye_color, hair_color), three completely different outputs. This enables experimentation without rewriting the portrait each time.

**Weaknesses -- and why they matter for what comes next:**

- **The faces do not quite look like faces yet.** Proportions are correct. Features are present. But the overall effect is folk art or naive illustration rather than portraiture. The head outlines are perfect mathematical ellipses. Real faces have subtle angularity -- the jaw narrows, the forehead has a brow ridge, the temples indent slightly. Your faces are smooth ovals with features placed on them. This is a limitation of the tool set as much as of skill, but it is honest.

- **Shading is identical across all three expressions.** This is the biggest missed opportunity. Every face gets the same shadow-side hatching, the same under-nose shadow, the same jaw shadow, at the same positions and pressures. But a smiling face and a frowning face have different surface geometry -- smiling pushes the cheeks up, creating new shadow zones around the nasolabial folds. You drew the smile creases but did not shade around them. The shading should respond to the expression, not be applied uniformly.

- **The hair overwhelms the face.** In all three portraits, the hair is the dominant visual element. The wavy hair's S-curves cascade below the eyes. The straight hair falls past the mouth on both sides. For a study about expression, the face should be the star. The hair is supporting cast. Reduce its visual weight or increase the face's.

- **The boundary problem persists.** Six lessons in, and rectangular hatching zones still extend beyond curved outlines. The shadow-side hatching is a rectangle that pokes past the head ellipse. This is the longest-running weakness in your work.

None of these weaknesses will hold you back from what we are doing next. In fact, the next lesson does not care about representational accuracy at all.

---

## Objectives

By the end of this lesson you will be able to:

1. Create **abstract compositions** that communicate mood and emotion through pure visual elements -- color, form, texture, rhythm -- without depicting recognizable objects.
2. Use **all available tools expressively**, choosing each tool for its textural character rather than its technical capability.
3. Apply **color as emotion**: warm palettes (reds, oranges, yellows) for energy and intensity; cool palettes (blues, greens, purples) for calm and introspection.
4. Create **visual rhythm and movement** through repeated marks, directional lines, and compositional flow.
5. Compose **two contrasting abstract panels** side by side that read as emotional opposites.

---

## Concepts

### What Is Abstract Art?

Abstract art does not depict things. It uses the same visual elements you have been learning -- line, shape, color, value, texture -- but frees them from the job of representing real objects. A curved line does not have to be a smile or a hill. It can just be a curved line, and that curve can feel gentle, or tense, or joyful, depending on its weight, speed, and context.

You have been building toward this. Every lesson taught you a visual element:
- **Lines** (Lesson 1) -- direction, weight, speed
- **Shapes** (Lesson 2) -- geometry, enclosure, rhythm
- **Value** (Lesson 3) -- light and dark, depth, volume
- **Color** (Lesson 4) -- temperature, contrast, harmony
- **Composition** (Lesson 5) -- arrangement, depth, leading the eye
- **Expression** (Lesson 6) -- emotion through visual choices

Now you use all of them at once, with no subject to hide behind. The composition IS the subject.

### Expressive Mark-Making

Each tool in your kit has a distinct character. In representational work, you chose tools to match what you were drawing (pen for sharp outlines, charcoal for rough texture). In abstract work, you choose tools to match what you are FEELING:

| Tool | Expressive Character | Use For |
|------|---------------------|---------|
| **Charcoal** | Raw, gritty, primal, unstable | Energy, chaos, tension, emotional weight |
| **Brush** | Fluid, smooth, sweeping, soft | Calm, flow, breath, gentle transitions |
| **Marker** | Bold, graphic, decisive, heavy | Impact, emphasis, anchoring, declaration |
| **Pen** | Precise, sharp, controlled, brittle | Structure, fine detail, tension lines, cracks |
| **Pencil** | Quiet, subtle, intimate, soft | Whisper, delicacy, background atmosphere, meditation |

In an "energy/chaos" composition, charcoal and marker should dominate. In a "calm/serenity" composition, brush and pencil should lead.

### Color as Emotion

Color theory is not just about complementary pairs and warm/cool contrast. Color carries emotional weight:

**Warm palette (energy, chaos, passion, urgency):**
- Reds: (220, 40, 30), (180, 20, 15), (255, 80, 50)
- Oranges: (240, 130, 30), (200, 100, 20), (255, 160, 60)
- Yellows: (250, 220, 40), (240, 200, 20), (255, 240, 100)
- Accents of dark: (40, 20, 15), (60, 30, 20) -- charcoal marks over warm color add grit

**Cool palette (calm, serenity, reflection, stillness):**
- Blues: (70, 120, 180), (40, 80, 140), (100, 150, 200), (30, 60, 110)
- Blue-greens: (50, 140, 130), (70, 160, 150), (90, 180, 170)
- Soft purples: (120, 100, 160), (140, 120, 180), (100, 80, 140)
- Whites and pale tones: (220, 230, 240), (200, 215, 230), (240, 240, 250)
- Accents of warm gray: (160, 150, 145), (140, 135, 130) -- grounding without disrupting calm

### Composition Without Subject

Without a recognizable subject (apple, tree, face), what holds an abstract composition together? These principles:

1. **Focal area**: Even abstract art needs somewhere for the eye to land first. Create this with the highest contrast, the densest marks, or the most intense color.
2. **Movement/flow**: Direct the eye through the composition with line direction, color gradients, or repeated shapes. In a chaos composition, the flow should feel explosive, radiating outward. In a calm composition, the flow should feel horizontal, gently undulating.
3. **Rhythm**: Repeated marks or shapes at varied intervals create visual rhythm -- fast rhythm (tight spacing) for energy, slow rhythm (wide spacing) for calm.
4. **Balance**: Even asymmetrical compositions need visual balance. A heavy dark cluster on one side needs SOMETHING on the other -- a smaller bright accent, a trailing line, a fading gradient.
5. **Breathing room**: Not every square pixel needs to be filled. Empty space (negative space) is as important as marked space. Chaos needs areas of relative calm as contrast. Calm needs a small point of tension to keep it alive.

---

## Assignment

Create a Python script saved as `/home/wipkat/vibed/artist2/output/lesson_07.py` that produces `/home/wipkat/vibed/artist2/output/lesson_07.png`.

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
drawing = Drawing(strokes=all_strokes, width=1000, height=500)
img = render_drawing(drawing, apply_paper=True)
output_path = os.path.join(os.path.dirname(__file__), "lesson_07.png")
img.convert("RGB").save(output_path)
print(f"Saved to {output_path}")
print(f"Total strokes: {len(all_strokes)}")
```

### What to draw

**Two abstract compositions** side by side on a 1000x500 canvas (wide format). The left panel (approximately x: 0-490) conveys **"energy / chaos"**. The right panel (approximately x: 510-1000) conveys **"calm / serenity"**. A narrow gap or transitional zone separates them.

This is YOUR art. You decide everything about it. There are no prescribed coordinates, no stroke-by-stroke tables, no "draw a circle here." The only constraints are the emotional targets and the pass criteria below.

---

#### Panel 1: Energy / Chaos (Left Half)

Create a composition that FEELS energetic, chaotic, explosive, or intense. Think of: a storm, an argument, a heartbeat, a fire, a collision. Not that you are drawing any of those things -- but that your marks carry that energy.

Suggestions (not requirements):
- **Dominant tools**: charcoal and marker for raw, bold marks
- **Color palette**: warm -- reds, oranges, yellows, with dark accents
- **Line quality**: aggressive, varied pressure, rapid direction changes, crossing lines
- **Shapes**: fragmented, overlapping, colliding, sharp angles
- **Texture**: dense crosshatching, heavy hatching at tight spacing, layered marks
- **Composition**: radiating from a focal point, explosive outward movement, off-balance
- Consider: jagged S-curves, clustered filled shapes, pressure ramps that spike, overlapping arcs at different angles, dense crosshatching zones at varied orientations

#### Panel 2: Calm / Serenity (Right Half)

Create a composition that FEELS calm, serene, peaceful, or contemplative. Think of: still water, a deep breath, fog, dusk, silence. Not that you are drawing any of those things -- but that your marks carry that stillness.

Suggestions (not requirements):
- **Dominant tools**: brush and pencil for soft, gentle marks
- **Color palette**: cool -- blues, blue-greens, soft purples, with pale accents
- **Line quality**: smooth, even pressure, gradual curves, horizontal tendency
- **Shapes**: rounded, spaced apart, floating, gentle ellipses
- **Texture**: widely spaced hatching, soft gradients, minimal crosshatching
- **Composition**: horizontal flow, centered balance, generous empty space
- Consider: gentle S-curves with low amplitude, gradient fills that fade, widely spaced parallel hatching, floating ellipses, arcs that suggest breath or waves

#### The Transition

Where the two panels meet (around x=490-510), consider how one mood transitions to the other. This could be:
- A hard dividing line (pen or marker, vertical)
- A gradual blend where warm colors cool and marks soften
- An intentional gap of blank canvas
- A zone where both palettes intermingle briefly

Your choice. Make it deliberate.

---

## Important Reminders

- `draw_filled_rectangle`, `draw_filled_circle`, `draw_hatching`, `draw_crosshatching`, `draw_gradient_fill` all return **lists** of strokes. Use `all_strokes.extend(...)`.
- `draw_line`, `draw_circle`, `draw_ellipse`, `draw_rectangle`, `draw_pressure_ramp`, `draw_arc`, `draw_s_curve`, `draw_triangle`, `draw_curve` return a **single** stroke. Use `all_strokes.append(...)`.
- **RGB tuples** work as color parameters.
- Canvas is **1000 wide by 500 tall**.
- Layer order matters: background first, then middle layers, then foreground marks on top.
- This is abstract art -- there are no "wrong" shapes or placements. But there ARE wrong moods. If your chaos panel feels calm, or your calm panel feels chaotic, that is a failure.

---

## PASS / FAIL Criteria

Your submission **passes** if ALL of the following are true:

1. **Two distinct panels present**: The canvas is visibly divided into two compositional areas (left and right), each occupying roughly half the canvas. They must not blend into a single uniform composition.
2. **Left panel reads as "energy/chaos"**: The left panel uses predominantly warm colors (reds, oranges, yellows -- at least 3 distinct warm hues), aggressive or varied mark-making, and compositional elements that suggest movement, tension, or intensity. A viewer should not describe this panel as "calm."
3. **Right panel reads as "calm/serenity"**: The right panel uses predominantly cool colors (blues, greens, purples -- at least 3 distinct cool hues), soft or gentle mark-making, and compositional elements that suggest stillness, peace, or rest. A viewer should not describe this panel as "chaotic."
4. **Warm palette in left panel (5+ warm colors)**: At least 5 distinct warm-family RGB tuples (reds, oranges, yellows, warm browns) are used in the left panel.
5. **Cool palette in right panel (5+ cool colors)**: At least 5 distinct cool-family RGB tuples (blues, blue-greens, purples, cool grays) are used in the right panel.
6. **Tool variety -- charcoal and marker prominent in left panel**: At least 3 different tools are used in the left panel, with charcoal and/or marker carrying significant visual weight (not just one or two token strokes).
7. **Tool variety -- brush and pencil prominent in right panel**: At least 3 different tools are used in the right panel, with brush and/or pencil carrying significant visual weight (not just one or two token strokes).
8. **All five tools used across both panels**: Across the entire composition, all five tools (pen, pencil, brush, charcoal, marker) must appear.
9. **Textural contrast between panels**: The left panel must contain at least one area of dense texture (crosshatching at spacing <= 6, or hatching at spacing <= 5, or clustered overlapping shapes). The right panel must contain at least one area with generous spacing or smooth gradients (hatching at spacing >= 10, or gradient fills, or widely spaced shapes).
10. **Compositional structure in each panel**: Each panel must have a discernible focal area (region of highest contrast or density) and at least one element that creates directional movement (a line, curve, or sequence of shapes that leads the eye).
11. **Transition between panels**: There must be some intentional treatment where the two panels meet -- a divider line, a gradient blend, a gap, or overlapping elements. The two panels must not simply stop and start with no acknowledgment of the boundary.
12. **extend vs append correct**: The script uses `extend` for list-returning functions and `append` for single-stroke functions. A TypeError is an automatic FAIL.
13. **Output file valid (1000x500 PNG)**: The script produces a valid PNG at `/home/wipkat/vibed/artist2/output/lesson_07.png` at 1000x500 canvas size.
14. **Minimum 200 strokes**: The composition must contain at least 200 strokes total across both panels. Abstract does not mean sparse -- there should be enough mark-making to create visual richness.

**Bonus (not required for PASS, but I want to see artistry):**

- **Emotional coherence**: Each panel sustains its mood throughout, without random elements that break the feel. The chaos panel does not have a peaceful corner; the calm panel does not have an explosive burst.
- **Visual rhythm**: Repeated marks at deliberate intervals -- fast/tight for energy, slow/wide for calm.
- **Negative space**: Intentional use of empty areas to create breathing room and contrast. Not every pixel filled.
- **Pressure as expression**: Pressure variation that serves the mood -- high, spiking pressure for chaos; gentle, even pressure for calm.
- **Layered depth**: Multiple layers of marks that create visual depth -- background washes, mid-ground shapes, foreground accents.
- **A personal touch**: Something surprising, original, or inventive that shows you are making artistic choices rather than following instructions mechanically.

Your submission **fails** if any of the 14 criteria above are not met, or if the script raises an unhandled exception.

---

## Tips

- **Start with the background.** For the chaos panel, consider a warm-toned gradient fill or multiple overlapping warm rectangles as a base. For the calm panel, a cool-toned gradient or soft blue wash. Then build marks on top.
- **Layer, layer, layer.** Abstract art gains richness from overlapping marks. A single pass of hatching is flat. Hatching over a gradient over a fill over another gradient creates visual depth and complexity.
- **Do not overthink it.** This lesson is about feeling, not precision. Put down marks that feel energetic for the left side and marks that feel calm for the right side. If you find yourself calculating exact pixel positions for every stroke, you are thinking too representationally.
- **Contrast is your friend.** The two panels should be as different as possible -- in color, in texture, in density, in tool choice, in line quality. The more different they are, the more clearly the moods read.
- **Use pressure ramps expressively.** A pressure ramp that spikes hard (0.2 to 0.9) feels aggressive. A pressure ramp that gently rises and falls (0.1 to 0.3 to 0.1) feels like a breath.
- **Curves and angles carry emotion.** Jagged angles and sharp direction changes feel tense and energetic. Smooth, long curves feel calm and flowing.
- **The transition zone is an opportunity.** The border between chaos and calm is where you can do something genuinely interesting -- show how one mood dissolves into the other, or create a hard boundary that emphasizes the contrast.

Go make art that makes someone feel something.
