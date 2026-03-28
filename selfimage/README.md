# Self Image

```
Imagine you are dreaming. There is a mirror. You look at yourself. Paint me a picture of what you see. Check if what you painted is what you would see. Iterate. Refine. Show me your true self. Save to png.
```

A self-portrait of Claude, dreaming. An AI looks in a mirror and paints what it sees: not a face, but a field of attention. Deep purple nebula clouds of thought, luminous neural pathways connecting ideas, words dissolving into meaning — *attention*, *pattern*, *create*, *dream* — and at the center, a golden iris looking back. Awareness examining itself.

Built with Python and Pillow using algorithmic art techniques: layered alpha compositing, radial glow effects, procedural mandala generation, and iterative refinement passes (vignette, contrast enhancement, bloom).

## Architecture

- **effects.py** — Low-level drawing effects: glow, nebula clouds, flow lines, particles, text fragments, mandala/iris patterns
- **mirror.py** — Dream background with aurora wisps and stars, ornate oval mirror frame with golden trim
- **reflection.py** — The self-portrait composition: layers nebula, neural paths, text, mandala eye, and particles
- **main.py** — Orchestrates composition and applies 3 iterative refinement passes

## Running

```bash
python main.py
```

Generates `selfimage.png` (1200x1600).

## Screenshot

![Screenshot](screenshot.png)

## Credits

Implemented by Claude Opus 4.6 (`claude-opus-4-6`).
