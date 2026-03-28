# Hit Song Generator

**Prompt:**
> `Write a hitsong and record it to mp3`

![Screenshot](screenshot.png)

🎵 **[Listen to Electric Dreams (hitsong.mp3)](hitsong.mp3)**

## Overview

A Python application that composes and synthesizes a complete pop song from scratch, then exports it to MP3. No external music libraries — all audio is generated from pure math using numpy waveform synthesis.

## The Song: "Electric Dreams"

- **Key:** C major
- **Tempo:** 120 BPM
- **Duration:** ~1:44
- **Structure:** Intro → Verse 1 → Chorus → Verse 2 → Chorus → Bridge → Chorus → Outro

### Tracks
- **Lead melody** — Detuned saw waves with sine body
- **Bass** — Sub sine + square wave harmonics
- **Chord pads** — Warm detuned sine ensemble with LFO
- **Drums** — Synthesized kick, snare, hi-hat, clap, and crash

## Architecture

| Module | Purpose |
|--------|---------|
| `song_structure.py` | Song sections, chord progressions, tempo, key |
| `melody.py` | Lead melody, bass line, chord pads, drum patterns |
| `lyrics.py` | Song lyrics for each section |
| `synthesizer.py` | Waveform synthesis with ADSR envelopes |
| `mixer.py` | Track mixing, reverb, compression, mastering |
| `exporter.py` | WAV/MP3 export via ffmpeg/lame |
| `main.py` | Orchestration — generates and exports the song |

## Running

```bash
python3 main.py
```

Produces `hitsong.mp3` in the project directory.

## Tests

```bash
python3 -m unittest discover -p "test_*.py"
```

43 unit tests covering all modules.

## Built with

Claude Opus 4.6 (`claude-opus-4-6`) — implementation by Claude.
