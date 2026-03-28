# Washing Machine

```
Use svg to create an image of a washing machine. Iterate and refine until it looks as real as possible. Store as jpeg.
```

![Screenshot](screenshot.png)

## Overview

Python application that generates a photorealistic washing machine image using SVG, then converts it to JPEG. The SVG is built through 5 iterative refinement passes — base shapes, materials/gradients, lighting/shadows, fine details, and final polish — producing a detailed vector rendering with chrome trim, glass door, perforated drum, visible clothes, water tint, control panel with LCD display and knobs, and realistic lighting effects.

## Output

- `washing_machine.svg` — The raw SVG source (vector)
- `washing_machine.jpeg` — Final rendered output at 1600x1800px

## Usage

```bash
python3 main.py
```

## Tests

```bash
python3 -m unittest test_svg_generator test_converter test_main -v
```

## Built with

Claude Opus 4.6 (`claude-opus-4-6`)
