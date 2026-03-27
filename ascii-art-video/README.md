# ASCII Art Video - Ultimate Stick Figure Showdown

```
write an application that generates an ascii art video. Content: title page, then 2 stick figures fighting,
then something really really funny happens, fade out, finally end-credits. When you're done ask yourself,
how can I make it cooler, more amazing, flashier... do that! over and over until you're satisfied.
```

![Demo](demo.gif)

## Overview

A fully animated ASCII art video that plays in your terminal at 30fps, featuring:

1. **Title Screen** - Matrix rain intro that morphs into a rainbow-cycling title with fire effects, energy auras, and lightning strikes
2. **Epic Fight Sequence** - Two stick figures in an 8-phase choreographed battle with punches, kicks, hadouken projectiles, flying kicks, and shoryuken uppercuts. Complete with health bars, combo counter, speed lines, and shockwave effects
3. **The Funny Moment** - A banana peel falls from the sky mid-fight. One fighter slips, crashes into the other, creating a cartoon fight cloud. They end up becoming friends!
4. **Sunset Fade Out** - Beautiful sunset scene with silhouettes walking together, fading to black with a heartwarming message
5. **End Credits** - Star Wars-style scrolling credits with fireworks

## Architecture

- **renderer.py** - Screen buffer engine with 256-color ANSI terminal rendering, differential updates for performance
- **animation.py** - Scene timeline, frame timing, easing functions (ease-in/out, bounce, lerp)
- **effects.py** - Particle systems, explosions, sparks, fireworks, screen shake, matrix rain, shockwaves, energy auras, fire, lightning, speed lines
- **scenes.py** - All scene content with 15+ unique stick figure poses and choreographed transitions
- **main.py** - Application entry point

## Running

```bash
cd ascii-art-video
python main.py
```

Requires a terminal of at least 60x20 characters. Press Ctrl+C to exit early.

## Tests

```bash
python -m pytest -v
```

79 unit tests covering all modules.

## Implementation

Built by **Claude Opus 4.6** (`claude-opus-4-6`).
