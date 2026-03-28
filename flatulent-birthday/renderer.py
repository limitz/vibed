"""
Song renderer — combines the synthesis engine with a melody to produce audio.
"""

import numpy as np
import subprocess
import tempfile
import wave
from typing import List, Tuple

from synth import synthesize


def render_song(
    notes: List[Tuple[float, float]],
    sample_rate: int = 44100,
    master_volume: float = 0.3,
) -> np.ndarray:
    """Render a sequence of notes using the flatulence synthesizer.

    Args:
        notes: List of (frequency_hz, duration_seconds). freq=0 means silence.
        sample_rate: Audio sample rate.
        master_volume: Overall volume scaling (0-1). Default 0.3 = not too loud.

    Returns:
        Mono float64 numpy array of the full song.
    """
    segments = []

    for freq, dur in notes:
        n_samples = int(sample_rate * dur)
        if freq <= 0:
            segments.append(np.zeros(n_samples))
        else:
            # Staccato: play note for 40% of duration, silence for the rest
            play_dur = dur * 0.40
            silence_dur = dur - play_dur
            note_audio = synthesize(freq, play_dur, sample_rate=sample_rate)
            # Quick fade-out (15ms) for clean cutoff
            fade = min(int(0.015 * sample_rate), len(note_audio) // 4)
            if fade > 0:
                note_audio[-fade:] *= np.linspace(1, 0, fade)
            silence = np.zeros(int(sample_rate * silence_dur))
            segments.append(np.concatenate([note_audio, silence]))

    if not segments:
        return np.zeros(0)

    song = np.concatenate(segments)
    song *= master_volume

    # Ensure no clipping
    peak = np.max(np.abs(song))
    if peak > 1.0:
        song /= peak

    return song


def save_mp3(
    audio: np.ndarray,
    filename: str,
    sample_rate: int = 44100,
) -> None:
    """Save audio array to MP3 file.

    Args:
        audio: Mono float64 array normalized to [-1, 1].
        filename: Output file path.
        sample_rate: Sample rate of the audio.
    """
    # Convert to 16-bit PCM
    pcm = (audio * 32767).astype(np.int16)

    # Write WAV to temp file, then encode with lame
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
        tmp_path = tmp.name
        with wave.open(tmp, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(pcm.tobytes())

    try:
        subprocess.run(
            ['lame', '--quiet', '-b', '192', tmp_path, filename],
            check=True,
        )
    finally:
        import os
        os.unlink(tmp_path)
