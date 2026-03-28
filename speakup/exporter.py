"""Audio export — save numpy audio arrays to WAV and MP3 files."""

from __future__ import annotations

import os
import struct
import subprocess
import tempfile
import wave

import numpy as np


def normalize(samples: np.ndarray, peak: float = 0.95) -> np.ndarray:
    """Normalize audio to target peak level."""
    max_val = np.max(np.abs(samples))
    if max_val == 0:
        return samples.copy()
    return samples * (peak / max_val)


def save_wav(samples: np.ndarray, filepath: str, sample_rate: int = 44100) -> None:
    """Save audio samples to WAV file."""
    clipped = np.clip(samples, -1.0, 1.0)
    pcm = (clipped * 32767).astype(np.int16)
    with wave.open(filepath, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(pcm.tobytes())


def save_mp3(samples: np.ndarray, filepath: str, sample_rate: int = 44100,
             bitrate: int = 192) -> None:
    """Save audio samples to MP3 via ffmpeg or lame."""
    # Write temp WAV first
    wav_path = filepath.rsplit(".", 1)[0] + "_temp.wav"
    save_wav(samples, wav_path, sample_rate)

    try:
        # Try ffmpeg first
        subprocess.run(
            ["ffmpeg", "-y", "-i", wav_path, "-b:a", f"{bitrate}k", filepath],
            capture_output=True, check=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        try:
            # Fallback to lame
            subprocess.run(
                ["lame", "-b", str(bitrate), wav_path, filepath],
                capture_output=True, check=True,
            )
        except (FileNotFoundError, subprocess.CalledProcessError):
            # No encoder available — keep WAV
            os.rename(wav_path, filepath.rsplit(".", 1)[0] + ".wav")
            print(f"Warning: no MP3 encoder found, saved as WAV")
            return
    finally:
        if os.path.exists(wav_path):
            os.unlink(wav_path)


def save_audio(samples: np.ndarray, filepath: str, sample_rate: int = 44100) -> None:
    """Save to WAV or MP3 based on file extension."""
    if filepath.lower().endswith(".mp3"):
        save_mp3(samples, filepath, sample_rate)
    else:
        save_wav(samples, filepath, sample_rate)
