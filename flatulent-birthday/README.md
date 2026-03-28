# Flatulent Birthday

```
Make an application that, given a base frequency and duration, synthesizes the sound of flatulence with those approximate parameters.
Make sure synthesis is based solely on scientific, anatomic and acoustic principles, and as the sounds are random in nature, no 2 should ever be the same.
Do at least 3 refinements of the algorithm, making sure the sound is indistinguishable from the original.
Then use it to sing happy birthday and save to mp3. Not too loud please.
```

![Screenshot](screenshot.png)

## How It Works

Physically-inspired aeroacoustic model. The sphincter is modeled as an oscillating valve that periodically opens and closes, letting pressurized gas through in bursts:

1. **Aperture oscillation** — The sphincter oscillates as a skewed sawtooth (fast open, slow close). Half-wave rectified to zero (tissue can't open negatively) — this is the key nonlinearity that generates the harmonic-rich "raspberry" buzz, the same mechanism as brass lip buzzes.
2. **Airflow** — Flow = sqrt(pressure) x aperture. Turbulence noise is pre-filtered to low frequencies and scales with flow velocity (Reynolds number), so noise is embedded in the physics rather than mixed in artificially.
3. **Buttcheek resonance** — Low-frequency bandpass (40-130 Hz) adds thick, rumbly body from the flesh mass vibrating sympathetically.
4. **Tissue filtering** — 3rd-order low-pass through surrounding flesh, applied last to kill all HF artifacts.
5. **Sputter modulation** — Multiple overlapping flutter modes (4-25 Hz) with brief dropouts and rough amplitude noise for the characteristic sputtering quality.
6. **Pressure envelope** — Randomly crescendo or decrescendo, with monotonic pitch slide (up or down 15-40%) per note.

### Refinement History

- **V1-V3**: Oscillator + noise approaches — too musical/synthetic
- **V4-V6**: Chaotic oscillator, pulse-gated noise — timpani/echo artifacts
- **V7**: Physically-inspired rewrite — half-wave rectified aperture model
- **V8-V10**: Tuned staccato, buttcheek resonance, sputter depth, pitch slides, aggressive saturation, HF elimination

Every sound is unique due to randomized parameters across all components.

## Modules

- `synth.py` — Core flatulence synthesis engine
- `melody.py` — Happy Birthday note sequence definition
- `renderer.py` — Combines synth + melody, exports to MP3
- `main.py` — Entry point

## Usage

```bash
python3 main.py
```

Outputs `happy_birthday_flatulent.mp3` (192 kbps, ~14s, 30% volume).

## Tests

```bash
python3 -m unittest discover -v
```

26 tests covering synthesis, melody, and rendering.

## Implementation

Built by **Claude Opus 4.6** (`claude-opus-4-6`).
