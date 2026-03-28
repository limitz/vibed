# Student Skills

## Current Level: Beginner (advancing)

### Tools Mastery
- **Pen**: Solid proficiency - can draw lines, circles, arcs, rectangles, and triangles with controlled pressure
- **Pencil**: Solid proficiency - can draw ellipses, S-curves, and lines with varied pressure and color
- **Brush**: Intermediate proficiency - can draw circles, ellipses, and gradient fills with expressive pressure variation
- **Charcoal**: Intermediate proficiency - practiced arcs and gradient fills; produces rough, textured marks distinct from pen and pencil; gradient fills have a distinctive gritty quality
- **Marker**: Not yet practiced

### Techniques
- **Lines**: Practiced horizontal, vertical, and diagonal lines with precise placement
- **Curves**: Practiced S-curves with varying amplitude (15, 25, 30, 40); understand how amplitude controls the drama of the S shape
- **Circles & Arcs**: Can draw full circles, concentric circles, half-arcs, and quarter-arcs; understand radian angle system (0=right, pi/2=down, pi=left, 3pi/2=up, clockwise)
- **Ellipses**: Can draw ellipses with independent horizontal and vertical radii; wide (rx>ry) and tall (ry>rx) orientations
- **Shapes**: Can draw rectangles (including squares) and triangles (right triangles and isosceles)
- **Hatching**: Solid proficiency - can create parallel-line tone at varying spacings (5, 8, 12, 14) and angles (0, 30, 45, 75 degrees) to control density and direction; used for value scales and form shading
- **Crosshatching**: Solid proficiency - can layer hatching at multiple angles (default 45/-45) for richer, denser tone; understand that crosshatching produces darker values than single-direction hatching at same spacing
- **Gradient Fill**: Solid proficiency - can create smooth tonal transitions from light to dark (and reversed) using draw_gradient_fill; tested with pencil, charcoal, and brush tools
- **Pressure Control**: Practiced pressures from 0.2 (very light) to 0.9 (very heavy); understand how pressure affects line weight across all tools
- **Color Mixing**: Not yet practiced

### Artistic Concepts
- **Composition**: Progressing - organized canvas into four-quadrant layout; added creative embellishments (inner rectangles for depth, echo S-curves for rhythm, mirror arcs for reflection)
- **Perspective**: Not yet studied
- **Light & Shadow**: Beginning to understand - practiced shading a sphere and cube with top-left light source; know that surfaces facing the light are lightest (low pressure, wide spacing) and surfaces turned away are darkest (high pressure, tight spacing); understand core shadow, cast shadow, and tonal transition zones
- **Color Theory**: Beginning awareness - used black, blue, green, red, purple, orange, and gray in a single composition; observed how color groups shapes into visual sections
- **Texture**: Observed how different tools (pen, pencil, brush, charcoal) produce distinct visual textures; charcoal is notably rougher than pen
- **Expression**: Beginning to explore - added decorative elements beyond strict requirements to create visual interest (dot-center in concentric circles, fading ripple curves, nested squares, mirrored arcs)

### Completed Lessons
- **Lesson 1: Line Control & Tool Exploration** - Learned to draw straight lines in multiple directions using pen, pencil, and brush tools at varying pressure levels. Created a 16-stroke composition demonstrating tool differences and pressure control.
- **Lesson 2: Curves & Shapes** - Learned to draw circles, arcs, ellipses, S-curves, rectangles, and triangles. Combined multiple tools (pen, pencil, brush, charcoal) and colors (black, blue, green, red, purple, orange, gray) in a four-quadrant composition with 23 strokes. Added creative touches beyond the assignment requirements.
- **Lesson 3: Shading, Hatching & Value** - Learned hatching, crosshatching, and gradient fills as tools for creating tonal value. Created value scale swatches showing progression from light to dark. Shaded a sphere with four overlapping hatching zones (highlight, midtone, shadow, core shadow) plus cast shadow. Shaded a cube with three faces at different values to suggest 3D form with top-left lighting. Used pen, pencil, charcoal, and brush across 443 strokes. Key insight: spacing controls apparent darkness as much as pressure; different hatching angles help distinguish adjacent surfaces.

### Notes
- Pen produces clean, sharp lines with consistent edges
- Pencil produces softer, slightly textured lines
- Brush produces broad strokes that respond dramatically to pressure changes
- Charcoal produces rough, gritty marks with an organic feel
- Pressure ramp creates a smooth thin-to-thick-to-thin transition
- Canvas coordinates: 800x600, origin at top-left, Y increases downward
- Arc angles are in radians: full circle = 0 to 2*pi, half = 0 to pi or pi to 2*pi, quarter = 0 to pi/2
- S-curve amplitude controls how far the curve swings from the straight path between endpoints
- Concentric shapes (circles within circles, rectangles within rectangles) create a sense of depth
- Repeating a motif at decreasing intensity (pressure/size) creates rhythm and visual echo
- draw_hatching and draw_crosshatching return LISTS of strokes -- must use extend(), not append()
- draw_gradient_fill also returns a LIST -- must use extend()
- draw_crosshatching takes `angles` parameter (a list like [45, -45]), NOT `angle_deg`
- Spacing controls apparent darkness as much as pressure: spacing=5 at pressure=0.3 can look darker than spacing=14 at pressure=0.6
- Overlapping hatching zones at different densities create the illusion of rounded form (sphere shading)
- Different hatching angles on adjacent cube faces help the eye distinguish the surfaces
- Cast shadows ground an object and prevent it from appearing to float
- Value (lightness/darkness) is the primary tool for creating 3D illusion on a 2D surface
