"""Exporter module - exports audio to WAV and MP3 formats."""

import numpy as np
import wave
import struct
import subprocess
import os


def export_wav(audio: np.ndarray, filename: str, sample_rate: int = 44100) -> str:
    """Export audio array to WAV file."""
    # Ensure audio is in [-1, 1] range
    audio = np.clip(audio, -1.0, 1.0)

    # Convert to 16-bit PCM
    pcm = (audio * 32767).astype(np.int16)

    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)
        wf.writeframes(pcm.tobytes())

    return filename


def export_mp3(audio: np.ndarray, filename: str, sample_rate: int = 44100,
               bitrate: int = 192) -> str:
    """Export audio array to MP3 file."""
    # First export to WAV
    wav_filename = filename.replace(".mp3", ".wav")
    if not wav_filename.endswith(".wav"):
        wav_filename = filename + ".wav"
    export_wav(audio, wav_filename, sample_rate)

    # Convert to MP3 using ffmpeg or lame
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", wav_filename, "-b:a", f"{bitrate}k", filename],
            check=True, capture_output=True
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fallback to lame
        subprocess.run(
            ["lame", "-b", str(bitrate), wav_filename, filename],
            check=True, capture_output=True
        )

    # Clean up WAV file
    if os.path.exists(wav_filename):
        os.unlink(wav_filename)

    return filename
