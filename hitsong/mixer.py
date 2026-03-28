"""Mixer module - combines audio tracks and applies effects."""

import numpy as np
from typing import List, Tuple


def mix_tracks(tracks: List[Tuple[np.ndarray, float]], sample_rate: int = 44100) -> np.ndarray:
    """Mix multiple audio tracks with individual volume levels."""
    if not tracks:
        return np.zeros(sample_rate)

    max_len = max(len(audio) for audio, _ in tracks)
    output = np.zeros(max_len)

    for audio, volume in tracks:
        padded = np.zeros(max_len)
        padded[:len(audio)] = audio
        output += padded * volume

    return output


def apply_reverb(audio: np.ndarray, room_size: float = 0.3,
                 sample_rate: int = 44100) -> np.ndarray:
    """Apply simple reverb effect using comb filter approximation."""
    output = audio.copy().astype(np.float64)
    # Multiple delay lines at different lengths
    delays_ms = [23, 37, 53, 71]
    for delay_ms in delays_ms:
        delay_samples = int(delay_ms * sample_rate / 1000)
        decay = room_size * 0.6
        delayed = np.zeros_like(output)
        if delay_samples < len(output):
            delayed[delay_samples:] = output[:-delay_samples] * decay
            output += delayed

    # Normalize to prevent clipping
    peak = np.max(np.abs(output))
    if peak > 0:
        output *= np.max(np.abs(audio)) / peak

    return output


def apply_compression(audio: np.ndarray, threshold: float = 0.7,
                      ratio: float = 4.0) -> np.ndarray:
    """Apply dynamic range compression."""
    output = audio.copy().astype(np.float64)

    abs_audio = np.abs(output)
    mask = abs_audio > threshold

    if np.any(mask):
        excess = abs_audio[mask] - threshold
        compressed_excess = excess / ratio
        output[mask] = np.sign(output[mask]) * (threshold + compressed_excess)

    return output


def normalize(audio: np.ndarray, target_peak: float = 0.95) -> np.ndarray:
    """Normalize audio to target peak level."""
    peak = np.max(np.abs(audio))
    if peak == 0:
        return audio.copy()
    return audio * (target_peak / peak)


def master(audio: np.ndarray, sample_rate: int = 44100) -> np.ndarray:
    """Apply mastering chain: compression, reverb, limiting, normalization."""
    # Light compression
    output = apply_compression(audio, threshold=0.6, ratio=3.0)
    # Subtle reverb
    output = apply_reverb(output, room_size=0.2, sample_rate=sample_rate)
    # Hard limiter
    output = np.clip(output, -0.98, 0.98)
    # Final normalization
    output = normalize(output, 0.95)
    return output
