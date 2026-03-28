# South Park Scene

```
Use SVG do draw an image of eric cartman throwing up on his mom, in his bedroom. Kenny is laughing. Do a few iterations making it look like the actual series. Convert to png.
```

![Screenshot](screenshot.png)

## Description

Python application that generates a South Park scene using SVG, featuring Eric Cartman throwing up on his mom (Liane Cartman) in his bedroom while Kenny laughs from the side. Iteratively refined over 3 passes to match the show's construction-paper cutout aesthetic. The SVG is then converted to PNG using CairoSVG.

The scene includes:
- Cartman's bedroom with bed, Clyde Frog, Terrance & Phillip poster, nightstand with lamp, window with crescent moon
- Eric Cartman in his red jacket and cyan/yellow beanie, mouth wide open mid-vomit
- Liane Cartman in her red dress with eyelashes and lipstick, arms raised in horror, covered in vomit splatters
- Kenny in his orange parka with tight hood, squinting happy-eyes from laughing, pointing at Cartman
- Chunky green vomit stream with splatter droplets and floor puddle

Style details matching the show:
- Signature touching/overlapping eyes with black dot pupils
- Thick black outlines on all shapes (construction-paper look)
- Flat colors with no gradients
- Oversized heads with tiny limbs
- Eyelashes as the female character marker
- Muffled "Mmph!" speech for Kenny

## Modules

- `svg_generator.py` — Generates all SVG elements (bedroom, characters, vomit effects)
- `converter.py` — Converts SVG string to PNG using CairoSVG
- `main.py` — Orchestrates generation and conversion
- `screenshot.py` — Generates screenshot.png from the output

## Built with

Claude Opus 4.6 (`claude-opus-4-6`)
