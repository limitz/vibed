# Lesson 5: Landscape & Atmospheric Perspective

## Feedback from Lesson 4

**Result: PASS**

You met all 13 criteria. The still life reads as a coherent scene -- three objects on a table in front of a wall, with clear spatial depth from the warm/cool foreground/background separation. Your color shading is the biggest leap forward: every object's shadow uses a darker version of its own hue rather than black, which keeps the colors alive. The color theory strip is thorough and complete. Your code remains clean and well-organized. 971+ strokes with zero TypeErrors.

**Strengths:**
- The still life is your first composed scene that tells a spatial story. Warm table, cool wall, three distinct objects with different colors and positions. It works.
- Color shading is well-executed. The apple's dark red shadow, the vase's dark blue shadow, the lemon's ochre shadow -- each object maintains its color identity through the value range. This is a significant advance over Lesson 3's all-black hatching.
- The color theory strip demonstrates all three complementary pairs cleanly. The overlaid crosshatching shows you understand optical mixing.
- extend/append is now fully automatic for you.

**Weaknesses -- and I need to push you on two things:**

- **You are not making compositional decisions.** Every object in the still life was placed exactly where I told you to put it. You used the exact coordinates from the assignment table. This is obedient, but it is not composition. Composition means *you* decide where things go, based on what looks right. In Lesson 5, I will give you a framework but not a stroke-by-stroke table. You will have to decide placement, sizing, and arrangement yourself.

- **Your creative initiative has disappeared.** In Lesson 2, you added 4 extra elements beyond the assignment. In Lessons 3 and 4: zero extras, zero experiments, zero surprises. You are executing instructions perfectly but not exploring. Art requires both skill and curiosity. I want to see you make choices that are yours, not mine.

- **The hatching-beyond-boundary problem persists.** Your hatching zones are rectangular and extend past object outlines (the apple, the lemon). This makes objects look like circles drawn on top of hatched rectangles. We will not address this technically in Lesson 5 -- the landscape setting works better with rectangular fills -- but be aware that this remains an unsolved problem for round objects.

- **Marker and charcoal are collecting dust.** You have five tools. You use three (pen, pencil, brush). In Lesson 5, you will use all five. No exceptions.

---

## Objectives

By the end of this lesson you will be able to:

1. Create a **complete landscape scene** that combines lines, shapes, shading, color, and composition.
2. Apply **atmospheric perspective**: distant objects are lighter, cooler, and less detailed; near objects are darker, warmer, and more detailed.
3. Organize a scene into **foreground, middle ground, and background** layers with clear spatial separation.
4. Draw **natural elements**: sky, ground, hills, trees, water.
5. Use **all five tools** (pen, pencil, brush, charcoal, marker) in a single composition.
6. Make **independent compositional decisions** -- choosing where to place elements and how to size them based on visual logic, not a coordinate table.

---

## Concepts

### Atmospheric Perspective

When you look at a real landscape, distant things look different from near things in three specific ways:

1. **Value**: Distant objects are lighter (closer to the sky's value). Near objects have the full range from light to dark.
2. **Color temperature**: Distant objects shift toward cool blue/gray. Near objects retain their warm, saturated colors.
3. **Detail**: Distant objects have less visible detail -- smoother, simpler shapes. Near objects have visible texture, hatching, and sharp edges.

This is not artistic opinion. It is physics -- light scatters through atmosphere, and more atmosphere means more scattering. Painters have used this for 500 years to create the illusion of depth on a flat surface.

In your drawing, you will implement atmospheric perspective through:
- **Pressure**: Lower pressure for distant elements, higher pressure for near elements.
- **Color**: Cool, desaturated colors (blue-gray, light purple) for background; warm, saturated colors (green, brown, dark green) for foreground.
- **Spacing**: Wider hatching spacing for distant elements (less detail), tighter spacing for near elements (more detail).
- **Tool choice**: Soft tools (brush, charcoal) for distant/atmospheric elements; sharp tools (pen, marker) for near/detailed elements.

### Foreground, Middle Ground, Background

A landscape composition typically has three depth zones:

- **Background** (top of canvas): Sky, distant mountains or hills. Lightest values, coolest colors. Minimal detail.
- **Middle ground** (center): Rolling hills, fields, maybe a body of water. Moderate values, transitional colors. Some detail.
- **Foreground** (bottom of canvas): Ground, rocks, grass, tree trunks. Darkest values, warmest colors. Maximum detail and texture.

Each layer partially overlaps the one behind it. The hills overlap the sky. The foreground overlaps the middle ground. This overlapping is one of the strongest depth cues you have.

### Drawing Order for Landscapes

Draw back to front:
1. Sky (gradient fill -- the entire canvas backdrop)
2. Distant hills (lighter, cooler)
3. Middle-ground hills and features (moderate values)
4. Water or fields (if present)
5. Foreground ground (darkest, warmest)
6. Objects and details (trees, rocks, grass textures)

This ensures that nearer elements overlap and cover the edges of farther elements, creating natural depth.

### Natural Elements -- How to Build Them

You do not have a "draw tree" function. You build natural elements from the primitives you already know:

- **Sky**: A gradient fill from light blue (top) to lighter blue or pale yellow (horizon).
- **Hills**: A series of overlapping filled rectangles or gradient fills, each layer slightly darker and warmer than the one behind it. The top edge of each "hill" can be suggested by a curve or a line.
- **Trees**: A tree is a vertical line (trunk) plus a filled circle or hatched circle (canopy). Distant trees are small, pale, and simple. Near trees are large, dark, and textured.
- **Water**: A filled rectangle in blue tones with horizontal hatching for ripple texture.
- **Ground/grass**: Filled rectangles with diagonal hatching overlay for texture. Foreground grass can have individual short diagonal lines.
- **Rocks**: Small filled circles or rectangles with crosshatching for shading.
- **Sun or moon**: A filled circle in the sky, with light-colored hatching around it for glow.

---

## Assignment

Create a Python script saved as `/home/wipkat/vibed/artist2/output/lesson_05.py` that produces `/home/wipkat/vibed/artist2/output/lesson_05.png`.

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
drawing = Drawing(strokes=all_strokes, width=1000, height=600)
img = render_drawing(drawing, apply_paper=True)
output_path = os.path.join(os.path.dirname(__file__), "lesson_05.png")
img.convert("RGB").save(output_path)
print(f"Saved to {output_path}")
print(f"Total strokes: {len(all_strokes)}")
```

### What to draw

A **complete landscape scene** with atmospheric perspective. The scene should include a sky, distant hills, middle-ground features, and a detailed foreground. You must use all five tools.

**I am NOT giving you a stroke-by-stroke table.** You decide the composition. Below is a framework -- the elements you must include and guidelines for how to build them. You choose the exact coordinates, sizes, colors, and arrangement.

---

#### Layer 1 -- Sky (background, y: 0-250 approximately)

Build a sky gradient from a medium blue at the top of the canvas to a lighter, warmer tone near the horizon. The sky should fill the full width of the canvas (1000px).

- Use `draw_gradient_fill` with the **brush** tool for the main sky wash.
- Consider adding a sun or warm glow near the horizon using a filled circle and/or light-colored hatching.
- The sky sets the overall mood: a warm sunset, a cool morning, or a bright midday. Choose one mood and commit to it.

#### Layer 2 -- Distant Hills (background, overlapping the sky)

Draw at least **two layers of distant hills** that overlap the lower portion of the sky. These hills demonstrate atmospheric perspective:

- Use **cool, light colors**: pale blue-gray, light purple, lavender. These are the most distant elements.
- Use **low pressure** (0.1-0.25) and **wide hatching spacing** (10-14) if adding any texture.
- Use the **brush** or **charcoal** tool for soft, atmospheric edges.
- Each hill layer should be a filled rectangle or gradient fill that spans the canvas width, with the top edge suggested by a line or curve.
- The further hill should be lighter and cooler than the nearer one.

#### Layer 3 -- Middle Ground (y: 250-400 approximately)

This is the transitional zone. Add at least **two features** here:

- **Rolling green hills or a field**: Use moderate greens -- not as bright as foreground, not as gray as background. Gradient fills work well.
- **A body of water** (lake or river): A filled rectangle in blue-gray tones with horizontal hatching for ripple texture. Water reflects the sky, so its color should relate to the sky color but be slightly darker.
- Or: a **path, fence, or field boundary** -- any element that leads the eye from middle ground toward the foreground.
- Use **pencil** and/or **charcoal** for moderate detail. Pressure range: 0.2-0.4.

#### Layer 4 -- Foreground (y: 400-600 approximately)

The foreground is the closest, warmest, most detailed area:

- **Ground surface**: A filled rectangle or gradient fill in warm earth tones (brown, dark green, ochre). This should be noticeably warmer and darker than the middle ground.
- **Texture**: Add diagonal hatching or crosshatching to suggest grass, dirt, or rocky ground. Use the **marker** tool for at least some foreground texture -- bold, graphic marks that contrast with the softer background.
- **At least one tree**: A trunk (vertical line or narrow filled rectangle, using **pen** or **marker**) and a canopy (filled circle with hatching overlay, using **charcoal** or **pencil**). The tree should be large enough to be a significant compositional element -- not a tiny afterthought.
- **Detail elements**: Add at least two small details -- rocks (small filled circles with crosshatching), grass tufts (short diagonal lines), flowers (small colored dots), or a path. Use **pen** for sharp detail.
- Pressure range: 0.4-0.8. Hatching spacing: 4-7. These are the densest, most detailed marks in the drawing.

#### Layer 5 -- Atmospheric Details & Final Touches

- Add at least one element that specifically demonstrates atmospheric perspective by contrasting a **distant version** and a **near version** of the same type of object. Example: a small, pale, simple tree on a distant hill AND a large, dark, detailed tree in the foreground.
- Add any finishing touches: a horizon line, a grounding line along the bottom edge, additional texture where needed.

---

## Tool Requirements

You MUST use all five tools in this lesson. Here are suggested roles (you may adapt these):

| Tool | Suggested Role | Character |
|------|---------------|-----------|
| **brush** | Sky gradients, filled shapes, large washes | Soft, broad, atmospheric |
| **charcoal** | Distant hills, tree canopy texture, ground texture | Rough, gritty, organic |
| **pencil** | Middle-ground detail, hatching, shading on objects | Moderate texture, controlled |
| **pen** | Outlines, sharp foreground details, small elements | Clean, precise, sharp |
| **marker** | Foreground texture, bold accents, tree trunk | Bold, graphic, high-contrast |

---

## Important Reminders

- `draw_filled_rectangle`, `draw_filled_circle`, `draw_hatching`, `draw_crosshatching`, `draw_gradient_fill` all return **lists** of strokes. Use `all_strokes.extend(...)`.
- `draw_line`, `draw_circle`, `draw_ellipse`, `draw_rectangle`, `draw_pressure_ramp`, `draw_arc`, `draw_s_curve`, `draw_triangle` return a **single** stroke. Use `all_strokes.append(...)`.
- **RGB tuples** work as color parameters. Use them for the many subtle colors a landscape requires (pale blue-gray, warm ochre, dark forest green, etc.).
- Canvas is **1000 wide by 600 tall**.
- **Draw back to front**: sky first, then distant hills, then middle ground, then foreground, then details on top.
- **Atmospheric perspective** is the central concept: distant = light, cool, soft, simple. Near = dark, warm, sharp, detailed.
- You are making your own compositional decisions. There is no single correct answer. I am looking for a scene that reads as a landscape with clear depth.

---

## PASS / FAIL Criteria

Your submission **passes** if ALL of the following are true:

1. **Sky gradient**: A gradient fill spanning the full canvas width creates a sky that transitions from a cooler/darker tone at the top to a lighter/warmer tone near the horizon.
2. **Distant hills (2+ layers)**: At least two overlapping hill layers are visible behind the middle ground, drawn in cool, light colors (blue-gray, lavender, pale purple) at low pressure.
3. **Atmospheric perspective -- color temperature**: Distant elements use cooler colors (blues, grays, purples) and foreground elements use warmer colors (greens, browns, ochres, warm earth tones). The temperature shift must be clearly visible.
4. **Atmospheric perspective -- value**: Distant elements are lighter (lower pressure, wider hatching spacing) and foreground elements are darker (higher pressure, tighter hatching spacing). The value contrast must be clearly visible.
5. **Middle-ground feature**: At least one identifiable feature in the middle ground (water, field, rolling hills) that is intermediate in value and color temperature between the background and foreground.
6. **Foreground ground texture**: The foreground has visible texture created by hatching, crosshatching, or individual marks -- not just a flat fill. The foreground must be noticeably more detailed than the background.
7. **Tree(s) present**: At least one tree with a visible trunk and canopy. If multiple trees are present at different depths, they must show atmospheric perspective (distant tree lighter/smaller, near tree darker/larger).
8. **All five tools used**: pen, pencil, brush, charcoal, and marker must each appear at least once in the drawing.
9. **Color variety (8+ distinct colors/tuples)**: The landscape requires a wide palette. At least 8 distinct named colors or RGB tuples must be used.
10. **Layered depth (3 zones)**: The scene must have clearly distinguishable background, middle ground, and foreground zones. Elements in nearer zones must overlap/cover elements in farther zones.
11. **extend vs append correct**: The script uses `extend` for list-returning functions and `append` for single-stroke functions. A TypeError is an automatic FAIL.
12. **Output file valid**: The script produces a valid PNG at `/home/wipkat/vibed/artist2/output/lesson_05.png` at 1000x600 canvas size.
13. **Minimum 150 strokes**: A landscape with texture and atmospheric perspective requires substantial drawing. At least 150 strokes total.

**Bonus (not required for PASS, but I want to see growth):**

- **Creative additions**: Elements beyond the minimum requirements -- flowers, birds, clouds, a path, a fence, reflections in water, interesting foreground objects. Show me you are making artistic choices, not just checking boxes.
- **Compositional intent**: Evidence that you thought about where to place elements for visual balance and interest, not just filling zones mechanically.
- **Mood**: Does the scene have a consistent mood (warm sunset, cool morning, bright midday)? Do the colors and values work together to create that mood?

Your submission **fails** if any of the 13 criteria above are not met, or if the script raises an unhandled exception.

---

## Tips

- **Start with the sky and work forward.** Each layer covers the bottom edge of the layer behind it, creating natural overlap. If you draw the foreground first and then the sky, the sky will cover your foreground.
- **Use RGB tuples for landscape colors.** Named colors like "green" and "blue" are too saturated for a natural landscape. Real landscapes are full of muted, mixed tones: (140, 170, 140) for a soft sage green, (100, 80, 60) for warm earth, (180, 190, 210) for distant blue-gray. Think of every color as needing a specific recipe, not just a name.
- **Charcoal is your friend for atmosphere.** Its rough, gritty texture naturally suggests distant haze, tree canopy foliage, and organic ground texture. Try it at low pressure (0.1-0.2) for distant hills.
- **Marker is bold.** Use it for the foreground where you want graphic impact -- a tree trunk, a rock outline, bold grass strokes. Do not use marker for distant elements; it is too sharp and heavy.
- **Trees get simpler with distance.** A foreground tree might have a pen-outlined trunk, charcoal-hatched canopy, and visible branches. A distant tree is just a small filled circle on a tiny line, in pale gray-green.
- **The horizon is NOT a hard line.** In a landscape with hills, the horizon is implied by the lowest hill overlapping the sky. You do not need to draw a ruler-straight horizon line (though you can draw a subtle one if you like).
- **Overlap is the most powerful depth cue.** A hill that overlaps the sky reads as in front of the sky. A tree that overlaps a hill reads as in front of the hill. Use overlap aggressively.

Go paint a landscape.
