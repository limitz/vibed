"""Synthesizer module - generates audio waveforms from notes."""

import numpy as np
from typing import List
from melody import Note, DrumHit


def apply_envelope(signal: np.ndarray, attack: float, decay: float,
                   sustain: float, release: float, sample_rate: int = 44100) -> np.ndarray:
    """Apply ADSR envelope to a signal."""
    n = len(signal)
    envelope = np.zeros(n)

    attack_samples = int(attack * sample_rate)
    decay_samples = int(decay * sample_rate)
    release_samples = int(release * sample_rate)
    sustain_samples = max(0, n - attack_samples - decay_samples - release_samples)

    idx = 0
    # Attack
    if attack_samples > 0:
        end = min(idx + attack_samples, n)
        envelope[idx:end] = np.linspace(0, 1, end - idx)
        idx = end
    # Decay
    if idx < n and decay_samples > 0:
        end = min(idx + decay_samples, n)
        envelope[idx:end] = np.linspace(1, sustain, end - idx)
        idx = end
    # Sustain
    if idx < n and sustain_samples > 0:
        end = min(idx + sustain_samples, n)
        envelope[idx:end] = sustain
        idx = end
    # Release
    if idx < n:
        envelope[idx:] = np.linspace(sustain, 0, n - idx)

    return signal * envelope


def _make_buffer(notes: List[Note], sample_rate: int) -> np.ndarray:
    """Create an output buffer large enough for all notes."""
    if not notes:
        return np.zeros(sample_rate)
    max_end = max(n.start + n.duration for n in notes)
    return np.zeros(int(max_end * sample_rate) + sample_rate)


def synthesize_lead(notes: List[Note], sample_rate: int = 44100) -> np.ndarray:
    """Synthesize lead melody with a bright saw-like synth sound."""
    output = _make_buffer(notes, sample_rate)

    for note in notes:
        if note.pitch <= 0:
            continue
        n_samples = int(note.duration * sample_rate)
        t = np.arange(n_samples) / sample_rate

        # Detuned saw waves for richness
        saw1 = 2.0 * (note.pitch * t % 1.0) - 1.0
        saw2 = 2.0 * (note.pitch * 1.003 * t % 1.0) - 1.0
        signal = (saw1 + saw2) * 0.3

        # Add a bit of sine for body
        signal += 0.2 * np.sin(2 * np.pi * note.pitch * t)

        # ADSR envelope
        signal = apply_envelope(signal, 0.01, 0.08, 0.6, 0.05, sample_rate)
        signal *= note.velocity

        start_idx = int(note.start * sample_rate)
        end_idx = start_idx + len(signal)
        if end_idx <= len(output):
            output[start_idx:end_idx] += signal

    return output


def synthesize_bass(notes: List[Note], sample_rate: int = 44100) -> np.ndarray:
    """Synthesize bass line with a deep sub bass + square wave."""
    output = _make_buffer(notes, sample_rate)

    for note in notes:
        if note.pitch <= 0:
            continue
        n_samples = int(note.duration * sample_rate)
        t = np.arange(n_samples) / sample_rate

        # Sub sine
        sub = 0.5 * np.sin(2 * np.pi * note.pitch * t)
        # Square wave one octave up for presence
        square = 0.15 * np.sign(np.sin(2 * np.pi * note.pitch * 2 * t))
        signal = sub + square

        signal = apply_envelope(signal, 0.005, 0.05, 0.8, 0.03, sample_rate)
        signal *= note.velocity

        start_idx = int(note.start * sample_rate)
        end_idx = start_idx + len(signal)
        if end_idx <= len(output):
            output[start_idx:end_idx] += signal

    return output


def synthesize_pads(chords: List[List[Note]], sample_rate: int = 44100) -> np.ndarray:
    """Synthesize chord pads with a warm pad sound."""
    all_notes = [n for chord in chords for n in chord]
    output = _make_buffer(all_notes, sample_rate) if all_notes else np.zeros(sample_rate)

    for chord in chords:
        for note in chord:
            if note.pitch <= 0:
                continue
            n_samples = int(note.duration * sample_rate)
            t = np.arange(n_samples) / sample_rate

            # Soft detuned sines with slow LFO
            lfo = 1.0 + 0.003 * np.sin(2 * np.pi * 3.5 * t)
            s1 = np.sin(2 * np.pi * note.pitch * t)
            s2 = np.sin(2 * np.pi * note.pitch * 1.002 * t * lfo)
            s3 = np.sin(2 * np.pi * note.pitch * 0.998 * t)
            signal = (s1 + s2 + s3) * 0.15

            signal = apply_envelope(signal, 0.15, 0.1, 0.7, 0.2, sample_rate)
            signal *= note.velocity

            start_idx = int(note.start * sample_rate)
            end_idx = start_idx + len(signal)
            if end_idx <= len(output):
                output[start_idx:end_idx] += signal

    return output


def _synth_kick(sample_rate: int, velocity: float) -> np.ndarray:
    """Synthesize a kick drum."""
    duration = 0.15
    n = int(duration * sample_rate)
    t = np.arange(n) / sample_rate
    # Pitch sweep from 150Hz down to 50Hz
    freq = 50 + 100 * np.exp(-30 * t)
    phase = 2 * np.pi * np.cumsum(freq) / sample_rate
    signal = np.sin(phase) * np.exp(-8 * t) * velocity
    return signal


def _synth_snare(sample_rate: int, velocity: float) -> np.ndarray:
    """Synthesize a snare drum."""
    duration = 0.15
    n = int(duration * sample_rate)
    t = np.arange(n) / sample_rate
    # Tone component
    tone = np.sin(2 * np.pi * 200 * t) * np.exp(-20 * t) * 0.5
    # Noise component
    noise = np.random.randn(n) * np.exp(-15 * t) * 0.5
    return (tone + noise) * velocity


def _synth_hihat(sample_rate: int, velocity: float) -> np.ndarray:
    """Synthesize a hi-hat."""
    duration = 0.05
    n = int(duration * sample_rate)
    t = np.arange(n) / sample_rate
    noise = np.random.randn(n) * np.exp(-40 * t) * 0.3
    return noise * velocity


def _synth_clap(sample_rate: int, velocity: float) -> np.ndarray:
    """Synthesize a clap."""
    duration = 0.12
    n = int(duration * sample_rate)
    t = np.arange(n) / sample_rate
    noise = np.random.randn(n) * np.exp(-18 * t) * 0.4
    # Add slight "spread" with multiple bursts
    spread = np.zeros(n)
    for offset in [0, 0.01, 0.02]:
        start = int(offset * sample_rate)
        if start < n:
            spread[start:] += np.exp(-25 * t[:n - start])
    spread /= np.max(spread) if np.max(spread) > 0 else 1
    return noise * spread * velocity


def _synth_crash(sample_rate: int, velocity: float) -> np.ndarray:
    """Synthesize a crash cymbal."""
    duration = 0.8
    n = int(duration * sample_rate)
    t = np.arange(n) / sample_rate
    noise = np.random.randn(n) * np.exp(-3 * t) * 0.35
    # Add some metallic tone
    tone = np.sin(2 * np.pi * 3000 * t) * np.exp(-5 * t) * 0.1
    return (noise + tone) * velocity


_DRUM_SYNTHS = {
    "kick": _synth_kick,
    "snare": _synth_snare,
    "hihat": _synth_hihat,
    "clap": _synth_clap,
    "crash": _synth_crash,
}


def synthesize_drums(hits: List[DrumHit], sample_rate: int = 44100) -> np.ndarray:
    """Synthesize drum track."""
    if not hits:
        return np.zeros(sample_rate)

    max_time = max(h.start for h in hits) + 1.0
    output = np.zeros(int(max_time * sample_rate) + sample_rate)

    np.random.seed(42)  # Reproducible drums
    for hit in hits:
        synth_fn = _DRUM_SYNTHS.get(hit.drum)
        if synth_fn is None:
            continue
        signal = synth_fn(sample_rate, hit.velocity)
        start_idx = int(hit.start * sample_rate)
        end_idx = start_idx + len(signal)
        if end_idx <= len(output):
            output[start_idx:end_idx] += signal

    return output
