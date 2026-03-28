# SpeakUp

**Prompt:**
> `Using only FM synthesis, learn how to speak.`

A Python application that uses pure FM (Frequency Modulation) synthesis to generate human speech from text. No audio samples, no pre-recorded data — just math.

![Screenshot](screenshot.png)

## How It Works

Speech is built from formants — resonant frequencies of the vocal tract. Each formant is modeled by an FM operator pair: a carrier oscillator at the formant frequency, modulated by a sine wave at the fundamental pitch (F0). Three parallel carrier-modulator pairs create the formant structure of each vowel.

Consonants are synthesized differently: fricatives use noise-modulated FM, plosives use silence followed by a short FM noise burst, and nasals use low-frequency formants with damped higher harmonics.

## The Learning Progression

The app generates 6 audio files showing FM synthesis "learning to speak":

1. **Raw FM Tones** — Pure FM building blocks: sine waves, modulation sweeps
2. **Vowels** — Individual vowels: AH, EE, EH, OH, OO, AE, IH, UH
3. **Babbling** — Consonant-vowel pairs like a baby: ba, da, ma, pa, ta, ka
4. **First Words** — Simple words: mama, papa, hello, hi, no, yes
5. **Speaking** — Full sentences: "Hello world", "I am learning to speak"
6. **The Prompt** — "Using only FM synthesis, learn how to speak"

## Output Files

- [01_raw_fm_tones.mp3](output/01_raw_fm_tones.mp3) — Pure FM tones and modulation sweeps (3.9s)
- [02_vowels.mp3](output/02_vowels.mp3) — Individual vowels: AH, EE, EH, OH, OO, AE, IH, UH (4.8s)
- [03_babbling.mp3](output/03_babbling.mp3) — Consonant-vowel babbling: ba, da, ma, pa, ta, ka (4.3s)
- [04_first_words.mp3](output/04_first_words.mp3) — First words: mama, papa, hello, hi, no, yes (4.2s)
- [05_speaking.mp3](output/05_speaking.mp3) — Full sentences: "Hello world", "I am learning to speak" (5.2s)
- [06_the_prompt.mp3](output/06_the_prompt.mp3) — "Using only FM synthesis, learn how to speak" (4.7s)

## Architecture

| Module | Purpose |
|---|---|
| `fm_engine.py` | FM operators, ADSR envelopes, patches, noise-modulated FM |
| `phonemes.py` | 30+ phonemes defined as FM parameter sets (formant frequencies, amplitudes, bandwidths) |
| `text_to_phoneme.py` | English text → phoneme sequence (dictionary + letter rules) |
| `speech.py` | Phoneme sequences → audio with coarticulation and intonation |
| `exporter.py` | WAV/MP3 file export |
| `main.py` | Orchestrates the 6-stage learning progression |

## Usage

```bash
python -m speakup.main
```

Output files are written to `speakup/output/`.

## Running Tests

```bash
python -m pytest speakup/tests/ -v
```

## Built With

Claude Opus 4.6 (`claude-opus-4-6`) — implementation by Claude.
