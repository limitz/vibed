# South Park Scene

```
Use SVG do draw an image of eric cartman throwing up on his mom, in his bedroom. Kenny is laughing. Convert to png.
```

![Screenshot](screenshot.png)

## Description

Python application that generates a South Park scene using SVG, featuring Eric Cartman throwing up on his mom (Liane Cartman) in his bedroom while Kenny laughs from the side. The SVG is then converted to PNG using CairoSVG.

The scene includes:
- Cartman's bedroom with bed, Clyde Frog, Terrance & Phillip poster, nightstand with lamp, window with moon
- Eric Cartman in his red jacket and teal hat, mouth wide open
- Liane Cartman in her red dress, covered in vomit splatters
- Kenny in his orange parka, squinting eyes from laughing, pointing at Cartman
- Green vomit stream with splatter effects on the floor

## Modules

- `svg_generator.py` — Generates all SVG elements (bedroom, characters, vomit effects)
- `converter.py` — Converts SVG string to PNG using CairoSVG
- `main.py` — Orchestrates generation and conversion
- `screenshot.py` — Generates screenshot.png from the output

## Built with

Claude Opus 4.6 (`claude-opus-4-6`)
