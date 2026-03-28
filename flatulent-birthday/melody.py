"""
Happy Birthday melody definition.

Provides the note sequence (frequency, duration) for "Happy Birthday to You".
"""

from typing import List, Tuple

# Note name -> semitone offset from C
_NOTE_OFFSETS = {
    'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5,
    'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11,
}


def _note_freq(name: str, octave: int) -> float:
    """Convert note name + octave to frequency in Hz (A4 = 440)."""
    semitone = _NOTE_OFFSETS[name] + (octave - 4) * 12
    # Relative to A4
    semitone_from_a4 = semitone - 9  # A is 9 semitones above C
    return 440.0 * (2.0 ** (semitone_from_a4 / 12.0))


# Happy Birthday melody: (note_name, octave_offset, beat_duration)
# octave_offset is relative to base_octave
# Standard "Happy Birthday to You" in key of C
_HAPPY_BIRTHDAY = [
    # "Hap-py birth-day to you"
    ('C', 0, 0.75), ('C', 0, 0.25), ('D', 0, 1.0), ('C', 0, 1.0), ('F', 0, 1.0), ('E', 0, 2.0),
    # "Hap-py birth-day to you"
    ('C', 0, 0.75), ('C', 0, 0.25), ('D', 0, 1.0), ('C', 0, 1.0), ('G', 0, 1.0), ('F', 0, 2.0),
    # "Hap-py birth-day dear [name]"
    ('C', 0, 0.75), ('C', 0, 0.25), ('C', 1, 1.0), ('A', 0, 1.0), ('F', 0, 1.0), ('E', 0, 1.0), ('D', 0, 2.0),
    # "Hap-py birth-day to you"
    ('A#', 0, 0.75), ('A#', 0, 0.25), ('A', 0, 1.0), ('F', 0, 1.0), ('G', 0, 1.0), ('F', 0, 2.0),
]


def happy_birthday(base_octave: int = 4, tempo_bpm: float = 120.0) -> List[Tuple[float, float]]:
    """Return Happy Birthday as a list of (frequency_hz, duration_seconds) tuples.

    Args:
        base_octave: Starting octave (4 = middle C region).
        tempo_bpm: Tempo in beats per minute.

    Returns:
        List of (freq, duration) pairs. freq=0 means rest.
    """
    beat_duration = 60.0 / tempo_bpm  # seconds per beat

    notes = []
    for note_name, octave_offset, beats in _HAPPY_BIRTHDAY:
        freq = _note_freq(note_name, base_octave + octave_offset)
        dur = beats * beat_duration
        notes.append((freq, dur))

    return notes
