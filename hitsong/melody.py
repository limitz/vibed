"""Melody module - generates melodies, bass lines, and drum patterns."""

from dataclasses import dataclass
from typing import List, Dict
import numpy as np
import random

from song_structure import SongStructure, Section


@dataclass
class Note:
    """A musical note."""
    pitch: float       # Frequency in Hz (0 = rest)
    start: float       # Start time in seconds
    duration: float    # Duration in seconds
    velocity: float    # 0.0 to 1.0


@dataclass
class DrumHit:
    """A drum hit."""
    drum: str          # "kick", "snare", "hihat", "clap", "crash"
    start: float       # Start time in seconds
    velocity: float    # 0.0 to 1.0


# Note name to semitone offset from C
_NOTE_SEMITONES = {
    "C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
    "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
    "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11
}

# Chord definitions: chord name suffix -> list of semitone intervals from root
_CHORD_INTERVALS: Dict[str, List[int]] = {
    "": [0, 4, 7],       # major
    "m": [0, 3, 7],      # minor
    "7": [0, 4, 7, 10],  # dominant 7
    "m7": [0, 3, 7, 10], # minor 7
}

# Scale degrees for C major (semitones from C)
_C_MAJOR_SCALE = [0, 2, 4, 5, 7, 9, 11]


def note_to_freq(note_name: str, octave: int) -> float:
    """Convert note name and octave to frequency in Hz."""
    semitone = _NOTE_SEMITONES[note_name]
    # A4 = 440 Hz, A is 9 semitones above C
    midi_note = (octave + 1) * 12 + semitone
    return 440.0 * (2.0 ** ((midi_note - 69) / 12.0))


def _parse_chord(chord_name: str):
    """Parse chord name into root note and quality. Returns (root_semitone, intervals)."""
    # Try two-char root first (e.g., "C#", "Bb")
    if len(chord_name) >= 2 and chord_name[1] in ('#', 'b'):
        root = chord_name[:2]
        quality = chord_name[2:]
    else:
        root = chord_name[0]
        quality = chord_name[1:]

    root_semitone = _NOTE_SEMITONES[root]
    intervals = _CHORD_INTERVALS.get(quality, [0, 4, 7])
    return root_semitone, intervals


def _semitone_to_freq(semitone: int, octave: int) -> float:
    """Convert semitone (0=C) and octave to frequency."""
    midi_note = (octave + 1) * 12 + semitone
    return 440.0 * (2.0 ** ((midi_note - 69) / 12.0))


def _get_scale_notes_in_key(key: str = "C") -> List[int]:
    """Get semitones of the major scale for a given key."""
    root = _NOTE_SEMITONES[key]
    major_intervals = [0, 2, 4, 5, 7, 9, 11]
    return [(root + i) % 12 for i in major_intervals]


def generate_lead_melody(song: SongStructure) -> List[Note]:
    """Generate the lead melody for the entire song."""
    random.seed(42)
    notes = []
    current_time = 0.0
    spb = song.seconds_per_beat
    scale = _get_scale_notes_in_key(song.key)

    for section in song.sections:
        style = section.melody_style

        for bar_idx, chord_name in enumerate(section.chords):
            root_semi, intervals = _parse_chord(chord_name)

            if style == "intro" or style == "outro":
                # Sparse arpeggiated notes
                for beat in range(0, song.beats_per_bar, 2):
                    semi = (root_semi + intervals[beat // 2 % len(intervals)]) % 12
                    freq = _semitone_to_freq(semi, 5)
                    t = current_time + beat * spb
                    vel = 0.5 if style == "outro" else 0.6
                    notes.append(Note(freq, t, spb * 1.5, vel))

            elif style == "verse":
                # Melodic pattern following chord tones with passing notes
                chord_tones = [(root_semi + i) % 12 for i in intervals]
                pattern = _verse_pattern(chord_tones, scale)
                for i, (semi, dur_beats) in enumerate(pattern):
                    freq = _semitone_to_freq(semi, 5)
                    t = current_time + sum(d * spb for _, d in pattern[:i])
                    if t >= current_time + song.beats_per_bar * spb:
                        break
                    notes.append(Note(freq, t, dur_beats * spb * 0.9, 0.7))

            elif style == "chorus":
                # Higher energy, more notes, wider intervals
                chord_tones = [(root_semi + i) % 12 for i in intervals]
                pattern = _chorus_pattern(chord_tones, scale)
                for i, (semi, dur_beats) in enumerate(pattern):
                    freq = _semitone_to_freq(semi, 5)
                    t = current_time + sum(d * spb for _, d in pattern[:i])
                    if t >= current_time + song.beats_per_bar * spb:
                        break
                    notes.append(Note(freq, t, dur_beats * spb * 0.9, 0.85))

            elif style == "bridge":
                # Slower, more emotional
                semi = (root_semi + intervals[0]) % 12
                freq = _semitone_to_freq(semi, 5)
                notes.append(Note(freq, current_time, spb * 2.0, 0.75))
                semi2 = (root_semi + intervals[min(2, len(intervals) - 1)]) % 12
                freq2 = _semitone_to_freq(semi2, 5)
                notes.append(Note(freq2, current_time + spb * 2, spb * 2.0, 0.7))

            current_time += song.beats_per_bar * spb

    return notes


def _verse_pattern(chord_tones, scale):
    """Generate a verse melodic pattern."""
    patterns = [
        [(chord_tones[0], 1), (scale[2], 0.5), (scale[4], 0.5),
         (chord_tones[min(1, len(chord_tones)-1)], 1), (chord_tones[0], 1)],
        [(chord_tones[0], 0.5), (scale[3], 0.5), (chord_tones[min(1, len(chord_tones)-1)], 1),
         (scale[4], 1), (chord_tones[0], 1)],
    ]
    return random.choice(patterns)


def _chorus_pattern(chord_tones, scale):
    """Generate a chorus melodic pattern - more energetic."""
    patterns = [
        [(chord_tones[min(2, len(chord_tones)-1)], 0.5), (scale[4], 0.5),
         (scale[5 % len(scale)], 0.5), (chord_tones[0], 0.5),
         (chord_tones[min(1, len(chord_tones)-1)], 1),
         (chord_tones[min(2, len(chord_tones)-1)], 1)],
        [(scale[4], 0.5), (scale[5 % len(scale)], 0.5),
         (chord_tones[min(2, len(chord_tones)-1)], 1),
         (chord_tones[min(1, len(chord_tones)-1)], 0.5), (chord_tones[0], 0.5),
         (scale[4], 1)],
    ]
    return random.choice(patterns)


def generate_bass_line(song: SongStructure) -> List[Note]:
    """Generate the bass line for the entire song."""
    notes = []
    current_time = 0.0
    spb = song.seconds_per_beat

    for section in song.sections:
        for chord_name in section.chords:
            root_semi, intervals = _parse_chord(chord_name)
            root_freq = _semitone_to_freq(root_semi, 2)
            fifth_freq = _semitone_to_freq((root_semi + 7) % 12, 2)

            if section.melody_style in ("intro", "outro"):
                # Whole note bass
                notes.append(Note(root_freq, current_time, spb * 4 * 0.9, 0.7))
            elif section.melody_style == "verse":
                # Root on 1 and 3, fifth on 2.5
                notes.append(Note(root_freq, current_time, spb * 0.9, 0.8))
                notes.append(Note(fifth_freq, current_time + spb * 1.5, spb * 0.4, 0.6))
                notes.append(Note(root_freq, current_time + spb * 2, spb * 0.9, 0.75))
                notes.append(Note(fifth_freq, current_time + spb * 3.5, spb * 0.4, 0.6))
            elif section.melody_style == "chorus":
                # Driving eighth note pattern
                for beat in range(song.beats_per_bar):
                    freq = root_freq if beat % 2 == 0 else fifth_freq
                    vel = 0.85 if beat == 0 else 0.7
                    notes.append(Note(freq, current_time + beat * spb, spb * 0.8, vel))
            elif section.melody_style == "bridge":
                # Sustained notes
                notes.append(Note(root_freq, current_time, spb * 2 * 0.9, 0.75))
                oct_freq = _semitone_to_freq(root_semi, 3)
                notes.append(Note(oct_freq, current_time + spb * 2, spb * 2 * 0.9, 0.65))

            current_time += song.beats_per_bar * spb

    return notes


def generate_chord_pads(song: SongStructure) -> List[List[Note]]:
    """Generate chord pad notes (list of chords, each chord is a list of notes)."""
    chords = []
    current_time = 0.0
    spb = song.seconds_per_beat

    for section in song.sections:
        for chord_name in section.chords:
            root_semi, intervals = _parse_chord(chord_name)
            bar_duration = song.beats_per_bar * spb

            chord_notes = []
            for interval in intervals:
                semi = (root_semi + interval) % 12
                freq = _semitone_to_freq(semi, 4)
                vel = 0.4 if section.melody_style in ("intro", "outro") else 0.6
                chord_notes.append(Note(freq, current_time, bar_duration * 0.95, vel))

            chords.append(chord_notes)
            current_time += bar_duration

    return chords


def generate_drum_pattern(song: SongStructure) -> List[DrumHit]:
    """Generate drum pattern for the entire song."""
    hits = []
    current_time = 0.0
    spb = song.seconds_per_beat

    for section in song.sections:
        style = section.melody_style

        for bar_idx in range(section.bars):
            if style == "intro":
                # Light hihat pattern, kick on 1
                hits.append(DrumHit("kick", current_time, 0.6))
                for beat in range(song.beats_per_bar):
                    hits.append(DrumHit("hihat", current_time + beat * spb, 0.4))
                if bar_idx == section.bars - 1:
                    hits.append(DrumHit("crash", current_time + 3 * spb, 0.7))

            elif style == "verse":
                # Standard rock beat
                hits.append(DrumHit("kick", current_time, 0.85))
                hits.append(DrumHit("kick", current_time + 2 * spb, 0.8))
                hits.append(DrumHit("snare", current_time + spb, 0.8))
                hits.append(DrumHit("snare", current_time + 3 * spb, 0.8))
                for beat in range(song.beats_per_bar * 2):
                    hits.append(DrumHit("hihat", current_time + beat * spb * 0.5, 0.5))

            elif style == "chorus":
                # Driving pattern with crash on first bar
                if bar_idx == 0:
                    hits.append(DrumHit("crash", current_time, 0.9))
                hits.append(DrumHit("kick", current_time, 0.9))
                hits.append(DrumHit("kick", current_time + 1.5 * spb, 0.7))
                hits.append(DrumHit("kick", current_time + 2 * spb, 0.85))
                hits.append(DrumHit("snare", current_time + spb, 0.9))
                hits.append(DrumHit("snare", current_time + 3 * spb, 0.9))
                hits.append(DrumHit("clap", current_time + spb, 0.6))
                hits.append(DrumHit("clap", current_time + 3 * spb, 0.6))
                for beat in range(song.beats_per_bar * 2):
                    hits.append(DrumHit("hihat", current_time + beat * spb * 0.5, 0.55))

            elif style == "bridge":
                # Sparse, building
                hits.append(DrumHit("kick", current_time, 0.7))
                hits.append(DrumHit("snare", current_time + 2 * spb, 0.6))
                for beat in range(song.beats_per_bar):
                    hits.append(DrumHit("hihat", current_time + beat * spb, 0.35))

            elif style == "outro":
                # Fading pattern
                vel_scale = 1.0 - (bar_idx / max(section.bars, 1)) * 0.6
                hits.append(DrumHit("kick", current_time, 0.7 * vel_scale))
                hits.append(DrumHit("snare", current_time + spb, 0.6 * vel_scale))
                hits.append(DrumHit("kick", current_time + 2 * spb, 0.65 * vel_scale))
                for beat in range(song.beats_per_bar):
                    hits.append(DrumHit("hihat", current_time + beat * spb, 0.4 * vel_scale))

            current_time += song.beats_per_bar * spb

    return hits
