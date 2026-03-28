# 2001: A Space Odyssey — ASCII Art Re-enactment

```
Make an application that re-enacts the entire film "2001 a space odyssey" using only ascii art. Add controls to fast-forward / rewind.
```

![Screenshot](screenshot.png)

A terminal-based ASCII art re-enactment of Stanley Kubrick's *2001: A Space Odyssey*, built with Python curses. All 10 iconic scenes are rendered procedurally as pure functions of time, enabling seamless rewind and fast-forward at any point.

## Scenes

1. **The Dawn of Man** — African landscape, apes, monolith, bone tool
2. **The Match Cut** — Bone tumbles skyward, dissolves into space station
3. **Space Station V** — Rotating ring station, shuttle docking sequence
4. **Tycho Magnetic Anomaly One** — Moon monolith discovery, signal burst
5. **Jupiter Mission** — Discovery One drifts across star field toward Jupiter
6. **HAL 9000** — The iconic red eye, conversations with Dave
7. **I'm Sorry, Dave** — HAL refuses to open the pod bay doors
8. **Daisy, Daisy...** — Dave disconnects HAL's logic modules
9. **Jupiter and Beyond the Infinite** — Stargate sequence with speed lines, tunnel, color cycling
10. **The Star Child** — Earth, glowing embryo, fade to black

## Controls

| Key | Action |
|-----|--------|
| `SPACE` | Play / Pause |
| `→` / `l` | Cycle forward speed (1x → 2x → 4x) |
| `←` / `h` | Cycle rewind speed (1x → 2x → 4x) |
| `n` / `PgDn` | Skip to next scene |
| `p` / `PgUp` | Skip to previous scene |
| `r` | Restart from beginning |
| `q` / `ESC` | Quit |

## How to Run

```bash
cd 2001
python main.py
```

## Architecture

- **Pure render functions** — Each scene's `render_fn(buffer, progress)` is a pure function of progress (0.0–1.0), making rewind trivial
- **Seeded procedural generation** — Star fields, particles, and effects use deterministic math so any frame can be computed at any time
- **Modular design** — 8 modules: renderer, timeline, player, input handler, effects, scenes, HUD, main

## Tests

```bash
python -m pytest tests/ -v
```

112 unit tests covering all modules.

---

Built by Claude Opus 4.6 (`claude-opus-4-6`)
