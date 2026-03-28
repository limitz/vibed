"""SpeakUp — Learn to speak using only FM synthesis.

Generates a progressive series of audio files demonstrating FM synthesis
learning to produce human speech.
"""

from __future__ import annotations

import os
import numpy as np

from .fm_engine import FMOperator, Envelope, mix_signals, noise_modulated_fm
from .phonemes import PHONEMES
from .text_to_phoneme import text_to_phonemes
from .speech import render_phoneme, render_utterance
from .exporter import normalize, save_wav


SAMPLE_RATE = 44100
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")


def stage_1_raw_fm() -> np.ndarray:
    """Stage 1: Raw FM tones — exploring FM synthesis building blocks."""
    print("  Stage 1: Raw FM tones...")
    segments = []
    t_tone = np.linspace(0, 0.4, int(0.4 * SAMPLE_RATE), endpoint=False)
    pause = np.zeros(int(0.15 * SAMPLE_RATE))

    # Pure sine
    op = FMOperator(frequency=200, amplitude=0.5)
    segments.append(op.generate(t_tone))
    segments.append(pause)

    # FM with increasing modulation index
    for mod_idx in [1.0, 3.0, 6.0, 10.0]:
        op = FMOperator(frequency=400, amplitude=0.4, modulation_index=mod_idx)
        modulator = np.sin(2 * np.pi * 200 * t_tone)
        segments.append(op.generate(t_tone, modulator_signal=modulator))
        segments.append(pause)

    # Frequency sweep
    t_sweep = np.linspace(0, 1.0, int(1.0 * SAMPLE_RATE), endpoint=False)
    sweep_freq = np.linspace(100, 1000, len(t_sweep))
    sweep = 0.4 * np.sin(2 * np.pi * np.cumsum(sweep_freq) / SAMPLE_RATE)
    segments.append(sweep)
    segments.append(pause)

    return np.concatenate(segments)


def stage_2_vowels() -> np.ndarray:
    """Stage 2: Individual vowels — first recognizable sounds."""
    print("  Stage 2: Vowels...")
    segments = []
    pause = np.zeros(int(0.2 * SAMPLE_RATE))
    vowels = ["AH", "EE", "EH", "OH", "OO", "AE", "IH", "UH"]

    for name in vowels:
        spec = PHONEMES[name]
        audio = render_phoneme(spec, 0.4, 120.0, SAMPLE_RATE)
        segments.append(audio)
        segments.append(pause)

    return np.concatenate(segments)


def stage_3_babbling() -> np.ndarray:
    """Stage 3: Babbling — consonant-vowel pairs like a baby."""
    print("  Stage 3: Babbling...")
    syllables = [
        ["B", "AH"], ["D", "AH"], ["M", "AH"],
        ["P", "AH"], ["T", "AH"], ["K", "AH"],
        ["B", "EE"], ["M", "EE"], ["D", "EE"],
        ["G", "OO"], ["N", "AH"], ["L", "AH"],
    ]
    segments = []
    pause = np.zeros(int(0.15 * SAMPLE_RATE))

    for syllable in syllables:
        audio = render_utterance(syllable, SAMPLE_RATE, f0_base=150.0, speed=0.8)
        segments.append(audio)
        segments.append(pause)

    return np.concatenate(segments)


def stage_4_first_words() -> np.ndarray:
    """Stage 4: First words — simple recognizable words."""
    print("  Stage 4: First words...")
    words = ["mama", "papa", "hello", "hi", "no", "yes"]
    segments = []
    pause = np.zeros(int(0.3 * SAMPLE_RATE))

    for word in words:
        phonemes = text_to_phonemes(word)
        audio = render_utterance(phonemes, SAMPLE_RATE, f0_base=130.0, speed=0.7)
        segments.append(audio)
        segments.append(pause)

    return np.concatenate(segments)


def stage_5_speaking() -> np.ndarray:
    """Stage 5: Full sentences."""
    print("  Stage 5: Speaking...")
    sentences = [
        "Hello world",
        "I am learning to speak",
        "Can you hear me",
    ]
    segments = []
    pause = np.zeros(int(0.4 * SAMPLE_RATE))

    for sentence in sentences:
        phonemes = text_to_phonemes(sentence)
        audio = render_utterance(phonemes, SAMPLE_RATE, f0_base=120.0, speed=0.8)
        segments.append(audio)
        segments.append(pause)

    return np.concatenate(segments)


def stage_6_the_prompt() -> np.ndarray:
    """Stage 6: The prompt itself — the culmination."""
    print("  Stage 6: The prompt...")
    text = "Using only FM synthesis, learn how to speak"
    phonemes = text_to_phonemes(text)
    audio = render_utterance(phonemes, SAMPLE_RATE, f0_base=115.0, speed=0.7)
    return audio


def main():
    """Generate audio files showing the learning progression."""
    print("SpeakUp: Learning to speak with FM synthesis...\n")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    stages = [
        ("01_raw_fm_tones.wav", stage_1_raw_fm),
        ("02_vowels.wav", stage_2_vowels),
        ("03_babbling.wav", stage_3_babbling),
        ("04_first_words.wav", stage_4_first_words),
        ("05_speaking.wav", stage_5_speaking),
        ("06_the_prompt.wav", stage_6_the_prompt),
    ]

    for filename, stage_fn in stages:
        audio = stage_fn()
        audio = normalize(audio, peak=0.6)
        filepath = os.path.join(OUTPUT_DIR, filename)
        save_wav(audio, filepath, SAMPLE_RATE)
        duration = len(audio) / SAMPLE_RATE
        print(f"    -> {filepath} ({duration:.1f}s)\n")

    print("Done! Generated 6 audio files in output/")


if __name__ == "__main__":
    main()
